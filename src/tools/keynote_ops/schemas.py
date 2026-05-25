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
            name="set_item_opacity",
            description="Set the opacity (0-100) of an existing iWork item on a slide. item_kind must be one of: table, shape, image, line, group, movie, audio_clip, chart, text_item. Returns JSON with the new opacity value.",
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
                    "opacity": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100,
                        "description": "Opacity in percent (0 = fully transparent, 100 = fully opaque)"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "item_kind", "item_index", "opacity"]
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
            description=(
                "Create a new line on a slide between two points (in slide coordinates, points). "
                "Returns JSON with slide_number, kind='line', and the per-kind index of the new line.\n\n"
                "STYLING LIMITATIONS (Keynote AppleScript constraints):\n"
                "- Line color, weight, dash pattern, arrow style, and Keynote's style presets are "
                "NOT exposed via AppleScript. New lines get the theme's default line style. "
                "Endpoint/position/rotation/opacity ARE settable (set_item_position / set_item_rotation / "
                "set_item_opacity), but visual styling has to be done manually in Keynote's Format inspector."
            ),
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
            description=(
                "Create a new rectangle shape on a slide. Position and size are in slide coordinates "
                "(points, top-left origin). Returns JSON with slide_number, kind='shape', and the "
                "per-kind index of the new shape.\n\n"
                "STYLING LIMITATIONS (Keynote AppleScript constraints):\n"
                "- Shape fill color CANNOT be set via AppleScript. The shape's `background fill type` "
                "is read-only and the actual fill color is not exposed at all. New shapes get the "
                "theme's default fill. To change the visual fill, the user has to set it manually in "
                "Keynote's Format inspector. This is a hard Keynote limitation, not a bug in this tool.\n"
                "- Style presets (Keynote's Format > Style swatches for shapes) are NOT exposed via "
                "AppleScript either. New shapes get the theme's default style. Same limitation family.\n"
                "- Opacity CAN be set via set_item_opacity. As a partial workaround for 'I want a "
                "differently-colored container,' you can dim the default fill with opacity (e.g. 8 "
                "for a near-transparent overlay).\n"
                "- To add text to the shape after creation, set its object text via "
                "run_applescript_snippet and then use set_text_font / set_text_size / set_text_color "
                "for styling. Paragraph alignment of that text also cannot be set programmatically "
                "(same AppleScript limitation as add_text_box)."
            ),
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

        # Text styling setters. Each sets one rich-text property (font / size /
        # color) on the entire object_text of a shape or text_item. These are
        # the only three properties Keynote's AppleScript dictionary exposes
        # as writable for rich text in shapes/text items. Paragraph alignment,
        # font weight ("bold"), font style ("italic"), and other paragraph-
        # level styling are NOT exposed by Keynote AppleScript — use a
        # bold/italic-flavored font name (e.g. "HelveticaNeue-Bold") to
        # approximate weight/style.
        Tool(
            name="set_text_font",
            description="Set the font of the entire object text of a shape or text_item. To get bold/italic, use a bold/italic-flavored font name like 'HelveticaNeue-Bold' or 'HelveticaNeue-Italic'. Returns JSON confirmation. Only item_kind 'shape' or 'text_item' is supported; other kinds (image, line, etc.) don't carry rich text.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {"type": "integer", "description": "Slide number (1-indexed)"},
                    "item_kind": {"type": "string", "enum": ["shape", "text_item"], "description": "Kind of the item to style"},
                    "item_index": {"type": "integer", "description": "1-indexed position of the item within its kind on the slide"},
                    "font_name": {"type": "string", "description": "PostScript font name (e.g. 'HelveticaNeue', 'HelveticaNeue-Bold', 'TimesNewRomanPS-ItalicMT')"},
                    "doc_name": {"type": "string", "description": "Document name (optional, defaults to front document)"}
                },
                "required": ["slide_number", "item_kind", "item_index", "font_name"]
            }
        ),
        Tool(
            name="set_text_size",
            description="Set the font size (in points) of the entire object text of a shape or text_item. Returns JSON confirmation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {"type": "integer", "description": "Slide number (1-indexed)"},
                    "item_kind": {"type": "string", "enum": ["shape", "text_item"], "description": "Kind of the item to style"},
                    "item_index": {"type": "integer", "description": "1-indexed position of the item within its kind on the slide"},
                    "size": {"type": "number", "description": "Point size (e.g. 12, 24, 48)"},
                    "doc_name": {"type": "string", "description": "Document name (optional, defaults to front document)"}
                },
                "required": ["slide_number", "item_kind", "item_index", "size"]
            }
        ),
        Tool(
            name="set_text_color",
            description="Set the text color of the entire object text of a shape or text_item. Color is a 3-element list of 16-bit RGB values (0-65535 each), matching the format returned by get_shape_text. Note: Keynote may slightly quantize the input color. Returns JSON confirmation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {"type": "integer", "description": "Slide number (1-indexed)"},
                    "item_kind": {"type": "string", "enum": ["shape", "text_item"], "description": "Kind of the item to style"},
                    "item_index": {"type": "integer", "description": "1-indexed position of the item within its kind on the slide"},
                    "color": {"type": "array", "items": {"type": "integer", "minimum": 0, "maximum": 65535}, "minItems": 3, "maxItems": 3, "description": "RGB color as [r, g, b], each 0-65535 (16-bit)"},
                    "doc_name": {"type": "string", "description": "Document name (optional, defaults to front document)"}
                },
                "required": ["slide_number", "item_kind", "item_index", "color"]
            }
        ),

        # -----------------------------------------------------------------------
        # Batch D — slide write, playback, and escape hatch
        # -----------------------------------------------------------------------

        Tool(
            name="set_presenter_notes",
            description="Set the presenter notes for a slide as plain text. Replaces any existing notes. Returns JSON with slide_number and characters_set.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number (1-indexed)"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Plain text content for the presenter notes"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    }
                },
                "required": ["slide_number", "notes"]
            }
        ),
        Tool(
            name="clear_slide",
            description="Delete all user-created content from a slide, preserving theme placeholders. Walks every iWork-item kind (tables, shapes, images, lines, groups, movies, audio clips, charts, text items) in reverse and deletes them. Text items at position [0, 0] with empty text are heuristically preserved as theme placeholders. Useful as a 'regenerate this slide from scratch' starting point. Returns JSON with slide_number and items_deleted count.",
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
            name="start_playback",
            description="Start Keynote slide show playback. Optionally start from a specific slide (1-indexed). Returns JSON with playing=true and from_slide. NOTE: This enters full-screen presentation mode — call stop_playback to exit.",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to front document)"
                    },
                    "from_slide": {
                        "type": "integer",
                        "description": "Slide number to start from (1-indexed). If omitted or 0, starts from current slide."
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="stop_playback",
            description="Stop Keynote slide show playback and return to editing mode. Returns JSON with stopped=true.",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, not used by the stop verb)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="show_next",
            description="Advance to the next slide or build during an active Keynote presentation. Only valid while playback is running — returns a JSON error if not in presentation mode. Returns JSON with action='show_next'.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="show_previous",
            description="Go back to the previous slide or build during an active Keynote presentation. Only valid while playback is running — returns a JSON error if not in presentation mode. Returns JSON with action='show_previous'.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="goto_slide",
            description="Navigate to a specific slide by number. Works in both editing and presentation mode by setting the current slide property. Returns JSON with current_slide.",
            inputSchema={
                "type": "object",
                "properties": {
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number to navigate to (1-indexed)"
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
            name="run_applescript_snippet",
            description=(
                "Power-user escape hatch: run an arbitrary AppleScript snippet against Keynote. "
                "Prefer structured tools first — this bypasses all validation and can leave the "
                "document in an unexpected state. Snippets are wrapped in a tell-application block "
                "by default. Returns JSON with result (string) or error field."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "snippet": {
                        "type": "string",
                        "description": "AppleScript code to execute"
                    },
                    "wrap_in_tell": {
                        "type": "boolean",
                        "description": "If true (default), wrap snippet in 'tell application Keynote ... end tell'. Set false to run snippet verbatim."
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "If provided (and wrap_in_tell is true), also wraps in 'tell document <doc_name>'. Ignored when wrap_in_tell is false."
                    }
                },
                "required": ["snippet"]
            }
        ),
    ]
