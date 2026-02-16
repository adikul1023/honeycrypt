# HoneyCrypt CLI Quick Reference

## Installation
```bash
pip install pycryptodome argon2-cffi
chmod +x honeycrypt
```

## Basic Commands

### Standard Encryption (2 decoys auto-generated)
```bash
./honeycrypt encrypt \
  --real <file> \
  --decoy <file> \
  --password <pass> \
  [--output <file>]
```

### Multi-Decoy Encryption (1-5 custom decoys)
```bash
./honeycrypt encrypt-multi \
  --real <file> \
  --decoys "file1,file2,file3" \
  --password <pass> \
  [--output <file>]
```

### Decryption
```bash
./honeycrypt decrypt \
  --input <file> \
  --password <pass> \
  [--output <file>]
```

## Advanced Options

### Padding (set target file size)
```bash
--pad <size_in_MB>        # e.g., --pad 100 for 100 MB
```

### Self-Destruct Password
```bash
--self-destruct <pass>    # WARNING: Permanently wipes file!
```

### Quiet Mode
```bash
--quiet                   # or -q
```

## Examples

### Simple encryption
```bash
./honeycrypt encrypt --real secret.pdf --decoy fake.pdf -p "pass123"
```

### With all features
```bash
./honeycrypt encrypt \
  --real sensitive.doc \
  --decoy dummy.doc \
  -p "mainpass" \
  --self-destruct "panicpass" \
  --pad 50 \
  -o secure.hcrypt
```

### Multi-decoy
```bash
./honeycrypt encrypt-multi \
  --real important.txt \
  --decoys "d1.txt,d2.pdf,d3.jpg" \
  -p "realpass"
```

### Decrypt
```bash
./honeycrypt decrypt -i encrypted.hcrypt -p "pass123" -o output.txt
```

## Tips

- **Save decoy passwords:** The CLI displays generated decoy passwords during encryption
- **Padding:** Use for privacy (hide true file size) or to meet size requirements
- **Self-destruct:** Memorize this password, don't write it down!
- **Scripting:** Use `--quiet` to suppress verbose output in scripts
- **Exit codes:** 0 = success, 1 = failure, 130 = interrupted

## File Extensions

- `.hcrypt` - Recommended extension for encrypted files
- Any extension works - the format is self-describing

## Security Notes

- Uses Argon2id for key derivation (~500ms intentionally slow)
- Automatic compression when beneficial (>5% reduction)
- Plausible deniability: no way to prove which password is "real"
- Secure file deletion recommended: `shred -vfz -n 10 original.txt`
