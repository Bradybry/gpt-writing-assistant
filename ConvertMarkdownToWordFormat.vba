Sub ConvertMarkdownToWordFormat()

    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Store current Track Changes state
    Dim trackChangesState As Boolean
    trackChangesState = doc.TrackRevisions
    
    ' Turn off Track Changes
    doc.TrackRevisions = False

    ' Find markdown bold formatting
    With doc.Content.Find
        .Text = "\*\*([!\*]@)\*\*"
        .MatchWildcards = True
        .Replacement.Font.Bold = True
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll
    End With
    
    ' Reset font boldness for the next Find-Replace operation
    doc.Content.Find.Replacement.Font.Bold = False
    
    ' Find markdown italic formatting
    With doc.Content.Find
        .Text = "\*([!\*]@)\*"
        .MatchWildcards = True
        .Replacement.Font.Italic = True
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll
    End With
    
    ' Restore Track Changes state
    doc.TrackRevisions = trackChangesState

End Sub