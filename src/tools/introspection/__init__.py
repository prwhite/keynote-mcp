"""
Introspection tools - Modular structure

Phase 2 is complete. The subpackage now covers:
- Reads (slide items, slide properties, presenter notes, document state)
- Table introspection (get_table_info, get_table_cell, get_cell_range)
- Table writes (set_cell_value, make_table, merge/unmerge/clear cells, sort)
- Item reads and writes (get/set position, size, rotation; delete)
- Item makers (make_line, make_shape, make_movie, make_audio_clip)
- Slide writes (set_presenter_notes)
- Playback verbs (start_playback, stop_playback, show_next, show_previous, goto_slide)
- Escape hatch (run_applescript_snippet)

The name "introspection" predates the write/playback scope expansion but
stays for module continuity.
"""

from .base import IntrospectionTools

__all__ = ['IntrospectionTools']
