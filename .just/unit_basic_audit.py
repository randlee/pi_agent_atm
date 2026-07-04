#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys


@dataclass(frozen=True)
class TaxonomyRule:
    match_kind: str
    pattern: str
    category: str
    rationale: str


CATEGORY_DEFINITIONS = {
    "unit_basic_fast_deterministic": (
        "Fast deterministic core-unit coverage retained in the first required gate."
    ),
    "async_timing_dependent_flow_tests": (
        "Real wall-clock timeout, retry, cooldown, abort, or completion timing paths "
        "that do not stay within a fast required gate."
    ),
    "fixture_vcr_inventory_audits": (
        "Fixture, VCR, conformance, or replay inventory audits that validate broader "
        "upstream contracts rather than the first PR gate."
    ),
    "network_http_streaming_dependent_tests": (
        "Credential, HTTP, streaming, local test-server, or provider request-capture "
        "tests that depend on network-style flows outside the early baseline."
    ),
    "extension_runtime_policy_integration_tests": (
        "Extension runtime, hostcall, policy, ledger, and dispatcher integration "
        "matrices that are broader than the first compile/basic-unit gate."
    ),
    "interactive_tui_workflow_tests": (
        "Interactive TUI, rendering, keybinding, and operator workflow tests that "
        "exercise higher-level UI behavior outside the first PR gate."
    ),
    "subprocess_bash_tool_execution_tests": (
        "Subprocess, bash-tool, grep-tool, package-manager, or doctor command-surface "
        "tests that are not part of the first strict unit gate."
    ),
    "rpc_command_queue_integration_tests": (
        "RPC retry, queue, bridge, and extension-command integration tests that are "
        "broader than the first required unit lane."
    ),
    "persistence_index_sqlite_artifact_tests": (
        "Session index, sqlite, storage, and persistence artifact verification tests "
        "that belong to broader persistence coverage."
    ),
    "subsystem_stress_or_endurance_tests": (
        "Stress, endurance, or broader system-behavior tests intentionally kept out "
        "of the first required gate."
    ),
}


