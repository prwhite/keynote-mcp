-- introspection_items.applescript
-- Per-item property reads and shape/text-item text extraction.
-- Uses helpers from introspection_json.applescript (must be prepended by caller).

on getItemProperties(docName, slideNumber, itemKind, itemIndex)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc

        -- Dispatch to the right element class
        set itm to missing value
        if itemKind is "table" then
            try
                set itm to table itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("table index out of range")}})
            end try
        else if itemKind is "shape" then
            try
                set itm to shape itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("shape index out of range")}})
            end try
        else if itemKind is "image" then
            try
                set itm to image itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("image index out of range")}})
            end try
        else if itemKind is "line" then
            try
                set itm to line itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("line index out of range")}})
            end try
        else if itemKind is "group" then
            try
                set itm to group itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("group index out of range")}})
            end try
        else if itemKind is "movie" then
            try
                set itm to movie itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("movie index out of range")}})
            end try
        else if itemKind is "audio_clip" then
            try
                set itm to audio clip itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("audio_clip index out of range")}})
            end try
        else if itemKind is "chart" then
            try
                set itm to chart itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("chart index out of range")}})
            end try
        else if itemKind is "text_item" then
            try
                set itm to text item itemIndex of targetSlide
            on error
                return my jsonRecord({{"error", my jsonString("text_item index out of range")}})
            end try
        else
            return my jsonRecord({{"error", my jsonString("unknown item_kind: " & itemKind)}})
        end if

        -- Read position
        try
            set pos to position of itm
            set posJson to my jsonList({my jsonNumber(item 1 of pos), my jsonNumber(item 2 of pos)})
        on error
            set posJson to my jsonNull()
        end try

        -- Read size (width, height)
        try
            set w to width of itm
            set h to height of itm
            set sizeJson to my jsonList({my jsonNumber(w), my jsonNumber(h)})
        on error
            set sizeJson to my jsonNull()
        end try

        -- Read rotation
        try
            set rot to rotation of itm
            if rot is missing value then
                set rotJson to my jsonNull()
            else
                set rotJson to my jsonNumber(rot)
            end if
        on error
            set rotJson to my jsonNull()
        end try

        -- Read locked
        try
            set lk to locked of itm
            if lk is missing value then
                set lockedJson to my jsonNull()
            else
                set lockedJson to my jsonBool(lk)
            end if
        on error
            set lockedJson to my jsonNull()
        end try

        -- Read opacity
        try
            set op to opacity of itm
            if op is missing value then
                set opacityJson to my jsonNull()
            else
                set opacityJson to my jsonNumber(op)
            end if
        on error
            set opacityJson to my jsonNull()
        end try

        -- Read reflection showing
        try
            set rs to reflection showing of itm
            if rs is missing value then
                set reflShowJson to my jsonNull()
            else
                set reflShowJson to my jsonBool(rs)
            end if
        on error
            set reflShowJson to my jsonNull()
        end try

        -- Read reflection value
        try
            set rv to reflection value of itm
            if rv is missing value then
                set reflValJson to my jsonNull()
            else
                set reflValJson to my jsonNumber(rv)
            end if
        on error
            set reflValJson to my jsonNull()
        end try

        -- Read parent kind
        try
            set parentKindJson to my jsonString(class of (parent of itm) as text)
        on error
            set parentKindJson to my jsonNull()
        end try

        return my jsonRecord({{"kind", my jsonString(itemKind)}, ¬
                              {"index", my jsonNumber(itemIndex)}, ¬
                              {"position", posJson}, ¬
                              {"size", sizeJson}, ¬
                              {"rotation", rotJson}, ¬
                              {"locked", lockedJson}, ¬
                              {"opacity", opacityJson}, ¬
                              {"reflection_showing", reflShowJson}, ¬
                              {"reflection_value", reflValJson}, ¬
                              {"parent_kind", parentKindJson}})
    end tell
end getItemProperties

