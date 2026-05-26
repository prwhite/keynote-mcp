# Keynote-MCP

A Model Context Protocol (MCP) server that enables AI assistants to control Keynote presentations through AppleScript automation.

> **🎉 This is an enhanced fork** featuring modular architecture, theme-aware content management, and comprehensive documentation improvements.

> **🍴 Further-enhanced fork at [prwhite/keynote-mcp](https://github.com/prwhite/keynote-mcp).** Adds a `KeynoteOps` subpackage with ~30 directly-AppleScript-backed tools (slide / item / table introspection + writes + playback + an escape hatch), fixes a few destructive AppleScript bugs inherited from upstream, ships a standalone macOS binary build via PyInstaller + GitHub Actions, and is verified against the renamed "Keynote Creator Studio" app (bundle `com.apple.Keynote`). See [What's new in prwhite/keynote-mcp](#-whats-new-in-prwhitekeynote-mcp) at the bottom.

## Features
- **Presentation Management**: Create, open, save, close presentations  
- **Slide Operations**: Add, delete, duplicate, move slides
- **Theme-Aware Content**: Professional content placement using Keynote's design elements
- **Modular Architecture**: Maintainable codebase with specialized AppleScript modules
- **Export Functions**: Screenshots, PDF export

## Quick Setup

1. **Clone the repository**
   ```bash
   # For the further-enhanced fork (recommended — includes KeynoteOps + macOS binary):
   git clone https://github.com/prwhite/keynote-mcp.git
   cd keynote-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Grant macOS permissions**
   - System Preferences > Security & Privacy > Privacy
   - Add Terminal and Python to **Accessibility** permissions  
   - Add Python to **Automation** permissions for Keynote

4. **Configure Claude Desktop**
   Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "keynote": {
         "command": "python3",
         "args": ["/path/to/keynote-mcp/mcp_server.py"]
       }
     }
   }
   ```

5. **Test the server**
   ```bash
   python3 test_server.py
   ```

> **Note**: Make sure Keynote is installed and you have appropriate permissions for automation.

## Available Tools (65 total in prwhite/keynote-mcp, 26 in the section below)

The list below documents the original tool surface from `betancur/keynote-mcp`. The prwhite fork adds an additional ~30 tools under the `KeynoteOps` subpackage — see [What's new in prwhite/keynote-mcp](#-whats-new-in-prwhitekeynote-mcp).

### Presentation Management
- `create_presentation` - Create new presentation
- `open_presentation` - Open existing presentation  
- `save_presentation` - Save presentation
- `close_presentation` - Close presentation

### Slide Operations
- `add_slide` - Add new slide
- `delete_slide` - Delete slide
- `duplicate_slide` - Copy slide
- `move_slide` - Reorder slides

### Content Management
- `add_text_box` - Add text to slide
- `add_image` - Add image to slide
- `set_slide_content` - 🆕 Set content using theme elements (recommended)
- `get_slide_default_elements` - 🆕 Check available theme elements

### Export & Capture
- `screenshot_slide` - Take slide screenshot
- `export_pdf` - Export as PDF

### Theme-Aware Features
Our latest update includes **theme-aware content management** that uses Keynote's built-in design elements for professional-looking presentations with consistent styling.

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](./docs/) directory:

- **[📖 Documentation Index](./docs/README.md)** - Complete documentation overview
- **[🏗️ Modular Architecture](./docs/MODULAR_ARCHITECTURE.md)** - AppleScript modular structure
- **[🎨 Theme-Aware Content](./docs/THEME_AWARE_CONTENT.md)** - Best practices for theme elements
- **[🗺️ Project Roadmap](./docs/ROADMAP.md)** - Future development plans and features

### Quick Links
- **Getting Started**: Follow the Quick Setup section above
- **For Developers**: [Modular Architecture](./docs/MODULAR_ARCHITECTURE.md)
- **Best Practices**: [Theme-Aware Content](./docs/THEME_AWARE_CONTENT.md)

## 💡 Usage Examples

### Theme-Aware Content (Recommended)
```python
# Create new presentation
result = await call_tool("create_presentation", {
    "name": "My Presentation"
})

# Add slide with theme-aware content
result = await call_tool("add_slide", {
    "title": "Welcome", 
    "layout": "Title & Content"
})

# Set content using theme elements (automatic positioning & styling)
result = await call_tool("set_slide_content", {
    "title": "Project Overview",
    "subtitle": "Q4 2024 Results", 
    "bullet_points": ["Revenue up 15%", "New markets entered", "Team expansion"]
})

# Check what theme elements are available
result = await call_tool("get_slide_default_elements", {"slide_number": 1})
```

### Manual Content Placement
```python
# Add text to specific position
result = await call_tool("add_text_box", {
    "text": "Custom positioned text",
    "x": 100,
    "y": 200
})

# Add image with precise placement
result = await call_tool("add_image", {
    "image_path": "/path/to/image.jpg",
    "x": 300,
    "y": 150
})
```

## 🚀 What's New in This Fork

This enhanced version includes significant improvements over the original:

### ✨ **Major Enhancements**
- **🏗️ Modular Architecture**: Split monolithic AppleScript into 5 specialized modules for better maintainability
- **🎨 Theme-Aware Content**: Smart content placement using Keynote's built-in design elements
- **📚 Comprehensive Documentation**: Complete guides in the `docs/` folder
- **🔧 Enhanced Integration**: Improved Python-AppleScript modular execution
- **🌍 Internationalization**: All Chinese comments translated to English

### 🎯 **Key Benefits**
- **Professional Results**: Theme-aware functions create presentations with consistent styling
- **Better Performance**: Modular loading only loads necessary AppleScript code
- **Easier Maintenance**: Specialized files for different functionality areas
- **Developer Friendly**: Complete documentation and architecture guides

## ✨ What's new in prwhite/keynote-mcp

Built on top of `betancur/keynote-mcp` (above), this fork adds a substantial layer of directly-AppleScript-backed tools and infrastructure for production use.

### 🧰 New tool family: `KeynoteOps` (~30 tools)

A subpackage of tools that talks to Keynote via the sdef-published scripting surface (and, in a couple of narrow cases, System Events). Distinct from the higher-level heuristic / orchestration tools above.

- **Reads.** `list_slide_items`, `get_table_info`, `get_table_cell`, `get_cell_range`, `get_item_properties`, `get_shape_text`, `get_text_item_text`, `get_presenter_notes`, `get_slide_properties`, `get_document_state` — ask Keynote what's on a slide and get structured JSON back.
- **Table writes.** `set_cell_value`, `make_table`, `merge_cells`, `unmerge_cells`, `clear_cells`, `sort_table`.
- **Item writes.** `set_item_position`, `set_item_size`, `set_item_rotation`, `set_item_opacity`, `delete_item` — works across all iWork item kinds (table / shape / image / line / group / movie / audio / chart / text item).
- **Item makers.** `make_line`, `make_shape`, `make_movie`, `make_audio_clip`.
- **Text styling.** `set_text_font`, `set_text_size`, `set_text_color` on shape and text-item rich text.
- **Slide writes.** `set_presenter_notes`, `clear_slide`.
- **Playback control.** `start_playback`, `stop_playback`, `show_next`, `show_previous`, `goto_slide`.
- **Escape hatch.** `run_applescript_snippet` for the long tail of things no structured tool covers.

Several Keynote AppleScript limitations are also documented in tool descriptions so an LLM consumer doesn't waste turns trying impossible things — paragraph alignment in shape text, shape fill color, style presets, and font weight via the (removed) `font style` property are all surfaced as known hard limits.

### 🐛 Bug fixes inherited from upstream

- **`move_slide`** was destructive — `move X to slide Y` overwrites slide Y. Fixed with insertion refs (`before slide N` / `after slide N`).
- **`duplicate_slide`** failed silently — `set newSlide to duplicate ...` doesn't bind the variable. Fixed by using `duplicate ... to before/after slide K`.
- **`add_text_box`** was completely broken — a stale `font style` property reference in another handler in the same AppleScript file blocked the whole file from compiling, breaking every handler in it. Fixed.

### 🖥️ Standalone macOS binary

A `make build` target produces an ad-hoc-codesigned ~15 MB Mach-O binary at `dist/keynote-mcp` via PyInstaller (modeled after [ByAxe/keynote-mcp's approach](https://github.com/ByAxe/keynote-mcp)). The binary bundles its own Python interpreter, all dependencies, and the AppleScript helper files — no Python required on the target machine. The bigger reason to use it is macOS permission isolation: the binary gets its own entry in System Settings → Privacy & Security → Automation, named `keynote-mcp`, rather than sharing permission with every Python tool on the machine.

A GitHub Actions workflow (`.github/workflows/build-macos-binary.yml`) builds + signs + smoke-tests the binary on every push to `master`, and on tag pushes (`v*`) attaches the binary to a GitHub Release.

```bash
# Local one-time setup:
make build-venv

# Each build:
make build           # PyInstaller + ad-hoc codesign → dist/keynote-mcp
make register        # claude mcp add of the local binary

# Or grab a pre-built binary from the Releases page on GitHub.
```

### 🔄 Updated for "Keynote Creator Studio"

The Keynote app was renamed to "Keynote Creator Studio.app" with the new bundle identifier `com.apple.Keynote` (was `com.apple.iWork.Keynote`). The fork is verified against the new app; the AppleScript `tell application "Keynote"` target still resolves transparently.

> **Credits**: This fork is based on the original [keynote-mcp](https://github.com/easychen/keynote-mcp) by [@easychen](https://github.com/easychen). We've enhanced it with modern architecture and professional content management features.

## License
MIT License
