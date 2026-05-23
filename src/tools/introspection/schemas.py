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
        )
    ]