INCLUDE_RULES = (
    TaxonomyRule(
        "prefix",
        "acp::tests",
        "unit_basic_fast_deterministic",
        "ACP protocol parsing and deterministic permission/client behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "agent::abort_tests",
        "unit_basic_fast_deterministic",
        "Agent abort state transitions with deterministic in-memory harnesses.",
    ),
    TaxonomyRule(
        "prefix",
        "agent::compatible_tool_parallelism_tests",
        "unit_basic_fast_deterministic",
        "Pure scheduling and compatibility calculations for tool parallelism.",
    ),
    TaxonomyRule(
        "prefix",
        "agent::extensions_integration_tests",
        "unit_basic_fast_deterministic",
        "Deterministic mocked extension-agent interactions without external I/O.",
    ),
    TaxonomyRule(
        "prefix",
        "agent::message_queue_tests",
        "unit_basic_fast_deterministic",
        "In-memory queue ordering and mode semantics.",
    ),
    TaxonomyRule(
        "prefix",
        "agent::tests",
        "unit_basic_fast_deterministic",
        "Core agent state, model selection, and compaction event serialization behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "agent::tool_effect_batch_planning_tests",
        "unit_basic_fast_deterministic",
        "Deterministic tool-effect batching invariants.",
    ),
    TaxonomyRule(
        "prefix",
        "agent::turn_event_tests",
        "unit_basic_fast_deterministic",
        "Ordered turn-event emission semantics.",
    ),
    TaxonomyRule(
        "prefix",
        "agent_cx::tests",
        "unit_basic_fast_deterministic",
        "Context wrapper and accessor behavior with in-memory handles.",
    ),
    TaxonomyRule(
        "prefix",
        "app::tests",
        "unit_basic_fast_deterministic",
        "CLI/app model-selection and normalization behavior without external systems.",
    ),
    TaxonomyRule(
        "prefix",
        "autocomplete::tests",
        "unit_basic_fast_deterministic",
        "Deterministic completion tokenization, ranking, and path logic.",
    ),
    TaxonomyRule(
        "prefix",
        "cli::tests",
        "unit_basic_fast_deterministic",
        "Pure command-line parsing and flag normalization coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "compaction::tests",
        "unit_basic_fast_deterministic",
        "Transcript compaction calculations and serialization rules.",
    ),
    TaxonomyRule(
        "prefix",
        "config::tests",
        "unit_basic_fast_deterministic",
        "Configuration parsing and merge behavior using local fixtures only.",
    ),
    TaxonomyRule(
        "prefix",
        "connectors::tests",
        "unit_basic_fast_deterministic",
        "Small connector invariants without external services.",
    ),
    TaxonomyRule(
        "prefix",
        "crypto_shim::tests",
        "unit_basic_fast_deterministic",
        "Pure crypto helper and hashing behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "error::tests",
        "unit_basic_fast_deterministic",
        "Error-shape, serialization, and classification invariants.",
    ),
    TaxonomyRule(
        "prefix",
        "error_hints::tests",
        "unit_basic_fast_deterministic",
        "Deterministic error-hint derivation logic.",
    ),
    TaxonomyRule(
        "prefix",
        "flake_classifier::tests",
        "unit_basic_fast_deterministic",
        "Static flake classification heuristics.",
    ),
    TaxonomyRule(
        "prefix",
        "migrations::tests",
        "unit_basic_fast_deterministic",
        "Migration metadata and schema-shape checks without live persistence flows.",
    ),
    TaxonomyRule(
        "prefix",
        "model::tests",
        "unit_basic_fast_deterministic",
        "Message/content-type serialization and conversion coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "model_routing::tests",
        "unit_basic_fast_deterministic",
        "Deterministic routing and selection helpers.",
    ),
    TaxonomyRule(
        "prefix",
        "models::tests",
        "unit_basic_fast_deterministic",
        "Built-in model registry resolution and alias behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "permissions::tests",
        "unit_basic_fast_deterministic",
        "Permission-store semantics and serialization invariants.",
    ),
    TaxonomyRule(
        "prefix",
        "platform::tests",
        "unit_basic_fast_deterministic",
        "Small platform helper invariants.",
    ),
    TaxonomyRule(
        "prefix",
        "provider::tests",
        "unit_basic_fast_deterministic",
        "Provider abstraction helpers without live provider transport behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "provider_metadata::tests",
        "unit_basic_fast_deterministic",
        "Provider metadata normalization and lookup behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "resources::tests",
        "unit_basic_fast_deterministic",
        "Resource loading and resolution logic using local fixtures only.",
    ),
    TaxonomyRule(
        "prefix",
        "sdk::tests",
        "unit_basic_fast_deterministic",
        "SDK request/response helper behavior without external runtime dependencies.",
    ),
    TaxonomyRule(
        "prefix",
        "session::tests",
        "unit_basic_fast_deterministic",
        "Core session tree and JSONL semantics without index/sqlite persistence sweeps.",
    ),
    TaxonomyRule(
        "prefix",
        "sse::tests",
        "unit_basic_fast_deterministic",
        "Pure SSE parser chunking and protocol invariants.",
    ),
    TaxonomyRule(
        "prefix",
        "tui::tests",
        "unit_basic_fast_deterministic",
        "Small deterministic TUI helper rendering invariants.",
    ),
)


