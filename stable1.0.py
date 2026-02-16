import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import zlib
import re
import hashlib
from argon2 import low_level
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# ═══════════════════════════════════════════════════════════════════════
# THEME CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

class Theme:
    """Centralized theme configuration with glassmorphism-inspired values"""
    
    # Color Palette - Dark Professional
    BG_PRIMARY = "#0a0e27"
    BG_SECONDARY = "#14213d"
    BG_SURFACE = "#1a2238"
    BG_ELEVATED = "#1e2749"
    BG_HOVER = "#252f51"
    
    ACCENT_PRIMARY = "#3d5a80"
    ACCENT_SECONDARY = "#4a6fa5"
    ACCENT_HOVER = "#5d7fb8"
    
    TEXT_PRIMARY = "#e8eaed"
    TEXT_SECONDARY = "#9aa0a6"
    TEXT_DISABLED = "#5f6368"
    
    BORDER_DEFAULT = "#2c3e50"
    BORDER_FOCUS = "#4a6fa5"
    BORDER_ERROR = "#e63946"
    
    SUCCESS = "#06d6a0"
    WARNING = "#ffd166"
    ERROR = "#e63946"
    
    # Spacing (8px grid system)
    SPACE_XS = 4
    SPACE_SM = 8
    SPACE_MD = 16
    SPACE_LG = 24
    SPACE_XL = 32
    SPACE_XXL = 48
    
    # Border Radius
    RADIUS_SM = 8
    RADIUS_MD = 12
    RADIUS_LG = 16
    RADIUS_FULL = 9999
    
    # Typography
    FONT_FAMILY = "Segoe UI"
    FONT_H1 = ("Segoe UI", 28, "bold")
    FONT_H2 = ("Segoe UI", 20, "bold")
    FONT_H3 = ("Segoe UI", 16, "bold")
    FONT_BODY = ("Segoe UI", 10)
    FONT_BODY_LARGE = ("Segoe UI", 11)
    FONT_CAPTION = ("Segoe UI", 9)
    FONT_BUTTON = ("Segoe UI", 10, "bold")
    
    # Animations
    ANIM_DURATION_FAST = 150
    ANIM_DURATION_NORMAL = 250
    ANIM_DURATION_SLOW = 400
    
    # Shadows (simulated with borders)
    SHADOW_SM = "#000000"
    SHADOW_MD = "#000000"
    SHADOW_LG = "#000000"

    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb):
        """Convert RGB tuple to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    @staticmethod
    def interpolate_color(color1, color2, factor):
        """Interpolate between two colors (factor: 0-1)"""
        rgb1 = Theme.hex_to_rgb(color1)
        rgb2 = Theme.hex_to_rgb(color2)
        rgb = tuple(rgb1[i] + (rgb2[i] - rgb1[i]) * factor for i in range(3))
        return Theme.rgb_to_hex(rgb)

# ═══════════════════════════════════════════════════════════════════════
# ANIMATION UTILITIES
# ═══════════════════════════════════════════════════════════════════════

class AnimationController:
    """Manages smooth animations for widgets"""
    
    @staticmethod
    def fade_in(widget, duration=Theme.ANIM_DURATION_NORMAL, callback=None):
        """Fade in animation"""
        steps = 20
        delay = duration // steps
        
        def animate(step=0):
            if step <= steps:
                alpha = step / steps
                try:
                    widget.configure(alpha=alpha)
                except:
                    pass
                widget.after(delay, lambda: animate(step + 1))
            elif callback:
                callback()
        
        animate()
    
    @staticmethod
    def slide_in(widget, direction='down', duration=Theme.ANIM_DURATION_NORMAL):
        """Slide in animation (simulated with geometry changes)"""
        pass  # Simplified for cross-platform compatibility
    
    @staticmethod
    def animate_color(widget, property_name, start_color, end_color, duration=Theme.ANIM_DURATION_FAST):
        """Animate color transition"""
        steps = 10
        delay = duration // steps
        
        def animate(step=0):
            if step <= steps:
                factor = step / steps
                current_color = Theme.interpolate_color(start_color, end_color, factor)
                try:
                    widget.configure(**{property_name: current_color})
                except:
                    pass
                if step < steps:
                    widget.after(delay, lambda: animate(step + 1))
        
        animate()

# ═══════════════════════════════════════════════════════════════════════
# STYLED COMPONENTS
# ═══════════════════════════════════════════════════════════════════════

class StyledFrame(tk.Frame):
    """Custom frame with glassmorphism-inspired styling"""
    
    def __init__(self, parent, elevated=False, **kwargs):
        bg_color = Theme.BG_ELEVATED if elevated else Theme.BG_SURFACE
        super().__init__(
            parent,
            bg=bg_color,
            highlightthickness=1,
            highlightbackground=Theme.BORDER_DEFAULT,
            **kwargs
        )

class StyledButton(tk.Canvas):
    """Custom button with hover effects and rounded corners"""
    
    def __init__(self, parent, text="Button", command=None, variant="primary", width=120, height=40, **kwargs):
        self.parent = parent
        self.text = text
        self.command = command
        self.variant = variant
        self.width = width
        self.height = height
        self.is_hovered = False
        self.is_pressed = False
        
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=Theme.BG_SURFACE,
            highlightthickness=0,
            **kwargs
        )
        
        self.draw()
        self.bind_events()
    
    def draw(self):
        """Draw button with current state"""
        self.delete("all")
        
        # Determine colors based on variant and state
        if self.variant == "primary":
            bg = Theme.ACCENT_PRIMARY
            if self.is_pressed:
                bg = Theme.ACCENT_SECONDARY
            elif self.is_hovered:
                bg = Theme.ACCENT_HOVER
            fg = Theme.TEXT_PRIMARY
        elif self.variant == "secondary":
            bg = Theme.BG_ELEVATED
            if self.is_pressed:
                bg = Theme.BG_HOVER
            elif self.is_hovered:
                bg = Theme.BG_HOVER
            fg = Theme.TEXT_PRIMARY
        elif self.variant == "success":
            bg = Theme.SUCCESS
            if self.is_hovered:
                bg = "#07f0b6"
            fg = Theme.BG_PRIMARY
        elif self.variant == "danger":
            bg = Theme.ERROR
            if self.is_hovered:
                bg = "#ff4757"
            fg = Theme.TEXT_PRIMARY
        else:
            bg = Theme.BG_ELEVATED
            fg = Theme.TEXT_PRIMARY
        
        # Draw rounded rectangle
        radius = Theme.RADIUS_MD
        self.create_rounded_rect(0, 0, self.width, self.height, radius, fill=bg, outline="")
        
        # Draw text
        self.create_text(
            self.width // 2,
            self.height // 2,
            text=self.text,
            fill=fg,
            font=Theme.FONT_BUTTON
        )
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def bind_events(self):
        """Bind mouse events"""
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def on_enter(self, event):
        self.is_hovered = True
        self.draw()
        self.configure(cursor="hand2")
    
    def on_leave(self, event):
        self.is_hovered = False
        self.is_pressed = False
        self.draw()
        self.configure(cursor="")
    
    def on_press(self, event):
        self.is_pressed = True
        self.draw()
    
    def on_release(self, event):
        self.is_pressed = False
        self.draw()
        if self.is_hovered and self.command:
            self.command()
    
    def set_text(self, text):
        """Update button text"""
        self.text = text
        self.draw()

class StyledEntry(tk.Frame):
    """Custom entry field with modern styling"""
    
    def __init__(self, parent, placeholder="", show=None, width=30, **kwargs):
        super().__init__(parent, bg=Theme.BG_SURFACE, **kwargs)
        
        self.show = show
        self.placeholder = placeholder
        self.has_focus = False
        
        # Entry widget
        self.entry = tk.Entry(
            self,
            bg=Theme.BG_ELEVATED,
            fg=Theme.TEXT_PRIMARY,
            insertbackground=Theme.ACCENT_PRIMARY,
            font=Theme.FONT_BODY_LARGE,
            relief=tk.FLAT,
            bd=0,
            show=show,
            width=width
        )
        self.entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Border frame
        self.configure(
            highlightthickness=1,
            highlightbackground=Theme.BORDER_DEFAULT
        )
        
        # Bind focus events
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        
        # Placeholder
        if placeholder:
            self.show_placeholder()
            self.entry.bind("<FocusIn>", self.on_placeholder_focus_in)
            self.entry.bind("<FocusOut>", self.on_placeholder_focus_out)
    
    def on_focus_in(self, event):
        self.has_focus = True
        self.configure(highlightbackground=Theme.BORDER_FOCUS)
        AnimationController.animate_color(
            self, 'highlightbackground',
            Theme.BORDER_DEFAULT, Theme.BORDER_FOCUS,
            Theme.ANIM_DURATION_FAST
        )
    
    def on_focus_out(self, event):
        self.has_focus = False
        self.configure(highlightbackground=Theme.BORDER_DEFAULT)
    
    def show_placeholder(self):
        self.entry.insert(0, self.placeholder)
        self.entry.configure(fg=Theme.TEXT_DISABLED)
    
    def on_placeholder_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=Theme.TEXT_PRIMARY)
        self.on_focus_in(event)
    
    def on_placeholder_focus_out(self, event):
        if not self.entry.get():
            self.show_placeholder()
        self.on_focus_out(event)
    
    def get(self):
        value = self.entry.get()
        return "" if value == self.placeholder else value
    
    def delete(self, first, last):
        self.entry.delete(first, last)
    
    def insert(self, index, string):
        self.entry.insert(index, string)

class StyledLabel(tk.Label):
    """Custom label with consistent styling"""
    
    def __init__(self, parent, text="", variant="body", **kwargs):
        if variant == "h1":
            font = Theme.FONT_H1
            fg = Theme.TEXT_PRIMARY
        elif variant == "h2":
            font = Theme.FONT_H2
            fg = Theme.TEXT_PRIMARY
        elif variant == "h3":
            font = Theme.FONT_H3
            fg = Theme.TEXT_PRIMARY
        elif variant == "caption":
            font = Theme.FONT_CAPTION
            fg = Theme.TEXT_SECONDARY
        else:  # body
            font = Theme.FONT_BODY
            fg = Theme.TEXT_PRIMARY
        
        super().__init__(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=Theme.BG_SURFACE,
            **kwargs
        )

class StyledCard(StyledFrame):
    """Card component with header and content"""
    
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, elevated=True, **kwargs)
        self.configure(bd=0)
        
        # Padding container
        self.container = tk.Frame(self, bg=Theme.BG_ELEVATED)
        self.container.pack(fill=tk.BOTH, expand=True, padx=Theme.SPACE_MD, pady=Theme.SPACE_MD)
        
        # Title
        if title:
            self.title_label = StyledLabel(self.container, text=title, variant="h3")
            self.title_label.configure(bg=Theme.BG_ELEVATED)
            self.title_label.pack(anchor=tk.W, pady=(0, Theme.SPACE_SM))
        
        # Content frame
        self.content = tk.Frame(self.container, bg=Theme.BG_ELEVATED)
        self.content.pack(fill=tk.BOTH, expand=True)

class StyledProgressBar(tk.Canvas):
    """Custom progress bar with smooth animation"""
    
    def __init__(self, parent, width=400, height=4, **kwargs):
        self.width = width
        self.height = height
        self.progress = 0
        
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=Theme.BG_SECONDARY,
            highlightthickness=0,
            **kwargs
        )
        
        self.draw()
    
    def draw(self):
        """Draw progress bar"""
        self.delete("all")
        
        # Background
        self.create_rectangle(0, 0, self.width, self.height, fill=Theme.BG_SECONDARY, outline="")
        
        # Progress
        progress_width = int(self.width * (self.progress / 100))
        if progress_width > 0:
            self.create_rectangle(0, 0, progress_width, self.height, fill=Theme.ACCENT_PRIMARY, outline="")
    
    def set_progress(self, value):
        """Set progress value (0-100)"""
        self.progress = max(0, min(100, value))
        self.draw()

class StyledModal(tk.Toplevel):
    """Modal dialog with modern styling"""
    
    def __init__(self, parent, title="", message="", icon="", buttons=None, show_entry=False, entry_type=None):
        super().__init__(parent)
        
        self.result = None
        self.title(title)
        self.configure(bg=Theme.BG_PRIMARY)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Window properties
        self.resizable(False, False)
        
        # Main container
        main_frame = StyledFrame(self, elevated=True)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.SPACE_LG, pady=Theme.SPACE_LG)
        
        content_frame = tk.Frame(main_frame, bg=Theme.BG_ELEVATED)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.SPACE_XL, pady=Theme.SPACE_XL)
        
        # Icon
        if icon:
            icon_label = StyledLabel(content_frame, text=icon, variant="h1")
            icon_label.configure(bg=Theme.BG_ELEVATED, font=("Segoe UI", 48))
            icon_label.pack(pady=(0, Theme.SPACE_MD))
        
        # Title
        if title:
            title_label = StyledLabel(content_frame, text=title, variant="h2")
            title_label.configure(bg=Theme.BG_ELEVATED)
            title_label.pack(pady=(0, Theme.SPACE_SM))
        
        # Message
        if message:
            msg_label = StyledLabel(content_frame, text=message, variant="body")
            msg_label.configure(bg=Theme.BG_ELEVATED, wraplength=400, justify=tk.CENTER)
            msg_label.pack(pady=(0, Theme.SPACE_LG))
        
        # Entry field
        if show_entry:
            self.entry = StyledEntry(content_frame, show=entry_type, width=40)
            self.entry.pack(pady=(0, Theme.SPACE_LG), fill=tk.X)
            self.entry.entry.focus_set()
        
        # Buttons
        if buttons:
            btn_frame = tk.Frame(content_frame, bg=Theme.BG_ELEVATED)
            btn_frame.pack(pady=(Theme.SPACE_MD, 0))
            
            for btn_text, btn_command, btn_variant in buttons:
                btn = StyledButton(
                    btn_frame,
                    text=btn_text,
                    command=btn_command,
                    variant=btn_variant,
                    width=120,
                    height=40
                )
                btn.pack(side=tk.LEFT, padx=Theme.SPACE_XS)
        
        # Center window
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Bind keys
        self.bind('<Escape>', lambda e: self.cancel())
        if show_entry:
            self.bind('<Return>', lambda e: self.ok())
    
    def ok(self):
        if hasattr(self, 'entry'):
            self.result = self.entry.get()
        else:
            self.result = True
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()

class FileSelector(tk.Frame):
    """Reusable file selector component"""
    
    def __init__(self, parent, label="Select File", on_select=None, **kwargs):
        super().__init__(parent, bg=Theme.BG_SURFACE, **kwargs)
        
        self.file_path = None
        self.on_select = on_select
        
        # Label
        label_widget = StyledLabel(self, text=label, variant="caption")
        label_widget.configure(bg=Theme.BG_SURFACE)
        label_widget.pack(anchor=tk.W, pady=(0, Theme.SPACE_XS))
        
        # File display and button container
        file_frame = tk.Frame(self, bg=Theme.BG_SURFACE)
        file_frame.pack(fill=tk.X)
        
        # File path display
        self.file_label = StyledLabel(file_frame, text="No file selected", variant="body")
        self.file_label.configure(
            bg=Theme.BG_ELEVATED,
            anchor=tk.W,
            padx=Theme.SPACE_SM,
            pady=Theme.SPACE_SM
        )
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Browse button
        self.browse_btn = StyledButton(
            file_frame,
            text="Browse",
            command=self.browse_file,
            variant="secondary",
            width=100,
            height=36
        )
        self.browse_btn.pack(side=tk.LEFT, padx=(Theme.SPACE_SM, 0))
    
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            filename = os.path.basename(file_path)
            if len(filename) > 50:
                filename = filename[:47] + "..."
            self.file_label.configure(text=filename)
            if self.on_select:
                self.on_select(file_path)
    
    def get_path(self):
        return self.file_path

class PasswordField(tk.Frame):
    """Reusable password field with confirmation"""
    
    def __init__(self, parent, show_confirm=True, label="Password", **kwargs):
        super().__init__(parent, bg=Theme.BG_SURFACE, **kwargs)
        
        self.show_confirm = show_confirm
        self.password_visible = False
        
        # Password label and entry
        pwd_label = StyledLabel(self, text=label, variant="caption")
        pwd_label.configure(bg=Theme.BG_SURFACE)
        pwd_label.pack(anchor=tk.W, pady=(0, Theme.SPACE_XS))
        
        # Password entry with visibility toggle
        pwd_frame = tk.Frame(self, bg=Theme.BG_SURFACE)
        pwd_frame.pack(fill=tk.X, pady=(0, Theme.SPACE_XS))
        
        self.password_entry = StyledEntry(pwd_frame, show="●", width=40)
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, Theme.SPACE_XS))
        
        # Visibility toggle button
        self.toggle_btn = StyledButton(
            pwd_frame,
            text="👁",
            command=self.toggle_visibility,
            variant="secondary",
            width=40,
            height=32
        )
        self.toggle_btn.pack(side=tk.LEFT)
        
        # Bind password entry to strength meter update
        self.password_entry.bind("<KeyRelease>", self.update_strength_meter)
        
        # Strength meter
        strength_frame = tk.Frame(self, bg=Theme.BG_SURFACE)
        strength_frame.pack(fill=tk.X, pady=(0, Theme.SPACE_SM))
        
        self.strength_canvas = tk.Canvas(strength_frame, height=6, bg=Theme.BG_ELEVATED, highlightthickness=0)
        self.strength_canvas.pack(fill=tk.X, pady=(0, Theme.SPACE_XS))
        
        self.strength_label = StyledLabel(strength_frame, text="", variant="caption")
        self.strength_label.configure(bg=Theme.BG_SURFACE, fg=Theme.TEXT_SECONDARY)
        self.strength_label.pack(anchor=tk.W)
        
        # Confirmation entry
        if show_confirm:
            confirm_label = StyledLabel(self, text="Confirm Password", variant="caption")
            confirm_label.configure(bg=Theme.BG_SURFACE)
            confirm_label.pack(anchor=tk.W, pady=(0, Theme.SPACE_XS))
            
            confirm_frame = tk.Frame(self, bg=Theme.BG_SURFACE)
            confirm_frame.pack(fill=tk.X)
            
            self.confirm_entry = StyledEntry(confirm_frame, show="●", width=40)
            self.confirm_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, Theme.SPACE_XS))
            
            # Visibility toggle for confirm field
            self.confirm_toggle_btn = StyledButton(
                confirm_frame,
                text="👁",
                command=self.toggle_confirm_visibility,
                variant="secondary",
                width=40,
                height=32
            )
            self.confirm_toggle_btn.pack(side=tk.LEFT)
    
    def toggle_visibility(self):
        """Toggle password visibility"""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password_entry.entry.configure(show="")
            self.toggle_btn.set_text("🚫")
        else:
            self.password_entry.entry.configure(show="●")
            self.toggle_btn.set_text("👁")
    
    def toggle_confirm_visibility(self):
        """Toggle confirm password visibility"""
        if not hasattr(self, 'confirm_visible'):
            self.confirm_visible = False
        self.confirm_visible = not self.confirm_visible
        if self.confirm_visible:
            self.confirm_entry.entry.configure(show="")
            self.confirm_toggle_btn.set_text("🚫")
        else:
            self.confirm_entry.entry.configure(show="●")
            self.confirm_toggle_btn.set_text("👁")
    
    def update_strength_meter(self, event=None):
        """Update password strength meter"""
        password = self.password_entry.get()
        
        if not password:
            # Clear meter if empty
            self.strength_canvas.delete("all")
            self.strength_label.configure(text="")
            return
        
        # Calculate strength
        score, label, color = PasswordStrength.calculate_strength(password)
        
        # Update canvas bar
        canvas_width = self.strength_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 400  # Default width before render
        
        bar_width = (score / 7) * canvas_width  # Max score is 7
        
        self.strength_canvas.delete("all")
        self.strength_canvas.create_rectangle(0, 0, bar_width, 6, fill=color, outline="")
        
        # Update label
        self.strength_label.configure(text=f"Strength: {label}", fg=color)
    
    def get_password(self):
        return self.password_entry.get()
    
    def get_confirm(self):
        return self.confirm_entry.get() if self.show_confirm else self.password_entry.get()
    
    def validate(self):
        pwd = self.get_password()
        if not pwd:
            return False, "Password cannot be empty"
        if self.show_confirm:
            if pwd != self.get_confirm():
                return False, "Passwords do not match"
        return True, ""

# ═══════════════════════════════════════════════════════════════════════
# ENCRYPTION/DECRYPTION LOGIC
# ═══════════════════════════════════════════════════════════════════════

class CryptoEngine:
    """Core encryption and decryption logic"""
    
    @staticmethod
    def derive_key(password, salt):
        """Derive key using Argon2id (memory-hard, GPU-resistant)"""
        # Argon2id parameters: time_cost=3 (~500ms), memory_cost=64MB,  parallelism=4
        return low_level.hash_secret_raw(
            secret=password.encode('utf-8') if isinstance(password, str) else password,
            salt=salt,
            time_cost=3,
            memory_cost=65536,  # 64 MB
            parallelism=4,
            hash_len=32,
            type=low_level.Type.ID
        )
    
    @staticmethod
    def encrypt_data(data, key):
        cipher = AES.new(key, AES.MODE_GCM)
        ct_bytes, tag = cipher.encrypt_and_digest(pad(data, AES.block_size))
        return cipher.nonce + tag + ct_bytes
    
    @staticmethod
    def decrypt_data(ciphertext, key):
        try:
            nonce = ciphertext[:16]
            tag = ciphertext[16:32]
            ct = ciphertext[32:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            pt = unpad(cipher.decrypt_and_verify(ct, tag), AES.block_size)
            return pt
        except (ValueError, KeyError):
            return None
    
    @staticmethod
    def secure_delete_file(file_path, passes=1):
        try:
            if os.path.exists(file_path):
                length = os.path.getsize(file_path)
                with open(file_path, "wb") as f:
                    for _ in range(passes):
                        f.write(get_random_bytes(length))
                os.remove(file_path)
        except Exception as e:
            print(f"Error in secure deletion: {e}")

class PasswordGenerator:
    """Generate believable fake passwords"""
    
    common_words = ["password", "welcome", "monkey", "dragon", "football", "baseball", "superman",
                    "batman", "trustno1", "sunshine", "master", "hello", "freedom", "love", "princess"]
    
    strong_words = ["Thunder", "Lightning", "Mountain", "Fortress", "Quantum", "Nebula", "Galaxy",
                    "Infinity", "Horizon", "Cascade", "Vertex", "Matrix", "Cipher", "Crystal"]
    
    @staticmethod
    def generate_weak():
        """Generate a weak-looking password"""
        patterns = [
            lambda: random.choice(PasswordGenerator.common_words).lower() + str(random.randint(0, 9999)),
            lambda: random.choice(PasswordGenerator.common_words).lower() + str(random.randint(1960, 2010)),
            lambda: random.choice(PasswordGenerator.common_words).lower().replace('a', '@').replace('e', '3'),
        ]
        return random.choice(patterns)()
    
    @staticmethod
    def generate_strong(min_length=8):
        """Generate a strong-looking password"""
        word1 = random.choice(PasswordGenerator.strong_words)
        word2 = random.choice(PasswordGenerator.strong_words)
        number = random.randint(100, 999)
        special = random.choice("!@#$%^&*")
        password = f"{word1}{special}{number}{word2}"
        
        while len(password) < min_length:
            password += str(random.randint(0, 9))
        
        return password

class PasswordStrength:
    """Calculate password strength and provide visual feedback"""
    
    @staticmethod
    def calculate_strength(password):
        """Returns (strength_score, strength_label, color)"""
        if not password:
            return 0, "No Password", Theme.TEXT_DISABLED
        
        score = 0
        length = len(password)
        
        # Length scoring
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        
        # Character variety
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[^a-zA-Z0-9]', password):
            score += 1
        
        # Penalize common patterns
        if re.search(r'(password|123456|qwerty)', password.lower()):
            score -= 2
        
        # Map to strength levels
        if score <= 2:
            return score, "Weak", Theme.ERROR
        elif score <= 4:
            return score, "Medium", Theme.WARNING
        elif score <= 6:
            return score, "Strong", Theme.SUCCESS
        else:
            return score, "Very Strong", "#00ff88"

class SelfDestructService:
    """Handles self-destruct password checking and secure file wiping"""
    
    @staticmethod
    def hash_selfdestruct_password(password, salt):
        """Hash self-destruct password with salt"""
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 50000)
    
    @staticmethod
    def secure_wipe_file(file_path):
        """Securely wipe file with 100-200 random passes"""
        try:
            if not os.path.exists(file_path):
                return False
            
            file_size = os.path.getsize(file_path)
            passes = random.randint(100, 200)
            
            with open(file_path, 'r+b') as f:
                for _ in range(passes):
                    f.seek(0)
                    f.write(get_random_bytes(file_size))
                    f.flush()
                    os.fsync(f.fileno())
                
                # Final pass: all zeros
                f.seek(0)
                f.write(b'\x00' * file_size)
                f.flush()
                os.fsync(f.fileno())
            
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Secure wipe error: {e}")
            return False
    
    @staticmethod
    def check_and_destroy(encrypted_file_path, password, sd_salt, sd_hash):
        """Check if password matches self-destruct, wipe if true"""
        test_hash = SelfDestructService.hash_selfdestruct_password(password, sd_salt)
        if test_hash == sd_hash:
            # WIPE THE FILE
            SelfDestructService.secure_wipe_file(encrypted_file_path)
            return True
        return False

class CompressionService:
    """Handles lossless compression for file size reduction"""
    
    @staticmethod
    def compress_if_beneficial(data):
        """Compress data only if it reduces size (returns data, was_compressed, stats)"""
        try:
            original_size = len(data)
            compressed = zlib.compress(data, level=9)
            compressed_size = len(compressed)
            
            # Only use compressed version if it's at least 5% smaller
            if compressed_size < original_size * 0.95:
                savings_percent = ((original_size - compressed_size) / original_size) * 100
                stats = {
                    'compressed': True,
                    'original_size': original_size,
                    'final_size': compressed_size,
                    'savings_percent': savings_percent
                }
                return compressed, True, stats
            else:
                stats = {
                    'compressed': False,
                    'original_size': original_size,
                    'final_size': original_size,
                    'savings_percent': 0
                }
                return data, False, stats
        except:
            stats = {
                'compressed': False,
                'original_size': len(data),
                'final_size': len(data),
                'savings_percent': 0
            }
            return data, False, stats
    
    @staticmethod
    def decompress_if_needed(data, was_compressed):
        """Decompress data if it was compressed"""
        if was_compressed:
            try:
                return zlib.decompress(data)
            except:
                raise ValueError("Decompression failed - corrupted data")
        return data
    
    @staticmethod
    def estimate_compressed_size(data):
        """Estimate compressed size without actually compressing (fast)"""
        # Simple heuristic: assume 50% compression for estimation
        return len(data) // 2

class EncryptionService:
    """Handles encryption operations"""
    
    @staticmethod
    def encrypt_standard(real_data, fake_data, real_password, filename, padding_target_mb=0, selfdestruct_password=None):
        """Standard encryption with 2 decoy files, compression, optional padding, and optional self-destruct"""
        # Compress data first (lossless)
        compressed_real, real_compressed, real_stats = CompressionService.compress_if_beneficial(real_data)
        compressed_fake, fake_compressed, fake_stats = CompressionService.compress_if_beneficial(fake_data)
        
        # Generate salts and passwords
        real_salt = get_random_bytes(16)
        fake_salt_1 = get_random_bytes(16)
        fake_salt_2 = get_random_bytes(16)
        
        fake_password_1 = PasswordGenerator.generate_weak()
        fake_password_2 = PasswordGenerator.generate_strong(len(real_password))
        
        # Derive keys
        real_key = CryptoEngine.derive_key(real_password.encode('utf-8'), real_salt)
        fake_key_1 = CryptoEngine.derive_key(fake_password_1.encode('utf-8'), fake_salt_1)
        fake_key_2 = CryptoEngine.derive_key(fake_password_2.encode('utf-8'), fake_salt_2)
        
        ext = os.path.splitext(filename)[1].encode('utf-8')
        ext_len = len(ext)
        
        # Encrypt compressed data
        encrypted_real = CryptoEngine.encrypt_data(compressed_real, real_key)
        encrypted_fake_1 = CryptoEngine.encrypt_data(compressed_fake, fake_key_1)
        encrypted_fake_2 = CryptoEngine.encrypt_data(compressed_fake, fake_key_2)
        
        # Build compression flags byte (bit 0=real, bit 1=fake1, bit 2=fake2)
        compression_flags = 0
        if real_compressed:
            compression_flags |= 0b001
        if fake_compressed:
            compression_flags |= 0b010  # fake1
            compression_flags |= 0b100  # fake2 (same fake data)
        
        # Build encrypted data with version byte 0x03 (Argon2id + self-destruct support)
        result = (
            bytes([0x03]) +  # Version byte (Argon2id)
            bytes([compression_flags]) +
            real_salt + fake_salt_1 + fake_salt_2 +
            bytes([ext_len]) + ext +
            len(encrypted_real).to_bytes(4, 'big') +
            len(encrypted_fake_1).to_bytes(4, 'big') +
            len(encrypted_fake_2).to_bytes(4, 'big') +
            encrypted_real + encrypted_fake_1 + encrypted_fake_2
        )
        
        # Add self-destruct if provided
        if selfdestruct_password:
            sd_salt = get_random_bytes(16)
            sd_hash = SelfDestructService.hash_selfdestruct_password(selfdestruct_password, sd_salt)
            result = result + sd_salt + sd_hash + bytes([0x01])  # SD flag
        else:
            result = result + bytes([0x00])  # No SD flag
        
        # Add padding if requested
        if padding_target_mb > 0:
            target_size = int(padding_target_mb * 1024 * 1024)
            current_size = len(result)
            
            if target_size > current_size:
                padding_size = target_size - current_size - 4  # Reserve 4 bytes for padding length
                padding = get_random_bytes(padding_size)
                result = result + padding + padding_size.to_bytes(4, 'big')
            else:
                # No padding needed, but add 0 padding length for format consistency
                result = result + (0).to_bytes(4, 'big')
        else:
            # No padding, add 0 padding length
            result = result + (0).to_bytes(4, 'big')
        
        # Return with compression stats
        compression_stats = {
            'real': real_stats,
            'fake': fake_stats
        }
        return result, fake_password_1, fake_password_2, compression_stats
    
    @staticmethod
    def encrypt_multi_decoy(real_data, decoy_files, real_password, filename, padding_target_mb=0, selfdestruct_password=None):
        """Multi-decoy encryption with compression, optional padding, and optional self-destruct"""
        # Compress real data
        compressed_real, real_compressed, real_stats = CompressionService.compress_if_beneficial(real_data)
        
        # Compress decoy files
        compressed_decoys = []
        decoy_compressed_flags = []
        decoy_stats = []
        for decoy in decoy_files:
            comp_data, was_comp, stats = CompressionService.compress_if_beneficial(decoy['data'])
            compressed_decoys.append({'data': comp_data, 'password': decoy['password']})
            decoy_compressed_flags.append(was_comp)
            decoy_stats.append(stats)
        
        num_files = 1 + len(decoy_files)
        salts = [get_random_bytes(16) for _ in range(num_files)]
        
        real_key = CryptoEngine.derive_key(real_password.encode('utf-8'), salts[0])
        decoy_keys = [CryptoEngine.derive_key(d['password'].encode('utf-8'), s)
                      for d, s in zip(compressed_decoys, salts[1:])]
        
        ext = os.path.splitext(filename)[1].encode('utf-8')
        ext_len = len(ext)
        
        # Encrypt compressed data
        encrypted_real = CryptoEngine.encrypt_data(compressed_real, real_key)
        encrypted_decoys = [CryptoEngine.encrypt_data(d['data'], k)
                           for d, k in zip(compressed_decoys, decoy_keys)]
        
        # Build compression flags byte
        compression_flags = 0
        if real_compressed:
            compression_flags |= (1 << 0)
        for i, flag in enumerate(decoy_compressed_flags):
            if flag:
                compression_flags |= (1 << (i + 1))
        
        # Build result with version byte 0x03 (Argon2id)
        result = bytearray([0x03])  # Version byte
        result.append(num_files)
        result.append(compression_flags)
        
        for salt in salts:
            result.extend(salt)
        
        result.extend(len(encrypted_real).to_bytes(4, 'big'))
        for enc in encrypted_decoys:
            result.extend(len(enc).to_bytes(4, 'big'))
        
        result.extend(encrypted_real)
        for enc in encrypted_decoys:
            result.extend(enc)
        
        result = bytes(result)
        
        # Add self-destruct if provided
        if selfdestruct_password:
            sd_salt = get_random_bytes(16)
            sd_hash = SelfDestructService.hash_selfdestruct_password(selfdestruct_password, sd_salt)
            result = result + sd_salt + sd_hash + bytes([0x01])  # SD flag
        else:
            result = result + bytes([0x00])  # No SD flag
        
        # Add padding if requested
        if padding_target_mb > 0:
            target_size = int(padding_target_mb * 1024 * 1024)
            current_size = len(result)
            
            if target_size > current_size:
                padding_size = target_size - current_size - 4
                padding = get_random_bytes(padding_size)
                result = result + padding + padding_size.to_bytes(4, 'big')
            else:
                result = result + (0).to_bytes(4, 'big')
        else:
            result = result + (0).to_bytes(4, 'big')
        
        # Return with compression stats
        compression_stats = {
            'real': real_stats,
            'decoys': decoy_stats
        }
        return result, compression_stats

class DecryptionService:
    """Handles decryption operations"""
    
    @staticmethod
    def decrypt_unified(encrypted_data, password, file_path=None):
        """Unified decryption with self-destruct check, padding support, and Argon2id"""
        # Check for padding (last 4 bytes contain padding length)
        if len(encrypted_data) >= 4:
            try:
                padding_length = int.from_bytes(encrypted_data[-4:], 'big')
                # Validate padding length is reasonable
                if 0 <= padding_length < len(encrypted_data) - 4:
                    # Strip padding if present
                    if padding_length > 0:
                        encrypted_data = encrypted_data[:-4-padding_length]
                    else:
                        encrypted_data = encrypted_data[:-4]
            except:
                pass  # If padding parsing fails, try without stripping
        
        # Check for self-destruct flag (before padding)
        sd_flag = encrypted_data[-1] if len(encrypted_data) > 0 else 0x00
        if sd_flag == 0x01:
            # Self-destruct enabled, check password
            sd_salt = encrypted_data[-49:-33]  # 16 bytes before hash
            sd_hash = encrypted_data[-33:-1]   # 32 bytes hash
            
            if file_path and SelfDestructService.check_and_destroy(file_path, password, sd_salt, sd_hash):
                # File was wiped! Return None to indicate "corrupted"
                return None, None
            
            # Strip self-destruct data
            encrypted_data = encrypted_data[:-49]
        else:
            # No self-destruct, strip flag byte
            encrypted_data = encrypted_data[:-1]
        
        # Check version byte
        if len(encrypted_data) > 0 and encrypted_data[0] == 0x03:
            # Version 0x03: Argon2id + compression + self-destruct
            try:
                result = DecryptionService.decrypt_standard_v3(encrypted_data, password)
                if result[0] is not None:
                    return result
            except:
                pass
            
            try:
                result = DecryptionService.decrypt_multi_v3(encrypted_data, password)
                if result[0] is not None:
                    return result
            except:
                pass
        elif len(encrypted_data) > 0 and encrypted_data[0] == 0x02:
            # Old format (v0x02 with PBKDF2) - not supported anymore
            return None, None
        else:
            # Very old format - not supported
            return None, None
        
        return None, None
    
    @staticmethod
    def decrypt_standard_v3(encrypted_data, password):
        """Decrypt new standard format with compression and Argon2id"""
        try:
            if encrypted_data[0] != 0x03:
                return None, None
            
            compression_flags = encrypted_data[1]
            current_pos = 2
            
            real_salt = encrypted_data[current_pos:current_pos + 16]
            current_pos += 16
            fake_salt_1 = encrypted_data[current_pos:current_pos + 16]
            current_pos += 16
            fake_salt_2 = encrypted_data[current_pos:current_pos + 16]
            current_pos += 16
            
            ext_len = encrypted_data[current_pos]
            current_pos += 1
            ext = encrypted_data[current_pos:current_pos + ext_len]
            current_pos += ext_len
            
            real_length = int.from_bytes(encrypted_data[current_pos:current_pos + 4], 'big')
            current_pos += 4
            fake_length_1 = int.from_bytes(encrypted_data[current_pos:current_pos + 4], 'big')
            current_pos += 4
            fake_length_2 = int.from_bytes(encrypted_data[current_pos:current_pos + 4], 'big')
            current_pos += 4
            
            encrypted_real = encrypted_data[current_pos:current_pos + real_length]
            current_pos += real_length
            encrypted_fake_1 = encrypted_data[current_pos:current_pos + fake_length_1]
            current_pos += fake_length_1
            encrypted_fake_2 = encrypted_data[current_pos:current_pos + fake_length_2]
            
            key_combinations = [
                (real_salt, encrypted_real, True, (compression_flags & 0b001) != 0),
                (fake_salt_1, encrypted_fake_1, False, (compression_flags & 0b010) != 0),
                (fake_salt_2, encrypted_fake_2, False, (compression_flags & 0b100) != 0)
            ]
            
            for salt, encrypted, is_real, was_compressed in key_combinations:
                key = CryptoEngine.derive_key(password.encode('utf-8'), salt)
                decrypted = CryptoEngine.decrypt_data(encrypted, key)
                if decrypted:
                    # Decompress if needed
                    decrypted = CompressionService.decompress_if_needed(decrypted, was_compressed)
                    return decrypted, is_real
            
            return None, None
        except Exception as e:
            return None, None
    
    @staticmethod
    def decrypt_multi_v3(encrypted_data, password):
        """Decrypt new multi-decoy format with compression and Argon2id"""
        try:
            if encrypted_data[0] != 0x03:
                return None, None
            
            num_files = encrypted_data[1]
            compression_flags = encrypted_data[2]
            current_pos = 3
            
            salts = []
            for _ in range(num_files):
                salts.append(encrypted_data[current_pos:current_pos + 16])
                current_pos += 16
            
            lengths = []
            for _ in range(num_files):
                lengths.append(int.from_bytes(encrypted_data[current_pos:current_pos + 4], 'big'))
                current_pos += 4
            
            current_data_pos = current_pos
            for i, (salt, length) in enumerate(zip(salts, lengths)):
                key = CryptoEngine.derive_key(password.encode('utf-8'), salt)
                encrypted_data_section = encrypted_data[current_data_pos:current_data_pos + length]
                try:
                    decrypted = CryptoEngine.decrypt_data(encrypted_data_section, key)
                    if decrypted:
                        # Check if this file was compressed
                        was_compressed = (compression_flags & (1 << i)) != 0
                        decrypted = CompressionService.decompress_if_needed(decrypted, was_compressed)
                        return decrypted, i == 0
                except:
                    pass
                current_data_pos += length
            
            return None, None
        except Exception as e:
            return None, None

# ═══════════════════════════════════════════════════════════════════════
# DECOY FILE ENTRY COMPONENT
# ═══════════════════════════════════════════════════════════════════════

class DecoyFileEntry:
    """A single decoy file entry with file selection and password"""
    
    def __init__(self, parent_frame, index, on_remove=None):
        self.frame = StyledFrame(parent_frame, elevated=True)
        self.frame.pack(fill=tk.X, pady=(0, Theme.SPACE_SM))
        
        container = tk.Frame(self.frame, bg=Theme.BG_ELEVATED)
        container.pack(fill=tk.BOTH, expand=True, padx=Theme.SPACE_MD, pady=Theme.SPACE_MD)
        
        # Header
        header_frame = tk.Frame(container, bg=Theme.BG_ELEVATED)
        header_frame.pack(fill=tk.X, pady=(0, Theme.SPACE_SM))
        
        title_label = StyledLabel(header_frame, text=f"Decoy File #{index + 1}", variant="h3")
        title_label.configure(bg=Theme.BG_ELEVATED)
        title_label.pack(side=tk.LEFT)
        
        if on_remove:
            remove_btn = StyledButton(
                header_frame,
                text="✕",
                command=lambda: on_remove(self),
                variant="danger",
                width=32,
                height=32
            )
            remove_btn.pack(side=tk.RIGHT)
        
        # File selector
        self.file_selector = FileSelector(container, label="Decoy File")
        self.file_selector.configure(bg=Theme.BG_ELEVATED)
        for child in self.file_selector.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.file_selector.pack(fill=tk.X, pady=(0, Theme.SPACE_SM))
        
        # Password
        self.password_field = PasswordField(container, show_confirm=False, label="Decoy Password")
        self.password_field.configure(bg=Theme.BG_ELEVATED)
        for child in self.password_field.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.password_field.pack(fill=tk.X)
    
    def get_data(self):
        file_path = self.file_selector.get_path()
        password = self.password_field.get_password()
        
        if not file_path or not password:
            return None
        
        try:
            with open(file_path, 'rb') as f:
                return {
                    'data': f.read(),
                    'password': password,
                    'path': file_path
                }
        except:
            return None

# ═══════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════

class HoneyCryptApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("HoneyCrypt")
        self.root.configure(bg=Theme.BG_PRIMARY)
        
        # Window size and position
        window_width = 900
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(800, 600)
        
        self.setup_ui()
        
        # Fade-in animation
        self.root.attributes('-alpha', 0.0)
        self.animate_window_fade_in()
    
    def animate_window_fade_in(self):
        """Smooth fade-in animation for window"""
        alpha = self.root.attributes('-alpha')
        if alpha < 1.0:
            alpha = min(1.0, alpha + 0.05)
            self.root.attributes('-alpha', alpha)
            self.root.after(15, self.animate_window_fade_in)
    
    def setup_ui(self):
        """Setup main UI"""
        # Header
        header = tk.Frame(self.root, bg=Theme.BG_PRIMARY, height=80)
        header.pack(fill=tk.X, padx=Theme.SPACE_LG, pady=(Theme.SPACE_LG, 0))
        header.pack_propagate(False)
        
        title = StyledLabel(header, text="HoneyCrypt", variant="h1")
        title.configure(bg=Theme.BG_PRIMARY)
        title.pack(side=tk.LEFT, pady=Theme.SPACE_MD)
        
        subtitle = StyledLabel(header, text="Plausible Deniability Encryption", variant="caption")
        subtitle.configure(bg=Theme.BG_PRIMARY, fg=Theme.TEXT_SECONDARY)
        subtitle.pack(side=tk.LEFT, padx=(Theme.SPACE_MD, 0), pady=Theme.SPACE_MD)
        
        # Main content
        content_frame = tk.Frame(self.root, bg=Theme.BG_PRIMARY)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.SPACE_LG, pady=Theme.SPACE_MD)
        
        # Tab container
        self.tab_container = StyledFrame(content_frame, elevated=True)
        self.tab_container.pack(fill=tk.BOTH, expand=True)
        
        # Tab buttons
        tab_button_frame = tk.Frame(self.tab_container, bg=Theme.BG_ELEVATED, height=50)
        tab_button_frame.pack(fill=tk.X)
        tab_button_frame.pack_propagate(False)
        
        self.current_tab = None
        self.tabs = {}
        
        # Tab button container with padding
        tab_btn_container = tk.Frame(tab_button_frame, bg=Theme.BG_ELEVATED)
        tab_btn_container.pack(fill=tk.X, padx=Theme.SPACE_MD, pady=Theme.SPACE_SM)
        
        self.tab_buttons = {}
        for tab_name in ["Standard", "Multi-Decoy", "Decrypt"]:
            btn = StyledButton(
                tab_btn_container,
                text=tab_name,
                command=lambda name=tab_name: self.switch_tab(name),
                variant="secondary",
                width=140,
                height=36
            )
            btn.pack(side=tk.LEFT, padx=(0, Theme.SPACE_XS))
            self.tab_buttons[tab_name] = btn
        
        # Tab content area
        self.tab_content = tk.Frame(self.tab_container, bg=Theme.BG_ELEVATED)
        self.tab_content.pack(fill=tk.BOTH, expand=True, padx=Theme.SPACE_LG, pady=Theme.SPACE_MD)
        
        # Create tabs
        self.create_standard_tab()
        self.create_multi_decoy_tab()
        self.create_decrypt_tab()
        
        # Footer with progress
        footer = tk.Frame(self.root, bg=Theme.BG_PRIMARY)
        footer.pack(fill=tk.X, padx=Theme.SPACE_LG, pady=(0, Theme.SPACE_LG))
        
        self.progress_bar = StyledProgressBar(footer, width=856, height=4)
        self.progress_bar.pack(fill=tk.X, pady=(0, Theme.SPACE_SM))
        
        self.status_label = StyledLabel(footer, text="Ready", variant="caption")
        self.status_label.configure(bg=Theme.BG_PRIMARY)
        self.status_label.pack()
        
        # Show first tab
        self.switch_tab("Standard")
    
    def switch_tab(self, tab_name):
        """Switch between tabs with animation"""
        if self.current_tab == tab_name:
            return
        
        # Hide all tabs
        for name, frame in self.tabs.items():
            frame.pack_forget()
        
        # Show selected tab
        if tab_name in self.tabs:
            self.tabs[tab_name].pack(fill=tk.BOTH, expand=True)
            self.current_tab = tab_name
            
            # Update button styles
            for name, btn in self.tab_buttons.items():
                if name == tab_name:
                    btn.variant = "primary"
                else:
                    btn.variant = "secondary"
                btn.draw()
    
    def create_standard_tab(self):
        """Create standard encryption tab"""
        tab = tk.Frame(self.tab_content, bg=Theme.BG_ELEVATED)
        self.tabs["Standard"] = tab
        
        # Scrollable container
        canvas = tk.Canvas(tab, bg=Theme.BG_ELEVATED, highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview, bg=Theme.BG_ELEVATED)
        scrollable = tk.Frame(canvas, bg=Theme.BG_ELEVATED)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Real file card
        real_card = StyledCard(scrollable, title="Real File")
        real_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        self.std_real_file = FileSelector(real_card.content, label="Select the file you want to protect")
        self.std_real_file.configure(bg=Theme.BG_ELEVATED)
        for child in self.std_real_file.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.std_real_file.pack(fill=tk.X)
        
        # Fake file card
        fake_card = StyledCard(scrollable, title="Decoy File")
        fake_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        self.std_fake_file = FileSelector(fake_card.content, label="Select a decoy file (appears when using fake passwords)")
        self.std_fake_file.configure(bg=Theme.BG_ELEVATED)
        for child in self.std_fake_file.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.std_fake_file.pack(fill=tk.X)
        
        # Password card
        pass_card = StyledCard(scrollable, title="Password")
        pass_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        self.std_password = PasswordField(pass_card.content, show_confirm=True)
        self.std_password.configure(bg=Theme.BG_ELEVATED)
        for child in self.std_password.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.std_password.pack(fill=tk.X)
        
        # Self-Destruct card
        sd_card = StyledCard(scrollable, title="Self-Destruct (Optional)")
        sd_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        # Warning label
        warning_label = StyledLabel(
            sd_card.content,
            text="⚠️ WARNING: If someone enters this password, the encrypted file will be permanently destroyed",
            variant="caption"
        )
        warning_label.configure(bg=Theme.BG_ELEVATED, fg="#ff6b6b", wraplength=500)
        warning_label.pack(anchor=tk.W, pady=(0, Theme.SPACE_SM))
        
        # Self-destruct checkbox
        self.std_sd_var = tk.BooleanVar(value=False)
        sd_check = tk.Checkbutton(
            sd_card.content,
            text="Enable self-destruct password",
            variable=self.std_sd_var,
            bg=Theme.BG_ELEVATED,
            fg=Theme.TEXT_PRIMARY,
            selectcolor=Theme.BG_ELEVATED,
            activebackground=Theme.BG_ELEVATED,
            activeforeground=Theme.TEXT_PRIMARY,
            font=Theme.FONT_BODY,
            command=self.toggle_std_selfdestruct
        )
        sd_check.pack(anchor=tk.W, pady=(0, Theme.SPACE_SM))
        
        # Self-destruct password container
        self.std_sd_container = tk.Frame(sd_card.content, bg=Theme.BG_ELEVATED)
        
        sd_label = StyledLabel(self.std_sd_container, text="Self-destruct password:", variant="body")
        sd_label.configure(bg=Theme.BG_ELEVATED)
        sd_label.pack(anchor=tk.W, pady=(0, Theme.SPACE_XS))
        
        self.std_sd_password = PasswordField(self.std_sd_container, show_confirm=True)
        self.std_sd_password.configure(bg=Theme.BG_ELEVATED)
        for child in self.std_sd_password.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.std_sd_password.pack(fill=tk.X)
        
        # Padding card
        padding_card = StyledCard(scrollable, title="Padding (Optional)")
        padding_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        # Padding checkbox
        self.std_padding_var = tk.BooleanVar(value=False)
        padding_check = tk.Checkbutton(
            padding_card.content,
            text="Add padding to obscure file size",
            variable=self.std_padding_var,
            bg=Theme.BG_ELEVATED,
            fg=Theme.TEXT_PRIMARY,
            selectcolor=Theme.BG_ELEVATED,
            activebackground=Theme.BG_ELEVATED,
            activeforeground=Theme.TEXT_PRIMARY,
            font=Theme.FONT_BODY,
            command=self.toggle_std_padding
        )
        padding_check.pack(anchor=tk.W, pady=(0, Theme.SPACE_SM))
        
        # Padding input container
        self.std_padding_container = tk.Frame(padding_card.content, bg=Theme.BG_ELEVATED)
        
        padding_input_frame = tk.Frame(self.std_padding_container, bg=Theme.BG_ELEVATED)
        padding_input_frame.pack(fill=tk.X)
        
        padding_label = StyledLabel(padding_input_frame, text="Target final size:", variant="caption")
        padding_label.configure(bg=Theme.BG_ELEVATED)
        padding_label.pack(side=tk.LEFT, padx=(0, Theme.SPACE_SM))
        
        self.std_padding_entry = StyledEntry(self.std_padding_container, placeholder="0", width=10)
        self.std_padding_entry.pack(side=tk.LEFT, padx=(0, Theme.SPACE_XS))
        
        mb_label = StyledLabel(padding_input_frame, text="MB", variant="caption")
        mb_label.configure(bg=Theme.BG_ELEVATED)
        mb_label.pack(side=tk.LEFT)
        
        # Estimated size label
        self.std_estimate_label = StyledLabel(self.std_padding_container, text="", variant="caption")
        self.std_estimate_label.configure(bg=Theme.BG_ELEVATED, fg=Theme.TEXT_SECONDARY)
        self.std_estimate_label.pack(anchor=tk.W, pady=(Theme.SPACE_XS, 0))
        
        # Encrypt button
        encrypt_btn = StyledButton(
            scrollable,
            text="Encrypt Files",
            command=self.encrypt_standard,
            variant="primary",
            width=200,
            height=48
        )
        encrypt_btn.pack(pady=Theme.SPACE_MD)
    
    def create_multi_decoy_tab(self):
        """Create multi-decoy encryption tab"""
        tab = tk.Frame(self.tab_content, bg=Theme.BG_ELEVATED)
        self.tabs["Multi-Decoy"] = tab
        
        # Scrollable container
        canvas = tk.Canvas(tab, bg=Theme.BG_ELEVATED, highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview, bg=Theme.BG_ELEVATED)
        scrollable = tk.Frame(canvas, bg=Theme.BG_ELEVATED)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Real file card
        real_card = StyledCard(scrollable, title="Real File")
        real_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        self.multi_real_file = FileSelector(real_card.content, label="Select the file you want to protect")
        self.multi_real_file.configure(bg=Theme.BG_ELEVATED)
        for child in self.multi_real_file.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.multi_real_file.pack(fill=tk.X)
        
        # Password card
        pass_card = StyledCard(scrollable, title="Real Password")
        pass_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        self.multi_password = PasswordField(pass_card.content, show_confirm=True)
        self.multi_password.configure(bg=Theme.BG_ELEVATED)
        for child in self.multi_password.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.multi_password.pack(fill=tk.X)
        
        # Self-Destruct card
        sd_card = StyledCard(scrollable, title="Self-Destruct (Optional)")
        sd_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        # Warning label
        warning_label = StyledLabel(
            sd_card.content,
            text="⚠️ WARNING: If someone enters this password, the encrypted file will be permanently destroyed",
            variant="caption"
        )
        warning_label.configure(bg=Theme.BG_ELEVATED, fg="#ff6b6b", wraplength=500)
        warning_label.pack(anchor=tk.W, pady=(0, Theme.SPACE_SM))
        
        # Self-destruct checkbox
        self.multi_sd_var = tk.BooleanVar(value=False)
        sd_check = tk.Checkbutton(
            sd_card.content,
            text="Enable self-destruct password",
            variable=self.multi_sd_var,
            bg=Theme.BG_ELEVATED,
            fg=Theme.TEXT_PRIMARY,
            selectcolor=Theme.BG_ELEVATED,
            activebackground=Theme.BG_ELEVATED,
            activeforeground=Theme.TEXT_PRIMARY,
            font=Theme.FONT_BODY,
            command=self.toggle_multi_selfdestruct
        )
        sd_check.pack(anchor=tk.W, pady=(0, Theme.SPACE_SM))
        
        # Self-destruct password container
        self.multi_sd_container = tk.Frame(sd_card.content, bg=Theme.BG_ELEVATED)
        
        sd_label = StyledLabel(self.multi_sd_container, text="Self-destruct password:", variant="body")
        sd_label.configure(bg=Theme.BG_ELEVATED)
        sd_label.pack(anchor=tk.W, pady=(0, Theme.SPACE_XS))
        
        self.multi_sd_password = PasswordField(self.multi_sd_container, show_confirm=True)
        self.multi_sd_password.configure(bg=Theme.BG_ELEVATED)
        for child in self.multi_sd_password.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.multi_sd_password.pack(fill=tk.X)
        
        # Decoy files card
        decoy_card = StyledCard(scrollable, title="Decoy Files")
        decoy_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        self.decoy_entries = []
        self.decoy_container = tk.Frame(decoy_card.content, bg=Theme.BG_ELEVATED)
        self.decoy_container.pack(fill=tk.X, pady=(0, Theme.SPACE_SM))
        
        add_decoy_btn = StyledButton(
            decoy_card.content,
            text="+ Add Decoy File",
            command=self.add_decoy_entry,
            variant="secondary",
            width=180,
            height=40
        )
        add_decoy_btn.pack()
        
        # Padding card
        padding_card = StyledCard(scrollable, title="Padding (Optional)")
        padding_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        # Padding checkbox
        self.multi_padding_var = tk.BooleanVar(value=False)
        padding_check = tk.Checkbutton(
            padding_card.content,
            text="Add padding to obscure file size",
            variable=self.multi_padding_var,
            bg=Theme.BG_ELEVATED,
            fg=Theme.TEXT_PRIMARY,
            selectcolor=Theme.BG_ELEVATED,
            activebackground=Theme.BG_ELEVATED,
            activeforeground=Theme.TEXT_PRIMARY,
            font=Theme.FONT_BODY,
            command=self.toggle_multi_padding
        )
        padding_check.pack(anchor=tk.W, pady=(0, Theme.SPACE_SM))
        
        # Padding input container
        self.multi_padding_container = tk.Frame(padding_card.content, bg=Theme.BG_ELEVATED)
        
        padding_input_frame = tk.Frame(self.multi_padding_container, bg=Theme.BG_ELEVATED)
        padding_input_frame.pack(fill=tk.X)
        
        padding_label = StyledLabel(padding_input_frame, text="Target final size:", variant="caption")
        padding_label.configure(bg=Theme.BG_ELEVATED)
        padding_label.pack(side=tk.LEFT, padx=(0, Theme.SPACE_SM))
        
        self.multi_padding_entry = StyledEntry(self.multi_padding_container, placeholder="0", width=10)
        self.multi_padding_entry.pack(side=tk.LEFT, padx=(0, Theme.SPACE_XS))
        
        mb_label = StyledLabel(padding_input_frame, text="MB", variant="caption")
        mb_label.configure(bg=Theme.BG_ELEVATED)
        mb_label.pack(side=tk.LEFT)
        
        # Estimated size label
        self.multi_estimate_label = StyledLabel(self.multi_padding_container, text="", variant="caption")
        self.multi_estimate_label.configure(bg=Theme.BG_ELEVATED, fg=Theme.TEXT_SECONDARY)
        self.multi_estimate_label.pack(anchor=tk.W, pady=(Theme.SPACE_XS, 0))
        
        # Encrypt button
        encrypt_btn = StyledButton(
            scrollable,
            text="Encrypt Files",
            command=self.encrypt_multi,
            variant="primary",
            width=200,
            height=48
        )
        encrypt_btn.pack(pady=Theme.SPACE_MD)
    
    def create_decrypt_tab(self):
        """Create decryption tab"""
        tab = tk.Frame(self.tab_content, bg=Theme.BG_ELEVATED)
        self.tabs["Decrypt"] = tab
        
        # Scrollable container
        canvas = tk.Canvas(tab, bg=Theme.BG_ELEVATED, highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview, bg=Theme.BG_ELEVATED)
        scrollable = tk.Frame(canvas, bg=Theme.BG_ELEVATED)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Encrypted file card
        file_card = StyledCard(scrollable, title="Encrypted File")
        file_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        self.decrypt_file = FileSelector(file_card.content, label="Select encrypted file")
        self.decrypt_file.configure(bg=Theme.BG_ELEVATED)
        for child in self.decrypt_file.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.decrypt_file.pack(fill=tk.X)
        
        # Password card
        pass_card = StyledCard(scrollable, title="Password")
        pass_card.pack(fill=tk.X, pady=(0, Theme.SPACE_MD))
        
        self.decrypt_password = PasswordField(pass_card.content, show_confirm=False, label="Enter password")
        self.decrypt_password.configure(bg=Theme.BG_ELEVATED)
        for child in self.decrypt_password.winfo_children():
            try:
                child.configure(bg=Theme.BG_ELEVATED)
            except:
                pass
        self.decrypt_password.pack(fill=tk.X)
        
        # Decrypt button
        decrypt_btn = StyledButton(
            scrollable,
            text="Decrypt File",
            command=self.decrypt_file_action,
            variant="success",
            width=200,
            height=48
        )
        decrypt_btn.pack(pady=Theme.SPACE_MD)
    
    def add_decoy_entry(self):
        """Add a new decoy file entry"""
        entry = DecoyFileEntry(self.decoy_container, len(self.decoy_entries), self.remove_decoy_entry)
        self.decoy_entries.append(entry)
    
    def remove_decoy_entry(self, entry):
        """Remove a decoy file entry"""
        if entry in self.decoy_entries:
            self.decoy_entries.remove(entry)
            entry.frame.destroy()
    
    def toggle_std_padding(self):
        """Toggle padding controls for standard tab"""
        if self.std_padding_var.get():
            self.std_padding_container.pack(fill=tk.X, pady=(Theme.SPACE_SM, 0))
        else:
            self.std_padding_container.pack_forget()
    
    def toggle_multi_padding(self):
        """Toggle padding controls for multi-decoy tab"""
        if self.multi_padding_var.get():
            self.multi_padding_container.pack(fill=tk.X, pady=(Theme.SPACE_SM, 0))
        else:
            self.multi_padding_container.pack_forget()
    
    def toggle_std_selfdestruct(self):
        """Toggle self-destruct controls for standard tab"""
        if self.std_sd_var.get():
            self.std_sd_container.pack(fill=tk.X, pady=(Theme.SPACE_SM, 0))
        else:
            self.std_sd_container.pack_forget()
    
    def toggle_multi_selfdestruct(self):
        """Toggle self-destruct controls for multi-decoy tab"""
        if self.multi_sd_var.get():
            self.multi_sd_container.pack(fill=tk.X, pady=(Theme.SPACE_SM, 0))
        else:
            self.multi_sd_container.pack_forget()
    
    def update_progress(self, message, value):
        """Update progress bar and status"""
        self.progress_bar.set_progress(value)
        self.status_label.configure(text=message)
        self.root.update_idletasks()
    
    def show_error(self, message):
        """Show error modal"""
        modal = StyledModal(
            self.root,
            title="Error",
            message=message,
            icon="⚠️",
            buttons=[("OK", lambda: modal.ok(), "primary")]
        )
        modal.wait_window()
    
    def show_success(self, message):
        """Show success modal"""
        modal = StyledModal(
            self.root,
            title="Success",
            message=message,
            icon="✓",
            buttons=[("OK", lambda: modal.ok(), "success")]
        )
        modal.wait_window()
    
    def show_question(self, title, message, on_yes, on_no):
        """Show yes/no question modal"""
        modal = StyledModal(
            self.root,
            title=title,
            message=message,
            icon="?",
            buttons=[
                ("Yes", lambda: (on_yes(), modal.destroy()), "primary"),
                ("No", lambda: (on_no(), modal.destroy()), "secondary")
            ]
        )
        modal.wait_window()
    
    def encrypt_standard(self):
        """Handle standard encryption"""
        real_path = self.std_real_file.get_path()
        fake_path = self.std_fake_file.get_path()
        
        if not real_path or not fake_path:
            self.show_error("Please select both real and decoy files")
            return
        
        valid, msg = self.std_password.validate()
        if not valid:
            self.show_error(msg)
            return
        
        password = self.std_password.get_password()
        
        # Get self-destruct password if enabled
        selfdestruct_password = None
        if self.std_sd_var.get():
            valid_sd, msg_sd = self.std_sd_password.validate()
            if not valid_sd:
                self.show_error(f"Self-destruct password: {msg_sd}")
                return
            selfdestruct_password = self.std_sd_password.get_password()
            
            # Ensure SD password is different from main password
            if selfdestruct_password == password:
                self.show_error("Self-destruct password must be different from main password")
                return
        
        # Get padding value
        padding_mb = 0
        if self.std_padding_var.get():
            try:
                padding_mb = float(self.std_padding_entry.get())
                if padding_mb < 0:
                    self.show_error("Padding size must be positive")
                    return
            except ValueError:
                self.show_error("Invalid padding size")
                return
        
        def encrypt_thread():
            try:
                with open(real_path, 'rb') as f:
                    real_data = f.read()
                with open(fake_path, 'rb') as f:
                    fake_data = f.read()
                
                # Show estimated size
                estimated_size = (len(real_data) + len(fake_data) * 2) // 2  # Rough estimate
                estimated_mb = estimated_size / (1024 * 1024)
                self.root.after(0, lambda: self.std_estimate_label.configure(
                    text=f"Estimated size after compression: ~{estimated_mb:.2f} MB"
                ))
                
                # Validate padding
                if padding_mb > 0 and padding_mb < estimated_mb:
                    self.root.after(0, lambda: self.show_error(
                        f"Padding size ({padding_mb} MB) must be >= estimated size ({estimated_mb:.2f} MB)"
                    ))
                    return
                
                self.update_progress("Compressing...", 20)
                self.update_progress("Encrypting...", 40)
                
                encrypted_data, fake_pass1, fake_pass2, comp_stats = EncryptionService.encrypt_standard(
                    real_data, fake_data, password, real_path, padding_mb, selfdestruct_password
                )
                
                self.update_progress("Saving...", 70)
                
                self.root.after(0, lambda: self.save_encrypted_file(
                    encrypted_data, real_path, fake_path,
                    fake_pass1, fake_pass2, comp_stats
                ))
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Encryption failed: {str(e)}"))
                self.root.after(0, lambda: self.update_progress("Error", 0))
        
        threading.Thread(target=encrypt_thread, daemon=True).start()
    
    def save_encrypted_file(self, encrypted_data, real_path, fake_path, fake_pass1, fake_pass2, comp_stats):
        """Save encrypted file and show completion dialog"""
        output_file = filedialog.asksaveasfilename(
            defaultextension=".hcrypt",
            filetypes=[("HoneyCrypt files", "*.hcrypt"), ("All files", "*.*")]
        )
        
        if output_file:
            try:
                with open(output_file, 'wb') as f:
                    f.write(encrypted_data)
                
                self.update_progress("Complete", 100)
                
                # Build compression info
                real_comp_info = ""
                if comp_stats['real']['compressed']:
                    savings = comp_stats['real']['savings_percent']
                    real_comp_info = f"  Real file: Compressed ({savings:.1f}% smaller)\n"
                else:
                    real_comp_info = "  Real file: Not compressed (already optimal)\n"
                
                fake_comp_info = ""
                if comp_stats['fake']['compressed']:
                    savings = comp_stats['fake']['savings_percent']
                    fake_comp_info = f"  Decoy file: Compressed ({savings:.1f}% smaller)\n"
                else:
                    fake_comp_info = "  Decoy file: Not compressed (already optimal)\n"
                
                final_size_mb = len(encrypted_data) / (1024 * 1024)
                
                # Show fake passwords and ask about secure deletion
                password_info = (
                    f"Encryption complete!\n\n"
                    f"Final file size: {final_size_mb:.2f} MB\n\n"
                    f"Compression Results:\n"
                    f"{real_comp_info}"
                    f"{fake_comp_info}\n"
                    f"Two fake passwords have been generated:\n\n"
                    f"Fake Password 1: {fake_pass1}\n"
                    f"Fake Password 2: {fake_pass2}\n\n"
                    f"Save these passwords in case of deniability.\n\n"
                    f"Securely delete original files?"
                )
                
                def on_yes():
                    CryptoEngine.secure_delete_file(real_path)
                    CryptoEngine.secure_delete_file(fake_path)
                    self.show_success("Files encrypted and originals securely deleted")
                
                def on_no():
                    self.show_success("Files encrypted successfully")
                
                self.show_question("Encryption Complete", password_info, on_yes, on_no)
                
            except Exception as e:
                self.show_error(f"Failed to save file: {str(e)}")
        
        self.update_progress("Ready", 0)
    
    def encrypt_multi(self):
        """Handle multi-decoy encryption"""
        real_path = self.multi_real_file.get_path()
        
        if not real_path:
            self.show_error("Please select a real file")
            return
        
        valid, msg = self.multi_password.validate()
        if not valid:
            self.show_error(msg)
            return
        
        if not self.decoy_entries:
            self.show_error("Please add at least one decoy file")
            return
        
        password = self.multi_password.get_password()
        
        # Get self-destruct password if enabled
        selfdestruct_password = None
        if self.multi_sd_var.get():
            valid_sd, msg_sd = self.multi_sd_password.validate()
            if not valid_sd:
                self.show_error(f"Self-destruct password: {msg_sd}")
                return
            selfdestruct_password = self.multi_sd_password.get_password()
            
            # Ensure SD password is different from main password
            if selfdestruct_password == password:
                self.show_error("Self-destruct password must be different from main password")
                return
        
        # Get padding value
        padding_mb = 0
        if self.multi_padding_var.get():
            try:
                padding_mb = float(self.multi_padding_entry.get())
                if padding_mb < 0:
                    self.show_error("Padding size must be positive")
                    return
            except ValueError:
                self.show_error("Invalid padding size")
                return
        
        def encrypt_thread():
            try:
                with open(real_path, 'rb') as f:
                    real_data = f.read()
                
                decoy_data = []
                decoy_paths = []
                for entry in self.decoy_entries:
                    data = entry.get_data()
                    if data:
                        decoy_data.append(data)
                        decoy_paths.append(data['path'])
                
                if not decoy_data:
                    self.root.after(0, lambda: self.show_error("Please add valid decoy files"))
                    return
                
                # Show estimated size
                total_size = len(real_data) + sum(len(d['data']) for d in decoy_data)
                estimated_mb = (total_size // 2) / (1024 * 1024)  # Rough estimate with compression
                self.root.after(0, lambda: self.multi_estimate_label.configure(
                    text=f"Estimated size after compression: ~{estimated_mb:.2f} MB"
                ))
                
                # Validate padding
                if padding_mb > 0 and padding_mb < estimated_mb:
                    self.root.after(0, lambda: self.show_error(
                        f"Padding size ({padding_mb} MB) must be >= estimated size ({estimated_mb:.2f} MB)"
                    ))
                    return
                
                self.update_progress("Compressing...", 20)
                self.update_progress("Encrypting...", 40)
                
                encrypted_data, comp_stats = EncryptionService.encrypt_multi_decoy(
                    real_data, decoy_data, password, real_path, padding_mb, selfdestruct_password
                )
                
                self.update_progress("Saving...", 70)
                
                self.root.after(0, lambda: self.save_encrypted_file_multi(
                    encrypted_data, real_path, decoy_paths, comp_stats
                ))
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Encryption failed: {str(e)}"))
                self.root.after(0, lambda: self.update_progress("Error", 0))
        
        threading.Thread(target=encrypt_thread, daemon=True).start()
    
    def save_encrypted_file_multi(self, encrypted_data, real_path, decoy_paths, comp_stats):
        """Save multi-decoy encrypted file"""
        output_file = filedialog.asksaveasfilename(
            defaultextension=".hcrypt",
            filetypes=[("HoneyCrypt files", "*.hcrypt"), ("All files", "*.*")]
        )
        
        if output_file:
            try:
                with open(output_file, 'wb') as f:
                    f.write(encrypted_data)
                
                self.update_progress("Complete", 100)
                
                # Build compression info
                comp_info = "Compression Results:\n"
                if comp_stats['real']['compressed']:
                    savings = comp_stats['real']['savings_percent']
                    comp_info += f"  Real file: Compressed ({savings:.1f}% smaller)\n"
                else:
                    comp_info += "  Real file: Not compressed (already optimal)\n"
                
                for i, stats in enumerate(comp_stats['decoys']):
                    if stats['compressed']:
                        savings = stats['savings_percent']
                        comp_info += f"  Decoy {i+1}: Compressed ({savings:.1f}% smaller)\n"
                    else:
                        comp_info += f"  Decoy {i+1}: Not compressed (already optimal)\n"
                
                final_size_mb = len(encrypted_data) / (1024 * 1024)
                comp_info += f"\nFinal file size: {final_size_mb:.2f} MB\n"
                
                def on_yes():
                    CryptoEngine.secure_delete_file(real_path)
                    for path in decoy_paths:
                        CryptoEngine.secure_delete_file(path)
                    self.show_success("Files encrypted and originals securely deleted")
                
                def on_no():
                    self.show_success("Files encrypted successfully")
                
                self.show_question(
                    "Encryption Complete",
                    f"Encryption successful!\n\n{comp_info}\nSecurely delete original files?",
                    on_yes,
                    on_no
                )
                
            except Exception as e:
                self.show_error(f"Failed to save file: {str(e)}")
        
        self.update_progress("Ready", 0)
    
    def decrypt_file_action(self):
        """Handle decryption"""
        file_path = self.decrypt_file.get_path()
        password = self.decrypt_password.get_password()
        
        if not file_path or not password:
            self.show_error("Please select a file and enter a password")
            return
        
        def decrypt_thread():
            try:
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                
                self.update_progress("Decrypting...", 50)
                
                decrypted_data, is_real = DecryptionService.decrypt_unified(
                    encrypted_data, password, file_path
                )
                
                if decrypted_data is None:
                    self.root.after(0, lambda: self.show_error("Invalid password or corrupted file"))
                    self.root.after(0, lambda: self.update_progress("Error", 0))
                    return
                
                self.root.after(0, lambda: self.save_decrypted_file(decrypted_data))
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Decryption failed: {str(e)}"))
                self.root.after(0, lambda: self.update_progress("Error", 0))
        
        threading.Thread(target=decrypt_thread, daemon=True).start()
    
    def save_decrypted_file(self, decrypted_data):
        """Save decrypted file"""
        output_file = filedialog.asksaveasfilename(
            defaultextension=".bin",
            filetypes=[("All files", "*.*")]
        )
        
        if output_file:
            try:
                with open(output_file, 'wb') as f:
                    f.write(decrypted_data)
                
                self.update_progress("Complete", 100)
                self.show_success("File decrypted successfully!")
                
            except Exception as e:
                self.show_error(f"Failed to save file: {str(e)}")
        
        self.update_progress("Ready", 0)

# ═══════════════════════════════════════════════════════════════════════
# APPLICATION ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    
    # Set window icon
    try:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_icon.ico')
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass
    
    app = HoneyCryptApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
