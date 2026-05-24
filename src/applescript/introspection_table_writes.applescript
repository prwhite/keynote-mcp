-- introspection_table_writes.applescript
-- Table write handlers: set_cell_value, make_table, merge_cells, unmerge_cells,
-- clear_cells, sort_table.
-- Uses helpers from introspection_json.applescript (must be prepended by caller).

on setCellValue(docName, slideNumber, tableIndex, cellAddress, valueText)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        set t to table tableIndex of targetSlide
        set value of cell cellAddress of t to valueText
    end tell
    set pairs to {{"address", my jsonString(cellAddress)}, ¬
                  {"set_to", my jsonString(valueText)}}
    return my jsonRecord(pairs)
end setCellValue

on makeTable(docName, slideNumber, numRows, numCols, posX, posY, w, h, theName, headerRows)
    -- NOTE: "row count" and "column count" cannot be used in a `with properties` record
    -- inside a handler (AppleScript interprets `rows` as a keyword). Instead, we create
    -- the table with Keynote's defaults (5 rows x 4 cols) and then delete or add rows/cols.
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc

        -- Count existing tables before creation
        set tablesBefore to count of tables of targetSlide

        -- Create the table with position/size only (row count in properties
        -- causes a Keynote scripting error inside handlers)
        tell targetSlide
            set newTable to make new table with properties {position:{posX, posY}, width:w, height:h}
        end tell

        -- Trim rows to numRows (default Keynote creates 5 rows)
        repeat while (row count of newTable) > numRows
            delete row (row count of newTable) of newTable
        end repeat
        -- Add rows if numRows > default
        repeat while (row count of newTable) < numRows
            set lastRowIdx to row count of newTable
            tell newTable
                make new row at after row lastRowIdx of newTable
            end tell
        end repeat

        -- Trim columns to numCols (default Keynote creates 4 cols)
        repeat while (column count of newTable) > numCols
            delete column (column count of newTable) of newTable
        end repeat
        -- Add columns if numCols > default
        repeat while (column count of newTable) < numCols
            set lastColIdx to column count of newTable
            tell newTable
                make new column at after column lastColIdx of newTable
            end tell
        end repeat

        -- Apply name if non-empty
        if theName is not "" then
            set name of newTable to theName
        end if

        -- Apply header row count if > 0
        if headerRows > 0 then
            set header row count of newTable to headerRows
        end if

        -- The new table's per-kind index is tablesBefore + 1
        set newIndex to tablesBefore + 1

        -- Retrieve name for confirmation
        try
            set confirmedName to name of newTable
        on error
            set confirmedName to ""
        end try
    end tell
    set pairs to {{"slide_number", my jsonNumber(slideNumber)}, ¬
                  {"table_index", my jsonNumber(newIndex)}, ¬
                  {"name", my jsonString(confirmedName)}}
    return my jsonRecord(pairs)
end makeTable

on mergeCells(docName, slideNumber, tableIndex, rangeAddress)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        set t to table tableIndex of targetSlide
        merge range rangeAddress of t
    end tell
    set pairs to {{"merged", my jsonString(rangeAddress)}}
    return my jsonRecord(pairs)
end mergeCells

on unmergeCells(docName, slideNumber, tableIndex, rangeAddress)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        set t to table tableIndex of targetSlide
        unmerge range rangeAddress of t
    end tell
    set pairs to {{"unmerged", my jsonString(rangeAddress)}}
    return my jsonRecord(pairs)
end unmergeCells

on clearCells(docName, slideNumber, tableIndex, rangeAddress)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        set t to table tableIndex of targetSlide
        clear range rangeAddress of t
    end tell
    set pairs to {{"cleared", my jsonString(rangeAddress)}}
    return my jsonRecord(pairs)
end clearCells

on sortTable(docName, slideNumber, tableIndex, byColumn, direction)
    -- NOTE: The sort command's "by" parameter requires a column *object*, not an integer.
    -- Use `column byColumn of t` to get the object reference.
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to slide slideNumber of targetDoc
        set t to table tableIndex of targetSlide
        if direction is "ascending" then
            sort t by column byColumn of t direction ascending
        else
            sort t by column byColumn of t direction descending
        end if
    end tell
    set pairs to {{"sorted", my jsonBool(true)}, ¬
                  {"by_column", my jsonNumber(byColumn)}, ¬
                  {"direction", my jsonString(direction)}}
    return my jsonRecord(pairs)
end sortTable
