# GRAPH

Provisional name. **Consolidation workspace**, not a product: `from-facts/` envelope adapters, `gaps-kernel/` 7-layer paste, `from-code/` AST graph extractor. STACK: integration/research. **Not the live decision path.**

## 1. Pipeline Position & Role

**HISTORICAL / RESEARCH.** Conceptual ancestor of envelope/handshake thinking. GAPS moved here from EDDP.

## 2. Full System Scope & Architectural Depth

Three unrelated programs in one folder.

1. **from-facts** — `ContextEnvelope` (v2.1 vs v2.3 field sets). `GsaUniversalAdapter.process_payload` async: hooks → `execute_governance_logic` → SHA-256 "interlock". `UserInputModule`/`AiOutputModule` stamp `"USER_ORIGIN_VERIFIED"` / `"AI_OUTPUT_VERIFIED"` — **labels, not verification**.
2. **gaps-kernel** — L1–L7 `process(payload)` (`Foundation` → `Filtration` → `Lexicon` → `Context` → `Sentinel` → `Audit` → `Surface`) + `_gaps_authenticated` handshake. L5 sets `threat_detected`; L7 substitutes an error dict (does not halt the process earlier). L6 seal uses nonce+`time.time_ns()` (**not replay-stable**).
3. **from-code** — AST visitor. `from cns.graph import Node, Edge, Graph` — **private CNS**. Unrunnable publicly.

`_cached_signature_provider` is `@lru_cache` on a `ContextEnvelope` containing dicts → **TypeError: unhashable**. Documented, unfixed. "Rotational temporal interlock" is SHA-256 of msgpack + `"GENESIS"` parent every time (parent never rotates).

## 3. What It Does NOT Do / Non-Goals

Not a graph database, not live governance, not provenance proof.

## 4. Brutally Honest Current Status & Gaps

Flattened `gaps_multilayer_governance_source.py` unparseable; `_calculate_optimal_order` / `_red_blue_audit` unrecovered. Private `cns` git pin. Duplicate v2.3 recovered copy. Files ending with commented-out `.gitignore` paste. Name GRAPH is provisional because **there is no graph**.

## 5. Core Invariants & Guarantees

GAPS: missing module → PermissionError; missing seal → ValueError; oversized → MemoryError. Hash is unkeyed SHA-256. Origin stamps are strings.

## 6. Inputs, Outputs & Type Contracts

`_gaps_headers.{metadata, risk_metrics, structural_indices}`. Cognitive weights `analysis:0.6, synthesis:0.3, evaluation:0.1`. `max_token_length=1000`. L5 injection signatures include `"null"`, `"undefined"` (noise).

## 7. Stack Integration Topology

```text
EDDP GAPS paste → GRAPH/gaps-kernel
GsaUniversalAdapter name also appears in ICEBERG recovery / ANVIL — this copy is not imported
sentinel_os sage_k is a different graph
```

**Safe to archive.**

Proprietary. Copyright (c) 2026 William King. All rights reserved. See LICENSE.
