"""
Document-level state reads.
"""

import json
from typing import Any, Callable, List
from mcp.types import TextContent


class DocumentOperations:
    """Document state introspection."""

    def __init__(self, runner_caller: Callable[[str, str, list], Any]):
        self._run = runner_caller

    async def get_document_state(
        self,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_document.applescript",
                "getDocumentState",
                [doc_name],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ get_document_state failed: {e}")]
