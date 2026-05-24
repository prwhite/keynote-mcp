-- introspection_slide_items.applescript
-- Enumerate every iWork item on a slide.
-- Returns a JSON object: {"slide_number": N, "items": [{kind, index, name, position, size}, ...]}
-- Uses handlers from introspection_json.applescript (must be prepended by caller).

on listSlideItems(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc

        -- Per-kind iteration. AppleScript doesn't give polymorphic (kind, index)
        -- enumeration over iWork items, so we enumerate each element class.
        -- collectItems returns a list (AppleScript passes lists by value, so we
        -- can't mutate a caller's accumulator from inside a handler).
        set itemJsonList to {}
        set itemJsonList to itemJsonList & my collectItems("table", tables of targetSlide)
        set itemJsonList to itemJsonList & my collectItems("shape", shapes of targetSlide)
        set itemJsonList to itemJsonList & my collectItems("image", images of targetSlide)
        set itemJsonList to itemJsonList & my collectItems("line", lines of targetSlide)
        set itemJsonList to itemJsonList & my collectItems("group", groups of targetSlide)
        set itemJsonList to itemJsonList & my collectItems("movie", movies of targetSlide)
        set itemJsonList to itemJsonList & my collectItems("audio_clip", audio clips of targetSlide)
        set itemJsonList to itemJsonList & my collectItems("chart", charts of targetSlide)
        set itemJsonList to itemJsonList & my collectItems("text_item", text items of targetSlide)

        return my jsonRecord({{"slide_number", my jsonNumber(slideNumber)}, ¬
                              {"items", my jsonList(itemJsonList)}})
    end tell
end listSlideItems

on collectItems(kindName, itemList)
    -- Returns a list of JSON-encoded item records for the given kind.
    -- Caller concatenates results into the master list.
    tell application "Keynote"
        set acc to {}
        set i to 0
        repeat with itm in itemList
            set i to i + 1
            -- name: only `table` reliably has one; others may error.
            try
                set itmName to name of itm
                set nameJson to my jsonString(itmName)
            on error
                set nameJson to my jsonNull()
            end try
            set pos to position of itm
            set posJson to my jsonList({my jsonNumber(item 1 of pos), my jsonNumber(item 2 of pos)})
            set sizeJson to my jsonList({my jsonNumber(width of itm), my jsonNumber(height of itm)})
            set itemRecord to my jsonRecord({{"kind", my jsonString(kindName)}, ¬
                                             {"index", my jsonNumber(i)}, ¬
                                             {"name", nameJson}, ¬
                                             {"position", posJson}, ¬
                                             {"size", sizeJson}})
            set end of acc to itemRecord
        end repeat
        return acc
    end tell
end collectItems
