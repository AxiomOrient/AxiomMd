#!/usr/bin/env ruby

require "yaml"

REQUIRED_KEYS = %w[
  packet_version
  input_ref
  route
  reason_summary
  required_artifacts
  next_step
  open_questions
  blockers
].freeze

ALLOWED_ROUTES = %w[direct-package framing-first hold].freeze

def fail!(message)
  warn "[FAIL] #{message}"
  exit 1
end

path = ARGV[0]
fail!("usage: check_route_decision.rb <path/to/route.decision.yaml>") unless path
fail!("file not found: #{path}") unless File.exist?(path)

data = YAML.load_file(path)
fail!("route decision must be a mapping") unless data.is_a?(Hash)

REQUIRED_KEYS.each do |key|
  fail!("missing key: #{key}") unless data.key?(key)
end

fail!("packet_version must be 1") unless data["packet_version"] == 1
fail!("input_ref must be a non-empty string") unless data["input_ref"].is_a?(String) && !data["input_ref"].empty?
fail!("route must be one of #{ALLOWED_ROUTES.join(', ')}") unless ALLOWED_ROUTES.include?(data["route"])
fail!("reason_summary must be a non-empty string") unless data["reason_summary"].is_a?(String) && !data["reason_summary"].empty?
fail!("required_artifacts must be a list") unless data["required_artifacts"].is_a?(Array)
fail!("open_questions must be a list") unless data["open_questions"].is_a?(Array)
fail!("blockers must be a list") unless data["blockers"].is_a?(Array)
fail!("next_step must be a non-empty string") unless data["next_step"].is_a?(String) && !data["next_step"].empty?
fail!("framing-first route needs required_artifacts") if data["route"] == "framing-first" && data["required_artifacts"].empty?
fail!("hold route needs blockers") if data["route"] == "hold" && data["blockers"].empty?

puts "[PASS] route decision shape looks valid"
