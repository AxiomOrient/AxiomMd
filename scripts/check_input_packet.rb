#!/usr/bin/env ruby

require "yaml"

REQUIRED_KEYS = %w[
  packet_version
  request_summary
  target_kind
  source_context_refs
  output_contract_refs
  scope
  constraints
  done_signals
  open_questions
  evidence_refs
].freeze

def fail!(message)
  warn "[FAIL] #{message}"
  exit 1
end

path = ARGV[0]
fail!("usage: check_input_packet.rb <path/to/input.packet.yaml>") unless path
fail!("file not found: #{path}") unless File.exist?(path)

data = YAML.load_file(path)
fail!("packet must be a mapping") unless data.is_a?(Hash)

REQUIRED_KEYS.each do |key|
  fail!("missing key: #{key}") unless data.key?(key)
end

fail!("packet_version must be 1") unless data["packet_version"] == 1
scope = data["scope"]
fail!("scope must be a mapping") unless scope.is_a?(Hash)
fail!("scope.in must be a list") unless scope["in"].is_a?(Array)
fail!("scope.out must be a list") unless scope["out"].is_a?(Array)

%w[source_context_refs output_contract_refs constraints done_signals open_questions evidence_refs].each do |key|
  fail!("#{key} must be a list") unless data[key].is_a?(Array)
end

fail!("request_summary must be a non-empty string") unless data["request_summary"].is_a?(String) && !data["request_summary"].strip.empty?
fail!("target_kind must be a non-empty string") unless data["target_kind"].is_a?(String) && !data["target_kind"].strip.empty?
fail!("constraints must not be empty") if data["constraints"].empty?
fail!("done_signals must not be empty") if data["done_signals"].empty?
if data["source_context_refs"].empty? && data["evidence_refs"].empty?
  fail!("at least one of source_context_refs or evidence_refs must be non-empty")
end

puts "[PASS] input packet shape looks valid"
