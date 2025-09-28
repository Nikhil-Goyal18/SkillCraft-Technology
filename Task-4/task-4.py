import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime
import os
import threading

class FocusedKeyLogger:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Focused Key Logger")
        self.root.geometry("700x500")
        self.logging = False
        self.buffer = []
        self.flush_interval = 5
        self.log_file_path = os.path.join(os.getcwd(), f"keypress_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.start_periodic_flush()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=8, pady=6)
        self.start_btn = tk.Button(top_frame, text="Start Logging", width=14, command=self.toggle_logging)
        self.start_btn.pack(side=tk.LEFT, padx=4)
        self.stop_btn = tk.Button(top_frame, text="Stop Logging", width=14, command=self.stop_logging, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=4)
        self.save_btn = tk.Button(top_frame, text="Save As...", width=12, command=self.save_as)
        self.save_btn.pack(side=tk.LEFT, padx=4)
        self.clear_btn = tk.Button(top_frame, text="Clear Log", width=12, command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=4)
        self.info_label = tk.Label(top_frame, text="Focus this window and type. Only keys while this window is focused are recorded.")
        self.info_label.pack(side=tk.LEFT, padx=8)
        txt_frame = tk.Frame(self.root)
        txt_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        self.display = scrolledtext.ScrolledText(txt_frame, wrap=tk.WORD, state=tk.NORMAL)
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.insert(tk.END, "Keypress buffer (visible). Start logging to write to file.\n\n")
        self.display.configure(state=tk.DISABLED)
        self.root.bind("<Key>", self.on_key)

    def toggle_logging(self):
        if not self.logging:
            self.start_logging()
        else:
            self.stop_logging()

    def start_logging(self):
        self.logging = True
        self.start_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        self.append_display(f"Logging started | file: {self.log_file_path}\n")

    def stop_logging(self):
        if self.logging:
            self.logging = False
            self.start_btn.configure(state=tk.NORMAL)
            self.stop_btn.configure(state=tk.DISABLED)
            self.append_display("Logging stopped\n")
            self.flush_buffer_to_file()

    def on_key(self, event):
        if not event.keysym:
            return
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        key_repr = event.keysym
        if len(event.char) == 1 and event.char.isprintable():
            key_text = event.char
        else:
            key_text = f"<{key_repr}>"
        entry = f"{ts} {key_text}\n"
        self.append_to_buffer(entry)

    def append_to_buffer(self, text):
        self.buffer.append(text)
        self.append_display(text)

    def append_display(self, text):
        self.display.configure(state=tk.NORMAL)
        self.display.insert(tk.END, text)
        self.display.see(tk.END)
        self.display.configure(state=tk.DISABLED)

    def flush_buffer_to_file(self):
        if not self.buffer:
            return
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.writelines(self.buffer)
            self.buffer = []
            self.append_display(f"[Flushed to file at {datetime.now().strftime('%H:%M:%S')}]\n")
        except Exception as e:
            messagebox.showerror("Write Error", f"Failed to write log file:\n{e}")

    def start_periodic_flush(self):
        def periodic():
            while True:
                threading.Event().wait(self.flush_interval)
                if not self.root.winfo_exists():
                    break
                if not self.logging:
                    continue
                try:
                    self.root.after(0, self.flush_buffer_to_file)
                except:
                    pass
        t = threading.Thread(target=periodic, daemon=True)
        t.start()

    def save_as(self):
        p = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if p:
            try:
                if os.path.exists(self.log_file_path):
                    with open(self.log_file_path, "r", encoding="utf-8") as src, open(p, "w", encoding="utf-8") as dst:
                        dst.write(src.read())
                else:
                    with open(p, "w", encoding="utf-8") as dst:
                        dst.write("No logged data yet.\n")
                messagebox.showinfo("Saved", f"Log saved to:\n{p}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def clear_log(self):
        if messagebox.askyesno("Confirm", "Clear on-screen log and buffer? This does not delete existing file."):
            self.display.configure(state=tk.NORMAL)
            self.display.delete("1.0", tk.END)
            self.display.configure(state=tk.DISABLED)
            self.buffer = []
            self.append_display("On-screen log cleared\n")

    def on_close(self):
        if self.logging:
            if not messagebox.askyesno("Exit", "Logging is active. Stop logging and exit?"):
                return
        self.flush_buffer_to_file()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FocusedKeyLogger()
    app.run()
