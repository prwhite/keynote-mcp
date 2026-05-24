"""
Per-item property reads and text extraction for shapes and text items.
"""

import json
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
