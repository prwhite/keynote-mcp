"""
Introspection tools - Modular structure

Read-only tools for querying Keynote slide contents:
- slide_query_operations: list_slide_items
- table_operations: get_table_info, get_table_cell

Phase 2 will expand this subpackage to include narrowly-scoped writes
(set_cell_value, make_table, item geometry, etc.), playback verbs, and an
AppleScript escape hatch. The name "introspection" predates that scope
expansion but stays for module continuity.
"""

from .base import IntrospectionTools

__all__ = ['IntrospectionTools']
