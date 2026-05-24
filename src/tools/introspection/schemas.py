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
        ),
        Tool(
            name="get_table_cell",
            description="Get a single cell's full payload: value (typed envelope), formatted_value, formula, plus styling (font, alignment, colors, wrap). Cells are addressed by Keynote's A1-style cell address. Returns JSON.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "table_index": {
                        "type": "integer",
                        "description": "1-indexed position of the table on the slide"
                    },
                    "cell_address": {
                        "type": "string",
                        "description": "Cell address in A1 notation (e.g. 'B2')"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "table_index", "cell_address"]
            }
        ),
        Tool(
            name="get_item_properties",
            description="Get geometry and visual properties (position, size, rotation, locked, opacity, reflection) of a specific iWork item on a slide. item_kind must be one of: table, shape, image, line, group, movie, audio_clip, chart, text_item. Returns JSON.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "item_kind": {
                        "type": "string",
                        "description": "Kind of item: table | shape | image | line | group | movie | audio_clip | chart | text_item"
                    },
                    "item_index": {
                        "type": "integer",
                        "description": "1-indexed position within that kind (as returned by list_slide_items)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "item_kind", "item_index"]
            }
        ),
        Tool(
            name="get_shape_text",
            description="Get the text content of a shape on a slide, including per-paragraph font, size, and color. Returns JSON with text (full string) and paragraphs array.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "shape_index": {
                        "type": "integer",
                        "description": "1-indexed position of the shape on the slide (as returned by list_slide_items)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "shape_index"]
            }
        ),
        Tool(
            name="get_text_item_text",
            description="Get the text content of a text item (theme layout text placeholder) on a slide, including per-paragraph font, size, and color. Returns JSON with text (full string) and paragraphs array.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "text_item_index": {
                        "type": "integer",
                        "description": "1-indexed position of the text item on the slide (as returned by list_slide_items)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "text_item_index"]
            }
        ),
        Tool(
            name="get_presenter_notes",
            description="Get the presenter notes for a slide as plain text and per-paragraph detail (font, size, color). Returns JSON with slide_number, text, and paragraphs array.",
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
            name="get_slide_properties",
            description="Get metadata for a slide: title_showing, body_showing, skipped, base_layout name, and transition properties (automatic, delay, duration, effect). Returns JSON.",
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
            name="get_document_state",
            description="Get top-level document state: name, current slide, slide count, slide_numbers_showing, canvas dimensions, password_protected, and selection count. Returns JSON.",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_cell_range",
            description="Get a rectangular range of cells from a table as a 2D array. Each cell has address, value (typed envelope), formatted_value, and formula. Returns JSON.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "table_index": {
                        "type": "integer",
                        "description": "1-indexed position of the table on the slide"
                    },
                    "range_address": {
                        "type": "string",
                        "description": "Range address in A1:C3 notation (e.g. 'A1:C3')"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "table_index", "range_address"]
            }
        )
    ]
