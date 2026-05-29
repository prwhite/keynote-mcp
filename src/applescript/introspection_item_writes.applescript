-- introspection_item_writes.applescript
-- Item write handlers: set_item_position, set_item_size, set_item_rotation, delete_item,
-- make_line, make_shape, make_movie, make_audio_clip.
-- Uses helpers from introspection_json.applescript (must be prepended by caller).

-- ---------------------------------------------------------------------------
-- Shared helper: resolve item by kind and index
-- Returns the item object, or missing value on error (caller checks).
-- ---------------------------------------------------------------------------

on resolveItem(targetSlide, itemKind, itemIndex)
    tell application "Keynote"
        if itemKind is "table" then
            try
                return table itemIndex of targetSlide
            on error
                return missing value
            end try
        else if itemKind is "shape" then
            try
                return shape itemIndex of targetSlide
            on error
                return missing value
            end try
        else if itemKind is "image" then
            try
                return image itemIndex of targetSlide
            on error
                return missing value
            end try
        else if itemKind is "line" then
            try
                return line itemIndex of targetSlide
            on error
                return missing value
            end try
        else if itemKind is "group" then
            try
                return group itemIndex of targetSlide
            on error
                return missing value
            end try
        else if itemKind is "movie" then
            try
                return movie itemIndex of targetSlide
            on error
                return missing value
            end try
        else if itemKind is "audio_clip" then
            try
                return audio clip itemIndex of targetSlide
            on error
                return missing value
            end try
        else if itemKind is "chart" then
            try
                return chart itemIndex of targetSlide
            on error
                return missing value
            end try
        else if itemKind is "text_item" then
            try
                return text item itemIndex of targetSlide
            on error
                return missing value
            end try
        else
            return missing value
        end if
    end tell
end resolveItem

-- ---------------------------------------------------------------------------
-- C1. setItemPosition
-- ---------------------------------------------------------------------------

on setItemPosition(docName, slideNumber, itemKind, itemIndex, posX, posY)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)
    end tell

    set itm to my resolveItem(targetSlide, itemKind, itemIndex)
    if itm is missing value then
        return my jsonRecord({{"error", my jsonString(itemKind & " index out of range or unknown kind")}})
    end if

    tell application "Keynote"
        try
            set position of itm to {posX, posY}
        on error errMsg
            return my jsonRecord({{"error", my jsonString("set position failed: " & errMsg)}})
        end try
    end tell

    set pairs to {{"position", my jsonList({my jsonNumber(posX), my jsonNumber(posY)})}}
    return my jsonRecord(pairs)
end setItemPosition

-- ---------------------------------------------------------------------------
-- C2. setItemSize
-- ---------------------------------------------------------------------------

on setItemSize(docName, slideNumber, itemKind, itemIndex, w, h)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)
    end tell

    set itm to my resolveItem(targetSlide, itemKind, itemIndex)
    if itm is missing value then
        return my jsonRecord({{"error", my jsonString(itemKind & " index out of range or unknown kind")}})
    end if

    tell application "Keynote"
        try
            set width of itm to w
            set height of itm to h
        on error errMsg
            return my jsonRecord({{"error", my jsonString("set size failed: " & errMsg)}})
        end try
    end tell

    set pairs to {{"size", my jsonList({my jsonNumber(w), my jsonNumber(h)})}}
    return my jsonRecord(pairs)
end setItemSize

-- ---------------------------------------------------------------------------
-- C3. setItemRotation
-- ---------------------------------------------------------------------------

on setItemRotation(docName, slideNumber, itemKind, itemIndex, degrees)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)
    end tell

    set itm to my resolveItem(targetSlide, itemKind, itemIndex)
    if itm is missing value then
        return my jsonRecord({{"error", my jsonString(itemKind & " index out of range or unknown kind")}})
    end if

    tell application "Keynote"
        try
            set rotation of itm to degrees
        on error errMsg
            return my jsonRecord({{"error", my jsonString("set rotation failed: " & errMsg)}})
        end try
    end tell

    set pairs to {{"rotation", my jsonNumber(degrees)}}
    return my jsonRecord(pairs)
end setItemRotation

-- ---------------------------------------------------------------------------
-- C4. deleteItem
-- ---------------------------------------------------------------------------

