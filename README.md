# android-vbmeta-disable-verification

Patch Android vbmeta image and disable verification flags inside.  
Based on [vbmeta-disable-verify](https://github.com/libxzr/vbmeta-disable-verification) by LibXZR <i@xzr.moe>

## Usage

Give it a vbmeta image and then verification will be disabled on it.

```bash
android_vbmeta_disable_verification.py <vbmeta-image> [<vbmeta-output-image>]
```

Example:
```bash
$ python3 ./android_vbmeta_disable_verification.py vbmeta.img 
Patched vbmeta image was saved to the file 'vbmeta.patched.img'.
Successfully disabled verification on the provided vbmeta image.
```

You can also use android_vbmeta_disable_verification.py as a python module:
```python
import android_vbmeta_disable_verification as vbm
vbm.patch_vbmeta_file('vbmeta.img')
```

This should be equal to `fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img`.  
The only difference is that it directly patch the image file. Fastboot doesn't provide the ability to generate an image with verification disabled, but sometimes I need it :) .

## Requirements

Python >= 3.8 is required.

## References

- [libavb](https://android.googlesource.com/platform/external/avb/+/refs/tags/android-13.0.0_r15/libavb/avb_vbmeta_image.h)
- [fastboot](https://android.googlesource.com/platform/system/core/+/refs/tags/android-13.0.0_r15/fastboot/fastboot.cpp)

## License

[MIT](LICENSE)
