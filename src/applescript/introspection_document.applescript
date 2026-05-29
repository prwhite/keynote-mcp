-- introspection_document.applescript
-- Document-level state reads.
-- Uses helpers from introspection_json.applescript (must be prepended by caller).

on getDocumentState(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if

        -- name
        try
            set docNameVal to name of targetDoc
            set nameJson to my jsonString(docNameVal)
        on error
            set nameJson to my jsonNull()
        end try

        -- current_slide (absolute index — what slide_number params accept).
        -- IMPORTANT: `slide number of <slide ref>` returns the VISIBLE index
        -- (skips hidden slides). Writes use the ABSOLUTE index. We compute the
        -- absolute index by iterating, so callers can round-trip safely.
        -- Also collect hidden_slide_indices in the same pass.
        set curAbs to 0
        set hiddenList to {}
        try
            set curRef to current slide of targetDoc
            set numSlides to count of slides of targetDoc
            repeat with i from 1 to numSlides
                set s to slide i of targetDoc
                if s is curRef then set curAbs to i
                try
                    if skipped of s then set end of hiddenList to my jsonNumber(i)
                end try
            end repeat
        end try
        if curAbs > 0 then
            set curSlideJson to my jsonNumber(curAbs)
        else
            set curSlideJson to my jsonNull()
        end if

        -- current_slide_visible: the visible/navigator index (what Keynote shows
        -- as the slide number in the UI; counts only non-skipped slides). Kept
        -- alongside current_slide for debugging mismatches and for callers that
        -- want to display "what the user sees" — but never use this as a
        -- slide_number param: it doesn't round-trip when hidden slides exist.
        try
            set curVisible to slide number of current slide of targetDoc
            set curSlideVisibleJson to my jsonNumber(curVisible)
        on error
            set curSlideVisibleJson to my jsonNull()
        end try

        -- hidden_slide_indices: absolute indices of all skipped slides
        set hiddenIndicesJson to my jsonList(hiddenList)

        -- slide count
        try
            set sc to count of slides of targetDoc
            set slideCountJson to my jsonNumber(sc)
        on error
            set slideCountJson to my jsonNull()
        end try

        -- slide numbers showing
        try
            set sns to slide numbers showing of targetDoc
            if sns is missing value then
                set snsJson to my jsonNull()
            else
                set snsJson to my jsonBool(sns)
            end if
        on error
            set snsJson to my jsonNull()
        end try

        -- width
        try
            set w to width of targetDoc
            if w is missing value then
                set wJson to my jsonNull()
            else
                set wJson to my jsonNumber(w)
            end if
        on error
            set wJson to my jsonNull()
        end try

        -- height
        try
            set h to height of targetDoc
            if h is missing value then
                set hJson to my jsonNull()
            else
                set hJson to my jsonNumber(h)
            end if
        on error
            set hJson to my jsonNull()
        end try

        -- password protected
        try
            set pp to password protected of targetDoc
            if pp is missing value then
                set ppJson to my jsonNull()
            else
                set ppJson to my jsonBool(pp)
            end if
        on error
            set ppJson to my jsonNull()
        end try

        -- selection count (count only, no introspection of selection refs)
        try
            set selCount to count of selection of targetDoc
            set selJson to my jsonNumber(selCount)
        on error
            set selJson to my jsonNumber(0)
        end try

        return my jsonRecord({{"name", nameJson}, ¬
                              {"current_slide", curSlideJson}, ¬
                              {"current_slide_visible", curSlideVisibleJson}, ¬
                              {"hidden_slide_indices", hiddenIndicesJson}, ¬
                              {"slide_count", slideCountJson}, ¬
                              {"slide_numbers_showing", snsJson}, ¬
                              {"width", wJson}, ¬
                              {"height", hJson}, ¬
                              {"password_protected", ppJson}, ¬
                              {"selection_count", selJson}})
    end tell
end getDocumentState
