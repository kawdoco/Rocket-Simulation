import tkinter as tk
from tkinter import ttk
from Rocket import PRESETS


class SelectionScreen(ttk.Frame):
    """
    Advanced Space-themed Rocket Selection Screen using OOP concepts.
    Provides custom styling, dynamic preset previewing, and configuration.
    """

    def __init__(self, parent, on_launch):
        super().__init__(parent)
        self.on_launch = on_launch
        
        # Keep native keys list for reference
        self.preset_keys = list(PRESETS.keys())
        
        # Use IntVar to store index or type-safe selection
        self.selected_index = tk.IntVar(value=0)
        self.launch_angle = tk.DoubleVar(value=45.0)

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self):
        """Encapsulated style settings for Space Theme."""
        style = ttk.Style()
        style.configure("Space.TFrame", background="#0a0e1a")
        style.configure("Header.TLabel", background="#0a0e1a", foreground="#00f0ff", font=("Helvetica", 20, "bold"))
        style.configure("SubHeader.TLabel", background="#0a0e1a", foreground="#a0aabb", font=("Helvetica", 11))
        style.configure("Card.TFrame", background="#121829", relief="flat")
        style.configure("CardLabel.TLabel", background="#121829", foreground="#ffffff", font=("Helvetica", 10))

    def _build_ui(self):
        self.configure(style="Space.TFrame")

        # Top Banner
        header_frame = ttk.Frame(self, style="Space.TFrame")
        header_frame.pack(fill=tk.X, padx=30, pady=(20, 10))

        ttk.Label(header_frame, text="🚀 BCI ROCKET SIMULAT0R", style="Header.TLabel").pack(anchor=tk.W)
        ttk.Label(header_frame, text="Select an orbital configuration preset & trajectory angle below.", style="SubHeader.TLabel").pack(anchor=tk.W, pady=(2, 0))

        # Main Layout
        main_container = ttk.Frame(self, style="Space.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Left Column: Presets & Controls
        left_panel = ttk.Frame(main_container, style="Space.TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        ttk.Label(left_panel, text="CHOOSE ROCKET PRESET", style="SubHeader.TLabel").pack(anchor=tk.W, pady=(0, 10))

        # Radio Selectors for Presets
        for idx, preset_key in enumerate(self.preset_keys):
            card = ttk.Frame(left_panel, style="Card.TFrame", padding=10)
            card.pack(fill=tk.X, pady=5)

            rb = tk.Radiobutton(
                card,
                text=f"  Rocket Preset {preset_key}",
                variable=self.selected_index,
                value=idx,
                bg="#121829",
                fg="#00f0ff",
                selectcolor="#0a0e1a",
                activebackground="#121829",
                activeforeground="#ffffff",
                font=("Helvetica", 11, "bold"),
                anchor=tk.W,
                command=self._update_preview
            )
            rb.pack(fill=tk.X)

        # Launch Angle Slider
        angle_card = ttk.Frame(left_panel, style="Card.TFrame", padding=15)
        angle_card.pack(fill=tk.X, pady=(15, 0))

        ttk.Label(angle_card, text="Launch Angle (Degrees):", style="CardLabel.TLabel").pack(anchor=tk.W)
        
        self.angle_label = ttk.Label(angle_card, text="45.0°", style="CardLabel.TLabel", font=("Helvetica", 11, "bold"))
        self.angle_label.pack(anchor=tk.E, pady=(0, 5))

        angle_slider = ttk.Scale(
            angle_card,
            from_=10.0,
            to=85.0,
            variable=self.launch_angle,
            orient=tk.HORIZONTAL,
            command=self._on_angle_change
        )
        angle_slider.pack(fill=tk.X)

        # Right Column: Specification Preview
        self.right_panel = ttk.Frame(main_container, style="Card.TFrame", padding=20)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

        ttk.Label(self.right_panel, text="SPECIFICATION PREVIEW", style="CardLabel.TLabel", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        self.specs_label = ttk.Label(self.right_panel, text="", style="CardLabel.TLabel", font=("Courier", 10))
        self.specs_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)

        # Bottom Action Bar
        action_bar = ttk.Frame(self, style="Space.TFrame")
        action_bar.pack(fill=tk.X, padx=30, pady=20)

        launch_btn = tk.Button(
            action_bar,
            text="🚀 INITIATE LAUNCH SIMULATION",
            bg="#00f0ff",
            fg="#0a0e1a",
            activebackground="#00c8d6",
            activeforeground="#0a0e1a",
            font=("Helvetica", 12, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._handle_launch
        )
        launch_btn.pack(side=tk.RIGHT)

        self._update_preview()

    def _get_current_key(self):
        idx = self.selected_index.get()
        return self.preset_keys[idx]

    def _on_angle_change(self, val):
        self.angle_label.config(text=f"{float(val):.1f}°")

    def _update_preview(self):
        preset_key = self._get_current_key()
        preset_data = PRESETS.get(preset_key, {})
        
        details = f"Selected Preset Key: {preset_key}\n"
        details += "=" * 35 + "\n\n"
        
        if isinstance(preset_data, dict):
            for k, v in preset_data.items():
                details += f"{str(k):<18}: {v}\n"
        else:
            details += f"Data: {preset_data}\n"
            
        self.specs_label.config(text=details)

    def _handle_launch(self):
        if callable(self.on_launch):
            self.on_launch(self._get_current_key(), self.launch_angle.get())