## Protocol overview

The script interacts with a Gigaset bootloader over a serial port using AT-like commands.

### Initialization

1. Host sends: `AT^SRSR 2` followed by CRLF
2. Bootloader may send prompts such as:
   - `AT^SSWS` → Host responds `OK` (CRLF)
   - `AT^SSWR 20` → Host responds `OK` (CRLF)

### Data transfer

The bootloader requests arbitrary slices with a command like:

```
AT^SGBD <hex_offset>,<hex_size>
```

- `<hex_offset>` is hexadecimal, may include a trailing comma as seen in some firmwares (e.g., `0001A000,`).
- `<hex_size>` is hexadecimal length in bytes.

Host behavior:

1. Parse offset and size (strip any trailing comma from the offset).
2. `seek(offset)` into the firmware file.
3. Read `size` bytes.
4. Write the raw bytes to the serial port, immediately followed by `OK` and CRLF.

### Example transcript (abridged)

```
Host -> Dev: AT^SRSR 2\r\n
Dev  -> Host: AT^SSWS
Host -> Dev: OK\r\n
Dev  -> Host: AT^SSWR 20
Host -> Dev: OK\r\n
Dev  -> Host: AT^SGBD 00000000, 00000800
Host -> Dev: <first 0x800 bytes of firmware><OK\r\n>

Dev  -> Host: AT^SGBD 00000800, 00000800
Host -> Dev: <next 0x800 bytes><OK\r\n>
...
```

### Line endings

Commands and acknowledgements use CRLF (`\r\n`). The script appends CRLF when writing commands and `OK`.

### Error handling

- Serial port errors trigger a close and reopen retry loop with backoff.
- Any unexpected exception breaks the loop to avoid sending corrupt data.

