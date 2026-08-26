# GRAPH

## Governance, Routing, and Anchor Processing Hierarchy

> **Status: Consolidated architectural repository / integration baseline**
>
> The name GRAPH is provisional. The repository currently brings together two related bodies of governance-oriented processing code and the GAPS Kernel as a consolidated architectural workspace.

---

# Overview

GRAPH is an architectural construct for representing, processing, and preserving structured relationships between user-originated input, AI-generated output, session context, module identity, and governance-layer processing.

Its central concern is the controlled movement of information through a system while maintaining sufficient structure to distinguish:

- what entered the system;
- what the system generated;
- what contextual state accompanied the interaction;
- which module processed the information;
- how the payload was transformed;
- and what governance information should accompany the resulting representation.

The current repository is a consolidation of previously separated implementations.

It should therefore be understood as an **architectural integration baseline**, rather than as a finished single-purpose production product.

---

# Core Concept

GRAPH can be understood as a structured processing path:

    USER INPUT
        │
        ▼
    INPUT REPRESENTATION
        │
        ▼
    MODULE PROCESSING
        │
        ├── module identity
        ├── module version
        ├── processing hooks
        └── extraction mode
        │
        ▼
    AI / SYSTEM OUTPUT
        │
        ▼
    SYNTHESIZED PAYLOAD
        │
        ▼
    GOVERNANCE / DOWNSTREAM PROCESSING

The purpose is to retain structural relationships between the different pieces of information rather than flattening them into an undifferentiated payload.

---

# Why GRAPH Exists

Complex AI systems often combine several categories of information:

    HUMAN INPUT
    AI OUTPUT
    SESSION STATE
    MODULE STATE
    PROCESSING METADATA
    GOVERNANCE INFORMATION

If those elements are merged without preserving their relationships, downstream systems may no longer be able to determine where a piece of information originated or how it was produced.

GRAPH addresses this problem by treating the payload as a structured object whose components retain identifiable relationships.

---

# User / AI Separation

One of the current GRAPH implementations explicitly separates user input from AI output before synthesizing them into a combined payload.

Conceptually:

    ┌──────────────────┐
    │   USER INPUT     │
    └────────┬─────────┘
             │
             ▼
       USER PAYLOAD
             │
             │
             ├───────────────┐
             │               │
             ▼               ▼
       PROCESSING       AI OUTPUT
             │               │
             └───────┬───────┘
                     │
                     ▼
             SYNTHESIZED PAYLOAD

This separation preserves an important provenance distinction:

    WHAT THE USER PROVIDED

versus:

    WHAT THE SYSTEM GENERATED

The two can subsequently be combined into a representation suitable for downstream processing without requiring their origins to be forgotten.

---

# Dual-Payload Architecture

The `graph-module-registry.py` implementation represents the dual-payload family.

It:

- extracts user input separately;
- extracts AI output separately;
- combines the two into a synthesized full payload;
- supports pre-processing hooks;
- supports post-processing hooks;
- records module version;
- and identifies the extraction mode used.

This provides a structured representation of both sides of an interaction.

---

# Envelope Architecture

The `graph-v2.1-user-ai-modules.py` implementation represents a simpler envelope family.

It uses:

    payload_data
    +
    session_state_mapping

as the primary structured representation.

It also provides an optional preprocessing stage.

This implementation is particularly notable because it uses a copied payload and `dataclasses.replace()` rather than mutating the original envelope in place.

That provides a stronger immutability boundary around the represented payload.

---

# Immutability

An important architectural concern demonstrated by the current implementation is preservation of the original envelope.

The preferred pattern is:

    ORIGINAL PAYLOAD
          │
          ▼
       COPY / REPLACE
          │
          ▼
    TRANSFORMED PAYLOAD

rather than:

    ORIGINAL PAYLOAD
          │
          ▼
    IN-PLACE MUTATION

The distinction matters when payloads represent evidence, provenance, or governed state.

Once a payload has entered a processing boundary, downstream transformation should not silently rewrite the original representation.

---

# Module Identity

GRAPH preserves module-level information associated with processing.

This can include:

- module identity;
- module version;
- extraction mode;
- processing hooks;
- and associated payload information.

The resulting structure allows downstream systems to understand not merely the resulting data but something about the processing path that produced it.

Conceptually:

    PAYLOAD
       │
       ▼
    MODULE
       │
       ├── identity
       ├── version
       └── processing mode
       │
       ▼
    RESULT

