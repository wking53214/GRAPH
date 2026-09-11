# ===============================================================================
# ARCHITECTURAL SYNTHESIS NOTES
# Module: ast_graph_extractor.py
# Version: v1.0.0
#
# SYSTEM ROLE:
# This module represents the static intelligence extraction subsystem of the
# Sentinel architecture.
#
# It transforms raw Python source code into a deterministic graph-based
# intermediate representation (Graph IR) by extracting structural relationships,
# definitions, imports, and execution dependencies.
#
# This subsystem provides the foundation for code intelligence, architecture
# discovery, dependency mapping, system visualization, and automated knowledge
# extraction.
#
# ===============================================================================
#
# COMPILED KERNEL MAP:
#
# ASTParser_Mini_Analysis_Kernel.py
# ------------------------------------------------
# Purpose:
# Converts source code into a traversable abstract syntax tree representation.
#
# Responsibilities:
# - Parse Python source files.
# - Generate AST structures.
# - Enable deterministic syntax analysis.
# - Provide language-level structural understanding.
#
#
# NodeModel_Mini_Graph_Kernel.py
# ------------------------------------------------
# Purpose:
# Defines graph entities representing extracted code structures.
#
# Responsibilities:
# - Represent modules.
# - Represent functions.
# - Represent classes.
# - Maintain artifact identity and source location.
#
#
# EdgeModel_Mini_Relationship_Kernel.py
# ------------------------------------------------
# Purpose:
# Defines relationships between extracted code entities.
#
# Responsibilities:
# - Represent function calls.
# - Represent dependency links.
# - Store relationship evidence.
# - Preserve source-derived connections.
#
#
# GraphExtractor_Mini_Discovery_Kernel.py
# ------------------------------------------------
# Purpose:
# Performs deterministic AST traversal and relationship discovery.
#
# Responsibilities:
# - Visit syntax tree nodes.
# - Extract definitions.
# - Extract imports.
# - Extract function call relationships.
# - Build graph intermediate representation.
#
#
# ScopeResolver_Mini_Context_Kernel.py
# ------------------------------------------------
# Purpose:
# Maintains hierarchical naming context during extraction.
#
# Responsibilities:
# - Track nested scopes.
# - Generate qualified names.
# - Resolve class/function hierarchy.
# - Maintain extraction context.
#
#
# GraphSerialization_Mini_Utility_Kernel.py
# ------------------------------------------------
# Purpose:
# Converts graph structures into portable representations.
#
# Responsibilities:
# - Serialize nodes.
# - Serialize edges.
# - Export graph metadata.
# - Support downstream processing systems.
#
#
# ===============================================================================
#
# COMPILED SUBSYSTEM ARCHITECTURE:
#
#
#                 AST_GRAPH_EXTRACTOR
#
#                         |
#                         v
#
#                 Python Source Input
#
#                         |
#                         v
#
#                  AST Parser Layer
#
#                         |
#                         v
#
#              Deterministic Visitor Engine
#
#                         |
#             +-----------+-----------+
#             |                       |
#             v                       v
#
#        Node Extraction        Relationship Extraction
#
#             |                       |
#             +-----------+-----------+
#                         |
#                         v
#
#                 Graph Intermediate IR
#
#                         |
#                         v
#
#                 Serialized Graph Output
#
#
# ===============================================================================
#
# PRIMARY DATA FLOW:
#
# Python Source File
#        |
#        v
# ast.parse()
#        |
#        v
# GraphExtractor Visitor
#        |
#        +----------------+
#        |                |
#        v                v
# Node Registry      Edge Registry
#
#        |
#        v
#
# Graph IR Object
#
#        |
#        v
#
# Dictionary / Knowledge Graph Export
#
# ===============================================================================
#
# EXTRACTED KNOWLEDGE TYPES:
#
# MODULES
# - File-level architecture units.
#
# CLASSES
# - Object-oriented structural components.
#
# FUNCTIONS
# - Executable logic units.
#
# IMPORTS
# - External and internal dependencies.
#
# CALL RELATIONSHIPS
# - Runtime invocation relationships.
#
# ===============================================================================
#
# SYSTEM CAPABILITY:
#
# This module provides:
#
# - Automated source-code understanding.
# - Architecture reverse engineering.
# - Dependency graph creation.
# - Software knowledge extraction.
# - Repository intelligence generation.
#
# ===============================================================================
#
# ARCHITECTURAL POSITION:
#
# Layer:
# Code Intelligence / Knowledge Extraction Layer
#
# Depends On:
# - Python AST Runtime
# - Graph Data Model Layer
# - Serialization Utilities
#
# Provides:
# - Software architecture graphs.
# - Dependency intelligence.
# - Machine-readable code understanding.
#
# ===============================================================================
#
# ROLE WITHIN SENTINEL KNOWLEDGE SYSTEM:
#
# This module acts as the "compiler vision layer" of the architecture.
#
# It converts human-written software artifacts into structured machine-readable
# knowledge, enabling downstream systems to reason about:
#
# - What exists.
# - How components connect.
# - Where dependencies originate.
# - How systems evolve over time.
#
# ===============================================================================
#
# RECONSTRUCTION & PROVENANCE NOTES  (added on landing in GRAPH, Phase 1)
#
# Source: reconstructed from `content-pipeline-user-source.py` in the CODE repo -
# a flattened, single-line Gemini paste that does not parse. The GraphExtractor /
# extract_graph / graph_to_dict logic and the Node/Edge/Graph models originate
# there; this file is the runnable form, with the header above and the
# `total_row_count` field added.
#
# The "COMPILED KERNEL MAP" names sub-kernels (ASTParser_Mini_*, NodeModel_Mini_*,
# ...) as a conceptual decomposition. They are NOT separate files - this is a
# single self-contained module.
#
# resolve_attr_chain(): when a call target's attribute chain does not bottom out
# in a plain name (e.g. `make_factory().build()`), this returns the partial
# dotted name (`build`) and visit_Call still records the edge. A top-level
# function of the same name collides with it. Left as supplied.
#
# `DeterministicGraphExtractor`, a two-method stub in the same original source,
# is deliberately not carried over.
# ===============================================================================
from __future__ import annotations
import ast
from typing import Dict, List, Set, Optional

