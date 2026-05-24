"""
Main IntrospectionTools class. Read-only Keynote introspection.

All operations route AppleScript through a shared helper that prepends
the JSON encoding handlers (introspection_json.applescript) to the
target script before execution, so every introspection script can use
my jsonString(), my jsonRecord(), etc. without duplicating code.
"""

import json
from typing import List, Any
from mcp.types import Tool, TextContent
from ...utils import AppleScriptRunner

from .schemas import get_introspection_tool_schemas
from .slide_query_operations import SlideQueryOperations
from .table_operations import TableOperations


class IntrospectionTools:
    """Read-only introspection of Keynote slide contents."""

    def __init__(self):
        self.runner = AppleScriptRunner()
        self.slide_query_ops = SlideQueryOperations(self._run_introspection)
        self.table_ops = TableOperations(self._run_introspection)

    def get_tools(self) -> List[Tool]:
        return get_introspection_tool_schemas()

    def _run_introspection(self, script_file: str, function_name: str, args: list) -> Any:
        """
        Execute an introspection AppleScript function.

        Prepends the JSON helper script to the target script content,
        appends a call to function_name(args), executes via osascript,
        and json.loads() the result.
        """
        helper_path = self.runner.script_dir / "introspection_json.applescript"
        script_path = self.runner.script_dir / script_file

        helper_content = helper_path.read_text(encoding='utf-8')
        script_content = script_path.read_text(encoding='utf-8')

        formatted_args = []
        for arg in args:
            if isinstance(arg, bool):
                formatted_args.append("true" if arg else "false")
            elif isinstance(arg, (int, float)):
                formatted_args.append(str(arg))
            elif arg is None or arg == "":
                formatted_args.append('""')
            else:
                escaped = str(arg).replace('\\', '\\\\').replace('"', '\\"')
                formatted_args.append(f'"{escaped}"')

        call = f"{function_name}({', '.join(formatted_args)})"
        full_script = f"{helper_content}\n\n{script_content}\n\n{call}"

        raw = self.runner.execute_script(full_script)
        return json.loads(raw)

    # Slide queries
    async def list_slide_items(self, slide_number: int, doc_name: str = "") -> List[TextContent]:
        return await self.slide_query_ops.list_slide_items(slide_number, doc_name)

    # Table introspection
    async def get_table_info(
        self,
        slide_number: int,
        table_index: int,
        include_cells: bool = False,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.table_ops.get_table_info(slide_number, table_index, include_cells, doc_name)

    async def get_table_cell(
        self,
        slide_number: int,
        table_index: int,
        cell_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.table_ops.get_table_cell(slide_number, table_index, cell_address, doc_name)