This creates a relationship between data and the component responsible for processing it.

---

# Processing Hooks

The canonical GRAPH implementations provide pre- and post-processing hooks.

Conceptually:

    INPUT
      │
      ▼
    PRE-HOOK
      │
      ▼
    CORE PROCESSING
      │
      ▼
    POST-HOOK
      │
      ▼
    OUTPUT

This permits additional processing to be introduced at defined boundaries without necessarily rewriting the core processing path.

---

# Extraction Mode

The dual-payload implementation records the extraction mode associated with the resulting payload.

This is significant because extraction is itself a transformation.

Rather than treating the final payload as though it appeared directly from the source, the architecture can retain information about how the payload was constructed.

The distinction is:

    SOURCE

versus:

    SOURCE
       │
       ▼
    EXTRACTION METHOD
       │
       ▼
    REPRESENTATION

---

# Session Context

The envelope implementation incorporates session-state mapping alongside payload data.

This recognizes that the meaning of an individual payload may depend upon contextual state.

Conceptually:

    PAYLOAD
       +
    SESSION STATE
       │
       ▼
    CONTEXTUAL REPRESENTATION

This allows downstream processing to distinguish the data being processed from contextual information surrounding that data.

---

# Governance Relationship

GRAPH's architectural concern is closely related to governance because governance requires more than the final answer or action.

A governed system may need to know:

- what information entered the system;
- what the AI produced;
- what context existed;
- what module processed it;
- what transformation occurred;
- and what representation was passed onward.

GRAPH provides structures through which those relationships can remain visible.

It therefore operates naturally as an information-structuring layer within a larger governance architecture.

---

# Relationship to GAPS KERNEL

The repository currently contains a `gaps-kernel/` directory containing the GAPS multilayer governance source and adapter.

This component was moved into GRAPH from EDDP.

It represents a related governance-layer concept, but it is **not the same implementation as the `from-facts/` GRAPH processing code**.

The two components should therefore be understood as related architectural material currently consolidated within the same repository rather than as a single inseparable implementation.

`gaps-kernel/gaps_multilayer_governance_adapter.py` implements a seven-layer governance pipeline (`L1FoundationProcessor` through `L7SurfaceOutput`, bound together by `CoreOrchestratorBinder`) and has been verified to run end-to-end with no external dependencies beyond the standard library — `python3 gaps_multilayer_governance_adapter.py` executes the full pipeline and prints a clinical summary. This had not previously been confirmed; see Known Limitations below for what's still missing relative to `gaps_multilayer_governance_source.py`.

Conceptually:

    GRAPH PROCESSING
         │
         │ structured information /
         │ provenance relationships
         ▼
    GOVERNANCE LAYER
         │
         ▼
    GAPS KERNEL

The exact long-term repository boundary may change as the architecture matures.

---

# Repository Consolidation Status

GRAPH is currently the result of consolidation.

The original material was distributed across earlier repositories, including `FACTS`.

The current repository preserves the working GRAPH implementations while removing redundant or nonfunctional variants.

The consolidation resulted in two canonical GRAPH implementations:

    graph-module-registry.py

and:

    graph-v2.1-user-ai-modules.py

Other earlier variants had their useful logic incorporated into those canonical implementations or were identified as redundant.

This means the repository should be regarded as a **consolidated architectural baseline**.

---

# Historical Material

The former `FACTS` repository remains separately preserved as a historical record.

Its remaining material includes provenance and transcript documentation associated with the development history.

That historical repository should not be confused with the current GRAPH implementation.

GRAPH represents the consolidated working architectural material.

---

# Known Limitations

## from-facts/: cached signature provider

Both canonical GRAPH implementations currently contain a known issue involving the cached signature provider.

The implementation uses `functools.lru_cache` around a function receiving an argument containing an unhashable mapping structure.

Conceptually:

    CACHED FUNCTION
          │
          ▼
    SIGNATURE ARGUMENT
          │
          ▼
    UNHASHABLE MAPPING
          │
          ▼
       FAILURE

This has not been silently "fixed" because the correct resolution is an architectural decision.

Possible approaches include:

- serializing the payload before caching;
- removing the cache;
- or restructuring the payload type so that the cached argument is hashable.

The repository therefore preserves this issue as an explicit known limitation rather than presenting the current implementation as defect-free.

## gaps-kernel/: unrecovered functionality in the flattened source

