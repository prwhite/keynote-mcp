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
