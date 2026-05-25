"""
Per-item property reads and text extraction for shapes and text items.
Also includes item write operations (set position/size/rotation, delete)
and item makers (make_line, make_shape, make_movie, make_audio_clip).
"""

import json
import os
from typing import Any, Callable, List
from mcp.types import TextContent


class ItemOperations:
    """Per-item introspection: properties, shape text, text item text."""

    def __init__(self, runner_caller: Callable[[str, str, list], Any]):
        self._run = runner_caller

    async def get_item_properties(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_items.applescript",
                "getItemProperties",
                [doc_name, slide_number, item_kind, item_index],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ get_item_properties failed: {e}")]

    async def get_shape_text(
        self,
        slide_number: int,
        shape_index: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_items.applescript",
                "getShapeText",
                [doc_name, slide_number, shape_index],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ get_shape_text failed: {e}")]

    async def get_text_item_text(
        self,
        slide_number: int,
        text_item_index: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_items.applescript",
                "getTextItemText",
                [doc_name, slide_number, text_item_index],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ get_text_item_text failed: {e}")]

    # -------------------------------------------------------------------------
    # Item write operations (Batch C)
    # -------------------------------------------------------------------------

    async def set_item_position(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        position: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "setItemPosition",
                [doc_name, slide_number, item_kind, item_index, position[0], position[1]],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ set_item_position failed: {e}")]

    async def set_item_size(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        size: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "setItemSize",
                [doc_name, slide_number, item_kind, item_index, size[0], size[1]],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ set_item_size failed: {e}")]

    async def set_item_rotation(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        rotation: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "setItemRotation",
                [doc_name, slide_number, item_kind, item_index, rotation],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ set_item_rotation failed: {e}")]

    async def set_item_opacity(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        opacity: float,
        doc_name: str = "",
    ) -> List[TextContent]:
        if not (0 <= opacity <= 100):
            error = {"error": f"opacity must be in [0, 100]; got: {opacity}"}
            return [TextContent(type="text", text=json.dumps(error, indent=2))]
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "setItemOpacity",
                [doc_name, slide_number, item_kind, item_index, opacity],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ set_item_opacity failed: {e}")]

    async def delete_item(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "deleteItem",
                [doc_name, slide_number, item_kind, item_index],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ delete_item failed: {e}")]

    # -------------------------------------------------------------------------
    # Item makers (Batch C)
    # -------------------------------------------------------------------------

    async def make_line(
        self,
        slide_number: int,
        start_point: list,
        end_point: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "makeLine",
                [doc_name, slide_number, start_point[0], start_point[1], end_point[0], end_point[1]],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ make_line failed: {e}")]

    async def make_shape(
        self,
        slide_number: int,
        position: list,
        size: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "makeShape",
                [doc_name, slide_number, position[0], position[1], size[0], size[1]],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ make_shape failed: {e}")]

    async def make_movie(
        self,
        slide_number: int,
        file_path: str,
        position: list = None,
        size: list = None,
        doc_name: str = "",
    ) -> List[TextContent]:
        # Validate file exists before calling AppleScript
        if not os.path.exists(file_path):
            error = {"error": f"file not found: {file_path}"}
            return [TextContent(type="text", text=json.dumps(error, indent=2))]
        pos = position if position is not None else [100, 100]
        sz = size if size is not None else [400, 300]
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "makeMovie",
                [doc_name, slide_number, file_path, pos[0], pos[1], sz[0], sz[1]],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ make_movie failed: {e}")]

    async def make_audio_clip(
        self,
        slide_number: int,
        file_path: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        # Validate file exists before calling AppleScript
        if not os.path.exists(file_path):
            error = {"error": f"file not found: {file_path}"}
            return [TextContent(type="text", text=json.dumps(error, indent=2))]
        try:
            data = self._run(
                "introspection_item_writes.applescript",
                "makeAudioClip",
                [doc_name, slide_number, file_path],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ make_audio_clip failed: {e}")]

    async def set_text_font(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        font_name: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_items.applescript",
                "setTextFont",
                [doc_name, slide_number, item_kind, item_index, font_name],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ set_text_font failed: {e}")]

    async def set_text_size(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        size: float,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_items.applescript",
                "setTextSize",
                [doc_name, slide_number, item_kind, item_index, size],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ set_text_size failed: {e}")]

    async def set_text_color(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        color: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        if not (isinstance(color, list) and len(color) == 3):
            error = {"error": f"color must be a 3-element list [r, g, b] of 16-bit values (0-65535); got: {color!r}"}
            return [TextContent(type="text", text=json.dumps(error, indent=2))]
        try:
            data = self._run(
                "introspection_items.applescript",
                "setTextColor",
                [doc_name, slide_number, item_kind, item_index, color[0], color[1], color[2]],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ set_text_color failed: {e}")]
