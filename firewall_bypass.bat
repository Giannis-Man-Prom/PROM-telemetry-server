@echo off
netsh advfirewall firewall add rule name="Allow Python App on Port 8081" dir=in action=allow protocol=TCP localport=8081
echo Inbound rule for port 8081 has been created.
pause