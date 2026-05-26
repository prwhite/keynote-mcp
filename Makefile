# Makefile — common keynote-mcp dev shortcuts.
#
# Run `make help` for a colored cheat-sheet. Every target should have a
# `## description` comment so `help` picks it up.

.PHONY: help fixture test test-server inspector build build-venv sign register unregister clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# -----------------------------------------------------------------------------
# Dev loop — fixtures, tests, MCP Inspector
# -----------------------------------------------------------------------------

fixture: ## Regenerate the Keynote test fixture (introspection_fixture.key)
	osascript payton.nogit/fixtures/create_test_fixture.applescript

test: ## Run the KeynoteOps integration test suite (requires Keynote + fixture)
	python3 test_keynote_ops.py

test-server: ## Run the basic server smoke test (no Keynote interaction needed)
	python3 test_server.py

inspector: ## Launch the MCP Inspector against the local mcp_server.py entry point
	npx @modelcontextprotocol/inspector python3 mcp_server.py

# -----------------------------------------------------------------------------
# Standalone macOS binary (production deploy)
# -----------------------------------------------------------------------------

build-venv: ## One-time: create the isolated build venv with runtime + PyInstaller
	python3 -m venv .venv-build
	.venv-build/bin/pip install --upgrade pip
	.venv-build/bin/pip install -r requirements.txt -r requirements-dev.txt
	@echo "Build venv ready at .venv-build. Next: make build"

build: ## Build the standalone macOS binary (dist/keynote-mcp). Re-signs ad-hoc.
	@test -d .venv-build || { echo "No .venv-build yet. Run: make build-venv"; exit 1; }
	.venv-build/bin/pyinstaller --onefile --name keynote-mcp \
	  --add-data "src/applescript:src/applescript" \
	  -y mcp_server.py
	@$(MAKE) --no-print-directory sign

sign: ## Ad-hoc codesign the built binary (gives it its own macOS identity)
	@test -f dist/keynote-mcp || { echo "No dist/keynote-mcp. Run: make build"; exit 1; }
	codesign -s - -f dist/keynote-mcp
	@codesign -dvv dist/keynote-mcp 2>&1 | head -5

register: ## Register the local dist/keynote-mcp binary with Claude Code
	@test -f dist/keynote-mcp || { echo "No dist/keynote-mcp. Run: make build"; exit 1; }
	claude mcp remove keynote 2>/dev/null || true
	claude mcp add keynote -- $(PWD)/dist/keynote-mcp
	@echo "Registered. In a fresh Claude Code session, macOS will prompt for"
	@echo "Automation permission to 'keynote-mcp' on the first tool call."

unregister: ## Remove the keynote MCP from Claude Code
	claude mcp remove keynote

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

clean: ## Remove all build artifacts (binary, intermediate, spec). Keeps the venv.
	rm -rf build/ dist/ keynote-mcp.spec

clean-all: ## Like clean, plus removes the build venv. Forces a full rebuild next time.
	rm -rf build/ dist/ keynote-mcp.spec .venv-build/

# -----------------------------------------------------------------------------
# Releases — tag + push triggers .github/workflows/build-macos-binary.yml
# which builds, signs, smoke-tests, and attaches the binary to the GitHub
# Release for the tag.
# -----------------------------------------------------------------------------

release: ## Tag a new release locally. Usage: make release VERSION=v0.6.0
	@test -n "$(VERSION)" || { echo "Usage: make release VERSION=v0.6.0"; exit 1; }
	@echo "$(VERSION)" | grep -qE '^v[0-9]+\.[0-9]+\.[0-9]+([-+].+)?$$' \
	  || { echo "VERSION must match semver-ish: v<major>.<minor>.<patch>[-suffix]"; exit 1; }
	@test -z "$$(git status --porcelain)" \
	  || { echo "Working tree dirty — commit first"; exit 1; }
	@CURRENT=$$(git symbolic-ref --short HEAD); \
	  test "$$CURRENT" = "master" \
	  || { echo "Tag releases from master only (you're on $$CURRENT)"; exit 1; }
	@! git rev-parse $(VERSION) >/dev/null 2>&1 \
	  || { echo "Tag $(VERSION) already exists"; exit 1; }
	@LAST=$$(git describe --tags --abbrev=0 2>/dev/null); \
	  if [ -n "$$LAST" ]; then \
	    echo ""; echo "Commits since $$LAST:"; \
	    git log --pretty='  - %s' $$LAST..HEAD; \
	  else \
	    echo ""; echo "(No prior tag — this is the first release.)"; \
	  fi
	@echo ""
	@echo "About to create annotated tag $(VERSION) at $$(git rev-parse --short HEAD)."
	@echo "Editor will open for the tag message. Save & exit to create the tag."
	@echo ""
	git tag -a $(VERSION)
	@echo ""
	@echo "Tag $(VERSION) created locally. Next steps:"
	@echo "  git push origin master $(VERSION)    # Push branch + tag, triggers release build (~3-5 min)"
	@echo "  gh release view $(VERSION) --web      # Open the release page once CI publishes it"
	@echo ""
	@echo "Tag message can be reused as release notes:"
	@echo "  git tag -n99 -l $(VERSION) | tail -n +2 | sed 's/^    //' > /tmp/$(VERSION)-notes.md"
	@echo "  gh release edit $(VERSION) --notes-file /tmp/$(VERSION)-notes.md"

release-undo: ## Delete a local tag that hasn't been pushed yet. Usage: make release-undo VERSION=v0.6.0
	@test -n "$(VERSION)" || { echo "Usage: make release-undo VERSION=v0.6.0"; exit 1; }
	@! git ls-remote --tags origin $(VERSION) | grep -q $(VERSION) \
	  || { echo "Tag $(VERSION) is already on origin — delete it via 'git push origin :refs/tags/$(VERSION)' if you really mean it"; exit 1; }
	git tag -d $(VERSION)
