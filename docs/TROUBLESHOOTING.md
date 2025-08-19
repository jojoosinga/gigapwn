## Troubleshooting

### Permission denied opening serial port

- Linux: Add your user to the `dialout` group and re-login:

```bash
sudo usermod -aG dialout "$USER"
```

- Or run with elevated privileges if necessary.

### Port disappears during transfer

- This can happen when the device resets or re-enumerates. The tool will try to reopen automatically. If it fails repeatedly, verify cable quality and power.

### No `AT^SGBD` requests arrive

- Ensure the device is in the correct bootloader/update mode.
- Try sending the initialization step again by restarting the script so `AT^SRSR 2` is resent.
- Confirm baud rate. Try common values like `115200` or those used by vendor tools.

### Wrong or corrupt firmware

- Verify you pointed to the correct `.bin` image for your device/variant.
- Do not interrupt power during update.

### Windows COM port issues

- Close any other programs that may hold the COM port open.
- Check Device Manager for the assigned `COMx` and update the script arguments accordingly.

### Still stuck?

- Run with a serial monitor (e.g., `screen`, `minicom`, or `PuTTY`) to observe raw traffic.
- Cross-reference the included `docs/MacroClassDocumentationWithATCommands-20231108-211434.pdf` and your device documentation.

