"""
Academic Poster Evaluation System - GUI Application

A user-friendly interface for evaluating academic poster using AI.
Runs all 4 evaluation approaches automatically and generates Excel comparison reports.
"""

import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Dict

from .backend import SecretManager, ServerManager, EvaluationClient, ResultsProcessor


# University / Professional Color Scheme (Calm + Accessible)
COLORS = {
    "navy": "#0B1F3B",
    "navy_2": "#123A6F",
    "accent": "#2563EB",
    "accent_2": "#1D4ED8",
    "success": "#16A34A",
    "warning": "#D97706",
    "danger": "#DC2626",
    "muted": "#64748B",

    "bg": "#F6F8FC",
    "card": "#FFFFFF",
    "soft": "#EEF2FF",
    "border": "#E5E7EB",
    "border_2": "#D1D5DB",

    "text": "#0F172A",
    "text_2": "#334155",
    "text_3": "#64748B",
}


class PosterEvaluationGUI:
    """Main GUI application for poster evaluation"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Academic Poster Evaluation System")
        self.root.geometry("1200x820")
        self.root.minsize(1020, 720)
        self.root.resizable(True, True)
        self.root.configure(bg=COLORS["bg"])

        # Backend components
        self.server_manager = ServerManager()
        self.client = EvaluationClient()
        self.secret_manager = SecretManager()

        # State variables
        self.folder_path: Optional[str] = None
        self.current_job_ids: Dict[str, str] = {}  # approach -> job_id
        self.results_data = []
        self.server_started = False

        # Styles + UI
        self.configure_styles()
        self.setup_ui()

        # Load saved API key if available
        self.load_saved_api_key()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # -----------------------------
    # Thread-safe UI helper
    # -----------------------------
    def ui(self, fn):
        """Run UI updates on the main thread safely."""
        self.root.after(0, fn)

    def _clear_focus(self):
        """Remove focus from buttons to avoid dotted focus/outline after click (Windows)."""
        # Setting focus to root clears the dotted focus rectangle on ttk buttons
        try:
            self.root.focus_set()
        except Exception:
            pass

    # -----------------------------
    # Styles
    # -----------------------------
    def configure_styles(self):
        """Configure modern tkinter styles"""
        style = ttk.Style()

        # Best looking built-in theme for custom styling
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Base
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Card.TFrame", background=COLORS["card"], relief="flat", borderwidth=0)
        style.configure("Header.TFrame", background=COLORS["navy"])

        # Typography
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"),
                        background=COLORS["navy"], foreground="white")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10),
                        background=COLORS["navy"], foreground="#DCE7FF")

        style.configure("Section.TLabel", font=("Segoe UI", 12, "bold"),
                        background=COLORS["card"], foreground=COLORS["navy_2"])

        style.configure("TLabel", font=("Segoe UI", 9),
                        background=COLORS["bg"], foreground=COLORS["text"])

        style.configure("Field.TLabel", font=("Segoe UI", 9),
                        background=COLORS["soft"], foreground=COLORS["text_3"],
                        padding=(12, 10))

        # Inputs
        style.configure("TEntry", font=("Segoe UI", 10), foreground=COLORS["text"])
        style.configure("TCheckbutton", background=COLORS["card"], foreground=COLORS["text_2"])

        # Buttons
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"),
                        padding=(14, 10), relief="flat", borderwidth=0)
        style.map("Primary.TButton",
                  background=[("active", COLORS["accent_2"]), ("!active", COLORS["accent"])],
                  foreground=[("active", "white"), ("!active", "white")])

        style.configure("Success.TButton", font=("Segoe UI", 10, "bold"),
                        padding=(14, 10), relief="flat", borderwidth=0)
        style.map("Success.TButton",
                  background=[("active", "#15803D"), ("!active", COLORS["success"])],
                  foreground=[("active", "white"), ("!active", "white")])

        style.configure("Ghost.TButton", font=("Segoe UI", 10, "bold"),
                        padding=(14, 10))
        style.map("Ghost.TButton",
                  background=[("active", "#E8EEF9"), ("!active", COLORS["soft"])],
                  foreground=[("active", COLORS["navy_2"]), ("!active", COLORS["navy_2"])])

        # Muted/Disabled Button
        style.configure("Mute.TButton", font=("Segoe UI", 10, "bold"),
                        padding=(14, 10), relief="flat", borderwidth=0)
        style.map("Mute.TButton",
                  background=[("disabled", "#D1D5DB")],
                  foreground=[("disabled", "#9CA3AF")])

        # Progress bar
        style.configure("TProgressbar",
                        troughcolor="#EEF2F7",
                        bordercolor=COLORS["border"],
                        lightcolor=COLORS["accent"],
                        darkcolor=COLORS["accent"])

        # Treeview (table)
        style.configure("Treeview",
                        font=("Segoe UI", 9),
                        rowheight=30,
                        background=COLORS["card"],
                        fieldbackground=COLORS["card"],
                        foreground=COLORS["text"])
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background=COLORS["soft"],
                        foreground=COLORS["navy_2"])
        style.map("Treeview",
                  background=[("selected", COLORS["accent"])],
                  foreground=[("selected", "white")])

    # -----------------------------
    # UI Layout
    # -----------------------------
    def setup_ui(self):
        # Root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # ===== Header =====
        header = ttk.Frame(self.root, style="Header.TFrame", padding=(22, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        left = ttk.Frame(header, style="Header.TFrame")
        left.grid(row=0, column=0, sticky="w")

        ttk.Label(left, text="Academic Poster Evaluation System", style="Title.TLabel").pack(anchor="w")
        ttk.Label(left, text="AI-powered academic poster evaluation system using GPT-4 Vision",
                  style="Subtitle.TLabel").pack(anchor="w")

        # ===== Main =====
        main = ttk.Frame(self.root, padding=(22, 18))
        main.grid(row=1, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(4, weight=1)   # results table grows

        # ===== Card: Configuration =====
        config_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        config_card.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        config_card.columnconfigure(0, weight=1)

        ttk.Label(config_card, text="Configuration", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )
        ttk.Separator(config_card, orient="horizontal").grid(row=1, column=0, sticky="ew", pady=(0, 14))

        # API Key
        api_row = ttk.Frame(config_card, style="Card.TFrame")
        api_row.grid(row=2, column=0, sticky="ew")
        api_row.columnconfigure(1, weight=1)

        ttk.Label(
            api_row,
            text="OpenAI API Key",
            background=COLORS["card"],
            foreground=COLORS["text_2"],
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=(0, 12))

        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(api_row, textvariable=self.api_key_var, show="•")
        self.api_key_entry.grid(row=0, column=1, sticky="ew")
        self.api_key_entry.bind("<KeyRelease>", lambda e: self.check_ready_state())

        self.show_key_var = tk.BooleanVar(value=False)
        self.show_key_checkbox = ttk.Checkbutton(
            api_row,
            text="Show",
            variable=self.show_key_var,
            command=self.toggle_api_key_visibility,
            takefocus=0,
        )
        self.show_key_checkbox.grid(row=0, column=2, sticky="e", padx=(10, 0))
        self.show_key_checkbox.bind("<Enter>", self._on_widget_enter)
        self.show_key_checkbox.bind("<Leave>", self._on_widget_leave)

        # Folder
        folder_row = ttk.Frame(config_card, style="Card.TFrame")
        folder_row.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        folder_row.columnconfigure(0, weight=1)

        ttk.Label(
            folder_row,
            text="Poster folder (images)",
            background=COLORS["card"],
            foreground=COLORS["text_2"],
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        folder_line = ttk.Frame(folder_row, style="Card.TFrame")
        folder_line.grid(row=1, column=0, sticky="ew")
        folder_line.columnconfigure(0, weight=1)

        self.folder_var = tk.StringVar(value="No folder selected")
        folder_display = ttk.Label(folder_line, textvariable=self.folder_var, style="Field.TLabel")
        folder_display.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.browse_btn = ttk.Button(
            folder_line,
            text="Browse",
            command=self.browse_folder,
            style="Ghost.TButton",
            takefocus=0,
        )
        self.browse_btn.grid(row=0, column=1, sticky="e")
        self.browse_btn.bind("<Enter>", self._on_widget_enter)
        self.browse_btn.bind("<Leave>", self._on_widget_leave)

        # ===== Action buttons (ONLY Evaluate button here) =====
        actions = ttk.Frame(main)
        actions.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        actions.columnconfigure(0, weight=1)

        self.run_btn = ttk.Button(
            actions,
            text="Evaluate Posters",
            command=self.start_evaluation,
            state=tk.DISABLED,
            style="Mute.TButton" if not self.folder_path else "Primary.TButton",
            takefocus=0,
        )
        self.run_btn.grid(row=0, column=0, sticky="ew")
        self.run_btn.bind("<Enter>", self._on_button_enter)
        self.run_btn.bind("<Leave>", self._on_button_leave)

        # ===== Progress card =====
        progress_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        progress_card.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        progress_card.columnconfigure(0, weight=1)

        ttk.Label(progress_card, text="Progress", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )
        ttk.Separator(progress_card, orient="horizontal").grid(row=1, column=0, sticky="ew", pady=(0, 14))

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(progress_card, variable=self.progress_var, maximum=100, mode="determinate")
        self.progress_bar.grid(row=2, column=0, sticky="ew")

        # Status "pill" (tk.Label for reliable bg)
        self.status_var = tk.StringVar(value="Ready. Enter API key and select a folder.")
        self.status_label = tk.Label(
            progress_card,
            textvariable=self.status_var,
            fg=COLORS["text_3"],
            bg=COLORS["card"],
            font=("Segoe UI", 9),
            padx=12,
            pady=10,
            anchor="w",
        )
        self.status_label.grid(row=3, column=0, sticky="ew", pady=(12, 0))

        # ===== Results card =====
        results_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        results_card.grid(row=4, column=0, sticky="nsew")
        results_card.columnconfigure(0, weight=1)
        results_card.rowconfigure(2, weight=1)

        # --- Header row: Results (left) + Download (right)
        results_header = ttk.Frame(results_card, style="Card.TFrame")
        results_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        results_header.columnconfigure(0, weight=1)

        ttk.Label(results_header, text="Results", style="Section.TLabel").grid(
            row=0, column=0, sticky="w"
        )

        # ✅ Download button
        self.download_btn = ttk.Button(
            results_header,
            text="Download",
            command=self.download_excel,
            state=tk.DISABLED,
            style="Success.TButton" if self.results_data else "Mute.TButton",
            takefocus=0,
        )
        self.download_btn.grid(row=0, column=1, sticky="e")
        self.download_btn.bind("<Enter>", self._on_button_enter)
        self.download_btn.bind("<Leave>", self._on_button_leave)

        ttk.Separator(results_card, orient="horizontal").grid(row=1, column=0, sticky="ew", pady=(0, 14))

        tree_frame = ttk.Frame(results_card, style="Card.TFrame")
        tree_frame.grid(row=2, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        columns = ("Project Number", "Publisher Names", "Direct", "Reasoning", "Deep Analysis", "Strict")
        self.results_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
        )
        vsb.config(command=self.results_tree.yview)
        hsb.config(command=self.results_tree.xview)

        # Headings
        for c in columns:
            self.results_tree.heading(c, text=c)

        # Column widths
        self.results_tree.column("Project Number", width=150, anchor=tk.CENTER)
        self.results_tree.column("Publisher Names", width=320, anchor=tk.W)
        self.results_tree.column("Direct", width=110, anchor=tk.CENTER)
        self.results_tree.column("Reasoning", width=110, anchor=tk.CENTER)
        self.results_tree.column("Deep Analysis", width=130, anchor=tk.CENTER)
        self.results_tree.column("Strict", width=110, anchor=tk.CENTER)

        # Zebra tags + optional score tags
        self.results_tree.tag_configure("odd", background="#FFFFFF")
        self.results_tree.tag_configure("even", background="#F8FAFF")
        self.results_tree.tag_configure("good", foreground=COLORS["success"])
        self.results_tree.tag_configure("warn", foreground=COLORS["warning"])
        self.results_tree.tag_configure("bad", foreground=COLORS["danger"])

        self.results_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

    # -----------------------------
    # UI Actions
    # -----------------------------
    def _on_button_enter(self, event):
        """Handle cursor on button hover"""
        try:
            state = event.widget.cget("state")
        except Exception:
            state = None

        if state == tk.DISABLED:
            event.widget.config(cursor="x_cursor")
        else:
            event.widget.config(cursor="hand2")

    def _on_button_leave(self, event):
        """Handle cursor/state when leaving button (safe for ttk + tk widgets)"""
        event.widget.config(cursor="")
        # ttk widgets may keep focus visual state; remove it safely
        if hasattr(event.widget, "state"):
            try:
                event.widget.state(["!focus"])
            except Exception:
                pass

    def _on_widget_enter(self, event):
        """Handle cursor on widget hover (checkbox, button)"""
        event.widget.config(cursor="hand2")

    def _on_widget_leave(self, event):
        """Handle cursor when leaving widget"""
        event.widget.config(cursor="")

    def toggle_api_key_visibility(self):
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="•")
        self._clear_focus()

    def load_saved_api_key(self):
        saved_key = self.secret_manager.load_api_key()
        if saved_key:
            self.api_key_var.set(saved_key)
            self.server_started = True
            self.update_status("API key loaded. Select a folder to begin.", color=COLORS["success"])
            self.check_ready_state()
        else:
            self.update_status("Ready. Enter API key and select a folder.", color=COLORS["muted"])

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Folder Containing Posters")
        if folder:
            self.folder_path = folder
            display_path = folder if len(folder) < 70 else "..." + folder[-67:]
            self.folder_var.set(display_path)
            self.check_ready_state()
        self._clear_focus()

    def check_ready_state(self):
        api_key = self.api_key_var.get().strip()
        has_folder = self.folder_path is not None

        if api_key and has_folder:
            self.run_btn.config(state=tk.NORMAL, style="Primary.TButton")
            self.update_status('Ready to evaluate. Click "Evaluate Posters".', color=COLORS["success"])
        else:
            self.run_btn.config(state=tk.DISABLED, style="Mute.TButton")
            if not api_key:
                self.update_status("Please enter your OpenAI API key.", color=COLORS["warning"])
            elif not has_folder:
                self.update_status("Please select a folder containing poster images.", color=COLORS["warning"])

    def start_evaluation(self):
        self._clear_focus()

        # Disable buttons
        self.run_btn.config(state=tk.DISABLED, style="Mute.TButton")
        self.download_btn.config(state=tk.DISABLED, style="Mute.TButton")

        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results_data = []

        api_key = self.api_key_var.get().strip()
        self.secret_manager.save_api_key(api_key)

        thread = threading.Thread(target=self.run_evaluation_thread, daemon=True)
        thread.start()

    # -----------------------------
    # Background Work
    # -----------------------------
    def run_evaluation_thread(self):
        try:
            self.update_status("Server is running. Starting evaluation...", color=COLORS["muted"])
            self.update_progress(10)

            approaches = ["direct", "reasoning", "deep_analysis", "strict"]
            self.current_job_ids = {}
            approach_count = len(approaches)

            for i, approach in enumerate(approaches):
                approach_name = approach.replace("_", " ").title()
                self.update_status(f"Uploading posters for “{approach_name}” ({i+1}/{approach_count})...",
                                   color=COLORS["muted"])
                self.update_progress(10 + (i * 15))

                job_id = self.client.upload_batch(self.folder_path, approach)
                if not job_id:
                    self.update_status(f"Failed to upload for {approach_name}.", color=COLORS["danger"])
                    continue

                self.current_job_ids[approach] = job_id
                self.update_status(f"{approach_name} queued (Job ID: {job_id[:8]}…)", color=COLORS["success"])

            if not self.current_job_ids:
                self.update_status("No evaluations were started.", color=COLORS["danger"])
                self.ui(lambda: self.run_btn.config(state=tk.NORMAL, style="Primary.TButton"))
                return

            self.update_status("Processing evaluations… this may take several minutes.", color=COLORS["muted"])
            self.update_progress(70)

            completed = set()
            failed = set()
            max_wait = 600
            start_time = time.time()

            while len(completed) < len(self.current_job_ids) and len(failed) == 0:
                if time.time() - start_time > max_wait:
                    self.update_status("Evaluation timed out after 10 minutes.", color=COLORS["danger"])
                    break

                for approach, job_id in self.current_job_ids.items():
                    if approach in completed or approach in failed:
                        continue

                    status = self.client.poll_job_status(job_id)
                    job_status = status.get("status", "unknown")

                    if job_status == "failed":
                        error_msg = status.get("errors", [])
                        if error_msg and any("OpenAI API" in str(err) for err in error_msg):
                            self.update_status("CRITICAL: OpenAI API failure. Check API key and retry.",
                                               color=COLORS["danger"])
                            failed.add(approach)
                            break
                        else:
                            failed.add(approach)
                            approach_name = approach.replace("_", " ").title()
                            self.update_status(f"{approach_name} failed ({len(completed)}/{len(self.current_job_ids)})",
                                               color=COLORS["warning"])

                    elif job_status == "completed":
                        completed.add(approach)
                        approach_name = approach.replace("_", " ").title()
                        self.update_status(f"{approach_name} completed ({len(completed)}/{len(self.current_job_ids)})",
                                           color=COLORS["success"])
                        progress = 70 + (len(completed) / len(self.current_job_ids) * 20)
                        self.update_progress(progress)

                if failed and "OpenAI API" in self.status_var.get():
                    break

                time.sleep(2)

            if failed and "OpenAI API" in self.status_var.get():
                self.update_status("Stopped due to OpenAI API failure. Fix API key and try again.",
                                   color=COLORS["danger"])
                return

            self.update_status("Combining results from all approaches…", color=COLORS["muted"])
            self.update_progress(95)

            combined_results = ResultsProcessor.combine_multi_approach_results(
                self.current_job_ids,
                self.client
            )

            if combined_results:
                self.results_data = combined_results
                self.ui(lambda: self.display_results(combined_results))
                self.update_status(f"Done. {len(combined_results)} posters evaluated. Excel is ready.",
                                   color=COLORS["success"])
                self.update_progress(100)
                self.ui(lambda: self.download_btn.config(state=tk.NORMAL, style="Success.TButton"))
            else:
                self.update_status("No results to display.", color=COLORS["danger"])

        except Exception as e:
            self.update_status(f"Error: {str(e)}", color=COLORS["danger"])
        finally:
            self.ui(lambda: self.run_btn.config(state=tk.NORMAL, style="Primary.TButton"))

    # -----------------------------
    # Results rendering
    # -----------------------------
    def _grade_tag(self, grade: float):
        """Optional: color-code by grade (adjust thresholds to your rubric)."""
        try:
            g = float(grade)
        except Exception:
            return None
        if g >= 85:
            return "good"
        if g >= 70:
            return "warn"
        return "bad"

    def display_results(self, results):
        for i, result in enumerate(results):
            row_tag = "even" if i % 2 == 0 else "odd"

            direct = result.get("direct_grade", 0)
            reasoning = result.get("reasoning_grade", 0)
            deep = result.get("deep_analysis_grade", 0)
            strict = result.get("strict_grade", 0)

            try:
                avg = (float(direct) + float(reasoning) + float(deep) + float(strict)) / 4.0
            except Exception:
                avg = 0

            score_tag = self._grade_tag(avg)
            tags = (row_tag,) if not score_tag else (row_tag, score_tag)

            self.results_tree.insert(
                "",
                tk.END,
                values=(
                    result.get("project_number", "N/A"),
                    result.get("presenter_names", "N/A"),
                    direct,
                    reasoning,
                    deep,
                    strict,
                ),
                tags=tags
            )

    # -----------------------------
    # Excel
    # -----------------------------
    def download_excel(self):
        self._clear_focus()

        if not self.results_data:
            messagebox.showwarning("No Results", "Results are not available yet.")
            return

        if not self.current_job_ids:
            messagebox.showerror("Error", "No results to download.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Excel Results",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if not save_path:
            return



        self.update_status("Downloading Excel file…", color=COLORS["muted"])
        # Now we download the comparison report using all job IDs
        ok = self.client.download_comparison_excel(self.current_job_ids, save_path)
        if ok:
            messagebox.showinfo("Success", f"Excel file saved to:\n{save_path}")
            self.update_status("Excel downloaded successfully.", color=COLORS["success"])
        else:
            messagebox.showerror("Error", f"Failed to download Excel file.\nCheck server logs for details.")
            self.update_status("Error downloading Excel file.", color=COLORS["danger"])

    # -----------------------------
    # Status + Progress
    # -----------------------------
    def update_status(self, message: str, color: str = None):
        if color is None:
            color = COLORS["muted"]
        self.ui(lambda: self._set_status(message, color))

    def _set_status(self, message: str, color: str):
        self.status_var.set(message)

        if color == COLORS["success"]:
            bg = "#EAF7EF"
        elif color == COLORS["warning"]:
            bg = "#FFF4E5"
        elif color == COLORS["danger"]:
            bg = "#FDECEC"
        else:
            bg = COLORS["card"]

        self.status_label.config(fg=color, bg=bg)

    def update_progress(self, value: float):
        self.ui(lambda: self.progress_var.set(value))

    # -----------------------------
    # Window close
    # -----------------------------
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit? The server will be stopped."):
            self.server_manager.stop_server()
            self.root.destroy()
