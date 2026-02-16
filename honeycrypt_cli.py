#!/usr/bin/env python3
"""
HoneyCrypt CLI - Command-Line Interface for HoneyCrypt
Simple interactive CLI with hidden password input
Cross-platform: Linux, Windows, macOS
"""

import argparse
import sys
import os
import getpass
import platform
import importlib.util

# Import core services from stable1.0.py
# Using importlib to handle the dot in the filename
def import_honeycrypt_modules():
    """Import modules from stable1.0.py using importlib"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    module_path = os.path.join(script_dir, 'stable1.0.py')
    
    if not os.path.exists(module_path):
        print("Error: stable1.0.py not found in the same directory.", file=sys.stderr)
        print(f"Expected location: {module_path}", file=sys.stderr)
        sys.exit(1)
    
    # Load the module
    spec = importlib.util.spec_from_file_location("honeycrypt_core", module_path)
    if spec is None or spec.loader is None:
        print("Error: Failed to load stable1.0.py module.", file=sys.stderr)
        sys.exit(1)
    
    module = importlib.util.module_from_spec(spec)
    sys.modules["honeycrypt_core"] = module
    spec.loader.exec_module(module)
    
    return module

# Import the module
try:
    honeycrypt = import_honeycrypt_modules()
    EncryptionService = honeycrypt.EncryptionService
    DecryptionService = honeycrypt.DecryptionService
    CompressionService = honeycrypt.CompressionService
    CryptoEngine = honeycrypt.CryptoEngine
    PasswordGenerator = honeycrypt.PasswordGenerator
    SelfDestructService = honeycrypt.SelfDestructService
except Exception as e:
    print(f"Error: Failed to import HoneyCrypt modules: {str(e)}", file=sys.stderr)
    sys.exit(1)


class CLIProgress:
    """Simple progress indicator for CLI with cross-platform symbol support"""
    
    # Detect if we can use Unicode symbols (Linux/macOS or Windows with UTF-8 support)
    _use_unicode = (
        platform.system() != 'Windows' or 
        (hasattr(sys.stdout, 'encoding') and sys.stdout.encoding.lower().startswith('utf'))
    )
    
    # Symbol sets for different platforms
    _symbols = {
        'success': '✓' if _use_unicode else '[OK]',
        'error': '✗' if _use_unicode else '[ERROR]',
        'info': 'ℹ' if _use_unicode else '[i]'
    }
    
    @staticmethod
    def show(message, stage=None):
        """Show progress message"""
        if stage:
            print(f"[{stage}] {message}")
        else:
            print(message)
    
    @staticmethod
    def success(message):
        """Show success message"""
        symbol = CLIProgress._symbols['success']
        print(f"{symbol} {message}")
    
    @staticmethod
    def error(message):
        """Show error message"""
        symbol = CLIProgress._symbols['error']
        print(f"{symbol} Error: {message}", file=sys.stderr)
    
    @staticmethod
    def info(message):
        """Show info message"""
        symbol = CLIProgress._symbols['info']
        print(f"{symbol} {message}")


def validate_file_exists(filepath, file_type="File"):
    """Validate that a file exists (cross-platform path handling)"""
    # Normalize path for the current platform
    filepath = os.path.normpath(filepath)
    
    if not os.path.exists(filepath):
        CLIProgress.error(f"{file_type} not found: {filepath}")
        sys.exit(1)
    if not os.path.isfile(filepath):
        CLIProgress.error(f"{file_type} is not a regular file: {filepath}")
        sys.exit(1)
    
    return filepath


def validate_password(password, allow_empty=False):
    """Validate password"""
    if not allow_empty and not password:
        CLIProgress.error("Password cannot be empty")
        sys.exit(1)
    return password


def format_size(size_bytes):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def encrypt_standard(real_file, decoy_file):
    """Handle standard encryption with interactive password prompt"""
    CLIProgress.show("Standard Encryption", "HONEYCRYPT")
    print()
    
    # Validate inputs and normalize paths
    real_file = validate_file_exists(real_file, "Real file")
    decoy_file = validate_file_exists(decoy_file, "Decoy file")
    
    # Prompt for password (hidden input)
    print("Enter password for the real file:")
    password = getpass.getpass("Password: ")
    validate_password(password)
    
    # Read files
    try:
        CLIProgress.show(f"Reading real file: {real_file}", "READ")
        with open(real_file, 'rb') as f:
            real_data = f.read()
        
        CLIProgress.show(f"Reading decoy file: {decoy_file}", "READ")
        with open(decoy_file, 'rb') as f:
            decoy_data = f.read()
    except Exception as e:
        CLIProgress.error(f"Failed to read input files: {str(e)}")
        sys.exit(1)
    
    # Show file info
    CLIProgress.info(f"Real file size: {format_size(len(real_data))}")
    CLIProgress.info(f"Decoy file size: {format_size(len(decoy_data))}")
    print()
    
    # Perform encryption
    try:
        CLIProgress.show("Encrypting data...", "ENCRYPT")
        filename = os.path.basename(real_file)
        
        encrypted_data, fake_pass1, fake_pass2, comp_stats = EncryptionService.encrypt_standard(
            real_data,
            decoy_data,
            password,
            filename,
            padding_target_mb=0,
            selfdestruct_password=None
        )
        
        # Write output file
        output_file = f"{real_file}.hcrypt"
        CLIProgress.show(f"Writing encrypted file: {output_file}", "WRITE")
        
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)
        
        print()
        CLIProgress.success(f"Encryption complete!")
        print()
        CLIProgress.info(f"Output file: {output_file}")
        CLIProgress.info(f"Final size: {format_size(len(encrypted_data))}")
        print()
        CLIProgress.info("Generated decoy passwords (save these!):")
        CLIProgress.info(f"  Decoy password 1: {fake_pass1}")
        CLIProgress.info(f"  Decoy password 2: {fake_pass2}")
        print()
        return 0
        
    except Exception as e:
        CLIProgress.error(f"Encryption failed: {str(e)}")
        sys.exit(1)


def decrypt_file(encrypted_file):
    """Handle decryption with interactive password prompt"""
    CLIProgress.show("Decryption", "HONEYCRYPT")
    print()
    
    # Validate input and normalize path
    encrypted_file = validate_file_exists(encrypted_file, "Encrypted file")
    
    # Prompt for password (hidden input)
    print("Enter password to decrypt:")
    password = getpass.getpass("Password: ")
    validate_password(password)
    
    # Read encrypted file
    try:
        CLIProgress.show(f"Reading encrypted file: {encrypted_file}", "READ")
        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()
        
        CLIProgress.info(f"Encrypted file size: {format_size(len(encrypted_data))}")
        print()
    
    except Exception as e:
        CLIProgress.error(f"Failed to read encrypted file: {str(e)}")
        sys.exit(1)
    
    # Perform decryption
    try:
        CLIProgress.show("Decrypting data...", "DECRYPT")
        
        decrypted_data, is_real = DecryptionService.decrypt_unified(
            encrypted_data,
            password,
            file_path=encrypted_file
        )
        
        if decrypted_data is None:
            CLIProgress.error("Decryption failed - incorrect password or corrupted file")
            sys.exit(1)
        
        # Determine output filename
        base_name = encrypted_file
        if base_name.endswith('.hcrypt'):
            output_file = base_name[:-7] + '_decrypted'
        else:
            output_file = base_name + '_decrypted'
        
        # Write decrypted file
        CLIProgress.show(f"Writing decrypted file: {output_file}", "WRITE")
        
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        print()
        CLIProgress.success(f"Decryption complete!")
        print()
        CLIProgress.info(f"Output file: {output_file}")
        CLIProgress.info(f"Decrypted size: {format_size(len(decrypted_data))}")
        if is_real is not None:
            file_type = "REAL file" if is_real else "DECOY file"
            CLIProgress.info(f"Type: {file_type}")
        print()
        return 0
        
    except Exception as e:
        CLIProgress.error(f"Decryption failed: {str(e)}")
        sys.exit(1)


def encrypt_multi(real_file):
    """Handle multi-decoy encryption with interactive prompts"""
    CLIProgress.show("Multi-Decoy Encryption", "HONEYCRYPT")
    print()
    
    # Validate input and normalize path
    real_file = validate_file_exists(real_file, "Real file")
    
    # Prompt for real file password
    print("Enter password for the real file:")
    password = getpass.getpass("Password: ")
    validate_password(password)
    print()
    
    # Read real file
    try:
        CLIProgress.show(f"Reading real file: {real_file}", "READ")
        with open(real_file, 'rb') as f:
            real_data = f.read()
        CLIProgress.info(f"Real file size: {format_size(len(real_data))}")
        print()
    except Exception as e:
        CLIProgress.error(f"Failed to read real file: {str(e)}")
        sys.exit(1)
    
    # Interactive loop to add decoy files
    decoy_files = []
    decoy_count = 1
    
    while True:
        if decoy_count > 5:
            CLIProgress.error("Maximum 5 decoy files allowed")
            break
        
        print(f"--- Decoy File {decoy_count} ---")
        decoy_path = input("Enter decoy file path: ").strip()
        
        if not decoy_path:
            CLIProgress.error("File path cannot be empty")
            continue
        
        decoy_path = validate_file_exists(decoy_path, f"Decoy file {decoy_count}")
        
        # Read decoy file
        try:
            with open(decoy_path, 'rb') as f:
                decoy_data = f.read()
            CLIProgress.info(f"Decoy {decoy_count} size: {format_size(len(decoy_data))}")
        except Exception as e:
            CLIProgress.error(f"Failed to read decoy file: {str(e)}")
            continue
        
        # Prompt for decoy password
        print(f"Enter password for decoy file {decoy_count}:")
        decoy_password = getpass.getpass("Password: ")
        validate_password(decoy_password)
        
        decoy_files.append({
            'data': decoy_data,
            'password': decoy_password
        })
        
        print()
        
        # Ask if want to add another
        if decoy_count >= 5:
            print("Maximum number of decoy files reached (5)")
            break
        
        response = input("Do you want to add another decoy file? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            break
        
        print()
        decoy_count += 1
    
    if len(decoy_files) == 0:
        CLIProgress.error("At least one decoy file is required")
        sys.exit(1)
    
    # Perform encryption
    try:
        print()
        CLIProgress.show("Encrypting data...", "ENCRYPT")
        filename = os.path.basename(real_file)
        
        encrypted_data, comp_stats = EncryptionService.encrypt_multi_decoy(
            real_data,
            decoy_files,
            password,
            filename,
            padding_target_mb=0,
            selfdestruct_password=None
        )
        
        # Write output file
        output_file = f"{real_file}.hcrypt"
        CLIProgress.show(f"Writing encrypted file: {output_file}", "WRITE")
        
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)
        
        print()
        CLIProgress.success(f"Multi-decoy encryption complete!")
        print()
        CLIProgress.info(f"Output file: {output_file}")
        CLIProgress.info(f"Final size: {format_size(len(encrypted_data))}")
        CLIProgress.info(f"Total files: 1 real + {len(decoy_files)} decoys")
        print()
        return 0
        
    except Exception as e:
        CLIProgress.error(f"Encryption failed: {str(e)}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='honeycrypt',
        description='HoneyCrypt - Plausible Deniability Encryption',
        epilog='Simple interactive encryption with hidden password entry'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='HoneyCrypt CLI v1.0'
    )
    
    # Create mutually exclusive group for actions
    action_group = parser.add_mutually_exclusive_group(required=True)
    
    action_group.add_argument(
        '--encrypt',
        nargs=2,
        metavar=('REAL_FILE', 'DECOY_FILE'),
        help='Encrypt files (standard 2-decoy mode)'
    )
    
    action_group.add_argument(
        '--decrypt',
        metavar='FILE.hcrypt',
        help='Decrypt an encrypted file'
    )
    
    action_group.add_argument(
        '--multiencrypt',
        metavar='REAL_FILE',
        help='Multi-decoy encryption (interactive)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.encrypt:
        real_file, decoy_file = args.encrypt
        return encrypt_standard(real_file, decoy_file)
    elif args.decrypt:
        return decrypt_file(args.decrypt)
    elif args.multiencrypt:
        return encrypt_multi(args.multiencrypt)
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)
