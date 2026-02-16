# HoneyCrypt CLI Documentation

## Overview

HoneyCrypt CLI is a command-line interface for HoneyCrypt encryption/decryption operations. It provides non-interactive access to HoneyCrypt's plausible deniability encryption features, making it suitable for scripting and automation.

## Installation

### Requirements

- Python 3.7 or higher
- PyCryptodome
- argon2-cffi

### Setup

1. Install dependencies:
```bash
pip install pycryptodome argon2-cffi
```

2. Make the CLI executable:
```bash
chmod +x honeycrypt
```

3. Optionally, add to your PATH:
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="/path/to/honeycrypt:$PATH"
```

## Usage

### Basic Command Structure

```bash
./honeycrypt <command> [options]
```

### Available Commands

- `encrypt` - Standard 2-decoy encryption
- `encrypt-multi` - Multi-decoy encryption (1-5 decoys)
- `decrypt` - Decrypt an encrypted file

## Command Reference

### Standard Encryption

Encrypt a file with one decoy file (generates 2 additional decoy passwords automatically).

```bash
./honeycrypt encrypt \
  --real <real_file> \
  --decoy <decoy_file> \
  --password <password> \
  [--output <output_file>] \
  [--self-destruct <sd_password>] \
  [--pad <size_mb>] \
  [--quiet]
```

**Options:**
- `--real` (required) - Path to the real file to encrypt
- `--decoy` (required) - Path to the decoy file
- `--password, -p` (required) - Password for decrypting the real file
- `--output, -o` (optional) - Output file path (default: `<real_file>.hcrypt`)
- `--self-destruct` (optional) - Self-destruct password (permanently wipes file if used)
- `--pad` (optional) - Target file size in MB (adds random padding)
- `--quiet, -q` (optional) - Suppress verbose output

**Example:**
```bash
./honeycrypt encrypt \
  --real secret.pdf \
  --decoy fake.pdf \
  --password "MySecurePassword123!" \
  --output encrypted.hcrypt
```

**Example with self-destruct and padding:**
```bash
./honeycrypt encrypt \
  --real document.docx \
  --decoy dummy.docx \
  -p "mainpass" \
  --self-destruct "destroypass" \
  --pad 10 \
  -o secure.hcrypt
```

### Multi-Decoy Encryption

Encrypt a file with multiple decoy files (1-5 decoys).

```bash
./honeycrypt encrypt-multi \
  --real <real_file> \
  --decoys <file1,file2,file3> \
  --password <password> \
  [--output <output_file>] \
  [--self-destruct <sd_password>] \
  [--pad <size_mb>] \
  [--quiet]
```

**Options:**
- `--real` (required) - Path to the real file to encrypt
- `--decoys` (required) - Comma-separated list of decoy file paths
- `--password, -p` (required) - Password for decrypting the real file
- `--output, -o` (optional) - Output file path (default: `<real_file>.hcrypt`)
- `--self-destruct` (optional) - Self-destruct password
- `--pad` (optional) - Target file size in MB
- `--quiet, -q` (optional) - Suppress verbose output

**Example:**
```bash
./honeycrypt encrypt-multi \
  --real important.doc \
  --decoys "decoy1.txt,decoy2.pdf,decoy3.jpg" \
  --password "MyPassword" \
  -o encrypted.hcrypt
```

### Decryption

Decrypt an encrypted file using any valid password.

```bash
./honeycrypt decrypt \
  --input <encrypted_file> \
  --password <password> \
  [--output <output_file>] \
  [--quiet]
```

**Options:**
- `--input, -i` (required) - Path to the encrypted file
- `--password, -p` (required) - Password to decrypt the file
- `--output, -o` (optional) - Output file path (default: `<input>_decrypted`)
- `--quiet, -q` (optional) - Suppress verbose output

**Example:**
```bash
./honeycrypt decrypt \
  --input encrypted.hcrypt \
  --password "MyPassword" \
  --output decrypted.pdf
```

## Features

### Automatic Compression

HoneyCrypt automatically compresses files using zlib if compression reduces file size by at least 5%. Compression is lossless and transparent - decryption automatically decompresses the data.

**CLI Output:**
```
ℹ Real file compressed: 42.3% savings
ℹ Decoy file: no compression benefit
```

### Self-Destruct Password

The self-destruct feature allows you to specify a special password that will permanently destroy the encrypted file if entered. This provides "panic button" functionality.

**Warning:** Self-destruct is PERMANENT and irreversible. The file is overwritten with 100-200 passes of random data.

**Example:**
```bash
./honeycrypt encrypt \
  --real secret.txt \
  --decoy fake.txt \
  -p "realpass" \
  --self-destruct "panicpass"
