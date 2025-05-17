@echo off
netsh advfirewall firewall add rule name="Allow Python App on Port 5000" dir=in action=allow protocol=TCP localport=5000
echo Inbound rule for port 5000 has been created.
pause