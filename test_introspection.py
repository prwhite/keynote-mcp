#!/usr/bin/env python3
"""
Integration tests for introspection tools.

Requires Keynote running with the test fixture document open. The fixture
creation script lives at:

    payton.nogit/fixtures/create_test_fixture.applescript

That path is gitignored (everything under payton.nogit/ is dev-local), so
a fresh clone won't see it — you'll need to recreate the fixture before
running these tests. Run:

    osascript payton.nogit/fixtures/create_test_fixture.applescript

The script creates an `introspection_fixture.key` document with one slide
containing a 4×3 table named "Q1" with mixed types and a SUM formula in B4.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.tools.introspection import IntrospectionTools

FIXTURE_DOC = "introspection_fixture.key"

# Module-level state for write tests — set by test_make_table, read by subsequent tests.
WRITE_TEST_TABLE_INDEX = None


def parse_tool_result(result):
    """Tool methods return List[TextContent]; the first item's .text is JSON."""
    assert len(result) == 1, f"expected single TextContent, got {len(result)}"
    return json.loads(result[0].text)


async def test_list_slide_items():
    tools = IntrospectionTools()
    result = await tools.list_slide_items(slide_number=2, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)

    assert data["slide_number"] == 2
    kinds = [i["kind"] for i in data["items"]]
    assert "table" in kinds, f"missing table in {kinds}"
    assert "shape" in kinds, f"missing shape in {kinds}"

    table = next(i for i in data["items"] if i["kind"] == "table")
    assert table["name"] == "Q1"
    assert table["index"] == 1
    assert isinstance(table["position"], list) and len(table["position"]) == 2
    assert isinstance(table["size"], list) and len(table["size"]) == 2

    print("✅ list_slide_items")


