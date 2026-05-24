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

on encodeTextContent(textContainer, kindName, idx)
    -- Shared helper: encode a rich text container into {"kind","index","text","paragraphs"}.
    -- textContainer: the object text value (may be empty or missing value).
    -- kindName: e.g. "shape", "text_item"
    -- idx: integer index
    tell application "Keynote"
        -- Coerce to text for the top-level string
        if textContainer is missing value then
            set topText to ""
        else
            try
                set topText to textContainer as text
            on error
                set topText to ""
            end try
        end if

        -- Paragraphs
        set paraList to {}
        if textContainer is not missing value then
            try
                set paraCount to count of paragraphs of textContainer
                repeat with pi from 1 to paraCount
                    set p to paragraph pi of textContainer
                    set pText to p as text

                    -- font
                    try
                        set pFont to font of p
                        if pFont is missing value then
                            set pFontJson to my jsonNull()
                        else
                            set pFontJson to my jsonString(pFont)
                        end if
                    on error
                        set pFontJson to my jsonNull()
                    end try

                    -- size
                    try
                        set pSize to size of p
                        if pSize is missing value then
                            set pSizeJson to my jsonNull()
                        else
                            set pSizeJson to my jsonNumber(pSize)
                        end if
                    on error
                        set pSizeJson to my jsonNull()
                    end try

                    -- color (16-bit RGB list)
                    try
                        set pColor to color of p
                        if pColor is missing value then
                            set pColorJson to my jsonNull()
                        else
                            set pColorJson to my jsonList({my jsonNumber(item 1 of pColor), my jsonNumber(item 2 of pColor), my jsonNumber(item 3 of pColor)})
                        end if
                    on error
                        set pColorJson to my jsonNull()
                    end try

                    set paraRecord to my jsonRecord({{"text", my jsonString(pText)}, ¬
                                                    {"font", pFontJson}, ¬
                                                    {"size", pSizeJson}, ¬
                                                    {"color", pColorJson}})
                    set end of paraList to paraRecord
                end repeat
            on error
                -- paragraphs unavailable; leave paraList empty
            end try
        end if

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
        try
            set ot to object text of sh
        on error
            set ot to missing value
        end try
        return my encodeTextContent(ot, "shape", shapeIndex)
    end tell
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
        try
            set ot to object text of ti
        on error
            set ot to missing value
        end try
        return my encodeTextContent(ot, "text_item", textItemIndex)
    end tell
end getTextItemText
