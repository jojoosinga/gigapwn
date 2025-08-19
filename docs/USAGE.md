## Usage

Follow these steps to serve a firmware image to a Gigaset device bootloader.

### 1) Install prerequisites

```bash
python3 -m pip install pyserial
```

### 2) Identify the serial port

- Linux: after plugging in, check `dmesg | grep -i tty` or list by ID:

```bash
ls -l /dev/serial/by-id/
```

- Windows: Use Device Manager and look under Ports (COM & LPT) for `COMx`.

### 3) Determine the baud rate

Most bootloaders use `115200`. If unsure, consult device documentation or try common rates (57600, 115200, 230400).

### 4) Run the uploader

```bash
python3 gigapwn.py /dev/ttyACM0 115200 firmare/shark__upd.bin
```

On Windows:

```bash
py -3 gigapwn.py COM3 115200 C:\\path\\to\\firmware.bin
```

### 5) Observe the dialogue

The script prints lines it receives (e.g., `AT^SSWS`, `AT^SSWR 20`, `AT^SGBD ...`) and acknowledges with `OK` when expected. When a segment request arrives (offset and size in hex), the script seeks and transmits that slice followed by `OK`.

### 6) Completion

The device determines completion. Some bootloaders reset automatically when the final chunk is written. If the port disappears temporarily, the script will attempt to reopen it.

### Notes

- Ensure you are using the correct firmware for your exact device/variant.
- On Linux, membership in the `dialout` group is usually required to access `/dev/tty*` devices.
- The provided `firmare/` folder contains sample images used in research.

