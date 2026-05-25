"""
Escape-hatch operation: run arbitrary AppleScript snippets.

This is a power-user tool. The LLM should prefer structured tools.
The MCP host gates tool execution behind user permission, so this is
not a security risk, but it is a footgun if used carelessly — snippets
that write to the wrong document or crash mid-execution will not be
automatically reverted.
"""

import json
from typing import List
from mcp.types import TextContent

from ...utils import AppleScriptRunner, AppleScriptError


class EscapeOperations:
    """Run raw AppleScript snippets as an escape hatch."""

    def __init__(self, runner: AppleScriptRunner):
        # Takes the runner directly, not the _run_introspection wrapper,
        # because there is no JSON helper or named handler file to load.
        self.runner = runner

    async def run_applescript_snippet(
        self,
        snippet: str,
        wrap_in_tell: bool = True,
        doc_name: str = "",
    ) -> List[TextContent]:
        # Build the full script according to wrapping rules.
        if wrap_in_tell:
            if doc_name:
                escaped_doc = doc_name.replace('"', '\\"')
                full_script = (
                    'tell application "Keynote"\n'
                    f'tell document "{escaped_doc}"\n'
                    f'{snippet}\n'
                    'end tell\n'
                    'end tell'
                )
            else:
                full_script = (
                    'tell application "Keynote"\n'
                    f'{snippet}\n'
                    'end tell'
                )
        else:
            full_script = snippet

        try:
            stdout = self.runner.execute_script(full_script)
            result_value = stdout if stdout else None
            payload = {"result": result_value}
        except AppleScriptError as e:
            payload = {"error": str(e), "result": None}
        except Exception as e:
            payload = {"error": f"Unexpected error: {e}", "result": None}

        return [TextContent(type="text", text=json.dumps(payload, indent=2))]
