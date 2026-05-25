"""
KeynoteOps — directly-AppleScript-backed Keynote tools.

Umbrella for every tool that talks to Keynote via the sdef-published
scripting surface (or, in narrowly-scoped cases, System Events UI
scripting). Distinct from the higher-level heuristic/orchestration tools
elsewhere in `src/tools/` (zen_validation, guided_presentation,
smart_layout, content) which compose multiple low-level operations.

Surface (Phase 1 + Phase 2 + ongoing):
- Reads: slide items, table info, table cells, item properties, shape /
  text item text, presenter notes, slide properties, document state,
  cell range.
- Table writes: set_cell_value, make_table, merge / unmerge / clear
  cells, sort_table.
- Item writes: set_item_position / size / rotation, delete_item.
- Item makers: make_line / shape / movie / audio_clip.
- Text styling: set_text_font / size / color.
- Slide writes: set_presenter_notes.
- Playback: start_playback, stop_playback, show_next / previous,
  goto_slide.
- Escape hatch: run_applescript_snippet.

Historical naming: the AppleScript helper files under `src/applescript/`
keep the prefix `introspection_*.applescript` from the Phase 1 era. The
prefix is an internal implementation detail (script-file paths used by
ops modules) and was retained during the subpackage rename to keep the
diff focused. Future cleanup can rename those files in a separate pass.
"""

from .base import KeynoteOps

__all__ = ['KeynoteOps']
