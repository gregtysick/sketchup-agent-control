# frozen_string_literal: true

require 'sketchup.rb'
require 'extensions.rb'

module BeautifulInsights
  module SketchUpAgentControl
    EXTENSION_ID = 'beautiful_insights.sketchup_agent_control'
  end
end

unless file_loaded?(__FILE__)
  extension = SketchupExtension.new(
    'SketchUp Agent Control',
    'sketchup_agent_control/main'
  )
  extension.description = 'A local, auditable bridge for controlled SketchUp agent actions.'
  extension.version = '0.3.0'
  extension.creator = 'Beautiful Insights'
  Sketchup.register_extension(extension, true)
  file_loaded(__FILE__)
end
