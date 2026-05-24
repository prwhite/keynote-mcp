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
    print("=" * 40)
    print("🎉 All tests passed")


if __name__ == "__main__":
    asyncio.run(main())
