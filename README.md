# Sunplus SPHE8368-U Headunit Reverse Engineering

Payload scripts, MTD partition maps, and reverse engineering tools for Sunplus SPHE8368-U based automotive head units. Features RCE via gemn_auto.sh and Android Auto spoofing

This repository contains the payload scripts, partition mapping, and tools resulting from the reverse engineering of a white label multimedia head unit. The hardware is based on **Sunplus SPHE8368-U** SoC running Linux 4.9.

---

## Legal Disclaimer (Read before cloning)

**I DO NOT PROVIDE OFFICIAL BINARIES, FIRMWARES, OR COPYRIGHTED IMAGES.**
The content provided here is strictly educational and focused on embedded offensive security.

The Sunplus ISP (In-System Programming) scripts contain a **hardcoded MD5 hash** validated by the bootloader. Attempting to flash physical partitions (such as `mtd14` or `mtd11`) via the `dd` command without re-signing the image will result in an **IMMEDIATE AND IRREVERSIBLE HARD-BRICK**. You have been warned. Your hardware is your own responsibility.

---

## The Attack Vector: `gemn_auto.sh`

The manufacturer left a maintenance backdoor wide open in the system. Inserting a USB drive or microSD card containing a script named `gemn_auto.sh` in the root directory forces the Linux OS to execute it silently with **root** privileges. The UI displays a cynical "no known file found" message, completely hiding the background execution.

This repository leverages this vulnerability to act as a "Blind Terminal", writing the BusyBox output back to the USB drive or modifying YAFFS2 configuration files on the fly.

---

## Repository Structure

* 📁 **/payloads/**
  * `/Active processes and partition dump/gemn_auto.sh`: Base script to safely extract the YAFFS2 configuration partitions and the active process list via the blind terminal (without altering the system).
  * `/Wi-Fi & BT name/gemn_auto.sh`: Dynamically modifies `SETUPMENU.ini`, `bt_conf.ini`, and `softap.conf` to permanently lock the Wi-Fi SSID and Bluetooth broadcast name as **"Car Bt"**.
* 📁 **/docs/**
  * `partition-map.md`: Complete mapping of the MTD table (SquashFS vs. YAFFS2) and the NAND flash topology.
* 📁 **/scripts/**
  * `build_logo_container.py`: Python tool to convert standard images into the proprietary RAW RGBA container (Header `PART`/`OGOL`) required by the bootloader.

---

## Achieved Results

1. **Native Remote Code Execution:** Achieved without additional hardware (no soldering or EEPROM flashers required).
2. **Identity Spoofing:** The system bypasses the Android Auto handshake, being recognized as an OEM head unit by forcing `ro.product.manufacturer="CarManufacturer"`.
3. **Network Persistence:** Bluetooth and Wi-Fi networks persistently renamed via bash script.
4. **Logo MD5 Bypass:** Native automotive logos triggered via internal configuration files (completely bypassing the risk of bricking the physical partition).
