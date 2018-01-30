# Tamata-GpsD
Gps Tracking Position in NodeJS. With Raspberry Pi ( Stretch ), Recording position in PostGreSql


# install gpsd gps-clit
(procedure here)[http://www.catb.org/gpsd/troubleshooting.html#generaltroubleshooting]

sudo apt-get install gpsd gpsd-clients 

## Config GPS : 
( should appear into lsusb list ) and in directory /dev/tty... )

gpsctl -f -n /dev/ttyUSB0

result : 
/dev/ttyUSB0 identified as a SiRF GSW3.5.0_3.5.00.00-SDK-3EP2.01 SJ1-090717-NMEA4800_S_G1_CM205_K at 4800 baud.
gpsctl:SHOUT: switching to mode NMEA.

sudo service gpsd start


#### dmesg | grep tty  

[    0.000000] Kernel command line: 8250.nr_uarts=0 bcm2708_fb.fbwidth=1280 bcm2708_fb.fbheight=720 bcm2708_fb.fbswap=1 vc_mem.mem_base=0x3ec00000 vc_mem.mem_size=0x40000000  dwc_otg.lpm_enable=0 console=ttyS0,115200 console=tty1 root=PARTUUID=9c6f0308-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
[    0.000312] console [tty1] enabled
[    0.776185] 3f201000.serial: ttyAMA0 at MMIO 0x3f201000 (irq = 87, base_baud = 0) is a PL011 rev2
[242639.475775] usb 1-1.2: cp210x converter now attached to ttyUSB0
[243057.741034] cp210x ttyUSB0: cp210x converter now disconnected from ttyUSB0
[243089.920553] usb 1-1.2: cp210x converter now attached to ttyUSB0
[244061.517029] cp210x ttyUSB0: cp210x converter now disconnected from ttyUSB0
[244080.912965] usb 1-1.2: cp210x converter now attached to ttyUSB0
[250115.661191] cp210x ttyUSB0: cp210x converter now disconnected from ttyUSB0
[252614.929903] usb 1-1.2: cp210x converter now attached to ttyUSB0
[252768.589196] pps pps0: source "/dev/ttyUSB0" added
[253739.572820] pps pps0: source "/dev/ttyUSB0" added
[254107.390953] pps pps0: source "/dev/ttyUSB0" added
pi@TamataRaspi:/var/run $ 

## Test GPS 
gpsmon /dev/ttyUSB0

Time:       2018-01-30T22:25:44.000Z   ││PRN:   Elev:  Azim:  SNR:  Used: │
│    Latitude:    46.143033 N               ││                                 │
│    Longitude:    1.169138 W    

Google position : 
46.143033333 N
Longitude: -1.169138333 W

Ok ! ;) Now... trying to get Marine GPS position.