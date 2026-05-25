"""
Table-level introspection: table info and cell-level reads, plus table writes.
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

    async def get_cell_range(
        self,
        slide_number: int,
        table_index: int,
        range_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_tables.applescript",
                "getCellRange",
                [doc_name, slide_number, table_index, range_address],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ get_cell_range failed: {e}")]

    # -------------------------------------------------------------------------
    # Write operations (Batch B)
    # -------------------------------------------------------------------------

    async def set_cell_value(
        self,
        slide_number: int,
        table_index: int,
        cell_address: str,
        value: Any,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            value_text = str(value)
            data = self._run(
                "introspection_table_writes.applescript",
                "setCellValue",
                [doc_name, slide_number, table_index, cell_address, value_text],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ set_cell_value failed: {e}")]

    async def make_table(
        self,
        slide_number: int,
        rows: int,
        columns: int,
        position: list = None,
        width: int = 400,
        height: int = 200,
        name: str = "",
        header_row_count: int = 1,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            pos = position if position is not None else [100, 100]
            data = self._run(
                "introspection_table_writes.applescript",
                "makeTable",
                [doc_name, slide_number, rows, columns, pos[0], pos[1], width, height, name, header_row_count],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ make_table failed: {e}")]

    async def merge_cells(
        self,
        slide_number: int,
        table_index: int,
        range_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_table_writes.applescript",
                "mergeCells",
                [doc_name, slide_number, table_index, range_address],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ merge_cells failed: {e}")]

    async def unmerge_cells(
        self,
        slide_number: int,
        table_index: int,
        range_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_table_writes.applescript",
                "unmergeCells",
                [doc_name, slide_number, table_index, range_address],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ unmerge_cells failed: {e}")]

    async def clear_cells(
        self,
        slide_number: int,
        table_index: int,
        range_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_table_writes.applescript",
                "clearCells",
                [doc_name, slide_number, table_index, range_address],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ clear_cells failed: {e}")]

    async def sort_table(
        self,
        slide_number: int,
        table_index: int,
        by_column: int,
        direction: str = "ascending",
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_table_writes.applescript",
                "sortTable",
                [doc_name, slide_number, table_index, by_column, direction],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ sort_table failed: {e}")]
