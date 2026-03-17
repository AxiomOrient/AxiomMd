#!/usr/bin/env ruby

require "yaml"

REQUIRED_FILES = %w[
  intent.md
  package.yaml
  requirements.yaml
  invariants.yaml
  design.md
  tasks.md
  evals.yaml
  risks.yaml
  decisions.jsonl
  contracts
].freeze

REQUIRED_GENERIC_PACKAGE_KEYS = %w[
  feature_id
  title
  state
  review_mode
].freeze

def fail!(message)
  warn "[FAIL] #{message}"
  exit 1
end

def load_yaml(path)
  YAML.load_file(path)
end

def package_meta(data)
  return data["feature"] if data.is_a?(Hash) && data["feature"].is_a?(Hash)
  data
end

def parse_task_rows(tasks_path)
  raw = File.read(tasks_path)

  begin
    parsed = YAML.safe_load(raw, aliases: true)
    if parsed.is_a?(Hash) && parsed["tasks"].is_a?(Array)
      return parsed["tasks"].map do |task|
        {
          "id" => task["id"],
          "req_ids" => Array(task["req_ids"]),
          "eval_ids" => Array(task["eval_ids"]),
          "paths" => Array(task["touched_paths"] || task["paths"]),
          "done_when" => task["done_when"] || task["next"],
        }
      end
    end
  rescue StandardError
    # Fall back to markdown task parsing.
  end

  task_ids = raw.scan(/TASK-\d+/).uniq
  task_ids.map do |task_id|
    block = raw[/#{Regexp.escape(task_id)}.*?(?=\n- \[|\z)/m]
    {
      "id" => task_id,
      "req_ids" => block.to_s.scan(/REQ-\d+/).uniq,
      "eval_ids" => block.to_s.scan(/EVAL-\d+/).uniq,
      "paths" => block.to_s[/paths:\s*\[(.*?)\]/m, 1].to_s.split(",").map(&:strip).reject(&:empty?),
      "done_when" => block.to_s[/done_when:\s*(.+)$/, 1],
    }
  end
end

def design_has_required_sections?(content)
  accepted = [
    "Boundary",
    "Boundaries",
    "Data and State",
    "Data / State",
    "Interfaces",
    "Failure Modes",
    "Requirement mapping",
    "Mapping to Requirements",
  ]

  accepted.all? do |token|
    case token
    when "Boundary", "Boundaries"
      content.include?("Boundary") || content.include?("Boundaries")
    when "Data and State", "Data / State"
      content.include?("Data and State") || content.include?("Data / State")
    when "Requirement mapping", "Mapping to Requirements"
      content.include?("Requirement mapping") || content.include?("Mapping to Requirements")
    else
      content.include?(token)
    end
  end
end

root = ARGV[0]
fail!("usage: check_feature_package.rb <path/to/feature-package-dir>") unless root
fail!("feature package dir not found: #{root}") unless Dir.exist?(root)

missing = REQUIRED_FILES.reject { |file| File.exist?(File.join(root, file)) }
fail!("missing required files: #{missing.join(', ')}") unless missing.empty?

package = load_yaml(File.join(root, "package.yaml"))
requirements = load_yaml(File.join(root, "requirements.yaml"))
invariants = load_yaml(File.join(root, "invariants.yaml"))
evals = load_yaml(File.join(root, "evals.yaml"))
risks = load_yaml(File.join(root, "risks.yaml"))
design_md = File.read(File.join(root, "design.md"))
tasks = parse_task_rows(File.join(root, "tasks.md"))

meta = package_meta(package)
fail!("package.yaml must be a mapping") unless meta.is_a?(Hash)

REQUIRED_GENERIC_PACKAGE_KEYS.each do |key|
  generic_present =
    meta.key?(key) ||
    (key == "feature_id" && (meta.key?("id") || meta.key?("feature_id"))) ||
    (key == "title" && meta.key?("title")) ||
    (key == "state" && meta.key?("state")) ||
    (key == "review_mode" && meta.key?("review_mode"))
  fail!("package.yaml missing #{key}") unless generic_present
end

reqs = requirements["requirements"]
fail!("requirements.yaml must contain requirements list") unless reqs.is_a?(Array) && !reqs.empty?
fail!("invariants.yaml must contain invariants list") unless invariants["invariants"].is_a?(Array)
eval_list = evals["evals"]
fail!("evals.yaml must contain evals list") unless eval_list.is_a?(Array) && !eval_list.empty?
fail!("risks.yaml must contain risks list") unless risks["risks"].is_a?(Array)
fail!("tasks.md must contain at least one task") if tasks.empty?

req_ids = reqs.map { |item| item["id"] }.compact
eval_ids = eval_list.map { |item| item["id"] }.compact

blocking_by_req = Hash.new { |h, k| h[k] = [] }
eval_list.each do |item|
  fail!("each eval must have id") unless item["id"].is_a?(String) && !item["id"].empty?
  fail!("each eval must have req_ids list") unless item["req_ids"].is_a?(Array)
  fail!("each eval must have task_ids list") unless item["task_ids"].is_a?(Array)
  item["req_ids"].each do |rid|
    blocking = item["blocking"] == true || item["kind"] == "blocking"
    blocking_by_req[rid] << item if blocking
  end
end

reqs.each do |req|
  rid = req["id"]
  fail!("each requirement must have id") unless rid.is_a?(String) && !rid.empty?
  fail!("each requirement must have priority") unless req["priority"].is_a?(String) && !req["priority"].empty?
  fail!("must requirement #{rid} has no blocking eval") if req["priority"] == "must" && blocking_by_req[rid].empty?
end

tasks.each do |task|
  tid = task["id"]
  fail!("task missing id") unless tid.is_a?(String) && !tid.empty?
  fail!("task #{tid} missing req_ids") if task["req_ids"].empty?
  fail!("task #{tid} missing eval_ids") if task["eval_ids"].empty?
  fail!("task #{tid} missing touched path or path") if task["paths"].empty?
  fail!("task #{tid} missing done_when or next") if task["done_when"].to_s.strip.empty?
  task["req_ids"].each do |rid|
    fail!("task #{tid} references unknown requirement #{rid}") unless req_ids.include?(rid)
  end
  task["eval_ids"].each do |eid|
    fail!("task #{tid} references unknown eval #{eid}") unless eval_ids.include?(eid)
  end
end

fail!("design.md missing required sections") unless design_has_required_sections?(design_md)

puts "[PASS] feature package base checks look valid"
