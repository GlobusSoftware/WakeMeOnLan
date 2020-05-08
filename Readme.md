# WakeMeOnLan

There is small python 3 script. 
This script is an upgraded version of an existing one on github:
https://github.com/bentasker/Wake-On-Lan-Python

In this implementation, some changes have been made that seem more correct to me.

# How it work?

You need make classic .ini file to config WOL script. This file should be located in the script directory and called "wol.ini".
If you want use other name and path you can specify the file location in the script second parameters.

Example wol.ini:

```ini
[General]
broadcast=255.255.255.255

[Devices]
PC=1c:1b:0d:a7:3e:85
LapTop=00:00:00:00:00:00
```
In section General you can set broadcast address. Generally there is no need to change the default address.

In section Devices you cat set any more options with mac addresses of your devices.

To run script with default wol.ini location:

```
	./wol.py PC
	./wol.py LapTop
```

To run script with user wol.ini location:

```
	./wol.py PC ~/folder/users.ini
```