```

### Padding

Padding adds random data to the encrypted file to reach a target size. This is useful for:
- Hiding the true size of your data
- Meeting specific file size requirements
- Avoiding size-based analysis

**Example (target 100 MB):**
```bash
./honeycrypt encrypt \
  --real small_file.txt \
  --decoy decoy.txt \
  -p "pass" \
  --pad 100
```

### Plausible Deniability

HoneyCrypt's core feature is plausible deniability:
- Each encrypted file contains multiple versions (real + decoys)
- Different passwords decrypt to different files
- No way to prove which password decrypts the "real" data
- Decoy passwords are generated automatically (or can be specified in multi-decoy mode)

**Standard mode:** 1 real file + 2 decoy passwords (3 total possibilities)
**Multi-decoy mode:** 1 real file + 1-5 decoy files (2-6 total possibilities)

## Exit Codes

- `0` - Success
- `1` - Error (file not found, encryption/decryption failed, invalid input)
- `130` - Interrupted by user (Ctrl+C)

## Examples

### Complete Workflow

```bash
# 1. Create test files
echo "Secret data" > secret.txt
echo "Fake data" > fake.txt

# 2. Encrypt with standard mode
./honeycrypt encrypt \
  --real secret.txt \
  --decoy fake.txt \
  -p "mypassword" \
  -o encrypted.hcrypt

# Output shows generated decoy passwords:
# ℹ Generated decoy password 1: princess8370
# ℹ Generated decoy password 2: Vertex^378Quantum

# 3. Decrypt with real password
./honeycrypt decrypt \
  -i encrypted.hcrypt \
  -p "mypassword" \
  -o decrypted_real.txt

# 4. Decrypt with decoy password
./honeycrypt decrypt \
  -i encrypted.hcrypt \
  -p "princess8370" \
  -o decrypted_fake.txt
```

### Scripting Example

```bash
#!/bin/bash
# Batch encrypt multiple files

for file in *.pdf; do
    ./honeycrypt encrypt \
        --real "$file" \
        --decoy "template_decoy.pdf" \
        --password "SecurePass123" \
        --output "${file}.hcrypt" \
        --quiet
    
    if [ $? -eq 0 ]; then
        echo "✓ Encrypted: $file"
    else
        echo "✗ Failed: $file"
    fi
done
```

### With Environment Variables

```bash
# Store password in environment variable
export HCRYPT_PASSWORD="MySecurePassword"

# Use in script
./honeycrypt encrypt \
  --real data.txt \
  --decoy fake.txt \
  -p "$HCRYPT_PASSWORD"
```

## Security Considerations

### Password Security

- Use strong passwords (12+ characters, mixed case, numbers, symbols)
- Never store passwords in plain text files
- Consider using a password manager
- Self-destruct passwords should be memorized, not written down

### File Handling

- Securely delete original files after encryption
- Be aware of filesystem journaling and backups
- Consider using encrypted storage for sensitive files
- Use the `shred` command on Linux to securely delete files:
  ```bash
  shred -vfz -n 10 original_file.txt
  ```

### Key Derivation

HoneyCrypt uses Argon2id for key derivation:
- Memory-hard algorithm (resistant to GPU cracking)
- ~500ms derivation time on modern CPUs
- Intentionally slow to prevent brute-force attacks

## Troubleshooting

### "Error: stable1.0.py not found"

Ensure `honeycrypt_cli.py` is in the same directory as `stable1.0.py`.

### "No module named 'Crypto'"

Install PyCryptodome:
```bash
pip install pycryptodome
```

### "Failed to import HoneyCrypt modules"

Install required dependencies:
```bash
pip install pycryptodome argon2-cffi
```

### Decryption fails with correct password

- Check if self-destruct was triggered (file may be corrupted/wiped)
- Verify the encrypted file is not corrupted
- Ensure you're using the correct password

## Version History

### v1.0 (February 2026)
- Initial CLI implementation
- Standard 2-decoy encryption
- Multi-decoy encryption (1-5 decoys)
- Self-destruct password support
- Padding support
- Automatic compression
- Quiet mode
- Argon2id key derivation

## License

See main HoneyCrypt license.

## Support

For issues, questions, or contributions, please refer to the main HoneyCrypt repository.
