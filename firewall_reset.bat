@echo off
netsh advfirewall firewall delete rule name="Allow Python App on Port 5000" protocol=TCP localport=5000
echo Inbound rule for port 5000 has been removed.
pause
