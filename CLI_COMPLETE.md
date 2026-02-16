# HoneyCrypt CLI - Complete Implementation ✅

## Summary

The HoneyCrypt CLI has been **simplified** to be extremely user-friendly with interactive password prompts and hidden input.

## 🎯 Three Simple Commands

### 1. Encrypt (Standard)
```bash
./honeycrypt --encrypt FILE1 FILE2
```
- FILE1 = real file
- FILE2 = decoy file
- Prompts for password (hidden)
- Auto-generates 2 decoy passwords

### 2. Decrypt
```bash
./honeycrypt --decrypt FILE.hcrypt
```
- Prompts for password (hidden)
- Shows if REAL or DECOY
- Auto-names output file

### 3. Multi-Encrypt (Interactive)
```bash
./honeycrypt --multiencrypt FILE1
```
- Prompts for password (hidden)
- Interactive loop adds decoys:
  - Enter file path
  - Enter password
  - "Add another?" → repeat or done
- Max 5 decoys

## ✨ Key Features

✅ **Hidden Passwords** - No passwords shown/stored in history  
✅ **Interactive** - Prompts guide you through process  
✅ **Simple** - Only 3 commands to remember  
✅ **Automatic** - File naming handled automatically  
✅ **Secure** - Same Argon2id encryption as GUI  

## 📁 Files

**Main:**
- `honeycrypt` - Wrapper script (executable)
- `honeycrypt_cli.py` - CLI implementation (~350 lines)
- `stable1.0.py` - Core encryption engine

**Documentation:**
- `SIMPLE_CLI_GUIDE.md` - **START HERE** - User guide
- `CLI_DEMO.sh` - Usage demo script
- `SIMPLIFIED_CLI_CHANGELOG.md` - What changed
- `CLI_README.md` - Advanced reference (old version)
- `CLI_QUICKREF.md` - Quick reference card

## 🚀 Quick Start

```bash
# 1. Install dependencies (one-time)
pip install pycryptodome argon2-cffi

# 2. Make executable (one-time)
chmod +x honeycrypt

# 3. Encrypt a file
./honeycrypt --encrypt secret.txt fake.txt
# Enter password: ******** (hidden)
# ✓ Done! Saves: secret.txt.hcrypt

# 4. Decrypt
./honeycrypt --decrypt secret.txt.hcrypt
# Enter password: ******** (hidden)
# ✓ Done! Saves: secret.txt_decrypted
```

## 📖 Documentation

**For Users:**
- **[SIMPLE_CLI_GUIDE.md](SIMPLE_CLI_GUIDE.md)** - Complete user guide
- **[CLI_DEMO.sh](CLI_DEMO.sh)** - See example output

**For Developers:**
- [SIMPLIFIED_CLI_CHANGELOG.md](SIMPLIFIED_CLI_CHANGELOG.md) - Changes made
- [CLI_IMPLEMENTATION.md](CLI_IMPLEMENTATION.md) - Technical details
- [CLI_README.md](CLI_README.md) - Advanced reference

## 🎬 Demo

Run the demo to see example output:
```bash
./CLI_DEMO.sh
```

## ✅ Status

**COMPLETE** - Ready to use!

- ✅ Standard encryption
- ✅ Multi-decoy encryption
- ✅ Decryption
- ✅ Hidden password input
- ✅ Interactive prompts
- ✅ Automatic file naming
- ✅ Error handling
- ✅ Documentation
- ✅ Tested and working

## 🔒 Security

- **Argon2id** key derivation (~500ms)
- **AES-256** encryption
- **Plausible deniability** - different passwords = different files
- **No password storage** - getpass hides input
- **Auto compression** - reduces file size

## 📋 Example Session

```bash
$ ./honeycrypt --encrypt document.pdf dummy.pdf

[HONEYCRYPT] Standard Encryption

Enter password for the real file:
Password: ********

[READ] Reading real file: document.pdf
[READ] Reading decoy file: dummy.pdf
ℹ Real file size: 1.23 MB
ℹ Decoy file size: 856.00 KB

[ENCRYPT] Encrypting data...
[WRITE] Writing encrypted file: document.pdf.hcrypt

✓ Encryption complete!

ℹ Output file: document.pdf.hcrypt
ℹ Final size: 1.30 MB

ℹ Generated decoy passwords (save these!):
ℹ   Decoy password 1: butterfly2024
ℹ   Decoy password 2: Phoenix#523Thunder
```

## 🎓 Version

**HoneyCrypt CLI v1.0** (February 2026)

---

**For complete usage guide, see: [SIMPLE_CLI_GUIDE.md](SIMPLE_CLI_GUIDE.md)**
