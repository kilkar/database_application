import tkinter as tk
import os
from tkinter import ttk, filedialog, messagebox
from ManageDataValidation import ManageDataValidation


class ValidateDataWindow:
    def __init__(self, connection, database, main_window=None):
        self.database = database
        self.tables = []
        self.connection = connection
        self.main_window = main_window
        self.root = None
        self.tb_combobox = None
        self.file_entry = None
        self.file_path = tk.StringVar()

        self.manager = ManageDataValidation(self.connection, self.database)
        self.take_tables()

    def display_window(self):

        self.root = tk.Tk()
        self.root.title("Database Application")
        window_width = 450
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=15)

        file_label = ttk.Label(frame, text="Select Excel file:")
        file_label.grid(row=0, column=0, padx=10, pady=5)

        self.file_entry = ttk.Entry(frame, width=30)
        self.file_entry.grid(row=0, column=1, padx=10, pady=5)

        browse_button = ttk.Button(frame, text="Search", command=self.browse)
        browse_button.grid(row=0, column=2, padx=10, pady=5)

        table = ttk.Label(frame, text="Select table:")
        table.grid(row=1, column=0, padx=10, pady=5)

        self.tb_combobox = ttk.Combobox(frame)
        self.tb_combobox['values'] = self.tables
        self.tb_combobox.grid(row=1, column=1, padx=10, pady=5)

        validate_button = ttk.Button(frame, text="Validate data", command=self.check_data)
        validate_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        check_errors_button = ttk.Button(frame, text="Check errors", command=self.check_errors)
        check_errors_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        return_button = ttk.Button(frame, text="Back to menu", command=self.go_to_main_window)
        return_button.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        self.root.mainloop()

    def take_tables(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            self.tables = [table[0] for table in cursor.fetchall()]

    def browse(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki Excel", "*.xlsx;*.xls")])
        if file_path:
            self.file_path.set(file_path)
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def check_data(self):
        file_path = self.file_path.get()
        table_name = self.tb_combobox.get()

        if not file_path or not table_name:
            messagebox.showerror("Error", "Please select an Excel file and a table.")
            return

        self.manager.check_data(file_path, table_name)

    def check_errors(self):
        main_directory = os.path.dirname(os.path.abspath(__file__))
        errors_folder = os.path.join(main_directory, "errors")

        if not os.path.exists(errors_folder):
            messagebox.showerror("Error", "Errors folder does not exist.")
            return

        file_path = filedialog.askopenfilename(initialdir=errors_folder, title="Select a file",
                                               filetypes=(("Excel files", "*.xlsx;*.xls"),))
        if file_path:
            os.startfile(file_path)

    def go_to_main_window(self):
        self.root.destroy()
        self.main_window.deiconify()