# Node, Edge and Graph are the library's shared graph substrate and live in
# the cns package (the central nervous system: contracts only). This file
# carried its own copy until 2026-09-11; the copy was byte-for-byte the
# canonical one, so nothing about the output changed. The walk below is
# GRAPH's own and stays here.
from cns.graph import Node, Edge, Graph, graph_to_dict  # noqa: F401  (graph_to_dict re-exported)

class GraphExtractor(ast.NodeVisitor):
    def __init__(self, filename: str = ""):
        self.filename = filename
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.current_scope: List[str] = []
        self.defined: Set[str] = set()

    def add_node(self, name: str, kind: str):
        if name not in self.nodes:
            self.nodes[name] = Node(id=name, kind=kind, file=self.filename)

    def add_edge(self, src: str, dst: str, kind: str, evidence: str):
        self.edges.append(Edge(src, dst, kind, evidence))

    def current_qualname(self, name: str) -> str:
        if self.current_scope:
            return ".".join(self.current_scope + [name])
        return name

    def visit_Module(self, node: ast.Module):
        self.add_node(self.filename, "module")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        qname = self.current_qualname(node.name)
        self.add_node(qname, "function")
        self.defined.add(qname)
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        qname = self.current_qualname(node.name)
        self.add_node(qname, "async_function")
        self.defined.add(qname)
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_ClassDef(self, node: ast.ClassDef):
        qname = self.current_qualname(node.name)
        self.add_node(qname, "class")
        self.defined.add(qname)
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_Call(self, node: ast.Call):
        caller = ".".join(self.current_scope) if self.current_scope else self.filename
        callee = self.resolve_call(node.func)
        if callee:
            self.add_edge(src=caller, dst=callee, kind="CALL", evidence=ast.unparse(node))
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.add_node(alias.name, "import")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        for alias in node.names:
            full = f"{module}.{alias.name}" if module else alias.name
            self.add_node(full, "import")
        self.generic_visit(node)

    def resolve_call(self, func: ast.AST) -> Optional[str]:
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            return self.resolve_attr_chain(func)
        return None

    def resolve_attr_chain(self, node: ast.Attribute) -> str:
        parts = []
        cur = node
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
        return ".".join(reversed(parts))

def extract_graph(source: str, filename: str = "") -> Graph:
    tree = ast.parse(source)
    extractor = GraphExtractor(filename=filename)
    extractor.visit(tree)
    total_lines = len(source.splitlines()) if source else 0
    return Graph(nodes=extractor.nodes, edges=extractor.edges, total_row_count=total_lines)


if __name__ == "__main__":
    import json

    _sample = (
        "import os\n"
        "from collections import deque\n"
        "\n"
        "class Widget:\n"
        "    def run(self):\n"
        "        os.getcwd()\n"
        "        helper()\n"
        "\n"
        "def helper():\n"
        "    return deque()\n"
    )
    _g = extract_graph(_sample, "sample.py")
    print(json.dumps(graph_to_dict(_g), indent=2))
