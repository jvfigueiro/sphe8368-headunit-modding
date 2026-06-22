#!/usr/bin/env python3
"""
Sunplus SPHE8368-U Logo Packager (PART/OGOL Format)

This script takes a standard image (e.g., PNG/JPEG), resizes it to the hardware's 
native 1024x600 resolution, converts it to raw 32-bit RGBA, and prepends the 
proprietary Sunplus header ('PART' / 'OGOL') required for mtd14 flashing.

WARNING: Flashing this directly to mtd14 via 'dd' without recalculating the ISP 
script MD5 hash will result in a hard-brick. Use at your own risk.
"""

import struct
import sys
try:
    from PIL import Image
except ImportError:
    print("[-] Error: Pillow library not found. Install it using: pip install Pillow")
    sys.exit(1)

# Hardware constraints
TARGET_WIDTH = 1024
TARGET_HEIGHT = 600
MAGIC_PART = b'PART'
MAGIC_OGOL = b'OGOL'

def build_header(payload_size):
    """
    Constructs the proprietary Sunplus logo header.
    Note: The exact padding and byte offsets should be verified against 
    your specific hex dump of mtd14.
    """
    # Structural mock based on hex analysis:
    # [4 bytes MAGIC 'PART'] + [4 bytes Size] + [Padding] + [4 bytes MAGIC 'OGOL'] ...
    
    header = bytearray()
    header.extend(MAGIC_PART)
    header.extend(struct.pack('<I', payload_size)) # Little-endian payload size
    
    # Inject padding between headers (verify exact length in your hex editor)
    header.extend(b'\x00' * 24) 
    
    header.extend(MAGIC_OGOL)
    
    # Inject remaining padding before the raw image array
    header.extend(b'\x00' * 28) 
    
    return header

def create_logo_container(input_image_path, output_bin_path):
    try:
        print(f"[*] Opening {input_image_path}...")
        img = Image.open(input_image_path)
        
        # Force resize to hardware constraints
        print(f"[*] Resizing to {TARGET_WIDTH}x{TARGET_HEIGHT}...")
        img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        
        # Convert to 32-bit RGBA (Alpha channel required by hardware)
        print("[*] Converting to raw RGBA format...")
        img = img.convert("RGBA")
        raw_rgba_data = img.tobytes()
        
        payload_size = len(raw_rgba_data)
        header = build_header(payload_size)
        
        print(f"[*] Compiling binary container (Header + {payload_size} bytes of RAW data)...")
        with open(output_bin_path, 'wb') as f:
            f.write(header)
            f.write(raw_rgba_data)
            
        print(f"[+] Success! Container saved to {output_bin_path}")
        print("[!] REMINDER: Do not flash this without addressing the MD5 bootloader checksum.")

    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_logo_container.py <input_image.png> <output_logo.bin>")
        sys.exit(1)
        
    create_logo_container(sys.argv[1], sys.argv[2])