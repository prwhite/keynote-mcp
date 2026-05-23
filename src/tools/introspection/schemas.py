"""
Tool definitions for introspection operations
"""

from mcp.types import Tool


def get_introspection_tool_schemas():
    """Get all introspection tool schemas"""
    return [
        Tool(
            name="list_slide_items",
            description="List every iWork item on a slide (tables, shapes, images, lines, groups, movies, audio clips, charts, text items) with kind, per-kind index, name (if any), position, and size. Returns JSON.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="get_table_info",
            description="Get a table's metadata (name, row/column counts, header/footer counts). With include_cells=true, also returns the cell grid (value/formatted_value/formula per cell — no per-cell styling). Returns JSON.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "table_index": {
                        "type": "integer",
                        "description": "1-indexed position of the table on the slide (as returned by list_slide_items)"
                    },
                    "include_cells": {
                        "type": "boolean",
                        "description": "If true, include a 2D grid of cell contents. Default false."
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "table_index"]
            }
        )
    ]
