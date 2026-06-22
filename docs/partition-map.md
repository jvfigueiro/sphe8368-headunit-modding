# Sunplus SPHE8368-U MTD Partition Map

This document outlines the memory technology device layout discovered via the `gemn_auto.sh` blind terminal vulnerability. 

The Sunplus SPHE8368-U SoC utilizes a standard embedded Linux 4.9 topology, segregating the core system (read-only) from the user/configuration data (writable). 

## Flash Memory Topology

| MTD Block | File System | Access | Description / Role |
| :--- | :--- | :--- | :--- |
| `rootfs` | SquashFS | Read-Only | The core Linux root file system. Locked down by default. |
| `opt` | SquashFS | Read-Only | Vendor-specific applications and binaries. |
| `spapp` | SquashFS | Read-Only | The main Sunplus automotive application interface (multimedia core). |
| `nvm` | YAFFS2 | Writable | Non-Volatile Memory. Stores persistent hardware configurations, including boot parameters and identity strings. **Primary target for Android Auto spoofing.** |
| `userdata` | YAFFS2 | Writable | General user data, paired Bluetooth devices, and saved Wi-Fi networks. |
| `mtd14` | RAW (Custom) | Physical / Read-Write | Primary boot logo container. Uses the proprietary `PART`/`OGOL` header with RAW RGBA data. Protected by ISP script MD5 checks. |
| `mtd19` | RAW (Custom) | Physical / Read-Write | Secondary/ISP logo partition. Similar container structure to `mtd14`. |

### Engineering Notes
* **SquashFS Limitations:** Do not attempt to modify these directly on the live system. They are compressed, read-only file systems. 
* **YAFFS2 Exploitation:** Modifications here are persistent across reboots. Editing `init.rc` or `build.prop` equivalents inside the `nvm` partition is the safest vector for identity spoofing without triggering the bootloader's MD5 checksum trap.

 ```bash
[+] Info:
Linux Gemini 4.9.217 #8 Thu Apr 20 20:19:26 CST 2023 armv7l GNU/Linux

[+] Partitions:
dev:    size   erasesize  name
mtd0: 00020000 00020000 "nand_header"
mtd1: 00020000 00020000 "xboot1"
mtd2: 000e0000 00020000 "uboot1"
mtd3: 001e0000 00020000 "uboot2"
mtd4: 00080000 00020000 "env"
mtd5: 00080000 00020000 "env_redund"
mtd6: 00400000 00020000 "ecos"
mtd7: 00480000 00020000 "kernel"
mtd8: 00360000 00020000 "rootfs."
mtd9: 00060000 00020000 "opt."
mtd10: 02e00000 00020000 "spsdk."
mtd11: 00ea0000 00020000 "spapp."
mtd12: 01000000 00020000 "nvm"
mtd13: 00020000 00020000 "pq"
mtd14: 00260000 00020000 "logo"
mtd15: 00020000 00020000 "tcon"
mtd16: 00040000 00020000 "iop_car"
mtd17: 00100000 00020000 "runtime_cfg"
mtd18: 00020000 00020000 "vi"
mtd19: 00980000 00020000 "isp_logo"
mtd20: 00040000 00020000 "vendordata"
mtd21: 00bc0000 00020000 "pat_logo"
mtd22: 00040000 00020000 "version_info"
mtd23: 00040000 00020000 "vd_restore"
mtd24: 00500000 00020000 "anm_logo"
mtd25: 00020000 00020000 "config"
mtd26: 00400000 00020000 "userdata"

[+] Mount Points:
/dev/root on / type squashfs (ro,relatime)
devtmpfs on /dev type devtmpfs (rw,relatime,size=31668k,nr_inodes=7917,mode=755)
tmpfs on /tmp type tmpfs (rw,nosuid,relatime,mode=755)
devpts on /dev/pts type devpts (rw,relatime,mode=600,ptmxmode=000)
proc on /proc type proc (rw,relatime)
sysfs on /sys type sysfs (rw,relatime)
/dev/blockrom9 on /opt type squashfs (ro,relatime)
/dev/blockrom10 on /tmp/sp/usr/local type squashfs (ro,relatime)
/dev/blockrom11 on /tmp/sp/application type squashfs (ro,relatime)
/dev/mtdblock25 on /tmp/sp/application/config type squashfs (ro,relatime)
/dev/mtdblock12 on /tmp/sp/media/flash/nvm type yaffs2 (rw,noatime)
/dev/mtdblock26 on /tmp/sp/media/flash/userdata type yaffs2 (rw,noatime)
tmpfs on /etc type tmpfs (rw,nosuid,relatime,mode=755)
tmpfs on /root type tmpfs (rw,nosuid,relatime,mode=755)
overlay on /tmp/sp/system/etc type overlay (rw,relatime,lowerdir=/usr/local/etc,upperdir=/tmp/etc_up,workdir=/tmp/etc_wk)
/dev/sda1 on /tmp/sp/mnt/sda1 type vfat (rw,dirsync,nosuid,nodev,noatime,nodiratime,fmask=0077,dmask=0077,codepage=437,iocharset=utf8,shortname=mixed,errors=remount-ro)

[+] YAFFS2 Test:
Writable NVM
