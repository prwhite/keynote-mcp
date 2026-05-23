-- introspection_tables.applescript
-- Table and cell introspection handlers.
-- Uses helpers from introspection_json.applescript (must be prepended by caller).

on getTableInfo(docName, slideNumber, tableIndex, includeCells)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        set t to table tableIndex of targetSlide

        try
            set tName to name of t
            set nameJson to my jsonString(tName)
        on error
            set nameJson to my jsonNull()
        end try

        set rc to row count of t
        set cc to column count of t

        set pairs to {{"slide_number", my jsonNumber(slideNumber)}, ¬
                      {"table_index", my jsonNumber(tableIndex)}, ¬
                      {"name", nameJson}, ¬
                      {"row_count", my jsonNumber(rc)}, ¬
                      {"column_count", my jsonNumber(cc)}, ¬
                      {"header_row_count", my jsonNumber(header row count of t)}, ¬
                      {"header_column_count", my jsonNumber(header column count of t)}, ¬
                      {"footer_row_count", my jsonNumber(footer row count of t)}}

        if includeCells then
            set rowList to {}
            repeat with r from 1 to rc
                set colList to {}
                repeat with c from 1 to cc
                    set theCell to cell c of row r of t
                    set end of colList to my encodeCellBasic(theCell)
                end repeat
                set end of rowList to my jsonList(colList)
            end repeat
            set end of pairs to {"cells", my jsonList(rowList)}
        end if

        return my jsonRecord(pairs)
    end tell
end getTableInfo

on encodeCellBasic(c)
    -- Basic cell encoding: address, value (typed envelope), formatted_value, formula.
    -- No per-cell styling. Per-cell styling is in encodeCellFull (Task 8).
    tell application "Keynote"
        set addrJson to my jsonString(name of c)

        try
            set fv to formatted value of c
            if fv is missing value then
                set fvJson to my jsonNull()
            else
                set fvJson to my jsonString(fv)
            end if
        on error
            set fvJson to my jsonNull()
        end try

        try
            set fm to formula of c
            if fm is missing value then
                set fmJson to my jsonNull()
            else
                set fmJson to my jsonString(fm)
            end if
        on error
            set fmJson to my jsonNull()
        end try

        set v to value of c
        set valJson to my encodeValue(v)

        return my jsonRecord({{"address", addrJson}, ¬
                              {"value", valJson}, ¬
                              {"formatted_value", fvJson}, ¬
                              {"formula", fmJson}})
    end tell
end encodeCellBasic

on encodeValue(v)
    -- Tagged envelope: {"type": "...", "value": ...}
    if v is missing value then
        return my jsonRecord({{"type", my jsonString("empty")}, {"value", my jsonNull()}})
    end if
    set k to class of v
    if k is integer or k is real then
        return my jsonRecord({{"type", my jsonString("number")}, {"value", my jsonNumber(v)}})
    else if k is boolean then
        return my jsonRecord({{"type", my jsonString("boolean")}, {"value", my jsonBool(v)}})
    else if k is date then
        return my jsonRecord({{"type", my jsonString("date")}, {"value", my jsonString(my toIso8601(v))}})
    else
        -- text or anything coerce-able to text
        return my jsonRecord({{"type", my jsonString("text")}, {"value", my jsonString(v as text)}})
    end if
end encodeValue

on getTableCell(docName, slideNumber, tableIndex, cellAddress)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        set t to table tableIndex of targetSlide
        set theCell to cell cellAddress of t
        return my encodeCellFull(theCell)
    end tell
end getTableCell

on encodeCellFull(c)
    -- Full cell encoding with per-cell styling.
    tell application "Keynote"
        set addrJson to my jsonString(name of c)
        set rowAddr to address of (row of c)
        set colAddr to address of (column of c)

        try
            set fv to formatted value of c
            if fv is missing value then
                set fvJson to my jsonNull()
            else
                set fvJson to my jsonString(fv)
            end if
        on error
            set fvJson to my jsonNull()
        end try

        try
            set fm to formula of c
            if fm is missing value then
                set fmJson to my jsonNull()
            else
                set fmJson to my jsonString(fm)
            end if
        on error
            set fmJson to my jsonNull()
        end try

        set v to value of c
        set valJson to my encodeValue(v)

        -- Styling
        try
            set fn to font name of c
            if fn is missing value then
                set fnJson to my jsonNull()
            else
                set fnJson to my jsonString(fn)
            end if
        on error
            set fnJson to my jsonNull()
        end try

        try
            set fs to font size of c
            if fs is missing value then
                set fsJson to my jsonNull()
            else
                set fsJson to my jsonNumber(fs)
            end if
        on error
            set fsJson to my jsonNull()
        end try

        try
            set al to alignment of c
            if al is missing value then
                set alignJson to my jsonNull()
            else
                set alignJson to my jsonString(al as text)
            end if
        on error
            set alignJson to my jsonNull()
        end try

        try
            set va to vertical alignment of c
            if va is missing value then
                set vAlignJson to my jsonNull()
            else
                set vAlignJson to my jsonString(va as text)
            end if
        on error
            set vAlignJson to my jsonNull()
        end try

        -- text_color: required to be a 3-element list; default to [0,0,0] if unavailable
        try
            set tc to text color of c
            if tc is missing value then
                set tcJson to my jsonList({my jsonNumber(0), my jsonNumber(0), my jsonNumber(0)})
            else
                set tcJson to my jsonList({my jsonNumber(item 1 of tc), my jsonNumber(item 2 of tc), my jsonNumber(item 3 of tc)})
            end if
        on error
            set tcJson to my jsonList({my jsonNumber(0), my jsonNumber(0), my jsonNumber(0)})
        end try

        -- background_color: required to be a 3-element list; default to [65535,65535,65535] (white) if unavailable
        try
            set bc to background color of c
            if bc is missing value then
                set bcJson to my jsonList({my jsonNumber(65535), my jsonNumber(65535), my jsonNumber(65535)})
            else
                set bcJson to my jsonList({my jsonNumber(item 1 of bc), my jsonNumber(item 2 of bc), my jsonNumber(item 3 of bc)})
            end if
        on error
            set bcJson to my jsonList({my jsonNumber(65535), my jsonNumber(65535), my jsonNumber(65535)})
        end try

        -- text_wrap: required to be a bool; default to true if unavailable
        try
            set tw to text wrap of c
            if tw is missing value then
                set wrapJson to my jsonBool(true)
            else
                set wrapJson to my jsonBool(tw)
            end if
        on error
            set wrapJson to my jsonBool(true)
        end try

        return my jsonRecord({{"address", addrJson}, ¬
                              {"row", my jsonNumber(rowAddr)}, ¬
                              {"column", my jsonNumber(colAddr)}, ¬
                              {"value", valJson}, ¬
                              {"formatted_value", fvJson}, ¬
                              {"formula", fmJson}, ¬
                              {"font_name", fnJson}, ¬
                              {"font_size", fsJson}, ¬
                              {"alignment", alignJson}, ¬
                              {"vertical_alignment", vAlignJson}, ¬
                              {"text_color", tcJson}, ¬
                              {"background_color", bcJson}, ¬
                              {"text_wrap", wrapJson}})
    end tell
end encodeCellFull
