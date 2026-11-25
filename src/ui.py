import tkinter as tk
from tkinter import ttk, messagebox
from src.engine import TypingEngine

class TypingApp(tk.Tk):
    """Modern Tkinter dark-themed typing speed test GUI."""
    BG_COLOR = "#1e1e2e"
    PANEL_BG = "#25263a"
    TEXT_MUTED = "#6c7086"
    TEXT_CORRECT = "#a6e3a1"
    TEXT_WRONG = "#f38ba8"
    ACCENT_COLOR = "#89b4fa"
    FG_COLOR = "#cdd6f4"

    def __init__(self):
        super().__init__()
        self.title("Typing Speed Test")
        self.geometry("850x580")
        self.configure(bg=self.BG_COLOR)
        self.minsize(750, 480)

        self.engine = TypingEngine()
        self.user_input = ""
        self.timer_id = None
        self.time_remaining = 30

        self._setup_styles()
        self._create_widgets()
        self.bind("<Key>", self._on_key_press)
        self.reset_test()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG_COLOR)
        style.configure("Panel.TFrame", background=self.PANEL_BG)
        style.configure("TLabel", background=self.BG_COLOR, foreground=self.FG_COLOR, font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 18, "bold"), foreground=self.ACCENT_COLOR)
        style.configure("StatVal.TLabel", font=("Helvetica", 20, "bold"), foreground=self.ACCENT_COLOR, background=self.PANEL_BG)
        style.configure("StatLbl.TLabel", font=("Helvetica", 9), foreground=self.TEXT_MUTED, background=self.PANEL_BG)
        style.configure("TButton", font=("Helvetica", 10, "bold"), background=self.ACCENT_COLOR, foreground="#11111b", borderwidth=0)
        style.map("TButton", background=[("active", "#b4befe")])

    def _create_widgets(self):
        # Header Frame
        header_frame = ttk.Frame(self, style="TFrame")
        header_frame.pack(fill="x", px=25, py=15)
        
        ttk.Label(header_frame, text="⚡ TYPING SPEED TEST", style="Header.TLabel").pack(side="left")
        ttk.Button(header_frame, text="📊 History", command=self.show_history).pack(side="right")

        # Config Bar
        config_frame = ttk.Frame(self, style="Panel.TFrame")
        config_frame.pack(fill="x", px=25, py=10, ipady=5)

        ttk.Label(config_frame, text="Difficulty:", background=self.PANEL_BG).pack(side="left", px=(15, 5))
        self.diff_var = tk.StringVar(value="medium")
        diff_cb = ttk.Combobox(config_frame, textvariable=self.diff_var, values=["easy", "medium", "hard"], state="readonly", width=10)
        diff_cb.pack(side="left", px=5)
        diff_cb.bind("<<ComboboxSelected>>", lambda e: self.reset_test())

        ttk.Label(config_frame, text="Duration:", background=self.PANEL_BG).pack(side="left", px=(20, 5))
        self.dur_var = tk.IntVar(value=30)
        dur_cb = ttk.Combobox(config_frame, textvariable=self.dur_var, values=[15, 30, 60], state="readonly", width=5)
        dur_cb.pack(side="left", px=5)
        dur_cb.bind("<<ComboboxSelected>>", lambda e: self.reset_test())

        ttk.Button(config_frame, text="🔄 Restart", command=self.reset_test).pack(side="right", px=15)

        # Stats Dashboard
        stats_frame = ttk.Frame(self, style="TFrame")
        stats_frame.pack(fill="x", px=25, py=15)
        stats_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.lbl_time = self._create_stat_card(stats_frame, "TIME LEFT", "30s", 0)
        self.lbl_wpm = self._create_stat_card(stats_frame, "NET WPM", "0.0", 1)
        self.lbl_acc = self._create_stat_card(stats_frame, "ACCURACY", "100%", 2)
        self.lbl_cpm = self._create_stat_card(stats_frame, "CPM", "0", 3)

        # Text Box Container
        text_container = ttk.Frame(self, style="Panel.TFrame")
        text_container.pack(fill="both", expand=True, px=25, py=(0, 20))

        self.text_display = tk.Text(
            text_container,
            wrap="word",
            font=("Courier", 15),
            bg=self.PANEL_BG,
            fg=self.TEXT_MUTED,
            bd=0,
            highlightthickness=0,
            padx=20,
            pady=20
        )
        self.text_display.pack(fill="both", expand=True)
        self.text_display.tag_configure("correct", foreground=self.TEXT_CORRECT)
        self.text_display.tag_configure("incorrect", foreground=self.TEXT_WRONG, background="#45475a")
        self.text_display.tag_configure("cursor", underline=True, foreground=self.ACCENT_COLOR)
        self.text_display.tag_configure("untyped", foreground=self.TEXT_MUTED)
        self.text_display.config(state="disabled")

    def _create_stat_card(self, parent, title, initial_val, col):
        card = ttk.Frame(parent, style="Panel.TFrame")
        card.grid(row=0, column=col, sticky="ew", px=5)
        val_label = ttk.Label(card, text=initial_val, style="StatVal.TLabel")
        val_label.pack(py=(10, 0))
        ttk.Label(card, text=title, style="StatLbl.TLabel").pack(py=(0, 10))
        return val_label

    def reset_test(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        difficulty = self.diff_var.get()
        duration = int(self.dur_var.get())
        self.engine.start_test(difficulty=difficulty, duration=duration)
        self.user_input = ""
        self.time_remaining = duration

        self.lbl_time.config(text=f"{duration}s")
        self.lbl_wpm.config(text="0.0")
        self.lbl_acc.config(text="100%")
        self.lbl_cpm.config(text="0")

        self._render_text()

    def _on_key_press(self, event):
        if not self.engine.is_active:
            return

        # Handle backspace
        if event.keysym == "BackSpace":
            if len(self.user_input) > 0:
                self.user_input = self.user_input[:-1]
        elif len(event.char) == 1 and ord(event.char) >= 32:
            if len(self.user_input) < len(self.engine.target_text):
                self.user_input += event.char

        # Start timer tick on first character typed
        if len(self.user_input) == 1 and not self.timer_id:
            self._tick()

        self._render_text()
        self._update_stats()

        if len(self.user_input) >= len(self.engine.target_text):
            self.finish_test()

    def _tick(self):
        if not self.engine.is_active:
            return
        metrics = self.engine.evaluate(self.user_input)
        self.time_remaining = max(0, self.engine.duration - int(metrics["elapsed"]))
        self.lbl_time.config(text=f"{self.time_remaining}s")

        if self.time_remaining <= 0:
            self.finish_test()
        else:
            self.timer_id = self.after(200, self._tick)

    def _render_text(self):
        target = self.engine.target_text
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)

        for i, char in enumerate(target):
            if i < len(self.user_input):
                tag = "correct" if self.user_input[i] == char else "incorrect"
            elif i == len(self.user_input):
                tag = "cursor"
            else:
                tag = "untyped"
            self.text_display.insert(tk.END, char, tag)

        self.text_display.config(state="disabled")

    def _update_stats(self):
        metrics = self.engine.evaluate(self.user_input)
        self.lbl_wpm.config(text=f"{metrics['net_wpm']}")
        self.lbl_acc.config(text=f"{metrics['accuracy']}%")
        self.lbl_cpm.config(text=f"{int(metrics['cpm'])}")

    def finish_test(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        final_stats = self.engine.stop_test(self.user_input)
        if final_stats:
            msg = (
                f"🎉 Test Completed!\n\n"
                f"Net Speed: {final_stats['net_wpm']} WPM\n"
                f"Accuracy: {final_stats['accuracy']}%\n"
                f"Characters/Min: {final_stats['cpm']}\n"
                f"Total Typed: {final_stats['total_typed']} chars"
            )
            messagebox.showinfo("Results", msg)

    def show_history(self):
        history = self.engine.get_history()
        win = tk.Toplevel(self)
        win.title("Typing History")
        win.geometry("550x300")
        win.configure(bg=self.BG_COLOR)

        cols = ("Timestamp", "Diff", "Dur(s)", "WPM", "Acc (%)")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=10)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        tree.pack(fill="both", expand=True, px=15, py=15)

        for item in reversed(history):
            tree.insert("", tk.END, values=(
                item.get("timestamp", "-"),
                item.get("difficulty", "-"),
                item.get("duration", "-"),
                item.get("net_wpm", "-"),
                item.get("accuracy", "-")
            ))
