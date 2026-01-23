"""
Academic Poster Evaluation System - GUI Application

A user-friendly interface for evaluating academic posters using AI.
Runs all 4 evaluation approaches automatically and generates Excel comparison reports.
"""

import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Dict

from .backend import SecretManager, ServerManager, EvaluationClient, ResultsProcessor


class PosterEvaluationGUI:
    """Main GUI application for poster evaluation"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Poster Evaluation System")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Backend components
        self.server_manager = ServerManager()
        self.client = EvaluationClient()
        self.secret_manager = SecretManager()
        
        # State variables
        self.folder_path: Optional[str] = None
        self.current_job_ids: Dict[str, str] = {}  # approach -> job_id
        self.results_data = []
        self.server_started = False
        
        # Setup GUI
        self.setup_ui()
        
        # Load saved API key if available
        self.load_saved_api_key()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Setup all UI components"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Academic Poster Evaluation System",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Evaluates posters using 4 AI approaches: Direct, Reasoning, Deep Analysis, and Strict",
            font=("Arial", 10)
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # API Key Section
        row = 2
        ttk.Label(main_frame, text="OpenAI API Key:", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(
            main_frame,
            textvariable=self.api_key_var,
            show="*",
            width=50
        )
        self.api_key_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Show/Hide API Key button
        self.show_key_var = tk.BooleanVar(value=False)
        show_key_btn = ttk.Checkbutton(
            main_frame,
            text="Show",
            variable=self.show_key_var,
            command=self.toggle_api_key_visibility
        )
        show_key_btn.grid(row=row, column=2, sticky=tk.W, pady=5)
        
        # Folder Selection Section
        row += 1
        ttk.Label(main_frame, text="Posters Folder:", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        
        self.folder_var = tk.StringVar(value="No folder selected")
        folder_label = ttk.Label(
            main_frame,
            textvariable=self.folder_var,
            relief=tk.SUNKEN,
            padding=5
        )
        folder_label.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        browse_btn = ttk.Button(
            main_frame,
            text="Browse...",
            command=self.browse_folder
        )
        browse_btn.grid(row=row, column=2, sticky=tk.W, pady=5)
        
        # Run Evaluation Button
        row += 1
        self.run_btn = ttk.Button(
            main_frame,
            text="Evaluate Posters",
            command=self.start_evaluation,
            state=tk.DISABLED
        )
        self.run_btn.grid(row=row, column=0, columnspan=3, pady=20)
        
        # Progress Section
        row += 1
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.grid(row=row, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Status Label
        row += 1
        self.status_var = tk.StringVar(value="Ready. Please enter API key and select folder.")
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 9),
            foreground="blue"
        )
        self.status_label.grid(row=row, column=0, columnspan=3, pady=5)
        
        # Results Table
        row += 1
        ttk.Label(main_frame, text="Results:", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(20, 5)
        )
        
        # Create Treeview with scrollbar
        row += 1
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Configure main_frame to expand results table
        main_frame.rowconfigure(row, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ("Project Number", "Publisher Names", "Direct", "Reasoning", "Deep Analysis", "Strict")
        self.results_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=self.results_tree.yview)
        hsb.config(command=self.results_tree.xview)
        
        # Configure columns
        self.results_tree.heading("Project Number", text="Project Number")
        self.results_tree.heading("Publisher Names", text="Publisher Names")
        self.results_tree.heading("Direct", text="Direct Grade")
        self.results_tree.heading("Reasoning", text="Reasoning Grade")
        self.results_tree.heading("Deep Analysis", text="Deep Analysis Grade")
        self.results_tree.heading("Strict", text="Strict Grade")

        self.results_tree.column("Project Number", width=120)
        self.results_tree.column("Publisher Names", width=250)
        self.results_tree.column("Direct", width=80, anchor=tk.CENTER)
        self.results_tree.column("Reasoning", width=80, anchor=tk.CENTER)
        self.results_tree.column("Deep Analysis", width=120, anchor=tk.CENTER)
        self.results_tree.column("Strict", width=80, anchor=tk.CENTER)
        
        # Grid layout
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Download Excel Button
        row += 1
        self.download_btn = ttk.Button(
            main_frame,
            text="Download Excel Results",
            command=self.download_excel,
            state=tk.DISABLED
        )
        self.download_btn.grid(row=row, column=0, columnspan=3, pady=10)
    
    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
    
    def load_saved_api_key(self):
        """Load API key from .secret file if available"""
        saved_key = self.secret_manager.load_api_key()
        if saved_key:
            self.api_key_var.set(saved_key)
            # Server is managed by run.py, so just update status
            self.status_var.set("API key loaded. Server is running in background. Select folder to continue.")
            self.server_started = True
            self.check_ready_state()
        else:
            self.status_var.set("Ready. Please enter API key and select folder.")
    
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(title="Select Folder Containing Posters")
        if folder:
            self.folder_path = folder
            self.folder_var.set(folder)
            self.check_ready_state()
    
    def check_ready_state(self):
        """Check if ready to run evaluation and enable/disable button"""
        api_key = self.api_key_var.get().strip()
        has_folder = self.folder_path is not None
        
        if api_key and has_folder:
            self.run_btn.config(state=tk.NORMAL)
            self.status_var.set("Ready to evaluate. Click 'Evaluate Posters' to start.")
        else:
            self.run_btn.config(state=tk.DISABLED)
            if not api_key:
                self.status_var.set("Please enter your OpenAI API key.")
            elif not has_folder:
                self.status_var.set("Please select a folder containing poster images.")
    def start_evaluation(self):
        """Start evaluation process in background thread"""
        # Disable button to prevent multiple clicks
        self.run_btn.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.DISABLED)
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results_data = []
        
        # Save API key
        api_key = self.api_key_var.get().strip()
        self.secret_manager.save_api_key(api_key)
        
        # Start evaluation in background thread
        thread = threading.Thread(target=self.run_evaluation_thread, daemon=True)
        thread.start()
    
    def run_evaluation_thread(self):
        """Background thread for running evaluation"""
        try:
            # Server is already running from run.py
            self.update_status("Server is already running. Starting evaluation...")
            self.update_progress(10)
            
            # Step 1: Run all 4 approaches
            approaches = ['direct', 'reasoning', 'deep_analysis', 'strict']
            self.current_job_ids = {}
            
            for i, approach in enumerate(approaches):
                self.update_status(f"Uploading posters for evaluation...")
                progress = 10 + (i * 15)
                self.update_progress(progress)
                
                # Upload batch with specific approach
                job_id = self.client.upload_batch(self.folder_path, approach)
                if not job_id:
                    self.update_status(f"Error: Failed to upload for {approach} approach.")
                    continue
                
                self.current_job_ids[approach] = job_id
                self.update_status(f"Evaluation request sent to GPT backend using '{approach}' approach. Job ID: {job_id}")
            
            if not self.current_job_ids:
                self.update_status("Error: No evaluations were started.")
                self.run_btn.config(state=tk.NORMAL)
                return
            
            # Step 3: Poll all jobs until complete
            self.update_status("Processing evaluations... This may take several minutes.")
            self.update_progress(70)
            
            completed = set()
            failed = set()
            max_wait = 600  # 10 minutes max
            start_time = time.time()
            
            while len(completed) < len(self.current_job_ids) and len(failed) == 0:
                if time.time() - start_time > max_wait:
                    self.update_status("Error: Evaluation timed out.", color="red")
                    break
                
                for approach, job_id in self.current_job_ids.items():
                    if approach in completed or approach in failed:
                        continue
                    
                    status = self.client.poll_job_status(job_id)
                    job_status = status.get('status', 'unknown')
                    
                    # Check for OpenAI API failures
                    if job_status == 'failed':
                        error_msg = status.get('errors', [])
                        if error_msg and any('OpenAI API' in str(err) for err in error_msg):
                            self.update_status(
                                f"CRITICAL: OpenAI API failure detected. Stopping evaluation: {error_msg[0] if error_msg else 'Unknown error'}",
                                color="red"
                            )
                            failed.add(approach)
                            # Stop all processing
                            break
                        else:
                            # Non-critical failure
                            failed.add(approach)
                            self.update_status(f"Failed: {approach} ({len(completed)}/{len(self.current_job_ids)})", color="red")
                    elif job_status == 'completed':
                        completed.add(approach)
                        self.update_status(f"Completed: {approach} ({len(completed)}/{len(self.current_job_ids)})")
                        progress = 70 + (len(completed) / len(self.current_job_ids) * 20)
                        self.update_progress(progress)
                
                # Break if critical failure detected
                if failed and any('OpenAI API' in str(self.status_var.get()) for _ in [1]):
                    break
                
                time.sleep(2)  # Poll every 2 seconds
            
            # Check if there were critical failures
            if failed and 'OpenAI API' in self.status_var.get():
                self.update_status(
                    "Evaluation stopped due to OpenAI API failure. Please check your API key and try again.",
                    color="red"
                )
                return
            
            # Step 4: Combine and display results
            self.update_status("Combining results from all approaches responses...")
            self.update_progress(95)
            
            combined_results = ResultsProcessor.combine_multi_approach_results(
                self.current_job_ids,
                self.client
            )
            
            if combined_results:
                self.results_data = combined_results
                self.display_results(combined_results)
                self.update_status(f"Evaluation complete! {len(combined_results)} posters evaluated.")
                self.update_progress(100)
                self.download_btn.config(state=tk.NORMAL)
            else:
                self.update_status("Error: No results to display.")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            self.run_btn.config(state=tk.NORMAL)
    
    def display_results(self, results):
        """Display results in TreeView"""
        for result in results:
            self.results_tree.insert('', tk.END, values=(
                result.get('project_number', 'N/A'),
                result.get('presenter_names', 'N/A'),
                result.get('direct_grade', 0),
                result.get('reasoning_grade', 0),
                result.get('deep_analysis_grade', 0),
                result.get('strict_grade', 0)
            ))
    
    def download_excel(self):
        """Download Excel file with results"""
        if not self.current_job_ids:
            messagebox.showerror("Error", "No results to download.")
            return
        
        # Ask user where to save
        save_path = filedialog.asksaveasfilename(
            title="Save Excel Results",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not save_path:
            return  # User cancelled
        
        # Use first job ID to download (we'll need to implement multi-approach Excel endpoint)
        first_job_id = list(self.current_job_ids.values())[0]
        
        self.update_status("Downloading Excel file...")
        if self.client.download_excel(first_job_id, save_path):
            messagebox.showinfo("Success", f"Excel file saved to:\n{save_path}")
            self.update_status("Excel file downloaded successfully.")
        else:
            messagebox.showerror("Error", "Failed to download Excel file.")
            self.update_status("Error downloading Excel file.")
    
    def update_status(self, message: str, color: str = "blue"):
        """Update status label with optional color (thread-safe)"""
        self.root.after(0, lambda: self._set_status(message, color))
    
    def _set_status(self, message: str, color: str = "blue"):
        """Set status message and color"""
        self.status_var.set(message)
        self.status_label.config(foreground=color)
    
    def update_progress(self, value: float):
        """Update progress bar (thread-safe)"""
        self.root.after(0, lambda: self.progress_var.set(value))
    
    def on_closing(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit? The server will be stopped."):
            self.server_manager.stop_server()
            self.root.destroy()
