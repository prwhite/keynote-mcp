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
