# HoneyCrypt CLI - Simple Interactive Interface

## Quick Start

### Installation
```bash
pip install pycryptodome argon2-cffi
chmod +x honeycrypt
```

## Usage

### 1. Standard Encryption (2 decoys auto-generated)

**Command:**
```bash
./honeycrypt --encrypt <real_file> <decoy_file>
```

**Example:**
```bash
./honeycrypt --encrypt secret.pdf fake.pdf
```

Then you'll be prompted:
```
Enter password for the real file:
Password: ********
```

**Output:**
- Creates: `secret.pdf.hcrypt`
- Shows 2 generated decoy passwords (save these!)

---

### 2. Decryption  

**Command:**
```bash
./honeycrypt --decrypt <file.hcrypt>
```

**Example:**
```bash
./honeycrypt --decrypt secret.pdf.hcrypt
```

Then you'll be prompted:
```
Enter password to decrypt:
Password: ********
```

**Output:**
- Creates: `secret.pdf_decrypted`
- Shows whether it was REAL or DECOY file

---

### 3. Multi-Decoy Encryption (interactive)

**Command:**
```bash
./honeycrypt --multiencrypt <real_file>
```

**Example:**
```bash
./honeycrypt --multiencrypt important.doc
```

**Interactive prompts:**
```
Enter password for the real file:
Password: ********

--- Decoy File 1 ---
Enter decoy file path: decoy1.txt
Enter password for decoy file 1:
Password: ********
Do you want to add another decoy file? (yes/no): yes

--- Decoy File 2 ---
Enter decoy file path: decoy2.pdf
Enter password for decoy file 2:
Password: ********
Do you want to add another decoy file? (yes/no): no
```

**Output:**
- Creates: `important.doc.hcrypt`
- Up to 5 decoy files supported

---

## Features

✅ **Hidden Password Input** - Passwords are never shown on screen  
✅ **Automatic File Naming** - Output files named `<input>.hcrypt`  
✅ **Interactive** - Prompts guide you through the process  
✅ **Simple Commands** - Just 3 commands to remember  
✅ **Plausible Deniability** - Different passwords decrypt to different files  

## Security Notes

- **Argon2id encryption** - Very secure, slow key derivation
- **Automatic compression** - Reduces file size when beneficial
- **Decoy passwords** - Generated passwords look realistic
- **No history** - Passwords aren't stored in command history

## Tips

1. **Save decoy passwords** - Write them down after encryption
2. **Use strong passwords** - Mix upper/lower/numbers/symbols
3. **Test first** - Try with non-sensitive files first
4. **Secure deletion** - Delete original files securely:
   ```bash
   shred -vfz -n 10 original_file.txt
   ```

## Full Example Workflow

```bash
# 1. Encrypt your secret file
./honeycrypt --encrypt secret.txt fake.txt
# Enter password: MySecretPass123
# Save the displayed decoy passwords!

# 2. Delete original files securely
shred -vfz secret.txt fake.txt

# 3. Later, decrypt with your password
./honeycrypt --decrypt secret.txt.hcrypt
# Enter password: MySecretPass123
# Output: secret.txt_decrypted (your real file)

# 4. Or decrypt with decoy password
./honeycrypt --decrypt secret.txt.hcrypt
# Enter decoy password: sunshine1975
# Output: secret.txt_decrypted (fake file)
```

## Version
HoneyCrypt CLI v1.0 (February 2026)
