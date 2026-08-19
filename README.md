# GRAPH

**Name is provisional.** GRAPH (Governance, Routing, and Anchor
Processing Hierarchy) previously had no dedicated repo of its own —
almost all of its content was sitting in a repo named `FACTS`, despite
the name mismatch. Renaming this repo later is trivial (Settings →
rename), so this name wasn't a blocker on doing the consolidation.

## Contents

- `from-facts/` — real GRAPH code, consolidated down to two canonical,
  working implementations after a first integration pass (row-tag
  stripping, a `__slots__` dataclass bug fix, dependency install, and
  merging each variant family's best features together — see git log
  for the full account):

  - `graph-module-registry.py`: the "dual-payload" family — extracts
    user input and AI output separately, then combines them into a
    synthesized full payload. Has pre/post hooks, stores
    `module_version`, tags output with `extraction_mode`, and includes
    a runnable demo driver (`run_graph_driver`).
  - `graph-v2.1-user-ai-modules.py`: the "simple" family — a single
    `payload_data` + `session_state_mapping` envelope, with an
    optional `GeminiSanitizer` pre-processing stage. Has pre/post
    hooks and is the only variant that got envelope immutability right
    (copies the payload dict and uses `dataclasses.replace()` instead
    of mutating in place).

  Both require `msgpack` (`requirements.txt`) and both run into the
  same known, disclosed, not-yet-fixed bug: `_cached_signature_provider`
  is `@functools.lru_cache`'d but takes an argument containing a
  `MappingProxyType`/`dict`, which isn't hashable — a real design
  decision (serialize-then-cache vs. drop caching vs. restructure the
  payload type), not something fixed unilaterally in this pass.

  Eight other files (`graph-cryptographic-engine.py` — a pure
  duplicate of `graph-module-registry.py`; `graph-v2.1-indexed-audited.py`,
  `graph-v2.3-extraction-logic.py`, `graph-v2.3-indexed-driver.py`,
  `graph-adapter-hooks.py` — each had all their working, non-duplicate
  logic folded into one of the two canonical files above; and
  `graph-v2.1-flattened-base.py`, `graph-v2.3-driver-enabled.py`,
  `graph-v2.3-dual-extract-combined.py`, `graph-context-envelope.py` —
  genuinely flattened, single-line files with no real code left to
  recover) were removed as redundant once their content was accounted
  for elsewhere.

  `graph-v2.3-synthesis-payload.py` remains untouched — it's an
  embedded `MAGNA_Orchestrator`/`ComputeNode`/`ChatAggregator`
  side-thread, unrelated to GRAPH.

  AST-extractor-signature files that were also found in this repo went
  to `synapsis` instead (the recurring `GraphExtractor`/`extract_graph`
  tool, not GRAPH content).

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

`gaps-kernel/`'s content is unrelated to `from-facts/`'s integration
work above and untouched since the original move — files relocated,
git history not preserved cross-repo, no code edits.
