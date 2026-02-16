# 🔒 HoneyCrypt v1.0

**Plausible Deniability Encryption** - AES-GCM encryption with multiple decoy files

HoneyCrypt provides military-grade encryption with a unique twist: plausible deniability. When decrypting, different passwords reveal different files - making it impossible for an attacker to know if they've found the "real" file or just a decoy.

## 🌟 Features

- **🎭 Plausible Deniability** - Multiple passwords, each reveals a different file
- **🔐 Military-Grade Encryption** - AES-256-GCM with Argon2id key derivation
- **🗜️ Smart Compression** - Automatic zlib compression (only if >5% reduction)
- **📦 Custom Padding** - Add random padding to disguise file size
- **💥 Self-Destruct** - Optional password that securely wipes the file
- **🎨 GUI & CLI** - Full-featured desktop app and command-line interface
- **🌐 Cross-Platform** - Windows, Linux, macOS

## 🔧 Technical Details

- **Encryption**: AES-256-GCM (256-bit key, 96-bit nonce, 128-bit tag)
- **Key Derivation**: Argon2id (time_cost=3, memory_cost=65536, parallelism=4)
- **Compression**: zlib level 9 (applied only if saves >5%)
- **File Format**: Custom `.hcrypt` format with version byte (v0x03)
- **Security**: Each file has unique salt, nonce, and padding

## 📥 Installation

### Desktop Application (GUI)

