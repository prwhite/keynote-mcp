-- introspection_playback.applescript
-- Playback control verbs: start, stop, show next/previous, goto slide.
-- Uses helpers from introspection_json.applescript (must be prepended by caller).

-- startPlayback(docName, fromSlide)
-- fromSlide == 0 means "start from current slide".
-- fromSlide >= 1 means "start from that slide number".
on startPlayback(docName, fromSlide)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        if fromSlide is 0 then
            start targetDoc
            return my jsonRecord({{"playing", my jsonBool(true)}, ¬
                                  {"from_slide", my jsonNull()}})
        else
            start targetDoc from slide fromSlide of targetDoc
            return my jsonRecord({{"playing", my jsonBool(true)}, ¬
                                  {"from_slide", my jsonNumber(fromSlide)}})
        end if
    end tell
end startPlayback

-- stopPlayback()
on stopPlayback()
    tell application "Keynote"
        stop
        return my jsonRecord({{"stopped", my jsonBool(true)}})
    end tell
end stopPlayback

-- showNext()
on showNext()
    tell application "Keynote"
        show next
        return my jsonRecord({{"action", my jsonString("show_next")}})
    end tell
end showNext

-- showPrevious()
on showPrevious()
    tell application "Keynote"
        show previous
        return my jsonRecord({{"action", my jsonString("show_previous")}})
    end tell
end showPrevious

-- gotoSlide(docName, slideNumber)
-- Sets current slide property — works in both editing and playback mode.
on gotoSlide(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        set current slide of targetDoc to slide slideNumber of targetDoc
        return my jsonRecord({{"current_slide", my jsonNumber(slideNumber)}})
    end tell
end gotoSlide
