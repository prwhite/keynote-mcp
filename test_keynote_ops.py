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

from src.tools.keynote_ops import KeynoteOps

FIXTURE_DOC = "introspection_fixture.key"

# Module-level state for write tests — set by test_make_table, read by subsequent tests.
WRITE_TEST_TABLE_INDEX = None

# Module-level state for Batch C item tests — set by test_make_shape, used by
# test_set_item_position, test_set_item_size, test_set_item_rotation.
WRITE_TEST_SHAPE_INDEX = None


def parse_tool_result(result):
    """Tool methods return List[TextContent]; the first item's .text is JSON."""
    assert len(result) == 1, f"expected single TextContent, got {len(result)}"
    return json.loads(result[0].text)


async def test_list_slide_items():
    tools = KeynoteOps()
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
    tools = KeynoteOps()
    result = await tools.get_table_info(slide_number=2, table_index=1, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["row_count"] == 4
    assert data["column_count"] == 3
    assert data["header_row_count"] == 1
    assert data["name"] == "Q1"
    assert "cells" not in data, "cells should be absent by default"
    print("✅ get_table_info (default)")


async def test_get_table_info_with_cells():
    tools = KeynoteOps()
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
    tools = KeynoteOps()
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
    tools = KeynoteOps()
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
    tools = KeynoteOps()
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
    tools = KeynoteOps()
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
    tools = KeynoteOps()
    result = await tools.get_presenter_notes(slide_number=1, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["slide_number"] == 1
    assert isinstance(data["text"], str)
    assert isinstance(data["paragraphs"], list)
    print("✅ get_presenter_notes")


async def test_get_slide_properties():
    tools = KeynoteOps()
    result = await tools.get_slide_properties(slide_number=2, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["slide_number"] == 2
    assert isinstance(data["title_showing"], bool)
    assert isinstance(data["body_showing"], bool)
    assert isinstance(data["skipped"], bool)
    assert isinstance(data["transition"], dict)
    print("✅ get_slide_properties")


async def test_get_document_state():
    tools = KeynoteOps()
    result = await tools.get_document_state(doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["slide_count"] >= 1
    assert isinstance(data["width"], (int, float))
    assert isinstance(data["height"], (int, float))
    assert isinstance(data["current_slide"], int)
    print("✅ get_document_state")


async def test_get_cell_range():
    tools = KeynoteOps()
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


async def _ensure_write_test_table(tools: "KeynoteOps") -> int:
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
    tools = KeynoteOps()
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
    tools = KeynoteOps()
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
    tools = KeynoteOps()
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
    tools = KeynoteOps()
    tidx = await _ensure_write_test_table(tools)
    # Self-contained: merge first so unmerge has work to do. Without this
    # priming step the unmerge call silently no-ops and the test verifies
    # nothing about whether the unmerge actually ran.
    await tools.merge_cells(
        slide_number=2,
        table_index=tidx,
        range_address="A1:B1",
        doc_name=FIXTURE_DOC,
    )
    result = await tools.unmerge_cells(
        slide_number=2,
        table_index=tidx,
        range_address="A1:B1",
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert data["unmerged"] == "A1:B1", f"bad unmerged: {data['unmerged']}"
    print("✅ unmerge_cells")


async def test_clear_cells():
    tools = KeynoteOps()
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
    tools = KeynoteOps()
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


async def _cleanup_write_test_shapes():
    """Remove any leftover test shapes from a previous Batch C run.

    We delete all shapes on slide 3 except the first one (keep the fixture shape at index 1).
    Slide 2 is used by the table-write tests; we use slide 3 for shape/line tests to avoid
    cross-contamination.  If slide 3 has no shapes we leave it untouched.
    """
    import subprocess
    script = """
tell application "Keynote"
    set targetDoc to document "introspection_fixture.key"
    set targetSlide to slide 2 of targetDoc
    -- Delete all shapes beyond the first (the fixture shape at index 1)
    repeat while (count of shapes of targetSlide) > 1
        delete shape (count of shapes of targetSlide) of targetSlide
    end repeat
    -- Delete all lines (we create them in tests; none should be in the fixture)
    repeat while (count of lines of targetSlide) > 0
        delete line 1 of targetSlide
    end repeat
    return "ok"
end tell
"""
    subprocess.run(["osascript", "-e", script], capture_output=True)


# ---------------------------------------------------------------------------
# Batch C tests
# ---------------------------------------------------------------------------

async def test_make_shape():
    """Create a shape, record its index for subsequent geometry-write tests."""
    global WRITE_TEST_SHAPE_INDEX
    tools = KeynoteOps()

    # Clean up any leftover shapes/lines from a prior run
    await _cleanup_write_test_shapes()

    result = await tools.make_shape(
        slide_number=2,
        position=[200, 450],
        size=[120, 80],
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert "error" not in data, f"make_shape returned error: {data}"
    assert data["kind"] == "shape", f"expected kind='shape', got {data['kind']}"
    assert isinstance(data["index"], int) and data["index"] >= 1, f"bad index: {data['index']}"
    assert data["slide_number"] == 2
    WRITE_TEST_SHAPE_INDEX = data["index"]
    print(f"✅ make_shape (shape_index={WRITE_TEST_SHAPE_INDEX})")


async def test_set_item_position():
    """Move the test shape and verify via get_item_properties."""
    global WRITE_TEST_SHAPE_INDEX
    tools = KeynoteOps()
    assert WRITE_TEST_SHAPE_INDEX is not None, "test_make_shape must run first"

    result = await tools.set_item_position(
        slide_number=2,
        item_kind="shape",
        item_index=WRITE_TEST_SHAPE_INDEX,
        position=[300, 500],
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert "error" not in data, f"set_item_position returned error: {data}"
    assert data["position"] == [300, 500], f"unexpected position: {data['position']}"

    # Verify via get_item_properties
    verify = parse_tool_result(await tools.get_item_properties(
        slide_number=2, item_kind="shape", item_index=WRITE_TEST_SHAPE_INDEX, doc_name=FIXTURE_DOC
    ))
    pos = verify["position"]
    assert abs(pos[0] - 300) < 2 and abs(pos[1] - 500) < 2, f"position read-back mismatch: {pos}"
    print("✅ set_item_position")


async def test_set_item_size():
    """Resize the test shape and verify via get_item_properties."""
    global WRITE_TEST_SHAPE_INDEX
    tools = KeynoteOps()
    assert WRITE_TEST_SHAPE_INDEX is not None, "test_make_shape must run first"

    result = await tools.set_item_size(
        slide_number=2,
        item_kind="shape",
        item_index=WRITE_TEST_SHAPE_INDEX,
        size=[200, 150],
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert "error" not in data, f"set_item_size returned error: {data}"
    assert data["size"] == [200, 150], f"unexpected size: {data['size']}"

    # Verify via get_item_properties
    verify = parse_tool_result(await tools.get_item_properties(
        slide_number=2, item_kind="shape", item_index=WRITE_TEST_SHAPE_INDEX, doc_name=FIXTURE_DOC
    ))
    sz = verify["size"]
    assert abs(sz[0] - 200) < 2 and abs(sz[1] - 150) < 2, f"size read-back mismatch: {sz}"
    print("✅ set_item_size")


async def test_set_item_rotation():
    """Rotate the test shape and verify via get_item_properties."""
    global WRITE_TEST_SHAPE_INDEX
    tools = KeynoteOps()
    assert WRITE_TEST_SHAPE_INDEX is not None, "test_make_shape must run first"

    result = await tools.set_item_rotation(
        slide_number=2,
        item_kind="shape",
        item_index=WRITE_TEST_SHAPE_INDEX,
        rotation=45,
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert "error" not in data, f"set_item_rotation returned error: {data}"
    assert data["rotation"] == 45, f"unexpected rotation: {data['rotation']}"

    # Verify via get_item_properties
    verify = parse_tool_result(await tools.get_item_properties(
        slide_number=2, item_kind="shape", item_index=WRITE_TEST_SHAPE_INDEX, doc_name=FIXTURE_DOC
    ))
    assert verify["rotation"] == 45, f"rotation read-back mismatch: {verify['rotation']}"
    print("✅ set_item_rotation")


async def test_make_line():
    """Create a line and verify it appears in list_slide_items."""
    tools = KeynoteOps()

    # Count lines before
    items_before = parse_tool_result(await tools.list_slide_items(
        slide_number=2, doc_name=FIXTURE_DOC
    ))
    lines_before = sum(1 for i in items_before["items"] if i["kind"] == "line")

    result = await tools.make_line(
        slide_number=2,
        start_point=[50, 50],
        end_point=[200, 200],
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert "error" not in data, f"make_line returned error: {data}"
    assert data["kind"] == "line", f"expected kind='line', got {data['kind']}"
    assert data["slide_number"] == 2
    assert isinstance(data["index"], int) and data["index"] >= 1

    # Verify line count increased
    items_after = parse_tool_result(await tools.list_slide_items(
        slide_number=2, doc_name=FIXTURE_DOC
    ))
    lines_after = sum(1 for i in items_after["items"] if i["kind"] == "line")
    assert lines_after == lines_before + 1, f"line count mismatch: before={lines_before}, after={lines_after}"
    print("✅ make_line")


async def test_delete_item():
    """Create a transient shape, delete it, verify count drops."""
    tools = KeynoteOps()

    # Create a transient shape
    make_result = parse_tool_result(await tools.make_shape(
        slide_number=2,
        position=[600, 10],
        size=[50, 50],
        doc_name=FIXTURE_DOC,
    ))
    assert "error" not in make_result, f"make_shape for delete test failed: {make_result}"
    transient_index = make_result["index"]

    # Count shapes before delete
    items_before = parse_tool_result(await tools.list_slide_items(
        slide_number=2, doc_name=FIXTURE_DOC
    ))
    shapes_before = sum(1 for i in items_before["items"] if i["kind"] == "shape")

    # Delete it
    del_result = parse_tool_result(await tools.delete_item(
        slide_number=2,
        item_kind="shape",
        item_index=transient_index,
        doc_name=FIXTURE_DOC,
    ))
    assert "error" not in del_result, f"delete_item returned error: {del_result}"
    assert del_result["deleted"]["kind"] == "shape"
    assert del_result["deleted"]["index"] == transient_index

    # Verify count dropped
    items_after = parse_tool_result(await tools.list_slide_items(
        slide_number=2, doc_name=FIXTURE_DOC
    ))
    shapes_after = sum(1 for i in items_after["items"] if i["kind"] == "shape")
    assert shapes_after == shapes_before - 1, f"shape count after delete: before={shapes_before}, after={shapes_after}"
    print("✅ delete_item")


async def test_make_movie():
    """Test make_movie with a non-existent file — verifies file-not-found validation.

    Happy-path (embedding a real video) is not tested here because it requires a
    media file in the fixture, which is not checked in. This test confirms that:
    1. The tool wire path is correctly registered end-to-end.
    2. The Python-level file-existence check returns a well-formed JSON error.
    """
    tools = KeynoteOps()
    result = await tools.make_movie(
        slide_number=2,
        file_path="/tmp/nonexistent_video_for_test.mp4",
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert "error" in data, f"expected JSON error for missing file, got: {data}"
    assert "not found" in data["error"] or "nonexistent" in data["error"], f"unexpected error message: {data['error']}"
    print("✅ make_movie (error path: file not found)")


async def test_make_audio_clip():
    """Test make_audio_clip with a non-existent file — verifies file-not-found validation.

    Happy-path (embedding a real audio file) is not tested here because it requires a
    media file in the fixture, which is not checked in. This test confirms that:
    1. The tool wire path is correctly registered end-to-end.
    2. The Python-level file-existence check returns a well-formed JSON error.
    """
    tools = KeynoteOps()
    result = await tools.make_audio_clip(
        slide_number=2,
        file_path="/tmp/nonexistent_audio_for_test.aiff",
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert "error" in data, f"expected JSON error for missing file, got: {data}"
    assert "not found" in data["error"] or "nonexistent" in data["error"], f"unexpected error message: {data['error']}"
    print("✅ make_audio_clip (error path: file not found)")


async def test_set_text_font_size_color():
    """Make a transient shape, set font/size/color, verify via get_shape_text.

    Combined into one test because all three setters share the same scaffolding
    (create a shape, mutate, read back, clean up). Tests each setter independently
    so a single failure points at the right tool.
    """
    tools = KeynoteOps()
    # Make a transient shape on slide 1 — slide 1 has no existing user shapes
    make = await tools.make_shape(
        slide_number=1, position=[400, 400], size=[300, 100], doc_name=FIXTURE_DOC
    )
    mdata = parse_tool_result(make)
    sidx = mdata["index"]

    # Need to give the shape some text so font/size/color have something to apply to.
    await tools.run_applescript_snippet(
        snippet=f'set object text of shape {sidx} of slide 1 of front document to "style probe"',
        wrap_in_tell=True,
    )

    # set_text_font
    r1 = await tools.set_text_font(
        slide_number=1, item_kind="shape", item_index=sidx,
        font_name="HelveticaNeue-Bold", doc_name=FIXTURE_DOC,
    )
    d1 = parse_tool_result(r1)
    assert d1.get("font") == "HelveticaNeue-Bold", f"set_text_font response: {d1}"

    # set_text_size
    r2 = await tools.set_text_size(
        slide_number=1, item_kind="shape", item_index=sidx,
        size=48, doc_name=FIXTURE_DOC,
    )
    d2 = parse_tool_result(r2)
    assert d2.get("size") == 48, f"set_text_size response: {d2}"

    # set_text_color (full green, 16-bit)
    r3 = await tools.set_text_color(
        slide_number=1, item_kind="shape", item_index=sidx,
        color=[0, 65535, 0], doc_name=FIXTURE_DOC,
    )
    d3 = parse_tool_result(r3)
    assert d3.get("color") == [0, 65535, 0], f"set_text_color response: {d3}"

    # Round-trip verify via get_shape_text
    rt = await tools.get_shape_text(slide_number=1, shape_index=sidx, doc_name=FIXTURE_DOC)
    rtdata = parse_tool_result(rt)
    paragraphs = rtdata.get("paragraphs", [])
    assert paragraphs, f"expected paragraphs after text set; got: {rtdata}"
    p0 = paragraphs[0]
    # font/size should round-trip exactly; color may be quantized by Keynote
    assert p0["font"] == "HelveticaNeue-Bold", f"font round-trip: {p0}"
    assert p0["size"] == 48.0, f"size round-trip: {p0}"
    # Color: Keynote quantizes set color significantly (a {0, 65535, 0} input
    # may come back as {~8000, ~65000, ~1500}). Assert green dominates rather
    # than expecting exact channel values.
    r_v, g_v, b_v = p0["color"]
    assert g_v > 50000, f"green channel should dominate; got: {p0['color']}"
    assert g_v > r_v * 3 and g_v > b_v * 3, f"green should dwarf red/blue; got: {p0['color']}"

    # Cleanup: delete the transient shape
    await tools.delete_item(
        slide_number=1, item_kind="shape", item_index=sidx, doc_name=FIXTURE_DOC
    )

    print("✅ set_text_font / set_text_size / set_text_color")


async def test_set_presenter_notes():
    """Set notes on slide 1, then read back and verify content."""
    tools = KeynoteOps()
    test_notes = "Batch D test notes: Phase 2 complete."
    result = await tools.set_presenter_notes(
        slide_number=1,
        notes=test_notes,
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert "error" not in data, f"set_presenter_notes returned error: {data}"
    assert data["slide_number"] == 1, f"unexpected slide_number: {data['slide_number']}"
    assert data["characters_set"] == len(test_notes), f"unexpected characters_set: {data['characters_set']}"

    # Read back and verify
    read_result = await tools.get_presenter_notes(slide_number=1, doc_name=FIXTURE_DOC)
    read_data = parse_tool_result(read_result)
    # Plain text comparison (Keynote may append a trailing newline — strip both)
    assert read_data["text"].strip() == test_notes.strip(), \
        f"notes read-back mismatch: expected {test_notes!r}, got {read_data['text']!r}"
    print("✅ set_presenter_notes")


async def test_goto_slide():
    """Navigate to slide 2 and verify, then back to slide 1."""
    tools = KeynoteOps()

    result2 = await tools.goto_slide(slide_number=2, doc_name=FIXTURE_DOC)
    data2 = parse_tool_result(result2)
    assert "error" not in data2, f"goto_slide(2) returned error: {data2}"
    assert data2["current_slide"] == 2, f"unexpected current_slide: {data2['current_slide']}"

    # Verify via get_document_state
    state = parse_tool_result(await tools.get_document_state(doc_name=FIXTURE_DOC))
    assert state["current_slide"] == 2, f"document state shows wrong slide: {state['current_slide']}"

    # Navigate back to slide 1
    result1 = await tools.goto_slide(slide_number=1, doc_name=FIXTURE_DOC)
    data1 = parse_tool_result(result1)
    assert "error" not in data1, f"goto_slide(1) returned error: {data1}"
    assert data1["current_slide"] == 1, f"unexpected current_slide after nav back: {data1['current_slide']}"
    print("✅ goto_slide")


async def test_start_then_stop_playback():
    """Start playback then immediately stop it.

    We don't assert any mid-presentation state because timing is fragile.
    The test just verifies the wire path works end-to-end and that Keynote
    does not remain stuck in presentation mode after stop_playback is called.
    If start_playback fails (e.g., no display), we accept a JSON error response
    without failing the test — what matters is no Python crash and we still
    call stop to be safe.
    """
    tools = KeynoteOps()

    start_result = await tools.start_playback(doc_name=FIXTURE_DOC, from_slide=1)
    start_data = parse_tool_result(start_result)
    # start_data should be either {"playing": true, ...} or {"error": "..."}
    # Both are acceptable — what matters is parseable JSON and no Python crash.
    assert isinstance(start_data, dict), f"start_playback returned non-dict: {start_data}"

    # Always call stop regardless, to avoid leaving Keynote stuck.
    stop_result = await tools.stop_playback()
    stop_data = parse_tool_result(stop_result)
    assert isinstance(stop_data, dict), f"stop_playback returned non-dict: {stop_data}"
    print("✅ start_then_stop_playback")


async def test_show_next_outside_playback():
    """Call show_next outside of playback mode.

    Keynote will raise an error ('not currently playing a slideshow').
    The tool must catch it and return a parseable JSON error — not crash.
    """
    tools = KeynoteOps()
    result = await tools.show_next()
    data = parse_tool_result(result)
    # Either succeeds (if somehow in playback — unlikely) or returns JSON error.
    # What we care about: no exception, result is a dict.
    assert isinstance(data, dict), f"show_next returned non-dict: {data}"
    print("✅ show_next (error path accepted outside playback)")


async def test_show_previous_outside_playback():
    """Call show_previous outside of playback mode — same contract as show_next."""
    tools = KeynoteOps()
    result = await tools.show_previous()
    data = parse_tool_result(result)
    assert isinstance(data, dict), f"show_previous returned non-dict: {data}"
    print("✅ show_previous (error path accepted outside playback)")


async def test_run_applescript_snippet():
    """Three sub-tests for the escape hatch."""
    tools = KeynoteOps()

    # 1. Snippet wrapped in `tell application "Keynote"` only (no document
    # tell). Targeting the fixture explicitly because the user may have
    # other Keynote docs open and `front document` would resolve to those.
    result1 = await tools.run_applescript_snippet(
        snippet=f'return name of document "{FIXTURE_DOC}"',
        wrap_in_tell=True,
        doc_name="",
    )
    data1 = parse_tool_result(result1)
    assert "error" not in data1, f"snippet 1 returned error: {data1}"
    assert data1["result"] == FIXTURE_DOC, \
        f"snippet 1 result should equal fixture name; got: {data1['result']!r}"

    # 2. Simple arithmetic — wrap_in_tell=True, no doc_name.
    result2 = await tools.run_applescript_snippet(
        snippet="return (1 + 1) as text",
        wrap_in_tell=True,
        doc_name="",
    )
    data2 = parse_tool_result(result2)
    assert "error" not in data2, f"snippet 2 returned error: {data2}"
    assert data2["result"] == "2", f"snippet 2 arithmetic failed: {data2['result']!r}"

    # 3. Snippet that raises an error — should return {"error": "...", "result": null}.
    result3 = await tools.run_applescript_snippet(
        snippet="return undefined_variable_xyz_that_does_not_exist",
        wrap_in_tell=False,
    )
    data3 = parse_tool_result(result3)
    assert "error" in data3 and data3["error"], f"snippet 3 should have error field: {data3}"
    assert data3["result"] is None, f"snippet 3 result should be null: {data3['result']}"
    print("✅ run_applescript_snippet")


async def test_set_item_opacity():
    """Set opacity on a transient shape, verify via get_item_properties."""
    tools = KeynoteOps()
    # Make a transient shape on slide 1 so we don't touch fixture state on slide 2
    make = await tools.make_shape(
        slide_number=1, position=[300, 300], size=[100, 100], doc_name=FIXTURE_DOC
    )
    mdata = parse_tool_result(make)
    assert "index" in mdata, f"make_shape returned no index — full payload: {mdata}"
    sidx = mdata["index"]

    # Set opacity to 35
    r = await tools.set_item_opacity(
        slide_number=1, item_kind="shape", item_index=sidx,
        opacity=35, doc_name=FIXTURE_DOC,
    )
    d = parse_tool_result(r)
    assert d.get("opacity") == 35, f"set_item_opacity response: {d}"

    # Verify via get_item_properties
    rt = await tools.get_item_properties(
        slide_number=1, item_kind="shape", item_index=sidx, doc_name=FIXTURE_DOC,
    )
    rtdata = parse_tool_result(rt)
    assert rtdata["opacity"] == 35, f"opacity round-trip: {rtdata}"

    # Out-of-range guard returns a JSON error
    r2 = await tools.set_item_opacity(
        slide_number=1, item_kind="shape", item_index=sidx,
        opacity=150, doc_name=FIXTURE_DOC,
    )
    d2 = parse_tool_result(r2)
    assert "error" in d2, f"out-of-range opacity should error: {d2}"

    # Cleanup
    await tools.delete_item(
        slide_number=1, item_kind="shape", item_index=sidx, doc_name=FIXTURE_DOC,
    )
    print("✅ set_item_opacity")


async def test_clear_slide():
    """Populate a transient slide with stuff, clear it, verify items_deleted > 0."""
    tools = KeynoteOps()
    # Use slide 1 — empty of user content by default. Add a shape, a line, and a text item.
    await tools.make_shape(
        slide_number=1, position=[100, 100], size=[100, 100], doc_name=FIXTURE_DOC
    )
    await tools.make_shape(
        slide_number=1, position=[300, 100], size=[100, 100], doc_name=FIXTURE_DOC
    )
    await tools.make_line(
        slide_number=1, start_point=[200, 400], end_point=[600, 400], doc_name=FIXTURE_DOC
    )

    # Snapshot what was on the slide before clearing
    li_before = parse_tool_result(
        await tools.list_slide_items(slide_number=1, doc_name=FIXTURE_DOC)
    )
    shapes_before = sum(1 for i in li_before["items"] if i["kind"] == "shape")
    lines_before = sum(1 for i in li_before["items"] if i["kind"] == "line")
    assert shapes_before >= 2, f"expected >= 2 shapes after setup; got {shapes_before}"
    assert lines_before >= 1, f"expected >= 1 line after setup; got {lines_before}"

    # Clear
    r = await tools.clear_slide(slide_number=1, doc_name=FIXTURE_DOC)
    d = parse_tool_result(r)
    assert d["slide_number"] == 1
    assert d["items_deleted"] >= shapes_before + lines_before, \
        f"items_deleted ({d['items_deleted']}) should include the {shapes_before} shapes + {lines_before} line we added"

    # Verify the user content is gone
    li_after = parse_tool_result(
        await tools.list_slide_items(slide_number=1, doc_name=FIXTURE_DOC)
    )
    shapes_after = sum(1 for i in li_after["items"] if i["kind"] == "shape")
    lines_after = sum(1 for i in li_after["items"] if i["kind"] == "line")
    assert shapes_after == 0, f"shapes should be gone; remaining: {shapes_after}"
    assert lines_after == 0, f"lines should be gone; remaining: {lines_after}"
    print("✅ clear_slide")


# -----------------------------------------------------------------------------
# Slide-number sentinel tests (v0.6.0)
#
# Verify the "0 / omitted = current slide" sentinel pattern routes correctly
# through every layer (server → ops → AppleScript → resolveSlide helper) and
# that get_document_state exposes the right absolute/visible/hidden fields.
# -----------------------------------------------------------------------------


async def test_sentinel_routes_to_current_slide():
    """slide_number=0 should resolve to whatever Keynote considers `current slide`."""
    tools = KeynoteOps()
    # Navigate to slide 2 deterministically; goto_slide already takes absolute
    # indices and returns the resolved current_slide.
    await tools.goto_slide(slide_number=2, doc_name=FIXTURE_DOC)
    # Now ask list_slide_items with the sentinel.
    result_sentinel = await tools.list_slide_items(slide_number=0, doc_name=FIXTURE_DOC)
    data_sentinel = parse_tool_result(result_sentinel)
    # Sentinel should resolve to slide 2.
    assert data_sentinel["slide_number"] == 2, \
        f"sentinel expected to resolve to slide 2, got {data_sentinel['slide_number']}"
    # And the items should match an explicit slide_number=2 call.
    result_explicit = await tools.list_slide_items(slide_number=2, doc_name=FIXTURE_DOC)
    data_explicit = parse_tool_result(result_explicit)
    assert len(data_sentinel["items"]) == len(data_explicit["items"]), \
        "sentinel and explicit slide_number=2 returned different item counts"
    print("✅ sentinel_routes_to_current_slide")


async def test_sentinel_set_cell_value_round_trips():
    """Writing with sentinel should land on current slide and read back via explicit index."""
    tools = KeynoteOps()
    await tools.goto_slide(slide_number=2, doc_name=FIXTURE_DOC)
    # Write a marker to Q1's C3 (a free-form text column) using the sentinel.
    marker = "SentinelWrite-7"
    result = await tools.set_cell_value(
        slide_number=0,
        table_index=1,
        cell_address="C3",
        value=marker,
        doc_name=FIXTURE_DOC,
    )
    data = parse_tool_result(result)
    assert data["set_to"] == marker, f"unexpected response: {data}"
    # Read back via explicit slide_number=2 to prove the sentinel landed
    # on the correct slide.
    verify = await tools.get_table_cell(
        slide_number=2,
        table_index=1,
        cell_address="C3",
        doc_name=FIXTURE_DOC,
    )
    vdata = parse_tool_result(verify)
    assert vdata["value"]["value"] == marker, \
        f"round-trip failed: wrote {marker} via sentinel, read back {vdata['value']}"
    print("✅ sentinel_set_cell_value_round_trips")


async def test_sentinel_echoes_resolved_absolute_in_response():
    """When sentinel is used, the response should echo back the resolved absolute slide_number, not 0."""
    tools = KeynoteOps()
    await tools.goto_slide(slide_number=2, doc_name=FIXTURE_DOC)
    # get_table_info echoes slide_number — should be 2 (resolved), not 0 (passed).
    result = await tools.get_table_info(
        slide_number=0, table_index=1, doc_name=FIXTURE_DOC
    )
    data = parse_tool_result(result)
    assert data["slide_number"] == 2, \
        f"echo should be resolved absolute (2), got {data['slide_number']}"
    print("✅ sentinel_echoes_resolved_absolute_in_response")


async def test_get_document_state_absolute_current_slide():
    """current_slide should be the absolute index, even when slides are hidden."""
    tools = KeynoteOps()
    # Baseline: no hidden slides. current_slide should match visible.
    await tools.goto_slide(slide_number=2, doc_name=FIXTURE_DOC)
    result = await tools.get_document_state(doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["current_slide"] == 2, \
        f"baseline current_slide should be 2 (absolute), got {data['current_slide']}"
    assert "current_slide_visible" in data, "missing current_slide_visible field"
    assert "hidden_slide_indices" in data, "missing hidden_slide_indices field"
    assert isinstance(data["hidden_slide_indices"], list)
    print("✅ get_document_state_absolute_current_slide")


async def test_get_document_state_with_hidden_slide():
    """With slide 1 marked skipped, current_slide (absolute) and current_slide_visible should diverge."""
    tools = KeynoteOps()
    # Mark slide 1 as skipped via the escape hatch.
    skip_snippet = (
        'tell document "introspection_fixture.key" to '
        "set skipped of slide 1 to true"
    )
    try:
        await tools.run_applescript_snippet(snippet=skip_snippet, wrap_in_tell=True)
        await tools.goto_slide(slide_number=2, doc_name=FIXTURE_DOC)
        result = await tools.get_document_state(doc_name=FIXTURE_DOC)
        data = parse_tool_result(result)
        # Slide 2 is the only visible slide → visible index should be 1.
        assert data["current_slide"] == 2, \
            f"absolute current_slide should be 2 with hidden slide 1, got {data['current_slide']}"
        assert data["current_slide_visible"] == 1, \
            f"visible should be 1 when slide 1 is hidden, got {data['current_slide_visible']}"
        # hidden_slide_indices should include 1.
        assert 1 in data["hidden_slide_indices"], \
            f"slide 1 should be in hidden_slide_indices, got {data['hidden_slide_indices']}"
        # Sentinel write should still target absolute slide 2.
        marker = "PostHideSentinel-9"
        await tools.set_cell_value(
            slide_number=0, table_index=1, cell_address="C2",
            value=marker, doc_name=FIXTURE_DOC,
        )
        verify = await tools.get_table_cell(
            slide_number=2, table_index=1, cell_address="C2",
            doc_name=FIXTURE_DOC,
        )
        vdata = parse_tool_result(verify)
        assert vdata["value"]["value"] == marker, \
            f"sentinel write with hidden slides failed: read back {vdata['value']}"
    finally:
        # Unskip slide 1 so we don't leave the fixture in a weird state.
        unskip_snippet = (
            'tell document "introspection_fixture.key" to '
            "set skipped of slide 1 to false"
        )
        await tools.run_applescript_snippet(snippet=unskip_snippet, wrap_in_tell=True)
    print("✅ get_document_state_with_hidden_slide")


async def test_goto_slide_returns_absolute():
    """goto_slide's returned current_slide should be the absolute index."""
    tools = KeynoteOps()
    result = await tools.goto_slide(slide_number=1, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["current_slide"] == 1, \
        f"goto_slide should return absolute 1, got {data['current_slide']}"
    result = await tools.goto_slide(slide_number=2, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["current_slide"] == 2, \
        f"goto_slide should return absolute 2, got {data['current_slide']}"
    # Sentinel (0) should be a no-op and still return the current absolute index.
    result = await tools.goto_slide(slide_number=0, doc_name=FIXTURE_DOC)
    data = parse_tool_result(result)
    assert data["current_slide"] == 2, \
        f"goto_slide(0) should stay on 2, got {data['current_slide']}"
    print("✅ goto_slide_returns_absolute")


async def main():
    print("🧪 KeynoteOps integration tests")
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
    # Phase 2 Batch C — item writes and makers
    await test_make_shape()
    await test_set_item_position()
    await test_set_item_size()
    await test_set_item_rotation()
    await test_make_line()
    await test_delete_item()
    await test_make_movie()
    await test_make_audio_clip()
    await test_set_text_font_size_color()
    # Phase 2 Batch D — slide write, playback, escape hatch
    await test_set_presenter_notes()
    await test_goto_slide()
    await test_start_then_stop_playback()
    await test_show_next_outside_playback()
    await test_show_previous_outside_playback()
    await test_run_applescript_snippet()
    # Post-fork-eval additions. The start_playback test above can leave
    # the fixture in a "locked iWork document" state that blocks `make`
    # operations until the doc is closed and reopened. Re-running the
    # fixture script closes+saves+reopens the fixture, releasing the lock.
    import subprocess
    subprocess.run(
        ["osascript", "payton.nogit/fixtures/create_test_fixture.applescript"],
        check=True, capture_output=True,
    )
    await test_set_item_opacity()
    await test_clear_slide()
    # v0.6.0 — slide_number sentinel pattern
    await test_sentinel_routes_to_current_slide()
    await test_sentinel_set_cell_value_round_trips()
    await test_sentinel_echoes_resolved_absolute_in_response()
    await test_get_document_state_absolute_current_slide()
    await test_get_document_state_with_hidden_slide()
    await test_goto_slide_returns_absolute()
    print("=" * 40)
    print("🎉 All tests passed")


if __name__ == "__main__":
    asyncio.run(main())