**Windows:**
1. Download `HoneyCrypt.exe` from [Releases](https://github.com/adikul1023/honeycrypt/releases)
2. Run the executable (no installation needed)

**From Source:**
```bash
# Clone repository
git clone https://github.com/adikul1023/honeycrypt.git
cd honeycrypt

# Install dependencies
pip install argon2-cffi

# Run GUI application
python stable1.0.py
```

### Command-Line Interface (CLI)

**Linux/macOS:**
```bash
# Make the wrapper executable
chmod +x honeycrypt

# Run CLI
./honeycrypt --help
```

**Windows (PowerShell):**
```powershell
# Run CLI
.\honeycrypt.ps1 --help
```

**Windows (CMD):**
```cmd
honeycrypt.bat --help
```

**Direct Python:**
```bash
python honeycrypt_cli.py --help
```

## 🎯 Quick Start

### Desktop GUI

1. **Standard Encryption** (2 decoys):
   - Select real file and one decoy file
   - Enter password for real file
   - Two fake passwords are auto-generated
   
2. **Multi-Decoy Encryption** (up to 5 decoys):
   - Select real file
   - Add multiple decoy files with custom passwords
   - More realistic plausible deniability

3. **Decryption**:
   - Select encrypted `.hcrypt` file
   - Enter any password (real or decoy)
   - You'll get back the corresponding file

### CLI Usage

**Standard Encryption:**
```bash
# Linux/macOS
./honeycrypt --encrypt secret.pdf fake.txt

# Windows PowerShell
.\honeycrypt.ps1 --encrypt secret.pdf fake.txt

# Direct Python (cross-platform)
python honeycrypt_cli.py --encrypt secret.pdf fake.txt
```
Password will be prompted (hidden input). Outputs:
- Encrypted file: `secret.pdf.hcrypt`
- Two auto-generated fake passwords

**Multi-Decoy Encryption:**
```bash
# Interactive mode - prompts for multiple decoy files
./honeycrypt --multiencrypt secret.pdf
```

**Decryption:**
```bash
./honeycrypt --decrypt secret.pdf.hcrypt
```

**CLI Options:**
- `--help` - Show help message
- `--version` - Show version
- `--encrypt REAL DECOY` - Standard 2-decoy encryption
- `--multiencrypt REAL` - Multi-decoy encryption (interactive)
- `--decrypt FILE` - Decrypt any `.hcrypt` file

## 🔐 How Plausible Deniability Works

When you encrypt with HoneyCrypt:

1. **Real file** gets password A → decrypts to your actual secret
2. **Decoy file** gets password B → decrypts to innocuous fake data
3. Both are merged into one `.hcrypt` file

**Under duress scenario:**
- Attacker: "Decrypt this file!"
- You: *enters decoy password B*
- Result: Decoy file appears, looks legitimate
- Attacker has **no way to know** if there's another password

The encryption format makes it cryptographically impossible to determine:
- How many passwords exist
- Which password is "real"
- If you've revealed all passwords

## ⚙️ Advanced Features

### Custom Padding
Add random padding to disguise file size:
- Useful if attacker knows approximate size of target file
- GUI: Enter target size in MB
- Padding is cryptographically random data

### Self-Destruct Password
Optional password that **permanently destroys** the file:
- GUI: Enable in options
- 100-200 random write passes
- **WARNING**: Unrecoverable deletion
- Use case: Emergency "panic button"

### Compression Statistics
- Shows original size vs final size
- Displays compression ratio and bytes saved
- Automatically compresses only if beneficial (>5%)

## 🛡️ Security Considerations

**✅ What HoneyCrypt Protects Against:**
- Brute-force attacks (Argon2id is memory-hard)
- Known-plaintext attacks (AES-GCM with unique nonces)
- File size analysis (custom padding)
- Coerced decryption (plausible deniability)

**⚠️ What HoneyCrypt Does NOT Protect Against:**
- Keyloggers (they see your real password)
- Rubber-hose cryptanalysis (physical torture)
- Compromised system (malware can steal keys)
- Side-channel attacks (timing, power analysis)

**Best Practices:**
- Use **strong, unique passwords** (20+ characters)
- Make decoy files **realistic and believable**
- **Never** reveal the existence of multiple passwords
- Use full-disk encryption (BitLocker/LUKS) as first layer
- Keep software updated

## 🏗️ File Format (v0x03)

```
[Version: 1 byte = 0x03]
[Compression Flag: 1 byte]
[Real Salt: 32 bytes]
[Fake1 Salt: 32 bytes]
[Fake2 Salt: 32 bytes]
[Self-Destruct Salt: 32 bytes (if enabled)]
[Real Length: 8 bytes]
[Fake1 Length: 8 bytes]
[Fake2 Length: 8 bytes]
[Encrypted Data: variable]
[Random Padding: variable]
```

**Format Features:**
- Version byte allows future format changes
- Each layer has unique salt (prevents rainbow tables)
- Lengths are encrypted separately for each layer
- Self-destruct option adds additional salt
- Padding is cryptographically random

## 🧪 Testing

```bash
# Test encryption and decryption
# Create test files
echo "Secret data" > test_real.txt
echo "Fake data" > test_fake.txt

# Encrypt
./honeycrypt --encrypt test_real.txt test_fake.txt
# Enter password when prompted

# Decrypt with real password
./honeycrypt --decrypt test_real.txt.hcrypt
# Enter real password → get "Secret data"

# Decrypt with fake password
./honeycrypt --decrypt test_real.txt.hcrypt
# Enter fake password → get "Fake data"
```

## 📋 Requirements

- **Python**: 3.7 or higher
- **Dependencies**: 
  - `argon2-cffi` (key derivation)
  - `tkinter` (GUI only, usually pre-installed)
  
**Install dependencies:**
```bash
pip install argon2-cffi
```

## 🌍 Cross-Platform Compatibility

Files encrypted on any platform can be decrypted on any other:
- Windows ↔️ Linux ↔️ macOS
- Desktop GUI ↔️ CLI ↔️ Web version
- All use identical encryption format (v0x03)

## 📦 Repository Structure

```
honeycrypt/
├── stable1.0.py          # Desktop GUI application
├── honeycrypt_cli.py     # Cross-platform CLI
├── honeycrypt            # Linux/macOS wrapper (bash)
├── honeycrypt.ps1        # Windows PowerShell wrapper
├── honeycrypt.bat        # Windows CMD wrapper
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── LICENSE               # License file
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

**Areas for contribution:**
- Additional platform support
- Performance optimization
- UI/UX improvements
- Documentation
- Testing

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Key Points:**
- ✅ Free to use, modify, and distribute
- ✅ Commercial use allowed
- ✅ No warranty provided
- ⚠️ Must include copyright notice

## ⚠️ Disclaimer

This software is provided for educational and legitimate privacy purposes only. Users are responsible for compliance with local laws regarding encryption and data privacy. The authors assume no liability for misuse.

**Remember:** 
- Plausible deniability is not absolute
- Strong operational security is essential
- Use at your own risk

## 🔗 Links

- **Desktop App Repository**: [github.com/adikul1023/honeycrypt](https://github.com/adikul1023/honeycrypt)
- **Web Version**: [github.com/adikul1023/honaes](https://github.com/adikul1023/honaes)
- **Issues**: [Report bugs or request features](https://github.com/adikul1023/honeycrypt/issues)

## 💬 Support

If you encounter issues:
1. Check this README first
2. Search existing [GitHub Issues](https://github.com/adikul1023/honeycrypt/issues)
3. Create a new issue with:
   - Your OS and Python version
   - Steps to reproduce
   - Error messages (if any)

---

**Made with 🔐 by the adikul1023**

*"Privacy is not about having something to hide. Privacy is about having something to protect."*