EXCLUDE_RULES = (
    TaxonomyRule(
        "exact",
        "acp::tests::permission_request_times_out_fail_closed",
        "async_timing_dependent_flow_tests",
        "This case intentionally waits for a timeout path and is incompatible with a fast required gate.",
    ),
    TaxonomyRule(
        "prefix",
        "auth::tests",
        "network_http_streaming_dependent_tests",
        "Credential refresh, OAuth, device-flow, and local HTTP token-exchange coverage belongs to broader auth/provider testing.",
    ),
    TaxonomyRule(
        "prefix",
        "compaction_worker::tests",
        "async_timing_dependent_flow_tests",
        "Worker cooldown, abort, and pending-result timing behavior relies on real timing paths.",
    ),
    TaxonomyRule(
        "prefix",
        "conformance::normalization",
        "fixture_vcr_inventory_audits",
        "Conformance normalization checks are part of broader upstream replay/inventory coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "conformance::tests",
        "fixture_vcr_inventory_audits",
        "Conformance suites validate broader upstream replay and fixture contracts.",
    ),
    TaxonomyRule(
        "prefix",
        "conformance_shapes::tests",
        "fixture_vcr_inventory_audits",
        "Conformance shape audits belong to broader upstream compatibility evidence.",
    ),
    TaxonomyRule(
        "prefix",
        "doctor::tests",
        "subprocess_bash_tool_execution_tests",
        "Doctor coverage probes command-surface and system-diagnostic flows beyond the first unit gate.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_conformance_matrix::tests",
        "fixture_vcr_inventory_audits",
        "Extension conformance matrices validate broader compatibility inventories.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_dispatcher::tests",
        "extension_runtime_policy_integration_tests",
        "Dispatcher and delivery-path matrices belong to broader extension runtime coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_events::tests",
        "extension_runtime_policy_integration_tests",
        "Extension event translation and delivery semantics are broader runtime integration coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_inclusion::tests",
        "extension_runtime_policy_integration_tests",
        "Extension inclusion-policy matrices are broader than the first unit gate.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_index::tests",
        "extension_runtime_policy_integration_tests",
        "Extension indexing and discovery flows belong to broader extension runtime coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_license::tests",
        "extension_runtime_policy_integration_tests",
        "License/policy enforcement coverage belongs to broader extension governance testing.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_popularity::tests",
        "extension_runtime_policy_integration_tests",
        "Extension popularity and ranking audits are broader extension-surface checks.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_preflight::tests",
        "extension_runtime_policy_integration_tests",
        "Preflight checks exercise broader extension runtime validation paths.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_replay::tests",
        "fixture_vcr_inventory_audits",
        "Replay verification belongs to broader upstream fixture/replay coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_scoring::tests",
        "extension_runtime_policy_integration_tests",
        "Extension scoring and risk evaluation matrices are broader runtime policy coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_tools::tests",
        "extension_runtime_policy_integration_tests",
        "Extension tool registration and runtime integration exceeds the first unit gate.",
    ),
    TaxonomyRule(
        "prefix",
        "extension_validation::tests",
        "fixture_vcr_inventory_audits",
        "Validation suites enforce broader extension contract/audit behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "extensions::compatibility_scanner_comment_tests",
        "extension_runtime_policy_integration_tests",
        "Compatibility scanner coverage is part of broader extension runtime auditing.",
    ),
    TaxonomyRule(
        "prefix",
        "extensions::policy_snapshot_tests",
        "extension_runtime_policy_integration_tests",
        "Policy snapshot tests belong to broader extension policy integration coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "extensions::tests",
        "extension_runtime_policy_integration_tests",
        "Large extension-runtime, hostcall, ledger, and policy matrices are outside the first gate.",
    ),
    TaxonomyRule(
        "prefix",
        "extensions_js::tests",
        "extension_runtime_policy_integration_tests",
        "JS runtime bridge coverage exercises broader extension-host integration.",
    ),
    TaxonomyRule(
        "prefix",
        "hostcall_amac::tests",
        "extension_runtime_policy_integration_tests",
        "Hostcall AMAC execution coverage is broader extension runtime integration.",
    ),
    TaxonomyRule(
        "prefix",
        "hostcall_io_uring_lane::tests",
        "extension_runtime_policy_integration_tests",
        "Hostcall IO lane coverage is broader runtime/path execution behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "hostcall_queue::tests",
        "extension_runtime_policy_integration_tests",
        "Hostcall queue and scheduling semantics are broader runtime integration coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "hostcall_rewrite::tests",
        "extension_runtime_policy_integration_tests",
        "Hostcall rewrite/optimization flows are broader extension runtime behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "hostcall_s3_fifo::tests",
        "extension_runtime_policy_integration_tests",
        "Hostcall FIFO coordination belongs to broader runtime integration coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "hostcall_superinstructions::tests",
        "extension_runtime_policy_integration_tests",
        "Hostcall superinstruction compilation/execution is broader runtime integration coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "hostcall_trace_jit::tests",
        "extension_runtime_policy_integration_tests",
        "Trace/JIT and guard logic belongs to broader runtime optimization coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "http::client",
        "network_http_streaming_dependent_tests",
        "HTTP client transport and retry behavior belongs to provider/network coverage, not the first gate.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::agent",
        "interactive_tui_workflow_tests",
        "Interactive agent workflow coverage exercises higher-level TUI behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::commands",
        "interactive_tui_workflow_tests",
        "Interactive command-surface behavior belongs to broader TUI workflow coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::conversation",
        "interactive_tui_workflow_tests",
        "Conversation rendering/state flows belong to broader TUI workflow coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::ext_session",
        "interactive_tui_workflow_tests",
        "Interactive extension-session flows exercise broader UI/runtime coordination.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::file_refs",
        "interactive_tui_workflow_tests",
        "Interactive file-reference workflows belong to broader TUI behavior coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::keybindings",
        "interactive_tui_workflow_tests",
        "Interactive keybinding workflow tests are broader UI behavior coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::model_selector_ui",
        "interactive_tui_workflow_tests",
        "Model-selector UI flows belong to broader interactive coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::perf",
        "subsystem_stress_or_endurance_tests",
        "Interactive performance harness coverage is intentionally outside the first gate.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::share",
        "interactive_tui_workflow_tests",
        "Interactive share flows exercise broader operator workflow behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::startup_changelog_tests",
        "interactive_tui_workflow_tests",
        "Startup changelog UI coverage belongs to broader operator workflow behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::state",
        "interactive_tui_workflow_tests",
        "Interactive state-management flows are broader TUI behavior coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::tests",
        "interactive_tui_workflow_tests",
        "General interactive application tests exercise broader TUI workflows.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::tool_render",
        "interactive_tui_workflow_tests",
        "Interactive tool rendering coverage belongs to broader TUI behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "interactive::view",
        "interactive_tui_workflow_tests",
        "Interactive view/update flows are broader UI behavior coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "keybindings::tests",
        "interactive_tui_workflow_tests",
        "Keybinding rendering and input workflows belong to broader UI behavior coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "model_selector::tests",
        "interactive_tui_workflow_tests",
        "Model selector UI/state tests are broader interactive workflow coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "package_manager::tests",
        "subprocess_bash_tool_execution_tests",
        "Package-manager command-surface and process interactions are broader than the first gate.",
    ),
    TaxonomyRule(
        "prefix",
        "perf_build::tests",
        "subsystem_stress_or_endurance_tests",
        "Build/performance harness coverage is intentionally outside the first PR gate.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::anthropic",
        "network_http_streaming_dependent_tests",
        "Provider request/stream/header tests depend on local HTTP transport behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::azure",
        "network_http_streaming_dependent_tests",
        "Provider request/stream/header tests depend on local HTTP transport behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::bedrock",
        "network_http_streaming_dependent_tests",
        "Provider auth/signing and request-shape transport coverage belongs to broader provider testing.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::cohere",
        "network_http_streaming_dependent_tests",
        "Provider request/stream/header tests depend on local HTTP transport behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::copilot",
        "network_http_streaming_dependent_tests",
        "Credential exchange and provider transport behavior belongs to broader provider coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::gemini",
        "network_http_streaming_dependent_tests",
        "Provider request/stream/header tests depend on local HTTP transport behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::gitlab",
        "network_http_streaming_dependent_tests",
        "OAuth and transport behavior belongs to broader provider/network coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::model_fetch",
        "network_http_streaming_dependent_tests",
        "Model fetch/cache/provider URL behavior belongs to broader provider/network coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::openai",
        "network_http_streaming_dependent_tests",
        "Provider request/stream/header tests depend on local HTTP transport behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::openai_responses",
        "network_http_streaming_dependent_tests",
        "Responses API streaming/request-capture flows belong to broader provider/network coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::tests",
        "network_http_streaming_dependent_tests",
        "Cross-provider transport/runtime integration coverage is broader than the first unit gate.",
    ),
    TaxonomyRule(
        "prefix",
        "providers::vertex",
        "network_http_streaming_dependent_tests",
        "Provider auth/transport behavior belongs to broader provider/network coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "resource_governor::tests",
        "extension_runtime_policy_integration_tests",
        "Resource-governor coordination belongs to broader runtime policy coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "rpc::retry_tests",
        "rpc_command_queue_integration_tests",
        "RPC retry timelines and cancellation flows exceed the first strict unit gate.",
    ),
    TaxonomyRule(
        "prefix",
        "rpc::tests",
        "rpc_command_queue_integration_tests",
        "RPC command-queue and extension-session integration coverage is broader than the first gate.",
    ),
    TaxonomyRule(
        "prefix",
        "rpc::ui_bridge_tests",
        "rpc_command_queue_integration_tests",
        "RPC UI bridge flows exercise higher-level integration behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "scheduler::tests",
        "extension_runtime_policy_integration_tests",
        "Scheduler behavior participates in broader runtime/hostcall coordination coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "session_index::test_common",
        "persistence_index_sqlite_artifact_tests",
        "Session index/indexing fixtures belong to broader persistence coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "session_index::tests",
        "persistence_index_sqlite_artifact_tests",
        "Session index refresh, cold-start, and artifact handling are broader persistence coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "session_metrics::tests",
        "persistence_index_sqlite_artifact_tests",
        "Session metrics aggregation belongs to broader persistence/reporting coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "session_picker::tests",
        "interactive_tui_workflow_tests",
        "Session picker workflows exercise higher-level TUI behavior.",
    ),
    TaxonomyRule(
        "prefix",
        "session_sqlite::tests",
        "persistence_index_sqlite_artifact_tests",
        "SQLite session metadata/storage verification belongs to broader persistence coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "session_store_v2::proptests",
        "persistence_index_sqlite_artifact_tests",
        "Session store v2 persistence and quarantine behavior belongs to broader storage coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "swarm_activity_ledger::tests",
        "subsystem_stress_or_endurance_tests",
        "Swarm ledger aggregation and saturation analysis belongs to broader system-behavior coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "swarm_flight_recorder::tests",
        "subsystem_stress_or_endurance_tests",
        "Flight-recorder invariants belong to broader system-behavior coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "swarm_progress_slo::tests",
        "subsystem_stress_or_endurance_tests",
        "Swarm SLO and saturation profile tests belong to broader system-behavior coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "terminal_images::tests",
        "interactive_tui_workflow_tests",
        "Terminal image rendering behavior belongs to broader operator/UI coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "theme::tests",
        "interactive_tui_workflow_tests",
        "Theme discovery/rendering behavior belongs to broader UI coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "tools::tests",
        "subprocess_bash_tool_execution_tests",
        "Bash, grep, ls, and artifact spillover command-surface tests are broader than the first unit gate.",
    ),
    TaxonomyRule(
        "prefix",
        "vcr::tests",
        "fixture_vcr_inventory_audits",
        "VCR recording/replay behavior is broader fixture-contract coverage.",
    ),
    TaxonomyRule(
        "prefix",
        "version_check::tests",
        "network_http_streaming_dependent_tests",
        "Version-check behavior depends on broader remote/provider-style transport semantics.",
    ),
)


