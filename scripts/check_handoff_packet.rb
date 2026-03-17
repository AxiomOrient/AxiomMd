#!/usr/bin/env ruby

require "yaml"

REQUIRED_KEYS = %w[
  packet_version
  stage
  status
  input_ref
  changed_paths
  produced_paths
  evidence_refs
  open_questions
  next_step
  blockers
].freeze

ALLOWED_STAGES = %w[
  intake-and-routing
  framing
  feature-package-authoring
  readiness-and-handoff
  execution
  verification
  reconcile
].freeze

ALLOWED_STATUSES = %w[ready patch-required hold blocked].freeze

def fail!(message)
  warn "[FAIL] #{message}"
  exit 1
end

path = ARGV[0]
fail!("usage: check_handoff_packet.rb <path/to/handoff.packet.yaml>") unless path
fail!("file not found: #{path}") unless File.exist?(path)

data = YAML.load_file(path)
fail!("handoff packet must be a mapping") unless data.is_a?(Hash)

REQUIRED_KEYS.each do |key|
  fail!("missing key: #{key}") unless data.key?(key)
end

fail!("packet_version must be 1") unless data["packet_version"] == 1
fail!("stage must be one of #{ALLOWED_STAGES.join(', ')}") unless ALLOWED_STAGES.include?(data["stage"])
fail!("status must be one of #{ALLOWED_STATUSES.join(', ')}") unless ALLOWED_STATUSES.include?(data["status"])
fail!("input_ref must be a string") unless data["input_ref"].is_a?(String) && !data["input_ref"].empty?
fail!("next_step must be a string") unless data["next_step"].is_a?(String) && !data["next_step"].empty?

%w[changed_paths produced_paths evidence_refs open_questions blockers].each do |key|
  fail!("#{key} must be a list") unless data[key].is_a?(Array)
end

fail!("produced_paths must not be empty") if data["produced_paths"].empty?
fail!("evidence_refs must not be empty") if data["evidence_refs"].empty?

puts "[PASS] handoff packet shape looks valid"
