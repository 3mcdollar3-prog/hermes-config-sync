# USB OS Installer Guide

This reference details the constraints and procedures for creating bootable OS installers from within Hermes.

## Constraints
- **No GUI Tools:** Hermes cannot run GUI installers like Balena Etcher or GUI-based OS tools.
- **Hardware Access:** Hermes does not have direct raw access to USB hardware devices to flash images.
- **Safety:** Creating bootable installers involves `dd` or equivalent block-level write operations. These are dangerous and can wipe drives if the incorrect destination device is specified.

## Recommended Workflow
1. **Download:** Use Hermes to download the official recovery/install image (e.g., .img, .bin).
2. **Transfer:** Move the file to the user's host machine.
3. **Flash:** Direct the user to flash the image using an external tool:
   - **ChromeOS:** Use the "Chromebook Recovery Utility" (Chrome extension) on the host machine.
   - **Linux/General:** Use Balena Etcher or the native OS disk utility on the host machine.
4. **CLI Warning:** If the user insists on using `dd` via the terminal, ensure they first identify the correct device path (e.g., via `lsblk`) and perform the operation manually on their own host machine to ensure safety.

## References
- [ChromeOS Recovery Utility](https://chrome.google.com/webstore/detail/chromebook-recovery-utilit/jndclpdbaamdhonoechhpnmjmcahjdfg)
