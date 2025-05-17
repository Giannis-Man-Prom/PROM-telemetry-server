1. Run the run.bat inside the Telemetry folder if on Windows, run run.sh on Mac or Linux
1.5 If on Linux make sure to give the app the permissions to access the port 
2. Run firewall_bypass.bat (to allow firewall traffic through port 5000)
3. Upload the code on the ESP, the password is cargovroom
4. Run getip.bat to get the ip of the device
5. Connect the device to the ESP wifi hotspot as well as other devices
6. In order to access the webapp insert "ip_from_getip.bat":5000 to a browser

TO ALLOW FIREWALL IF NECESSARY
1. GO TO WINDOWS DEFENDER FIREWALL AND ADVANCED SECURITY
2. GO TO Inbound Rules AND SELECT New Rule
3. CHOOSE PORT, CLICK NEXT, KEEP THE TCP, TYPE 8081 IN THE Specific Local Port
4. THEN Allow the connection AND LEAVE EVERYTHING CHECKED
5. GIVE A NAME, EG Allow Python App on Port 5000, AND THEN CLICK OK