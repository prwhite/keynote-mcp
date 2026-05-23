#!/usr/bin/env python3
"""
Integration tests for introspection tools.
Requires:
  - Keynote running
  - introspection_fixture.key document open (run payton.nogit/fixtures/create_test_fixture.applescript)
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


async def main():
    print("🧪 Introspection integration tests")
    print("=" * 40)
    await test_list_slide_items()
    print("=" * 40)
    print("🎉 All tests passed")


if __name__ == "__main__":
    asyncio.run(main())
