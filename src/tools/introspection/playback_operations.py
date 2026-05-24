"""
Playback control operations: start, stop, show next/previous, goto slide.
"""

import json
from typing import Any, Callable, List
from mcp.types import TextContent


class PlaybackOperations:
    """Playback verbs for Keynote presentations."""

    def __init__(self, runner_caller: Callable[[str, str, list], Any]):
        # runner_caller is IntrospectionTools._run_introspection
        self._run = runner_caller

    async def start_playback(
        self,
        doc_name: str = "",
        from_slide: int = 0,
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_playback.applescript",
                "startPlayback",
                [doc_name, from_slide],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            error_payload = {"error": str(e)}
            return [TextContent(type="text", text=json.dumps(error_payload, indent=2))]

    async def stop_playback(self) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_playback.applescript",
                "stopPlayback",
                [],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            error_payload = {"error": str(e)}
            return [TextContent(type="text", text=json.dumps(error_payload, indent=2))]

    async def show_next(self) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_playback.applescript",
                "showNext",
                [],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            error_payload = {"error": str(e)}
            return [TextContent(type="text", text=json.dumps(error_payload, indent=2))]

    async def show_previous(self) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_playback.applescript",
                "showPrevious",
                [],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            error_payload = {"error": str(e)}
            return [TextContent(type="text", text=json.dumps(error_payload, indent=2))]

    async def goto_slide(
        self,
        slide_number: int,
        doc_name: str = "",
    ) -> List[TextContent]:
        try:
            data = self._run(
                "introspection_playback.applescript",
                "gotoSlide",
                [doc_name, slide_number],
            )
            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            error_payload = {"error": str(e)}
            return [TextContent(type="text", text=json.dumps(error_payload, indent=2))]
