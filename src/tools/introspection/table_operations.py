"""
Table-level introspection: table info and cell-level reads.
"""

import json
from typing import Any, Callable, List
from mcp.types import TextContent


class TableOperations:
    """Table introspection."""

    def __init__(self, runner_caller: Callable[[str, str, list], Any]):
        self._run = runner_caller

    async def get_table_info(
        self,
        slide_number: int,
        table_index: int,
        include_cells: bool = False,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_tables.applescript",
                "getTableInfo",
                [doc_name, slide_number, table_index, include_cells],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ get_table_info failed: {e}")]

    async def get_table_cell(
        self,
        slide_number: int,
        table_index: int,
        cell_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_tables.applescript",
                "getTableCell",
                [doc_name, slide_number, table_index, cell_address],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ get_table_cell failed: {e}")]
