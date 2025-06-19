@echo off
netsh advfirewall firewall delete rule name="Allow Python App on Port 8081" protocol=TCP localport=8081
echo Inbound rule for port 8081 has been removed.
pause
