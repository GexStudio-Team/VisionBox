Set ws = CreateObject("WScript.Shell")
ws.Run "wsl.exe -d Ubuntu -u root -- sh -c ""while true; do sleep 30; done""", 0, False