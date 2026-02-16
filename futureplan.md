# HoneyCrypt - Future Features Roadmap

This document tracks planned features for future versions of HoneyCrypt.

## Priority: High
Features that would significantly improve security or usability.

### 1. File Preview in FileSelector
**Status:** Planned  
**Description:** Show file info when selecting files
- Display: filename, size, type, estimated compressed size
- Preview thumbnail for images
- Drag-and-drop support for file selection

**Implementation Notes:**
- Extend FileSelector class with preview panel
- Use PIL for image thumbnails
- Add drag-drop event bindings (`<Drop>` event)
- Call `CompressionService.estimate_compressed_size()` for size prediction

---

## Priority: Medium
Nice-to-have features that improve user experience.

### 2. Command-Line Interface (CLI)
**Status:** Deferred  
**Description:** Non-interactive CLI for scripting and automation

**Proposed Command Structure:**
```bash
# Standard encryption
honeycrypt encrypt --real file.txt --decoy decoy.txt --password "pass" --output encrypted.hcrypt

# With self-destruct
honeycrypt encrypt --real secret.pdf --decoy fake.pdf -p "mainpass" --self-destruct "destroypass" -o out.hcrypt

# With padding
honeycrypt encrypt --real data.bin --decoy fake.bin -p "pass" --pad 100 -o out.hcrypt

# Multi-decoy encryption
honeycrypt encrypt-multi --real important.doc --decoys "d1.txt,d2.pdf,d3.jpg" -p "pass" -o out.hcrypt

# Decryption
honeycrypt decrypt --input encrypted.hcrypt --password "pass" --output decrypted.txt
```

**Implementation Notes:**
- Use `argparse` for argument parsing
- Call existing `EncryptionService` and `DecryptionService` methods
- Progress output with optional `--quiet` flag
- Return appropriate exit codes (0 = success, 1 = failure)

---

## Priority: Low
Advanced features for power users.

### 3. Split File Encryption
**Status:** Concept  
**Description:** Split large files into multiple encrypted chunks
- Useful for cloud storage limits (e.g., 100MB max)
- All chunks required for decryption (RAID-like)
- Each chunk encrypted separately with same password

**Use Case:** Encrypt a 500MB file into 5x 100MB chunks for email attachments

### 4. Encrypted Container Files
**Status:** Concept  
**Description:** Create encrypted container files (like TrueCrypt volumes)
- Mount as virtual drive
- Multiple files inside one container
- Plausible deniability: hidden volume inside container

**Technical Challenges:**
- Windows: Dokan library for virtual drives
- Linux: FUSE filesystem
- Complex implementation, high maintenance

---

## Completed Features (v0.9)

✅ **zlib Compression** - Lossless compression with >5% threshold  
✅ **Custom Padding** - User-specified final file size with random padding  
✅ **Argon2id KDF** - Replaced PBKDF2 with Argon2id (memory-hard, GPU-resistant)  
✅ **Self-Destruct Password** - Optional password that securely wipes the file (100-200 random passes)  
✅ **Compression Statistics** - Show compression results in UI  
✅ **Format Version 0x03** - New format with version byte, compression flags, self-destruct support  
✅ **Password Strength Meter** - Real-time visual strength indicator with color-coded bar (red/yellow/green)  
✅ **Password Visibility Toggle** - Eye icon (👁/🚫) to show/hide password text in all password fields

---

## Notes

- **Backward Compatibility:** v0x02 and earlier formats are NO LONGER SUPPORTED starting from v0.9
- **Self-Destruct Warning:** Always warn users prominently about self-destruct - it's PERMANENT
- **Argon2id Performance:** ~500ms for key derivation on modern CPUs (intentionally slow)
- **Security:** All new features maintain plausible deniability core principle

---

**Last Updated:** February 2026  
**Current Stable Version:** test0.9