UNIT_BASIC_INCLUDE_PREFIXES = tuple(rule.pattern for rule in INCLUDE_RULES)

UNIT_BASIC_SKIP_FILTERS_BY_PREFIX = {
    "acp::tests": ("permission_request_times_out_fail_closed",),
}


def classify_inline_test(test_name: str) -> TaxonomyRule:
    for rule in EXCLUDE_RULES:
        if rule.match_kind == "exact" and test_name == rule.pattern:
            return rule
    for rule in INCLUDE_RULES:
        if rule.match_kind == "prefix" and test_name.startswith(f"{rule.pattern}::"):
            return rule
    for rule in EXCLUDE_RULES:
        if rule.match_kind == "prefix" and test_name.startswith(f"{rule.pattern}::"):
            return rule
    raise KeyError(f"unclassified inline test: {test_name}")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def list_inline_tests() -> list[str]:
    completed = subprocess.run(
        ["cargo", "test", "--lib", "--", "--list"],
        cwd=repo_root(),
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        line.split(": test", 1)[0].strip()
        for line in completed.stdout.splitlines()
        if line.endswith(": test")
    ]


def category_counts(test_names: list[str]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for test_name in test_names:
        counts[classify_inline_test(test_name).category] += 1
    return counts


def unit_basic_inline_commands() -> tuple[tuple[str, tuple[str, ...]], ...]:
    commands: list[tuple[str, tuple[str, ...]]] = []
    for prefix in UNIT_BASIC_INCLUDE_PREFIXES:
        commands.append(
            (
                prefix,
                UNIT_BASIC_SKIP_FILTERS_BY_PREFIX.get(prefix, ()),
            )
        )
    return tuple(commands)


def emit_summary() -> str:
    test_names = list_inline_tests()
    counts = category_counts(test_names)
    include_count = counts["unit_basic_fast_deterministic"]
    exclude_count = len(test_names) - include_count

    lines = [
        f"total_inline_tests\t{len(test_names)}",
        f"unit_basic_include_count\t{include_count}",
        f"unit_basic_exclude_count\t{exclude_count}",
        f"unit_basic_include_prefixes\t{len(UNIT_BASIC_INCLUDE_PREFIXES)}",
    ]
    for category_name in sorted(counts):
        lines.append(f"category::{category_name}\t{counts[category_name]}")
    return "\n".join(lines) + "\n"


def emit_tsv() -> str:
    rows = [
        "\t".join(
            (
                "test_name",
                "included_in_unit_basic",
                "category",
                "rule_kind",
                "rule_pattern",
                "rationale",
            )
        )
    ]
    for test_name in list_inline_tests():
        rule = classify_inline_test(test_name)
        rows.append(
            "\t".join(
                (
                    test_name,
                    "yes" if rule.category == "unit_basic_fast_deterministic" else "no",
                    rule.category,
                    rule.match_kind,
                    rule.pattern,
                    rule.rationale,
                )
            )
        )
    return "\n".join(rows) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) == 1 or argv[1] == "summary":
        sys.stdout.write(emit_summary())
        return 0
    if argv[1] == "tsv":
        sys.stdout.write(emit_tsv())
        return 0
    if argv[1] == "commands":
        for prefix, skip_filters in unit_basic_inline_commands():
            print(f"{prefix}\t{','.join(skip_filters)}")
        return 0
    raise SystemExit("usage: unit_basic_audit.py [summary|tsv|commands]")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
