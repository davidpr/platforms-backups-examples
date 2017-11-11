#1. Open the connection with your NAS (IP in LAN)
net use \\192.168.1.xxx\IPC$ /u:yourUser yourPassword
#2. Copy the desired files 
#Find the robocopy usage here: https://technet.microsoft.com/en-us/library/cc733145(v=ws.11).aspx
#Purge deletes files in the destination that are no longes in the origin
#XO excludes older files
#R3 W1; retry 3 trimes and wait for 1 second in between trials
robocopy "\\192.168.1.xxx\folderLevel1.1\folderLevel2.1\" "L:\yourDestination1\" /XO /R:3 /W:1 /E /purge
robocopy "\\192.168.1.xxx\folderLevel1.1\folderLevel2.2\" "L:\yourDestination2\" /XO /R:3 /W:1 /E /purge
robocopy "\\192.168.1.xxx\folderLevel1.2\folderLevel2.1\" "L:\yourDestination3\" /XO /R:3 /W:1 /E /purge
robocopy "\\192.168.1.xxx\folderLevel1.2\folderLevel2.2\" "L:\yourDestination4\" /XO /R:3 /W:1 /E /purge
#3. Close the connection with your NAS
net use \\192.168.1.xxx\IPC$ /D
