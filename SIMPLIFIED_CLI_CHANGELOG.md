# HoneyCrypt CLI - Simplified Version

## What Changed

The CLI has been **completely simplified** to be more user-friendly with interactive password prompts.

### Before (Complex)
```bash
# Required all arguments upfront
./honeycrypt encrypt --real file.txt --decoy fake.txt --password "pass" --output out.hcrypt

# Many confusing options
--password, --output, --self-destruct, --pad, --quiet, etc.
```

### After (Simple) ✨
```bash
# Just specify files, password prompted interactively
./honeycrypt --encrypt file.txt fake.txt
# Then prompted: Password: ******** (hidden)

# Only 3 commands total
--encrypt, --decrypt, --multiencrypt
```

## New Usage

### 1. Encrypt (Standard Mode)
```bash
./honeycrypt --encrypt <real_file> <decoy_file>
```
- Prompts for password (hidden input)
- Automatically generates 2 decoy passwords
- Output: `<real_file>.hcrypt`

### 2. Decrypt
```bash
./honeycrypt --decrypt <file.hcrypt>
```
- Prompts for password (hidden input)
- Output: `<file>_decrypted`
- Shows if REAL or DECOY

### 3. Multi-Encrypt (Interactive)
```bash
./honeycrypt --multiencrypt <real_file>
```
- Prompts for real file password
- Interactive loop to add decoys:
  - Enter decoy file path
  - Enter decoy password
  - "Add another?" (yes/no)
- Max 5 decoys

## Key Improvements

✅ **Hidden Passwords** - Uses `getpass` module, passwords never shown  
✅ **Interactive** - Guides you through each step  
✅ **Simple** - Only 3 commands instead of complex subcommands  
✅ **No Arguments** - No need to remember `--password`, `--output`, etc.  
✅ **Automatic Naming** - Output files named automatically  
✅ **User-Friendly** - Error messages are clear  

## Technical Changes

### Code Changes
- Added `import getpass` for hidden password input
- Removed all optional arguments (--pad, --self-destruct, --quiet, --output)
- Simplified argparse to use mutually exclusive groups
- Changed from subparsers to simple flags
- Added interactive loop for multi-decoy mode

### Function Signatures
```python
# OLD: def encrypt_standard(args) - args had many fields
# NEW: def encrypt_standard(real_file, decoy_file) - simple parameters

# OLD: def decrypt(args) - complex args object
# NEW: def decrypt_file(encrypted_file) - one parameter

# OLD: def encrypt_multi(args) - CSV decoy list in args
# NEW: def encrypt_multi(real_file) - interactive prompts
```

### Removed Features (Simplification)
- `--pad` - Padding option removed
- `--self-destruct` - Self-destruct removed
- `--quiet` - Always shows output now
- `--output` - Automatic naming only
- All short flags (-p, -o, -q, -i)

Core encryption features are **unchanged**:
- Argon2id encryption
- Automatic compression
- Plausible deniability
- Format v0x03

## Example Workflow

```bash
# 1. Encrypt
$ ./honeycrypt --encrypt secret.txt fake.txt
Enter password for the real file:
Password: ******** (hidden)

✓ Encryption complete!
ℹ Output file: secret.txt.hcrypt
ℹ Generated decoy passwords (save these!):
ℹ   Decoy password 1: sunshine1975
ℹ   Decoy password 2: Cascade&911Cipher

# 2. Decrypt with real password
$ ./honeycrypt --decrypt secret.txt.hcrypt
Enter password to decrypt:
Password: ******** (your real password, hidden)

✓ Decryption complete!
ℹ Output file: secret.txt_decrypted
ℹ Type: REAL file

# 3. Decrypt with decoy password
$ ./honeycrypt --decrypt secret.txt.hcrypt
Enter password to decrypt:
Password: ******** (decoy password, hidden)

✓ Decryption complete!
ℹ Output file: secret.txt_decrypted
ℹ Type: DECOY file
```

## Files Modified

- `honeycrypt_cli.py` - Complete rewrite (~400 lines → ~350 lines simpler)

## Files Created

- `SIMPLE_CLI_GUIDE.md` - New user-friendly documentation
- `CLI_DEMO.sh` - Interactive demo script

## Documentation

See **SIMPLE_CLI_GUIDE.md** for complete user documentation.

The old detailed documentation (CLI_README.md) is kept for reference but the simple guide is now the primary docs.

## Summary

✅ **Much simpler** - 3 commands, no complex arguments  
✅ **More secure** - Passwords never visible in terminal or history  
✅ **Interactive** - Prompts guide the user  
✅ **User-friendly** - Easy to use for non-technical users  
✅ **Same security** - All encryption features preserved  

The CLI is now as simple as requested while maintaining full encryption functionality!
