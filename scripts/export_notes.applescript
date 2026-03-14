-- Export all notes from the "Recipes" folder in Apple Notes to a JSON file.
-- Usage: osascript scripts/export_notes.applescript

set outputPath to (do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/.notes-export.json"

set jsonEntries to {}

tell application "Notes"
    try
        set recipesFolder to folder "Recipes"
    on error
        display dialog "No 'Recipes' folder found in Apple Notes. Please create one and add your recipes there."
        return
    end try

    set allNotes to notes of recipesFolder
    set noteCount to count of allNotes

    repeat with i from 1 to noteCount
        set thisNote to item i of allNotes
        set noteTitle to name of thisNote
        set noteBody to body of thisNote
        set noteDate to modification date of thisNote

        -- Escape special characters for JSON
        set noteTitle to my escapeJSON(noteTitle)
        set noteBody to my escapeJSON(noteBody)
        set dateStr to my formatDate(noteDate)

        set jsonEntry to "{\"title\": \"" & noteTitle & "\", \"body\": \"" & noteBody & "\", \"dateModified\": \"" & dateStr & "\"}"
        set end of jsonEntries to jsonEntry
    end repeat
end tell

-- Join entries and wrap in array
set AppleScript's text item delimiters to ", "
set jsonArray to "[" & (jsonEntries as text) & "]"
set AppleScript's text item delimiters to ""

-- Write to file
do shell script "echo " & quoted form of jsonArray & " > " & quoted form of outputPath

return "Exported " & (count of jsonEntries) & " notes to " & outputPath

on escapeJSON(theText)
    set theText to my replaceText(theText, "\\", "\\\\")
    set theText to my replaceText(theText, "\"", "\\\"")
    set theText to my replaceText(theText, return, "\\n")
    set theText to my replaceText(theText, linefeed, "\\n")
    set theText to my replaceText(theText, tab, "\\t")
    return theText
end escapeJSON

on replaceText(theText, searchStr, replaceStr)
    set AppleScript's text item delimiters to searchStr
    set theItems to text items of theText
    set AppleScript's text item delimiters to replaceStr
    set theText to theItems as text
    set AppleScript's text item delimiters to ""
    return theText
end replaceText

on formatDate(theDate)
    set y to year of theDate as text
    set m to text -2 thru -1 of ("0" & ((month of theDate) as integer))
    set d to text -2 thru -1 of ("0" & (day of theDate))
    return y & "-" & m & "-" & d
end formatDate