on deleteItem(docName, slideNumber, itemKind, itemIndex)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)
    end tell

    set itm to my resolveItem(targetSlide, itemKind, itemIndex)
    if itm is missing value then
        return my jsonRecord({{"error", my jsonString(itemKind & " index out of range or unknown kind")}})
    end if

    tell application "Keynote"
        try
            delete itm
        on error errMsg
            return my jsonRecord({{"error", my jsonString("delete failed: " & errMsg)}})
        end try
    end tell

    set deletedRecord to my jsonRecord({{"kind", my jsonString(itemKind)}, {"index", my jsonNumber(itemIndex)}})
    return my jsonRecord({{"deleted", deletedRecord}})
end deleteItem

-- ---------------------------------------------------------------------------
-- C5. makeLine
-- ---------------------------------------------------------------------------

on makeLine(docName, slideNumber, startX, startY, endX, endY)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)

        -- Count existing lines before creation
        set linesBefore to count of lines of targetSlide

        tell targetSlide
            try
                make new line with properties {start point:{startX, startY}, end point:{endX, endY}}
            on error errMsg
                return my jsonRecord({{"error", my jsonString("make line failed: " & errMsg)}})
            end try
        end tell

        set newIndex to linesBefore + 1
    end tell

    set pairs to {{"slide_number", my jsonNumber(my resolveSlideNumber(targetDoc, slideNumber))}, ¬
                  {"kind", my jsonString("line")}, ¬
                  {"index", my jsonNumber(newIndex)}}
    return my jsonRecord(pairs)
end makeLine

-- ---------------------------------------------------------------------------
-- C6. makeShape
-- ---------------------------------------------------------------------------

on makeShape(docName, slideNumber, posX, posY, w, h)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)

        -- Count existing shapes before creation
        set shapesBefore to count of shapes of targetSlide

        tell targetSlide
            try
                make new shape with properties {position:{posX, posY}, width:w, height:h}
            on error errMsg
                return my jsonRecord({{"error", my jsonString("make shape failed: " & errMsg)}})
            end try
        end tell

        set newIndex to shapesBefore + 1
    end tell

    set pairs to {{"slide_number", my jsonNumber(my resolveSlideNumber(targetDoc, slideNumber))}, ¬
                  {"kind", my jsonString("shape")}, ¬
                  {"index", my jsonNumber(newIndex)}}
    return my jsonRecord(pairs)
end makeShape

-- ---------------------------------------------------------------------------
-- C7. makeMovie
-- ---------------------------------------------------------------------------

on makeMovie(docName, slideNumber, filePath, posX, posY, w, h)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)

        -- Count existing movies before creation
        set moviesBefore to count of movies of targetSlide

        tell targetSlide
            try
                make new movie with properties {file name:filePath, position:{posX, posY}, width:w, height:h}
            on error errMsg
                return my jsonRecord({{"error", my jsonString("make movie failed: " & errMsg)}})
            end try
        end tell

        set newIndex to moviesBefore + 1
    end tell

    set pairs to {{"slide_number", my jsonNumber(my resolveSlideNumber(targetDoc, slideNumber))}, ¬
                  {"kind", my jsonString("movie")}, ¬
                  {"index", my jsonNumber(newIndex)}}
    return my jsonRecord(pairs)
end makeMovie

-- ---------------------------------------------------------------------------
-- C8. makeAudioClip
-- ---------------------------------------------------------------------------

on makeAudioClip(docName, slideNumber, filePath)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)

        -- Count existing audio clips before creation
        set clipsBefore to count of audio clips of targetSlide

        tell targetSlide
            try
                make new audio clip with properties {file name:filePath}
            on error errMsg
                return my jsonRecord({{"error", my jsonString("make audio clip failed: " & errMsg)}})
            end try
        end tell

        set newIndex to clipsBefore + 1
    end tell

    set pairs to {{"slide_number", my jsonNumber(my resolveSlideNumber(targetDoc, slideNumber))}, ¬
                  {"kind", my jsonString("audio_clip")}, ¬
                  {"index", my jsonNumber(newIndex)}}
    return my jsonRecord(pairs)
end makeAudioClip


on setItemOpacity(docName, slideNumber, itemKind, itemIndex, opacityPct)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set targetSlide to my resolveSlide(targetDoc, slideNumber)
    end tell

    set itm to my resolveItem(targetSlide, itemKind, itemIndex)
    if itm is missing value then
        return my jsonRecord({{"error", my jsonString(itemKind & " index out of range or unknown kind")}})
    end if

    tell application "Keynote"
        try
            set opacity of itm to opacityPct
        on error errMsg
            return my jsonRecord({{"error", my jsonString("set opacity failed: " & errMsg)}})
        end try
    end tell

    set pairs to {{"opacity", my jsonNumber(opacityPct)}}
    return my jsonRecord(pairs)
end setItemOpacity
