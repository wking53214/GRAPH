# GRAPH

**Name is provisional.** GRAPH (Governance, Routing, and Anchor
Processing Hierarchy) previously had no dedicated repo of its own —
almost all of its content was sitting in a repo named `FACTS`, despite
the name mismatch. Renaming this repo later is trivial (Settings →
rename), so this name wasn't a blocker on doing the consolidation.

## Contents

- `from-facts/` — everything from the former
  [FACTS](https://github.com/wking53214/FACTS) repo except its
  AST-extractor-signature files (those were duplicates of the recurring
  `GraphExtractor`/`extract_graph` tool and went to `synapsis` instead).
  Includes `graph-module-registry.py` — the one file in the whole
  cross-repo sweep that's genuinely close to working (parses clean once
  `[Row ###]` tags are stripped, one small dataclass bug away from
  running) — plus the other `graph-v2.*.py` variants,
  `graph-cryptographic-engine.py`, `graph-adapter-hooks.py`, and
  `graph-context-envelope.py`.

  Note: `graph-v2.3-synthesis-payload.py` contains an embedded
  `MAGNA_Orchestrator`/`ComputeNode`/`ChatAggregator` side-thread that's
  unrelated to GRAPH — left in place as-is since separating it out would
  be a code edit, out of scope for this move-only pass.

- `gaps-kernel/` — `gaps_multilayer_governance_source.py`/`_adapter.py`,
  moved here from EDDP (formerly Data_files). This is the real GAPS
  KERNEL implementation (the `register_as_module` decorator referenced
  throughout ARCHIVE's report-generation prompts). GRAPH and GAPS are
  closely related governance-layer concepts, folded together here as a
  starting point — if William would rather split them into separate
  repos later, that's an easy follow-up, not a re-do.

The former `FACTS` repo still exists on GitHub but now only contains
`PROVENANCE.md`/`TRANSCRIPT.md` (the historical record) — left in place
for review, not auto-deleted.

This is a pure content move (files relocated, git history not
preserved cross-repo) — no code edits, bug fixes, or class renames were
made as part of this pass. That's a separate, later pass.
