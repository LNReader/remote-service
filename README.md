# LNReader Remote Service
- Required LNReader version: 1.xx
- LAN network - Wifi
- Windows PC

## About
* With this service, you can backup everything. Yes, I mean.. everything.
* Never face the errors from normal backup like `Weird backup path`, `Network Request failed`, `Run out of space` , ...

## Remote Backup
1. Start LNReaderRS.exe
* IPv4: To get your IPv4 in LAN network (Windows)
	* Window + R
	* Enter `cmd`
	* Enter `ipconfig`
	* You can see your IPv4 address in `Wireless LAN adapter Wi-Fi` 
		* Remember to make your network public [Make a Wi-Fi network public](https://support.microsoft.com/en-us/windows/make-a-wi-fi-network-public-or-private-in-windows-0460117d-8d3e-a7ac-f003-7a0da607448d#WindowsVersion=Windows_11)
		* In case you are using Ethernet Adapter then IPv4 is in `Ethernet adapter Ethernet` section
* Port: default is 8000, whaterver you want
* Folder: Whatever you want
2. Run remote serivce
*	Click `Start`
*	Screen should display `Server started at ws://your.ip.address:8000`
3. Backup
* Open LNReader android app
* Go to More -> Setting -> Backup -> Remote Backup
* Enter IPv4 and port above
* Run and wait

## Restore backup
1. Same as above
2. Same as above
3. Restore
* Open LNReader android app
* Go to More -> Setting -> Backup -> Remote Restore
* Enter IPv4 and port above
* Run and wait.

## Example
- [How to backup and restore (video)](https://youtu.be/Sg9RLLTecVk)
