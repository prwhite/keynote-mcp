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
