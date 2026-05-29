-- introspection_json.applescript
-- JSON serialization helpers for introspection scripts.
-- Each handler returns a JSON-string fragment. Callers compose fragments
-- via jsonList and jsonRecord. All output is valid JSON when assembled.

on jsonString(s)
    -- Escape a string and wrap in double quotes.
    set sText to s as text
    set out to ""
    repeat with i from 1 to length of sText
        set ch to character i of sText
        if ch is "\"" then
            set out to out & "\\\""
        else if ch is "\\" then
            set out to out & "\\\\"
        else if ch is (ASCII character 10) then
            set out to out & "\\n"
        else if ch is (ASCII character 13) then
            set out to out & "\\r"
        else if ch is (ASCII character 9) then
            set out to out & "\\t"
        else
            set out to out & ch
        end if
    end repeat
    return "\"" & out & "\""
end jsonString

on jsonNumber(n)
    -- Locale-safe formatting: AppleScript's `(n as text)` uses the system
    -- decimal separator (e.g. "," in de_DE locales), which would produce
    -- invalid JSON like `1,5`. Normalize any comma to period.
    set saved to AppleScript's text item delimiters
    set AppleScript's text item delimiters to ","
    set parts to text items of (n as text)
    set AppleScript's text item delimiters to "."
    set out to parts as text
    set AppleScript's text item delimiters to saved
    return out
end jsonNumber

on jsonBool(b)
    if b then
        return "true"
    else
        return "false"
    end if
end jsonBool

on jsonNull()
    return "null"
end jsonNull

on jsonList(theItems)
    -- theItems: list of already-encoded JSON fragments (strings).
    -- (`item` and `items` are reserved in AppleScript — use `theItems`/`itm`.)
    set out to "["
    set isFirst to true
    repeat with itm in theItems
        if isFirst then
            set isFirst to false
        else
            set out to out & ", "
        end if
        set out to out & (itm as text)
    end repeat
    return out & "]"
end jsonList

on jsonRecord(pairs)
    -- pairs: list of {keyString, encodedValueJSON} pairs.
    set out to "{"
    set isFirst to true
    repeat with p in pairs
        if isFirst then
            set isFirst to false
        else
            set out to out & ", "
        end if
        set keyStr to item 1 of p
        set valJson to item 2 of p
        set out to out & my jsonString(keyStr) & ": " & (valJson as text)
    end repeat
    return out & "}"
end jsonRecord

on toIso8601(d)
    -- Convert an AppleScript date to ISO 8601 in local time (no tz suffix).
    set y to year of d as text
    set m to text -2 thru -1 of ("0" & ((month of d as integer) as text))
    set dd to text -2 thru -1 of ("0" & (day of d as text))
    set hh to text -2 thru -1 of ("0" & ((hours of d) as text))
    set mn to text -2 thru -1 of ("0" & ((minutes of d) as text))
    set ss to text -2 thru -1 of ("0" & ((seconds of d) as text))
    return y & "-" & m & "-" & dd & "T" & hh & ":" & mn & ":" & ss
end toIso8601

-- ---------------------------------------------------------------------------
-- Slide resolution (Keynote-aware helper)
-- ---------------------------------------------------------------------------
-- Keynote has two slide-numbering systems that disagree in any deck with
-- hidden/skipped slides:
--   1. `slide N of doc` indexing uses ABSOLUTE positions (counts every slide).
--   2. `slide number of <slide ref>` returns the VISIBLE position (skips hidden).
-- Tools take slide numbers as absolute (system #1). A slideNumber of 0 is a
-- sentinel meaning "the slide currently selected in Keynote" — resolved by
-- this helper via `current slide`, which is reliable regardless of skipped
-- state and survives slide reorders/duplications between read and write.
on resolveSlide(targetDoc, slideNumber)
    tell application "Keynote"
        if slideNumber is 0 or slideNumber is missing value then
            return current slide of targetDoc
        else
            return slide slideNumber of targetDoc
        end if
    end tell
end resolveSlide

-- Resolve a slide number sentinel (0 / missing value) to the absolute index
-- of the slide currently selected in Keynote. Non-sentinel values pass through.
-- Used to echo a meaningful slide_number back to the caller in responses,
-- even when the call targeted "current slide" via the sentinel. O(N) over
-- slide count on sentinel input, O(1) on absolute input.
on resolveSlideNumber(targetDoc, slideNumber)
    if slideNumber is not 0 and slideNumber is not missing value then
        return slideNumber
    end if
    tell application "Keynote"
        set curRef to current slide of targetDoc
        set numSlides to count of slides of targetDoc
        repeat with i from 1 to numSlides
            if slide i of targetDoc is curRef then
                return i
            end if
        end repeat
    end tell
    return 0
end resolveSlideNumber
