from tkinter import ttk, filedialog, messagebox
import tkinter as tk
import os
import shutil
import sys


class EndConnection:

    def __init__(self, connection, main_window=None):
        self.connection = connection
        self.main_window = main_window
        self.root = None
        self.history_saved = False
        self.history_folder = "history"

    def display_window(self):
        self.root = tk.Tk()
        self.root.title("End Connection")
        window_width = 410
        window_height = 150
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=15)

        save_button = ttk.Button(frame, text="Save history before closing", command=self.save_history)
        save_button.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        end_connection_button = ttk.Button(frame, text="Close without saving history", command=self.end_connection)
        end_connection_button.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        back_to_menu_button = ttk.Button(frame, text="Back to main menu", command=self.go_to_main_window)
        back_to_menu_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

    def end_connection(self):
        if not self.history_saved and os.path.exists(self.history_folder):
            result = messagebox.askquestion("Question", "Your import history won't be saved. Do you want to end the "
                                                        "connection?")
            if result == 'no':
                return
            else:
                shutil.rmtree(self.history_folder)
                self.connection.close()
                self.root.destroy()
                sys.exit()
        else:
            if os.path.exists(self.history_folder):
                shutil.rmtree(self.history_folder)
            self.connection.close()
            self.root.destroy()
            sys.exit()

    def save_history(self):
        if not os.path.exists(self.history_folder):
            messagebox.showerror("Error", "No history to save")
            return
        else:
            new_folder = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save as",
                initialfile="history",
                filetypes=[("Folder", "")],
            )
            if new_folder:
                try:
                    shutil.copytree(self.history_folder, new_folder)
                    messagebox.showinfo("Information", "Change history has been saved successfully.")
                    self.history_saved = True
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving change history: {str(e)}")
        if self.history_saved:
            self.end_connection()

    def go_to_main_window(self):
        self.root.destroy()
        self.main_window.deiconify()
