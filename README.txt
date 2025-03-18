1. Run the run.bat inside the Telemetry folder
2. Upload the code on the ESP, the password is cargovroom
3. Run getip.bat to get the ip of the device
4. Connect the device to the ESP wifi hotspot as well as other devices
5. In order to access the webapp insert "ip_from_getip.bat":8081 to a browser

TO ALLOW FIREWALL IF NECESSARY
1. GO TO WINDOWS DEFENDER FIREWALL AND ADVANCED SECURITY
2. GO TO Inbound Rules AND SELECT New Rule
3. CHOOSE PORT, CLICK NEXT, KEEP THE TCP, TYPE 8081 IN THE Specific Local Port
4. THEN Allow the connection AND LEAVE EVERYTHING CHECKED
5. GIVE A NAME, EG Allow Python App on Port 8081, AND THEN CLICK OK