async def test_get_table_info_default():
    tools = IntrospectionTools()
    result = await tools.get_table_info(slide_number=2, table_index=1, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["row_count"] == 4
    assert data["column_count"] == 3
    assert data["header_row_count"] == 1
    assert data["name"] == "Q1"
    assert "cells" not in data, "cells should be absent by default"
    print("✅ get_table_info (default)")


async def test_get_table_info_with_cells():
    tools = IntrospectionTools()
    result = await tools.get_table_info(
        slide_number=2, table_index=1, include_cells=True, doc_name=FIXTURE_DOC
    )
    data = parse_tool_result(result)
    assert "cells" in data
    assert len(data["cells"]) == 4
    assert len(data["cells"][0]) == 3
    a1 = data["cells"][0][0]
    assert a1["address"] == "A1"
    assert a1["value"] == {"type": "text", "value": "Region"}
    b4 = data["cells"][3][1]
    assert b4["formula"] is not None and "SUM" in b4["formula"]
    assert b4["value"]["type"] == "number"
    print("✅ get_table_info (include_cells)")


async def test_get_table_cell():
    tools = IntrospectionTools()
    result = await tools.get_table_cell(
        slide_number=2, table_index=1, cell_address="B4", doc_name=FIXTURE_DOC
    )
    data = parse_tool_result(result)
    assert data["address"] == "B4"
    assert data["row"] == 4
    assert data["column"] == 2
    assert data["value"]["type"] == "number"
    assert data["formula"] is not None and "SUM" in data["formula"]
    assert "font_name" in data
    assert isinstance(data["text_color"], list) and len(data["text_color"]) == 3
    print("✅ get_table_cell")


async def test_get_item_properties():
    tools = IntrospectionTools()
    result = await tools.get_item_properties(
        slide_number=2, item_kind="shape", item_index=1, doc_name=FIXTURE_DOC
    )
    data = parse_tool_result(result)
    assert data["kind"] == "shape"
    assert data["index"] == 1
    assert isinstance(data["position"], list) and len(data["position"]) == 2
    assert isinstance(data["locked"], bool)
    assert isinstance(data["opacity"], (int, float))
    print("✅ get_item_properties")


async def test_get_shape_text():
    tools = IntrospectionTools()
    result = await tools.get_shape_text(
        slide_number=2, shape_index=1, doc_name=FIXTURE_DOC
    )
    data = parse_tool_result(result)
    assert data["kind"] == "shape"
    assert data["index"] == 1
    assert isinstance(data["text"], str)
    assert isinstance(data["paragraphs"], list)
    print("✅ get_shape_text")


async def test_get_text_item_text():
    tools = IntrospectionTools()
    result = await tools.get_text_item_text(
        slide_number=2, text_item_index=1, doc_name=FIXTURE_DOC
    )
    data = parse_tool_result(result)
    assert data["kind"] == "text_item"
    assert data["index"] == 1
    assert isinstance(data["text"], str)
    assert isinstance(data["paragraphs"], list)
    print("✅ get_text_item_text")


async def test_get_presenter_notes():
    tools = IntrospectionTools()
    result = await tools.get_presenter_notes(slide_number=1, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["slide_number"] == 1
    assert isinstance(data["text"], str)
    assert isinstance(data["paragraphs"], list)
    print("✅ get_presenter_notes")


async def test_get_slide_properties():
    tools = IntrospectionTools()
    result = await tools.get_slide_properties(slide_number=2, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["slide_number"] == 2
    assert isinstance(data["title_showing"], bool)
    assert isinstance(data["body_showing"], bool)
    assert isinstance(data["skipped"], bool)
    assert isinstance(data["transition"], dict)
    print("✅ get_slide_properties")


async def test_get_document_state():
    tools = IntrospectionTools()
    result = await tools.get_document_state(doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["slide_count"] >= 1
    assert isinstance(data["width"], (int, float))
    assert isinstance(data["height"], (int, float))
    assert isinstance(data["current_slide"], int)
    print("✅ get_document_state")


async def test_get_cell_range():
    tools = IntrospectionTools()
    result = await tools.get_cell_range(
        slide_number=2, table_index=1, range_address="A1:C2", doc_name=FIXTURE_DOC
    )
    data = parse_tool_result(result)
    # Should be 2D list: 2 rows x 3 cols
    assert isinstance(data, list), f"expected list, got {type(data)}"
    assert len(data) == 2, f"expected 2 rows, got {len(data)}"
    assert len(data[0]) == 3, f"expected 3 cols in row 0, got {len(data[0])}"
    first_cell = data[0][0]
    assert first_cell["address"].startswith("A"), f"first cell address should start with A, got {first_cell['address']}"
    print("✅ get_cell_range")


async def _ensure_write_test_table(tools: "IntrospectionTools") -> int:
    """Return WRITE_TEST_TABLE_INDEX, creating the WriteTest table if needed."""
    global WRITE_TEST_TABLE_INDEX
    if WRITE_TEST_TABLE_INDEX is not None:
        return WRITE_TEST_TABLE_INDEX
    # Clean up any leftover tables then create fresh
    await _cleanup_write_test_tables()
    result = await tools.make_table(
        slide_number=2,
        rows=3,
        columns=3,
        position=[100, 350],
        width=400,
        height=200,
        name="WriteTest",
        header_row_count=1,
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    WRITE_TEST_TABLE_INDEX = data["table_index"]
    return WRITE_TEST_TABLE_INDEX


async def _cleanup_write_test_tables():
    """Remove any leftover write-test tables (all except Q1 at index 1)."""
    import subprocess, json as _json
    # Use osascript to delete all tables except the first one (Q1)
    script = """
tell application "Keynote"
    set targetDoc to document "introspection_fixture.key"
    set targetSlide to slide 2 of targetDoc
    repeat while (count of tables of targetSlide) > 1
        delete table (count of tables of targetSlide) of targetSlide
    end repeat
    return count of tables of targetSlide
end tell
"""
    subprocess.run(["osascript", "-e", script], capture_output=True)


async def test_make_table():
    global WRITE_TEST_TABLE_INDEX
    # Clean up any leftover write-test tables from a previous run
    await _cleanup_write_test_tables()
    tools = IntrospectionTools()
    result = await tools.make_table(
        slide_number=2,
        rows=3,
        columns=3,
        position=[100, 350],
        width=400,
        height=200,
        name="WriteTest",
        header_row_count=1,
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert data["slide_number"] == 2, f"expected slide_number=2, got {data['slide_number']}"
    assert isinstance(data["table_index"], int) and data["table_index"] >= 1, f"bad table_index: {data['table_index']}"
    assert data["name"] == "WriteTest", f"expected name='WriteTest', got {data['name']}"
    WRITE_TEST_TABLE_INDEX = data["table_index"]
    print(f"✅ make_table (table_index={WRITE_TEST_TABLE_INDEX})")


async def test_set_cell_value():
    tools = IntrospectionTools()
    tidx = await _ensure_write_test_table(tools)
    # Set a value in the WriteTest table (row 2, col A — a data row)
    result = await tools.set_cell_value(
        slide_number=2,
        table_index=tidx,
        cell_address="A2",
        value="HelloWrite",
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert data["address"] == "A2", f"bad address: {data['address']}"
    assert data["set_to"] == "HelloWrite", f"bad set_to: {data['set_to']}"

    # Verify the value was actually set
    verify = await tools.get_table_cell(
        slide_number=2,
        table_index=tidx,
        cell_address="A2",
        doc_name=FIXTURE_DOC,
    )
    vdata = parse_tool_result(verify)
    assert vdata["value"]["value"] == "HelloWrite", f"cell read-back mismatch: {vdata['value']}"
    print("✅ set_cell_value")


async def test_merge_cells():
    tools = IntrospectionTools()
    tidx = await _ensure_write_test_table(tools)
    result = await tools.merge_cells(
        slide_number=2,
        table_index=tidx,
        range_address="B2:C2",
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert data["merged"] == "B2:C2", f"bad merged: {data['merged']}"
    # Verify no exception and table still has 3 rows/3 cols
    info = await tools.get_table_info(
        slide_number=2,
        table_index=tidx,
        doc_name=FIXTURE_DOC,
    )
    idata = parse_tool_result(info)
    assert idata["row_count"] == 3
    assert idata["column_count"] == 3
    print("✅ merge_cells")


async def test_unmerge_cells():
    tools = IntrospectionTools()
    tidx = await _ensure_write_test_table(tools)
    result = await tools.unmerge_cells(
        slide_number=2,
        table_index=tidx,
        range_address="B2:C2",
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert data["unmerged"] == "B2:C2", f"bad unmerged: {data['unmerged']}"
    print("✅ unmerge_cells")


async def test_clear_cells():
    tools = IntrospectionTools()
    tidx = await _ensure_write_test_table(tools)
    # First set a value so there is something to clear
    await tools.set_cell_value(
        slide_number=2,
        table_index=tidx,
        cell_address="A2",
        value="ToBeCleared",
        doc_name=FIXTURE_DOC,
    )
    result = await tools.clear_cells(
        slide_number=2,
        table_index=tidx,
        range_address="A2",
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert data["cleared"] == "A2", f"bad cleared: {data['cleared']}"

    # Verify A2 is now empty
    verify = await tools.get_table_cell(
        slide_number=2,
        table_index=tidx,
        cell_address="A2",
        doc_name=FIXTURE_DOC,
    )
    vdata = parse_tool_result(verify)
    assert vdata["value"]["type"] == "empty", f"expected empty, got {vdata['value']}"
    print("✅ clear_cells")


async def test_sort_table():
    tools = IntrospectionTools()
    tidx = await _ensure_write_test_table(tools)
    # Populate column B (rows 2..3) with descending integers: B2=30, B3=10
    await tools.set_cell_value(
        slide_number=2, table_index=tidx, cell_address="B2", value="30", doc_name=FIXTURE_DOC
    )
    await tools.set_cell_value(
        slide_number=2, table_index=tidx, cell_address="B3", value="10", doc_name=FIXTURE_DOC
    )
    # Also set A col so we can verify rows moved
    await tools.set_cell_value(
        slide_number=2, table_index=tidx, cell_address="A2", value="Row2", doc_name=FIXTURE_DOC
    )
    await tools.set_cell_value(
        slide_number=2, table_index=tidx, cell_address="A3", value="Row3", doc_name=FIXTURE_DOC
    )

    # Sort by column B ascending — B2 (30) should move after B3 (10)
    result = await tools.sort_table(
        slide_number=2,
        table_index=tidx,
        by_column=2,
        direction="ascending",
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert data["sorted"] is True
    assert data["by_column"] == 2
    assert data["direction"] == "ascending"

    # Verify B2 is now 10 and B3 is now 30 (ascending order)
    b2 = parse_tool_result(await tools.get_table_cell(
        slide_number=2, table_index=tidx, cell_address="B2", doc_name=FIXTURE_DOC
    ))
    b3 = parse_tool_result(await tools.get_table_cell(
        slide_number=2, table_index=tidx, cell_address="B3", doc_name=FIXTURE_DOC
    ))
    b2_val = b2["value"]["value"]
    b3_val = b3["value"]["value"]
    assert float(b2_val) < float(b3_val), f"sort failed: B2={b2_val}, B3={b3_val}"
    print("✅ sort_table")


async def main():
    print("🧪 Introspection integration tests")
    print("=" * 40)
    await test_list_slide_items()
    await test_get_table_info_default()
    await test_get_table_info_with_cells()
    await test_get_table_cell()
    # Phase 2 Batch A
    await test_get_item_properties()
    await test_get_shape_text()
    await test_get_text_item_text()
    await test_get_presenter_notes()
    await test_get_slide_properties()
    await test_get_document_state()
    await test_get_cell_range()
    # Phase 2 Batch B — table writes
    await test_make_table()
    await test_set_cell_value()
    await test_merge_cells()
    await test_unmerge_cells()
    await test_clear_cells()
    await test_sort_table()
    print("=" * 40)
    print("🎉 All tests passed")


if __name__ == "__main__":
    asyncio.run(main())
