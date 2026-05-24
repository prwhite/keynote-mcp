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
        ),

        # -----------------------------------------------------------------------
        # Batch B — table write tools
        # -----------------------------------------------------------------------

        Tool(
            name="set_cell_value",
            description="Set the value of a single cell in a table. Pass a string, number, boolean, or formula string (e.g. '=SUM(B2:B3)'). Keynote will parse numeric strings as numbers where appropriate. Returns JSON confirmation.",
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
                    "value": {
                        "description": "Value to set: string, number, boolean, or formula string starting with '='"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "table_index", "cell_address", "value"]
            }
        ),
        Tool(
            name="make_table",
            description="Create a new table on a slide. Position is in slide coordinates (top-left origin, points). The new table is appended after any existing tables. Returns JSON with slide_number, table_index (per-kind, 1-indexed), and name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "rows": {
                        "type": "integer",
                        "description": "Number of rows (including header rows)"
                    },
                    "columns": {
                        "type": "integer",
                        "description": "Number of columns"
                    },
                    "position": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[x, y] position in slide coordinates (default [100, 100])"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Width in points (default 400)"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Height in points (default 200)"
                    },
                    "name": {
                        "type": "string",
                        "description": "Optional name for the table"
                    },
                    "header_row_count": {
                        "type": "integer",
                        "description": "Number of header rows (default 1)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "rows", "columns"]
            }
        ),
        Tool(
            name="merge_cells",
            description="Merge a rectangular range of cells in a table. Returns JSON confirmation with the merged range address.",
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
                        "description": "Range to merge in A1:B2 notation"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "table_index", "range_address"]
            }
        ),
        Tool(
            name="unmerge_cells",
            description="Unmerge a previously merged range of cells in a table. Returns JSON confirmation with the unmerged range address.",
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
                        "description": "Range to unmerge in A1:B2 notation"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "table_index", "range_address"]
            }
        ),
        Tool(
            name="clear_cells",
            description="Clear the contents of a range of cells in a table (values and formulas removed, formatting preserved). Returns JSON confirmation.",
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
                        "description": "Range to clear in A1:B2 notation (single cell: 'A2')"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "table_index", "range_address"]
            }
        ),
        Tool(
            name="sort_table",
            description="Sort a table by a specific column. Returns JSON confirmation with the column and direction used.",
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
                    "by_column": {
                        "type": "integer",
                        "description": "1-indexed column number to sort by"
                    },
                    "direction": {
                        "type": "string",
                        "enum": ["ascending", "descending"],
                        "description": "Sort direction: 'ascending' or 'descending'"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "table_index", "by_column", "direction"]
            }
        ),

        # -----------------------------------------------------------------------
        # Batch C — item write tools
        # -----------------------------------------------------------------------

        Tool(
            name="set_item_position",
            description="Set the position (top-left origin in slide coordinates, points) of an existing iWork item on a slide. item_kind must be one of: table, shape, image, line, group, movie, audio_clip, chart, text_item. Returns JSON with the new position.",
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
                    "position": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[x, y] position in slide coordinates (points, top-left origin)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "item_kind", "item_index", "position"]
            }
        ),
        Tool(
            name="set_item_size",
            description="Set the size (width, height in points) of an existing iWork item on a slide. item_kind must be one of: table, shape, image, line, group, movie, audio_clip, chart, text_item. Returns JSON with the new size.",
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
                    "size": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[width, height] in points"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "item_kind", "item_index", "size"]
            }
        ),
        Tool(
            name="set_item_rotation",
            description="Set the rotation (in degrees, 0-359) of an existing iWork item on a slide. item_kind must be one of: table, shape, image, line, group, movie, audio_clip, chart, text_item. Returns JSON with the new rotation. Note: some item kinds (e.g. group) may not support rotation — a JSON error is returned in that case.",
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
                    "rotation": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 359,
                        "description": "Rotation in degrees (0-359)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "item_kind", "item_index", "rotation"]
            }
        ),
        Tool(
            name="delete_item",
            description="Delete an existing iWork item from a slide by kind and per-kind index. item_kind must be one of: table, shape, image, line, group, movie, audio_clip, chart, text_item. WARNING: deleting an item shifts the per-kind indices of all remaining items of the same kind — re-query list_slide_items after deletion. Returns JSON confirming the deleted kind and index.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "item_kind": {
                        "type": "string",
                        "description": "Kind of item to delete: table | shape | image | line | group | movie | audio_clip | chart | text_item"
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

        # -----------------------------------------------------------------------
        # Batch C — item maker tools
        # -----------------------------------------------------------------------

        Tool(
            name="make_line",
            description="Create a new line on a slide between two points (in slide coordinates, points). Returns JSON with slide_number, kind='line', and the per-kind index of the new line.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "start_point": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[x, y] start point of the line in slide coordinates (points)"
                    },
                    "end_point": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[x, y] end point of the line in slide coordinates (points)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "start_point", "end_point"]
            }
        ),
        Tool(
            name="make_shape",
            description="Create a new rectangle shape on a slide. Position and size are in slide coordinates (points, top-left origin). Returns JSON with slide_number, kind='shape', and the per-kind index of the new shape.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "position": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[x, y] position of the shape's top-left corner in slide coordinates (points)"
                    },
                    "size": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[width, height] of the shape in points"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "position", "size"]
            }
        ),
        Tool(
            name="make_movie",
            description="Embed a movie file on a slide. file_path must be an absolute POSIX path to an existing movie file. Returns JSON with slide_number, kind='movie', and the per-kind index of the new movie. Returns a JSON error if the file does not exist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Absolute POSIX path to the movie file (must exist)"
                    },
                    "position": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[x, y] position in slide coordinates (default [100, 100])"
                    },
                    "size": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "[width, height] in points (default [400, 300])"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "file_path"]
            }
        ),
        Tool(
            name="make_audio_clip",
            description="Embed an audio clip file on a slide. file_path must be an absolute POSIX path to an existing audio file. Returns JSON with slide_number, kind='audio_clip', and the per-kind index of the new audio clip. Returns a JSON error if the file does not exist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Absolute POSIX path to the audio file (must exist)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "file_path"]
            }
        ),
    ]
