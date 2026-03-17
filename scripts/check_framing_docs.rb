#!/usr/bin/env ruby

def fail!(message)
  warn "[FAIL] #{message}"
  exit 1
end

charter_path = ARGV[0]
blueprint_path = ARGV[1]
fail!("usage: check_framing_docs.rb <product-charter.md> <system-blueprint.md>") unless charter_path && blueprint_path
fail!("file not found: #{charter_path}") unless File.exist?(charter_path)
fail!("file not found: #{blueprint_path}") unless File.exist?(blueprint_path)

charter = File.read(charter_path)
blueprint = File.read(blueprint_path)

%w[Problem Users Goals Non-Goals Success Constraints].each do |token|
  fail!("product-charter.md missing #{token}") unless charter.include?(token)
end

%w[Current\ Scope Boundary Major\ Components Primary\ Flow Source\ Of\ Truth].each do |token|
  normalized = token.tr("\\", "")
  fail!("system-blueprint.md missing #{normalized}") unless blueprint.include?(normalized)
end

puts "[PASS] framing docs look valid"