on encodeTextContent(docName, slideNumber, kindName, idx)
    -- Encode a rich text container into {"kind","index","text","paragraphs"}.
    -- Takes RESOLUTION PARAMETERS rather than a rich-text reference because
    -- AppleScript silently coerces a rich-text container to a plain text
    -- snapshot when it crosses a handler boundary (even with `a reference to`
    -- — only the parent path survives, not the rich-text "live" semantics).
    -- So this handler reconstructs the full access path locally for every
    -- property read. The leaf properties (font/size/color) ARE primitive
    -- values that pass through handlers cleanly — the snapshot issue is
    -- specific to the rich-text container itself.
    --
    -- kindName ∈ {"shape", "text_item"} — slide presenter notes are handled
    -- by getPresenterNotes inline, since they have a different JSON shape.
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc

        -- Top text + paragraph count, via full path
        try
            if kindName is "shape" then
                set topText to (object text of shape idx of targetSlide) as text
                set paraCount to count of paragraphs of (object text of shape idx of targetSlide)
            else if kindName is "text_item" then
                set topText to (object text of text item idx of targetSlide) as text
                set paraCount to count of paragraphs of (object text of text item idx of targetSlide)
            else
                set topText to ""
                set paraCount to 0
            end if
        on error
            set topText to ""
            set paraCount to 0
        end try

        set paraList to {}
        repeat with pi from 1 to paraCount
            try
                if kindName is "shape" then
                    set pText to (paragraph pi of object text of shape idx of targetSlide) as text
                    set pFontVal to font of paragraph pi of object text of shape idx of targetSlide
                    set pSizeVal to size of paragraph pi of object text of shape idx of targetSlide
                    set pColorVal to color of paragraph pi of object text of shape idx of targetSlide
                else if kindName is "text_item" then
                    set pText to (paragraph pi of object text of text item idx of targetSlide) as text
                    set pFontVal to font of paragraph pi of object text of text item idx of targetSlide
                    set pSizeVal to size of paragraph pi of object text of text item idx of targetSlide
                    set pColorVal to color of paragraph pi of object text of text item idx of targetSlide
                else
                    set pText to ""
                    set pFontVal to missing value
                    set pSizeVal to missing value
                    set pColorVal to missing value
                end if

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
                -- skip this paragraph if anything goes wrong; keep going
            end try
        end repeat

        return my jsonRecord({{"kind", my jsonString(kindName)}, ¬
                              {"index", my jsonNumber(idx)}, ¬
                              {"text", my jsonString(topText)}, ¬
                              {"paragraphs", my jsonList(paraList)}})
    end tell
end encodeTextContent

on getShapeText(docName, slideNumber, shapeIndex)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        try
            set sh to shape shapeIndex of targetSlide
        on error
            return my jsonRecord({{"error", my jsonString("shape index out of range")}})
        end try
    end tell
    -- encodeTextContent reconstructs the full path locally — see its header
    -- for why we don't pass the rich-text container directly.
    return my encodeTextContent(docName, slideNumber, "shape", shapeIndex)
end getShapeText

on getTextItemText(docName, slideNumber, textItemIndex)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        try
            set ti to text item textItemIndex of targetSlide
        on error
            return my jsonRecord({{"error", my jsonString("text_item index out of range")}})
        end try
    end tell
    return my encodeTextContent(docName, slideNumber, "text_item", textItemIndex)
end getTextItemText


on setTextFont(docName, slideNumber, itemKind, itemIndex, fontName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        try
            if itemKind is "shape" then
                set itm to shape itemIndex of targetSlide
            else if itemKind is "text_item" then
                set itm to text item itemIndex of targetSlide
            else
                return my jsonRecord({{"error", my jsonString("set_text_font supports item_kind=shape or text_item; got: " & itemKind)}})
            end if
            set font of object text of itm to fontName
            return my jsonRecord({{"item_kind", my jsonString(itemKind)}, {"item_index", my jsonNumber(itemIndex)}, {"font", my jsonString(fontName)}})
        on error errMsg
            return my jsonRecord({{"error", my jsonString("setTextFont failed: " & errMsg)}})
        end try
    end tell
end setTextFont

on setTextSize(docName, slideNumber, itemKind, itemIndex, fontSize)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        try
            if itemKind is "shape" then
                set itm to shape itemIndex of targetSlide
            else if itemKind is "text_item" then
                set itm to text item itemIndex of targetSlide
            else
                return my jsonRecord({{"error", my jsonString("set_text_size supports item_kind=shape or text_item; got: " & itemKind)}})
            end if
            set size of object text of itm to fontSize
            return my jsonRecord({{"item_kind", my jsonString(itemKind)}, {"item_index", my jsonNumber(itemIndex)}, {"size", my jsonNumber(fontSize)}})
        on error errMsg
            return my jsonRecord({{"error", my jsonString("setTextSize failed: " & errMsg)}})
        end try
    end tell
end setTextSize

on setTextColor(docName, slideNumber, itemKind, itemIndex, r, g, b)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        try
            if itemKind is "shape" then
                set itm to shape itemIndex of targetSlide
            else if itemKind is "text_item" then
                set itm to text item itemIndex of targetSlide
            else
                return my jsonRecord({{"error", my jsonString("set_text_color supports item_kind=shape or text_item; got: " & itemKind)}})
            end if
            set color of object text of itm to {r, g, b}
            return my jsonRecord({{"item_kind", my jsonString(itemKind)}, {"item_index", my jsonNumber(itemIndex)}, {"color", my jsonList({my jsonNumber(r), my jsonNumber(g), my jsonNumber(b)})}})
        on error errMsg
            return my jsonRecord({{"error", my jsonString("setTextColor failed: " & errMsg)}})
        end try
    end tell
end setTextColor
