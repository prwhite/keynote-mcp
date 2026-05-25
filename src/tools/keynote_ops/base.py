"""
Main KeynoteOps class.

All operations route AppleScript through a shared helper that prepends
the JSON encoding handlers (`introspection_json.applescript`) to the
target script before execution, so every script can use my jsonString(),
my jsonRecord(), etc. without duplicating code.

(The `introspection_*` prefix on the AppleScript helper files is a
legacy from Phase 1 — see the subpackage `__init__.py` for context. The
prefix is an internal implementation detail; the Python class name is
the public surface that matters.)
"""

import json
from typing import List, Any
from mcp.types import Tool, TextContent
from ...utils import AppleScriptRunner

from .schemas import get_introspection_tool_schemas
from .slide_query_operations import SlideQueryOperations
from .table_operations import TableOperations
from .item_operations import ItemOperations
from .document_operations import DocumentOperations
from .playback_operations import PlaybackOperations
from .escape_operations import EscapeOperations


class KeynoteOps:
    """Directly-AppleScript-backed Keynote tools: reads, writes, playback, escape hatch."""

    def __init__(self):
        self.runner = AppleScriptRunner()
        self.slide_query_ops = SlideQueryOperations(self._run_introspection)
        self.table_ops = TableOperations(self._run_introspection)
        self.item_ops = ItemOperations(self._run_introspection)
        self.document_ops = DocumentOperations(self._run_introspection)
        self.playback_ops = PlaybackOperations(self._run_introspection)
        self.escape_ops = EscapeOperations(self.runner)

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

    async def get_cell_range(
        self,
        slide_number: int,
        table_index: int,
        range_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.table_ops.get_cell_range(slide_number, table_index, range_address, doc_name)

    # Item operations
    async def get_item_properties(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.get_item_properties(slide_number, item_kind, item_index, doc_name)

    async def get_shape_text(
        self,
        slide_number: int,
        shape_index: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.get_shape_text(slide_number, shape_index, doc_name)

    async def get_text_item_text(
        self,
        slide_number: int,
        text_item_index: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.get_text_item_text(slide_number, text_item_index, doc_name)

    # Slide properties
    async def get_slide_properties(
        self,
        slide_number: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.slide_query_ops.get_slide_properties(slide_number, doc_name)

    async def get_presenter_notes(
        self,
        slide_number: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.slide_query_ops.get_presenter_notes(slide_number, doc_name)

    # Document state
    async def get_document_state(
        self,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.document_ops.get_document_state(doc_name)

    # -------------------------------------------------------------------------
    # Table write operations (Batch B)
    # -------------------------------------------------------------------------

    async def set_cell_value(
        self,
        slide_number: int,
        table_index: int,
        cell_address: str,
        value: Any,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.table_ops.set_cell_value(slide_number, table_index, cell_address, value, doc_name)

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
        return await self.table_ops.make_table(slide_number, rows, columns, position, width, height, name, header_row_count, doc_name)

    async def merge_cells(
        self,
        slide_number: int,
        table_index: int,
        range_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.table_ops.merge_cells(slide_number, table_index, range_address, doc_name)

    async def unmerge_cells(
        self,
        slide_number: int,
        table_index: int,
        range_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.table_ops.unmerge_cells(slide_number, table_index, range_address, doc_name)

    async def clear_cells(
        self,
        slide_number: int,
        table_index: int,
        range_address: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.table_ops.clear_cells(slide_number, table_index, range_address, doc_name)

    async def sort_table(
        self,
        slide_number: int,
        table_index: int,
        by_column: int,
        direction: str = "ascending",
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.table_ops.sort_table(slide_number, table_index, by_column, direction, doc_name)

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
        return await self.item_ops.set_item_position(slide_number, item_kind, item_index, position, doc_name)

    async def set_item_size(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        size: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.set_item_size(slide_number, item_kind, item_index, size, doc_name)

    async def set_item_rotation(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        rotation: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.set_item_rotation(slide_number, item_kind, item_index, rotation, doc_name)

    async def set_item_opacity(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        opacity: float,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.set_item_opacity(slide_number, item_kind, item_index, opacity, doc_name)

    async def delete_item(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.delete_item(slide_number, item_kind, item_index, doc_name)

    # -------------------------------------------------------------------------
    # Item maker operations (Batch C)
    # -------------------------------------------------------------------------

    async def make_line(
        self,
        slide_number: int,
        start_point: list,
        end_point: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.make_line(slide_number, start_point, end_point, doc_name)

    async def make_shape(
        self,
        slide_number: int,
        position: list,
        size: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.make_shape(slide_number, position, size, doc_name)

    async def make_movie(
        self,
        slide_number: int,
        file_path: str,
        position: list = None,
        size: list = None,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.make_movie(slide_number, file_path, position, size, doc_name)

    async def make_audio_clip(
        self,
        slide_number: int,
        file_path: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.make_audio_clip(slide_number, file_path, doc_name)

    # Text styling (set font/size/color on a shape or text_item's object text)
    async def set_text_font(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        font_name: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.set_text_font(slide_number, item_kind, item_index, font_name, doc_name)

    async def set_text_size(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        size: float,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.set_text_size(slide_number, item_kind, item_index, size, doc_name)

    async def set_text_color(
        self,
        slide_number: int,
        item_kind: str,
        item_index: int,
        color: list,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.item_ops.set_text_color(slide_number, item_kind, item_index, color, doc_name)

    # -------------------------------------------------------------------------
    # Slide write operations (Batch D)
    # -------------------------------------------------------------------------

    async def set_presenter_notes(
        self,
        slide_number: int,
        notes: str,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.slide_query_ops.set_presenter_notes(slide_number, notes, doc_name)

    async def clear_slide(
        self,
        slide_number: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.slide_query_ops.clear_slide(slide_number, doc_name)

    # -------------------------------------------------------------------------
    # Playback operations (Batch D)
    # -------------------------------------------------------------------------

    async def start_playback(
        self,
        doc_name: str = "",
        from_slide: int = 0,
    ) -> List[TextContent]:
        return await self.playback_ops.start_playback(doc_name, from_slide)

    async def stop_playback(self) -> List[TextContent]:
        return await self.playback_ops.stop_playback()

    async def show_next(self) -> List[TextContent]:
        return await self.playback_ops.show_next()

    async def show_previous(self) -> List[TextContent]:
        return await self.playback_ops.show_previous()

    async def goto_slide(
        self,
        slide_number: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.playback_ops.goto_slide(slide_number, doc_name)

    # -------------------------------------------------------------------------
    # Escape hatch (Batch D)
    # -------------------------------------------------------------------------

    async def run_applescript_snippet(
        self,
        snippet: str,
        wrap_in_tell: bool = True,
        doc_name: str = "",
    ) -> List[TextContent]:
        return await self.escape_ops.run_applescript_snippet(snippet, wrap_in_tell, doc_name)
