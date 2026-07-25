# frozen_string_literal: true

require 'json'
require 'fileutils'
require 'pathname'
require 'time'

module BeautifulInsights
  module SketchUpAgentControl
    SCHEMA_VERSION = 1
    MAX_COMMAND_BYTES = 64 * 1024
    COMMANDS = ['get_status'].freeze
    DIRECTORIES = %w[inbox processing outbox errors snapshots exports backups logs].freeze

    class << self
      def data_root
        path = Sketchup.read_default(EXTENSION_ID, 'data_root', default_data_root)
        Pathname.new(path).expand_path
      end

      def default_data_root
        File.join(ENV.fetch('LOCALAPPDATA', ENV.fetch('APPDATA', Dir.home)), 'Beautiful Insights', 'SketchUp Agent Control')
      end

      def ensure_bridge_directories
        DIRECTORIES.each { |name| FileUtils.mkdir_p(data_root.join(name)) }
      end

      def start
        ensure_bridge_directories
        add_menu
        @processing_enabled = true
        @timer_id ||= UI.start_timer(0.5, true) { poll_once if @processing_enabled }
        log('startup complete')
      rescue StandardError => error
        UI.messagebox("SketchUp Agent Control failed to start: #{error.message}")
      end

      def add_menu
        return if @menu_added
        menu = UI.menu('Extensions').add_submenu('SketchUp Agent Control')
        menu.add_item('Bridge Status') { UI.messagebox(JSON.pretty_generate(status_result)) }
        menu.add_item('Open Bridge Folder') { UI.openURL(data_root.to_s) }
        menu.add_separator
        menu.add_item('Pause Command Processing') { @processing_enabled = false; log('processing paused') }
        menu.add_item('Resume Command Processing') { @processing_enabled = true; log('processing resumed') }
        menu.add_item('View Log') { UI.openURL(data_root.join('logs').to_s) }
        @menu_added = true
      end

      def poll_once
        inbox = data_root.join('inbox')
        request_path = Dir.glob(inbox.join('*.json').to_s).sort.first
        return unless request_path
        processing_path = data_root.join('processing', File.basename(request_path))
        File.rename(request_path, processing_path)
        process_request(processing_path)
      rescue Errno::ENOENT
        nil
      rescue StandardError => error
        log("poll error: #{error.class}: #{error.message}")
      end

      def process_request(path)
        started_at = Time.now.utc.iso8601
        request = JSON.parse(File.read(path))
        validate_request!(request)
        result = request.fetch('command') == 'get_status' ? status_result : raise('unsupported command')
        response = response_for(request, 'completed', started_at, result, nil)
        atomic_write_json(data_root.join('outbox', File.basename(path)), response)
        File.delete(path) if File.exist?(path)
      rescue StandardError => error
        request_id = request.is_a?(Hash) ? request['id'] : File.basename(path, '.json')
        response = response_for({'id' => request_id}, 'rejected', started_at || Time.now.utc.iso8601, {}, safe_error(error))
        atomic_write_json(data_root.join('errors', File.basename(path)), response)
        atomic_write_json(data_root.join('outbox', File.basename(path)), response) if valid_uuid?(request_id)
        File.delete(path) if File.exist?(path)
        log("request rejected: #{safe_error(error)['message']}")
      end

      def validate_request!(request)
        required = %w[schema_version id created_at command args confirm]
        raise 'request fields are invalid' unless request.is_a?(Hash) && request.keys.sort == required.sort
        raise 'unsupported schema_version' unless request['schema_version'] == SCHEMA_VERSION
        raise 'request id must be a UUID' unless valid_uuid?(request['id'])
        raise 'unsupported command' unless COMMANDS.include?(request['command'])
        raise 'get_status does not accept arguments' unless request['args'] == {}
        raise 'read-only commands must use confirm: false' unless request['confirm'] == false
        raise 'request exceeds maximum command size' if JSON.generate(request).bytesize > MAX_COMMAND_BYTES
      end

      def status_result
        {
          'extension_name' => 'SketchUp Agent Control',
          'extension_version' => '0.1.0',
          'sketchup_version' => Sketchup.version,
          'ruby_version' => RUBY_VERSION,
          'platform' => Sketchup.platform,
          'bridge_root' => data_root.to_s,
          'processing_enabled' => @processing_enabled != false,
          'read_only_commands' => COMMANDS
        }
      end

      def response_for(request, status, started_at, result, error)
        {'schema_version' => SCHEMA_VERSION, 'id' => request['id'], 'status' => status, 'started_at' => started_at, 'finished_at' => Time.now.utc.iso8601, 'result' => result, 'evidence' => [], 'error' => error}
      end

      def atomic_write_json(destination, value)
        temporary = "#{destination}.#{Process.pid}.tmp"
        File.open(temporary, 'w:utf-8') { |file| file.write(JSON.generate(value)); file.flush; file.fsync }
        File.rename(temporary, destination)
      ensure
        File.delete(temporary) if defined?(temporary) && File.exist?(temporary)
      end

      def valid_uuid?(value)
        value.is_a?(String) && value.match?(/\A[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\z/i)
      end

      def safe_error(error)
        {'code' => 'invalid_request', 'message' => error.message.to_s[0, 300]}
      end

      def log(message)
        ensure_bridge_directories
        File.open(data_root.join('logs', 'bridge.log'), 'a:utf-8') { |file| file.puts("#{Time.now.utc.iso8601} #{message}") }
      end
    end
  end
end

BeautifulInsights::SketchUpAgentControl.start
