# gigapwn

Command-line firmware uploader for Gigaset devices via AT commands over a serial interface.

This tool listens for device bootloader requests (e.g., `AT^SGBD <offset>,<size>`) and responds by streaming the requested slice from a firmware image, handling reconnection if the serial device momentarily disappears.

> Warning: Flashing firmware can permanently brick your device. Proceed at your own risk and ensure you understand the implications.

## Features

- Responds to bootloader prompts to serve firmware by offset/length
- Simple Python CLI, no external build required
- Automatic serial port reopen on transient failures
- Verbose logging of the bootloader dialogue

## Requirements

- Python 3.8 or newer
- `pyserial`

Install dependency:

```bash
python3 -m pip install pyserial
```

## Quick start

1. Connect your device so it exposes a serial port (e.g., `/dev/ttyACM0`, `/dev/ttyUSB0` on Linux).
2. Identify the correct port and baud rate used by the bootloader.
3. Run the uploader with your firmware file:

```bash
python3 gigapwn.py /dev/ttyACM0 115200 firmare/shark__upd.bin
```

Arguments:

- `<COM port>`: Serial device path, e.g., `/dev/ttyACM0` (Linux) or `COM3` (Windows)
- `<baud rate>`: Integer baud (e.g., `115200`)
- `<firmware file path>`: Path to the firmware image to serve

## How it works (high level)

The script initiates the update sequence, acknowledging bootloader setup prompts such as `AT^SSWS` and `AT^SSWR 20`, then enters a loop reading lines from the serial port. When the device sends `AT^SGBD <hex_offset>, <hex_size>`, the script seeks into the firmware file and transmits exactly that slice followed by `OK` to signal completion.

See `docs/PROTOCOL.md` for a more detailed message-flow description.

## Repository layout

- `gigapwn.py`: Main CLI script
- `firmare/`: Sample firmware images used for testing
- `docs/`: Documentation
  - `PROTOCOL.md`: AT dialogue and data exchange
  - `USAGE.md`: Step-by-step usage guide
  - `TROUBLESHOOTING.md`: Common problems and fixes
- `Gigaset firmware updater/`: Vendor updater artifacts (reference)
- `whole-firmware-update.txt`: Notes and research on full firmware update process

## Troubleshooting

If you encounter permission errors on Linux (e.g., cannot open `/dev/ttyACM0`), add your user to the `dialout` group or run with appropriate privileges. See `docs/TROUBLESHOOTING.md` for more.

## Disclaimer

This project is provided for research and interoperability purposes. You are responsible for complying with all applicable laws, licenses, and device warranty terms.