`gaps-kernel/gaps_multilayer_governance_source.py` is a flattened, single-line raw paste (no real line breaks) and does not parse as Python — the same class of defect the `from-facts/` flattened variants had before that directory's Step 1–3 consolidation. Unlike those variants, though, this one is **not** simply redundant with the working `gaps_multilayer_governance_adapter.py` file: it contains real logic that was never carried over.

Specifically, `source.py` implements:

- **Dynamic layer-ordering**: a `_calculate_optimal_order` method (with a nested `score_order` scoring function) that evaluates multiple candidate execution orders for the seven governance layers and selects the best-scoring one, rather than using a fixed sequence.
- **Self-audit**: a `_red_blue_audit` method that inspects a module instance for specific risk patterns (e.g. a stateful internal map exposed without a thread-safe accessor, oversized tokens) and proposes corresponding patches.
- A parameterized `register_as_module(name)` decorator factory, letting a module register under an explicit name independent of its class name — `adapter.py`'s version is a simpler unparameterized decorator that always keys by `cls.__name__`.

None of the three exist in `adapter.py`, which uses a static `base_order` list and has no audit method. Because `source.py` is flattened and unparseable, this logic is currently unavailable anywhere in runnable form — porting it into `adapter.py` would be real feature work (a design decision about whether dynamic ordering and self-audit belong in the pipeline), not a mechanical fix, so it's documented here rather than guess-ported.

---

# Dependency

The canonical GRAPH implementations require `msgpack`.

The dependency is declared in the repository's requirements.

---

# Domain Independence

The underlying GRAPH processing concept is not inherently restricted to one industry.

The architectural problem it addresses occurs whenever a system must preserve relationships between:

- source information;
- generated information;
- context;
- processing modules;
- transformations;
- and governance metadata.

Potential applications include:

- AI governance;
- enterprise workflow;
- autonomous systems;
- research systems;
- software agents;
- regulated information processing;
- knowledge systems;
- and other environments where provenance and contextual relationships matter.

These represent potential applications of the architecture rather than claims that each is currently implemented.

---

# What GRAPH Is Not

GRAPH should not currently be described as:

- a finished enterprise governance platform;
- a complete graph database;
- a universal knowledge graph;
- a complete provenance system;
- or a fully production-hardened governance framework.

The repository is a consolidated architectural implementation containing working components, known limitations, and related governance-layer material.

---

# Architectural Model

The core GRAPH concept can be summarized as:

    ┌─────────────────────┐
    │     HUMAN INPUT     │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │   INPUT PAYLOAD     │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ MODULE / PROCESSING  │
    │                     │
    │ identity            │
    │ version             │
    │ extraction mode     │
    │ pre/post hooks      │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │     AI OUTPUT       │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ SYNTHESIZED PAYLOAD │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ GOVERNANCE CONTEXT  │
    └─────────────────────┘

The alternative envelope implementation simplifies the structure:

    ┌─────────────────────┐
    │    PAYLOAD DATA     │
    ├─────────────────────┤
    │ SESSION STATE       │
    ├─────────────────────┤
    │ PROCESSING CONTEXT  │
    └─────────────────────┘

Both approaches share the same underlying concern:

> Preserve the relationships and provenance surrounding information as it moves through a processing system.

---

# Design Principles

## Preserve Origin

Human-originated information and AI-generated information should remain distinguishable.

## Preserve Context

Payloads should not be separated from the contextual state required to understand them.

## Preserve Processing Identity

Where meaningful, the system should retain information about which module and version processed the information.

## Make Transformation Explicit

Extraction and synthesis should be identifiable processing operations.

## Prefer Immutable Envelopes

Original representations should not be silently mutated during downstream processing.

## Preserve Governance Context

Information required for later governance should remain structurally available.

## Consolidate Without Concealing

Redundant implementations should be consolidated, but known limitations should remain explicitly documented.

---

# Current Status

GRAPH is a consolidated architectural repository.

Its current working material demonstrates two related approaches to structured user/AI payload processing, while also containing the GAPS Kernel as a related governance-layer component consolidated from earlier work.

The repository should therefore be understood as:

> **A developing architecture for preserving structured relationships between human input, AI output, context, processing modules, transformations, and governance information, currently represented through consolidated implementations and related governance-layer components.**

The current code provides a concrete demonstration of these concepts while retaining known implementation limitations for further architectural resolution.

---

# Central Proposition

> **Information moving through a governed AI system should not lose the relationships that explain where it came from, what produced it, what context surrounded it, or how it was transformed.**

GRAPH provides a structural foundation for preserving those relationships.