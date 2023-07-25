#!/usr/bin/env python
#!/usr/bin/python3
#!/usr/bin/python
#!python

# android-vbmeta-disable-verification.py by Stanislav Povolotsky
# https://github.com/Stanislav-Povolotsky/android-vbmeta-disable-verification
# based on vbmeta-disable-verify by LibXZR <i@xzr.moe>
# https://github.com/libxzr/vbmeta-disable-verification

import sys
from typing import Optional

# Magic for the vbmeta image header.
AVB_MAGIC                 = b"AVB0"
AVB_MAGIC_LEN             = 4

# Information about the verification flags
FLAGS_OFFSET              = 123
FLAG_DISABLE_VERITY       = 0x01
FLAG_DISABLE_VERIFICATION = 0x02

def cmdline_tool_show_help():
    print("android_vbmeta_disable_verification.py by Stanislav Povolotsky")
    print("\thttps://github.com/Stanislav-Povolotsky/android-vbmeta-disable-verification")
    print("\tbased on vbmeta-disable-verify by LibXZR <i@xzr.moe>")
    print("Usage:")
    print("\tandroid_vbmeta_disable_verification.py <vbmeta-image> [<vbmeta-output-image>]")

def patch_vbmeta_data(input_data: bytes, apply_flags: int = FLAG_DISABLE_VERITY | FLAG_DISABLE_VERIFICATION, apply_flags_mask: int = FLAG_DISABLE_VERITY | FLAG_DISABLE_VERIFICATION) -> bytes:
    data = bytearray(input_data)

    if (data[0 : 0 + AVB_MAGIC_LEN] != AVB_MAGIC) or (len(data) < (FLAGS_OFFSET + 1)):
        raise Exception("The provided image is not a valid vbmeta image")

    flags = data[FLAGS_OFFSET]
    new_flags = (flags & ~apply_flags_mask) | apply_flags

    data[FLAGS_OFFSET] = new_flags

    return bytes(data)

def patch_vbmeta_file(input_file: str, output_file: Optional[str] = None, apply_flags: int = FLAG_DISABLE_VERITY | FLAG_DISABLE_VERIFICATION, apply_flags_mask: int = FLAG_DISABLE_VERITY | FLAG_DISABLE_VERIFICATION) -> bool:
    try:
        with open(input_file, "rb") as f:
            data = f.read()
    except Exception as e:
        raise Exception("Unable to access the provided vbmeta image: %s" % e)

    new_data = patch_vbmeta_data(data)
    modified = new_data != data

    if(output_file is None):
      output_file = input_file
    try:
        with open(output_file, "wb") as f:
            f.write(new_data)
    except Exception as e:
        raise Exception("Unable to write modified vbmeta image: %s" % e)

    return modified

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        cmdline_tool_show_help()
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    if(output_file is None):
        output_file = input_file
        if(output_file.endswith(".img")): 
            output_file = output_file[:-4]
        output_file += ".patched.img"

    try:
        changed = patch_vbmeta_file(input_file, output_file)
        print("Patched vbmeta image was saved to the file '%s'." % output_file)
        if(changed):
            print("Successfully disabled verification for vbmeta image.")
        else:
            print("This vmbeta image already have verification disabled.")
    except Exception as e:
        print("Error: Failed when patching the vbmeta image: %s" % e)
