"""
Slide-level introspection queries (list items, slide properties, etc.)
"""

import json
from typing import Any, Callable, List
from mcp.types import TextContent


class SlideQueryOperations:
    """Slide-level introspection: list items on a slide."""

    def __init__(self, runner_caller: Callable[[str, str, list], Any]):
        # runner_caller is IntrospectionTools._run_introspection
        self._run = runner_caller

    async def list_slide_items(self, slide_number: int, doc_name: str = "") -> List[TextContent]:
        try:
            data = self._run(
                "introspection_slide_items.applescript",
                "listSlideItems",
                [doc_name, slide_number],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ list_slide_items failed: {e}")]
