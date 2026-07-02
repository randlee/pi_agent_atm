#!/usr/bin/env bash
# scripts/reconcile_beads_ledger.sh — idempotent diff of open bead set vs open ledger entries
#
# Cross-checks open beads against critical/high gaps in the parity ledger to prevent
# completion illusion where all beads are closed but critical gaps remain open.
#
# Usage:
#   ./scripts/reconcile_beads_ledger.sh
#
# Exit codes:
#   0: All active ledger gaps have corresponding active beads, no orphans
#   1: Found orphans (active ledger gaps without beads, or active gap beads without active ledger entries)
#   2: Script error (missing files, invalid JSON, etc.)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# File paths.
LEDGER_FILE="$PROJECT_ROOT/docs/evidence/dropin-parity-gap-ledger.json"
BEADS_FILE="$PROJECT_ROOT/.beads/issues.jsonl"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Check prerequisites
check_prerequisites() {
    if [[ ! -f "$LEDGER_FILE" ]]; then
        log_error "Gap ledger not found: $LEDGER_FILE"
        exit 2
    fi

    if ! command -v jq >/dev/null 2>&1; then
        log_error "jq is required but not installed"
        exit 2
    fi

    if [[ ! -f "$BEADS_FILE" ]]; then
        log_error "Beads ledger not found: $BEADS_FILE"
        exit 2
    fi
}

# Extract active critical/high gaps from ledger
get_open_ledger_gaps() {
    log_info "Extracting open critical/high gaps from ledger..."

    # Get entries with critical or high severity that are not retired/resolved/closed.
    # Missing status/mismatch_kind means the gap is still active.
    jq -r '.entries[] |
        select(.severity == "critical" or .severity == "high") |
        select((.status // "open") != "retired" and (.status // "open") != "resolved" and (.status // "open") != "closed") |
        select((.mismatch_kind // "open") != "retired" and (.mismatch_kind // "open") != "resolved" and (.mismatch_kind // "open") != "closed") |
        "\(.gap_id)|\(.severity)|\(.owner_issue_primary // "")|\(.area // "")"' "$LEDGER_FILE" | \
    while IFS='|' read -r gap_id severity owner_bead area; do
        echo "LEDGER_GAP:$gap_id:$severity:$owner_bead:$area"
    done
}

# Get active beads from the checked-in beads ledger
get_open_beads() {
    log_info "Fetching active beads..."

    jq -r 'select(type == "object") |
        select(.status == "open" or .status == "in_progress") |
        "\(.id)|\(.title // "")|\(.labels // [] | join(","))|\(.external_ref // .external_id // "")"' | \
    while IFS='|' read -r bead_id title labels external_ref; do
        echo "OPEN_BEAD:$bead_id|$title|$labels|$external_ref"
    done < <(jq -c '.' "$BEADS_FILE")
}

# Match ledger gaps with beads
match_gaps_to_beads() {
    log_info "Reading gap ledger entries..."
    log_info "Reading active beads..."

    LEDGER_FILE="$LEDGER_FILE" BEADS_FILE="$BEADS_FILE" python3 - <<'PY'
import json
import os
import sys
from pathlib import Path

ledger_file = Path(os.environ["LEDGER_FILE"])
beads_file = Path(os.environ["BEADS_FILE"])

ledger_payload = json.loads(ledger_file.read_text(encoding="utf-8"))
ledger_entries = ledger_payload.get("entries", [])
open_gaps = []
for entry in ledger_entries:
    if not isinstance(entry, dict):
        continue
    if entry.get("severity") not in {"critical", "high"}:
        continue
    status = str(entry.get("status", "open"))
    mismatch_kind = str(entry.get("mismatch_kind", "open"))
    if status in {"retired", "resolved", "closed"}:
        continue
    if mismatch_kind in {"retired", "resolved", "closed"}:
        continue
    open_gaps.append(
        {
            "gap_id": str(entry.get("gap_id", "")).strip(),
            "severity": str(entry.get("severity", "")).strip(),
            "owner_bead": str(entry.get("owner_issue_primary", "")).strip(),
            "area": str(entry.get("area", "")).strip(),
        }
    )

open_beads = []
for raw_line in beads_file.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if not line:
        continue
    bead = json.loads(line)
    if bead.get("status") not in {"open", "in_progress"}:
        continue
    open_beads.append(
        {
            "id": str(bead.get("id", "")).strip(),
            "title": str(bead.get("title", "")).strip(),
            "external_ref": str(bead.get("external_ref") or bead.get("external_id") or "").strip(),
        }
    )

print(f"\033[0;32m[INFO]\033[0m Found {len(open_gaps)} active ledger gaps and {len(open_beads)} active beads")

matched_bead_ids = set()
active_gap_ids = {gap["gap_id"] for gap in open_gaps if gap["gap_id"]}
ledger_orphan_count = 0
bead_orphan_count = 0

print("\033[0;32m[INFO]\033[0m Checking for ledger gaps without beads...")
for gap in open_gaps:
    match = None
    if gap["owner_bead"]:
        match = next((bead for bead in open_beads if bead["id"] == gap["owner_bead"]), None)
    if match is None and gap["gap_id"]:
        match = next((bead for bead in open_beads if bead["external_ref"] == gap["gap_id"]), None)
    if match is None:
        print(f"\033[0;31m[ERROR]\033[0m ORPHAN LEDGER GAP: {gap['gap_id']} ({gap['severity']} severity, area: {gap['area']})")
        if gap["owner_bead"]:
            print(f"\033[0;31m[ERROR]\033[0m   Expected owner bead: {gap['owner_bead']}")
        print(f"\033[0;31m[ERROR]\033[0m   Create or reopen a bead with --external-ref {gap['gap_id']}, or update owner_issue_primary to an open bead.")
        ledger_orphan_count += 1
    else:
        matched_bead_ids.add(match["id"])

print("\033[0;32m[INFO]\033[0m Checking for beads without corresponding ledger gaps...")
for bead in open_beads:
    external_ref = bead["external_ref"]
    if bead["id"] in matched_bead_ids:
        continue
    if external_ref.startswith("gap-") and external_ref not in active_gap_ids:
        print(f"\033[0;31m[ERROR]\033[0m ORPHAN GAP BEAD: {bead['id']} - {bead['title']}")
        print(f"\033[0;31m[ERROR]\033[0m   external_ref={external_ref} is not an active critical/high ledger gap")
        print("\033[0;31m[ERROR]\033[0m   Close the bead, clear/update external_ref, or restore the ledger gap if it is still active.")
        bead_orphan_count += 1

if ledger_orphan_count == 0 and bead_orphan_count == 0:
    print("\033[0;32m[INFO]\033[0m SUCCESS: No orphan ledger gaps or gap-tracking beads found")
    sys.exit(0)

print(f"\033[0;31m[ERROR]\033[0m FAILURE: Found {ledger_orphan_count} orphan ledger gaps and {bead_orphan_count} orphan gap beads")
sys.exit(1)
PY
}

# Main function
main() {
    log_info "Starting beads ↔ ledger reconciliation..."

    check_prerequisites

    if ! match_gaps_to_beads; then
        log_error "Reconciliation failed - there are orphan entries"
        exit 1
    fi

    log_info "Reconciliation completed successfully - no orphans found"
    exit 0
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
