-- introspection_slide_properties.applescript
-- Slide-level property reads: slide metadata and presenter notes.
-- Uses helpers from introspection_json.applescript (must be prepended by caller).

on getSlideProperties(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc

        -- title showing
        try
            set ts to title showing of targetSlide
            if ts is missing value then
                set tsJson to my jsonNull()
            else
                set tsJson to my jsonBool(ts)
            end if
        on error
            set tsJson to my jsonNull()
        end try

        -- body showing
        try
            set bs to body showing of targetSlide
            if bs is missing value then
                set bsJson to my jsonNull()
            else
                set bsJson to my jsonBool(bs)
            end if
        on error
            set bsJson to my jsonNull()
        end try

        -- skipped
        try
            set sk to skipped of targetSlide
            if sk is missing value then
                set skJson to my jsonNull()
            else
                set skJson to my jsonBool(sk)
            end if
        on error
            set skJson to my jsonNull()
        end try

        -- base layout name
        try
            set bl to name of base layout of targetSlide
            if bl is missing value then
                set blJson to my jsonNull()
            else
                set blJson to my jsonString(bl)
            end if
        on error
            set blJson to my jsonNull()
        end try

        -- transition properties
        try
            set tp to transition properties of targetSlide
            try
                set tpAuto to automatic transition of tp
                set tpAutoJson to my jsonBool(tpAuto)
            on error
                set tpAutoJson to my jsonNull()
            end try
            try
                set tpDelay to transition delay of tp
                if tpDelay is missing value then
                    set tpDelayJson to my jsonNull()
                else
                    set tpDelayJson to my jsonNumber(tpDelay)
                end if
            on error
                set tpDelayJson to my jsonNull()
            end try
            try
                set tpDuration to transition duration of tp
                if tpDuration is missing value then
                    set tpDurationJson to my jsonNull()
                else
                    set tpDurationJson to my jsonNumber(tpDuration)
                end if
            on error
                set tpDurationJson to my jsonNull()
            end try
            try
                set tpEffect to transition effect of tp
                if tpEffect is missing value then
                    set tpEffectJson to my jsonNull()
                else
                    set tpEffectJson to my jsonString(tpEffect as text)
                end if
            on error
                set tpEffectJson to my jsonNull()
            end try
            set transitionJson to my jsonRecord({{"automatic", tpAutoJson}, ¬
                                                 {"delay", tpDelayJson}, ¬
                                                 {"duration", tpDurationJson}, ¬
                                                 {"effect", tpEffectJson}})
        on error
            set transitionJson to my jsonNull()
        end try

        return my jsonRecord({{"slide_number", my jsonNumber(slideNumber)}, ¬
                              {"title_showing", tsJson}, ¬
                              {"body_showing", bsJson}, ¬
                              {"skipped", skJson}, ¬
                              {"base_layout", blJson}, ¬
                              {"transition", transitionJson}})
    end tell
end getSlideProperties

on setPresenterNotes(docName, slideNumber, notesText)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        set presenter notes of targetSlide to notesText
        return my jsonRecord({{"slide_number", my jsonNumber(slideNumber)}, ¬
                              {"characters_set", my jsonNumber(length of notesText)}})
    end tell
end setPresenterNotes

on getPresenterNotes(docName, slideNumber)
    -- NOTE: AppleScript coerces rich text to a plain text snapshot when it
    -- crosses handler boundaries, so we can't capture the container in a
    -- variable. Every per-paragraph property read reconstructs the full path
    -- (paragraph pi of presenter notes of slide slideNumber of targetDoc).
    -- See encodeTextContent in introspection_items.applescript for context.
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc

        try
            set topText to (presenter notes of targetSlide) as text
            set paraCount to count of paragraphs of (presenter notes of targetSlide)
        on error
            set topText to ""
            set paraCount to 0
        end try

        set paraList to {}
        repeat with pi from 1 to paraCount
            try
                set pText to (paragraph pi of presenter notes of targetSlide) as text
                set pFontVal to font of paragraph pi of presenter notes of targetSlide
                set pSizeVal to size of paragraph pi of presenter notes of targetSlide
                set pColorVal to color of paragraph pi of presenter notes of targetSlide

                if pFontVal is missing value then
                    set pFontJson to my jsonNull()
                else
                    set pFontJson to my jsonString(pFontVal)
                end if
                if pSizeVal is missing value then
                    set pSizeJson to my jsonNull()
                else
                    set pSizeJson to my jsonNumber(pSizeVal)
                end if
                if pColorVal is missing value then
                    set pColorJson to my jsonNull()
                else
                    set pColorJson to my jsonList({my jsonNumber(item 1 of pColorVal), my jsonNumber(item 2 of pColorVal), my jsonNumber(item 3 of pColorVal)})
                end if

                set paraRecord to my jsonRecord({{"text", my jsonString(pText)}, ¬
                                                {"font", pFontJson}, ¬
                                                {"size", pSizeJson}, ¬
                                                {"color", pColorJson}})
                set end of paraList to paraRecord
            on error
                -- skip this paragraph on error; keep going
            end try
        end repeat

        return my jsonRecord({{"slide_number", my jsonNumber(slideNumber)}, ¬
                              {"text", my jsonString(topText)}, ¬
                              {"paragraphs", my jsonList(paraList)}})
    end tell
end getPresenterNotes


on clearSlide(docName, slideNumber)
    -- Wipes user content from a slide, preserving theme placeholders.
    --
    -- Iterates each iWork-item kind in REVERSE so index shifts don't bite,
    -- and deletes everything. For text items only, applies a heuristic to
    -- preserve theme placeholders: a text item is considered a placeholder
    -- if its position is {0, 0} AND its text is empty. Theme placeholders
    -- on freshly-laid-out slides have these defaults; user-added text items
    -- effectively never sit at {0,0} with no text. Heuristic borrowed from
    -- ByAxe/keynote-mcp's clear_slide (commit 1d4a0cf).
    --
    -- Limitations: a user shape AT position {0,0} with no text would also
    -- be preserved (false negative); a placeholder that's been moved or
    -- typed into is no longer detected (false positive — gets deleted).
    -- Acceptable for "regenerate this slide" workflows.
    --
    -- Implementation note: we compute the deleted count by snapshotting
    -- totals before and after, rather than incrementing inside the tell
    -- block. AppleScript's `set X to ...` inside a `tell` block creates
    -- a tell-local variable that shadows the handler-scope X, so naive
    -- in-loop increments don't propagate out.

    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc

        -- Snapshot totals before clear
        set totalBefore to (count of tables of targetSlide) ¬
                        + (count of shapes of targetSlide) ¬
                        + (count of images of targetSlide) ¬
                        + (count of lines of targetSlide) ¬
                        + (count of groups of targetSlide) ¬
                        + (count of movies of targetSlide) ¬
                        + (count of audio clips of targetSlide) ¬
                        + (count of charts of targetSlide) ¬
                        + (count of text items of targetSlide)

        -- IMPORTANT Keynote AppleScript trap: within a single tell block,
        -- `count of <kind>` returns STALE values after a delete — the
        -- deletion commits but isn't reflected in the next `count` read
        -- until another model-touching op runs. Empirically, a fixed
        -- `repeat with i from (count of shapes) to 1 by -1` only ends up
        -- removing one shape per loop, leaving the rest. The robust
        -- pattern is a `while (count) > 0` loop that always targets the
        -- current last index AND uses a safety cap to avoid infinite
        -- loops if a kind contains undeletable items.
        tell targetSlide
            -- Tables
            set _safety to 0
            repeat while (count of tables) > 0 and _safety < 1000
                try
                    delete table (count of tables)
                end try
                set _safety to _safety + 1
            end repeat
            -- Shapes
            set _safety to 0
            repeat while (count of shapes) > 0 and _safety < 1000
                try
                    delete shape (count of shapes)
                end try
                set _safety to _safety + 1
            end repeat
            -- Images
            set _safety to 0
            repeat while (count of images) > 0 and _safety < 1000
                try
                    delete image (count of images)
                end try
                set _safety to _safety + 1
            end repeat
            -- Lines
            set _safety to 0
            repeat while (count of lines) > 0 and _safety < 1000
                try
                    delete line (count of lines)
                end try
                set _safety to _safety + 1
            end repeat
            -- Groups
            set _safety to 0
            repeat while (count of groups) > 0 and _safety < 1000
                try
                    delete group (count of groups)
                end try
                set _safety to _safety + 1
            end repeat
            -- Movies
            set _safety to 0
            repeat while (count of movies) > 0 and _safety < 1000
                try
                    delete movie (count of movies)
                end try
                set _safety to _safety + 1
            end repeat
            -- Audio clips
            set _safety to 0
            repeat while (count of audio clips) > 0 and _safety < 1000
                try
                    delete audio clip (count of audio clips)
                end try
                set _safety to _safety + 1
            end repeat
            -- Charts
            set _safety to 0
            repeat while (count of charts) > 0 and _safety < 1000
                try
                    delete chart (count of charts)
                end try
                set _safety to _safety + 1
            end repeat
            -- Text items — placeholder-aware. Iterate from the top index
            -- down, skipping placeholders. Use a fixed-index loop here
            -- because we skip some items rather than deleting all — the
            -- `while > 0` pattern would loop forever on a slide containing
            -- only placeholders. Index shifts only matter as we delete,
            -- and we always delete from highest index downward, so a
            -- snapshot of the initial count is fine for the iteration
            -- range; we just re-check the current count inside before
            -- accessing to avoid OOB reads.
            set _initialTextCount to count of text items
            repeat with i from _initialTextCount to 1 by -1
                if i ≤ (count of text items) then
                    try
                        set ti to text item i
                        set pos to position of ti
                        set txt to (object text of ti) as text
                        set isPlaceholder to ((item 1 of pos) is 0 and (item 2 of pos) is 0 and txt is "")
                        if not isPlaceholder then
                            delete ti
                        end if
                    end try
                end if
            end repeat
        end tell

        -- Snapshot totals after clear
        set totalAfter to (count of tables of targetSlide) ¬
                       + (count of shapes of targetSlide) ¬
                       + (count of images of targetSlide) ¬
                       + (count of lines of targetSlide) ¬
                       + (count of groups of targetSlide) ¬
                       + (count of movies of targetSlide) ¬
                       + (count of audio clips of targetSlide) ¬
                       + (count of charts of targetSlide) ¬
                       + (count of text items of targetSlide)
    end tell

    return my jsonRecord({{"slide_number", my jsonNumber(slideNumber)}, {"items_deleted", my jsonNumber(totalBefore - totalAfter)}})
end clearSlide
