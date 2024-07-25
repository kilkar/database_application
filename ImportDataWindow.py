import os
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from ManageDataImport import ManageDataImport
from ManageDataValidation import ManageDataValidation
from DataStore import DataStore


class ImportDataWindow:
    def __init__(self, connection, database, main_window=None):
        self.database = database
        self.tables = []
        self.connection = connection
        self.main_window = main_window
        self.root = None
        self.file_entry = None
        self.tb_combobox = None
        self.data_store = DataStore()
        self.file_path = tk.StringVar()

        self.manager_import = ManageDataImport(self.connection, self.database, self.data_store)
        self.manager_validation = ManageDataValidation(self.connection, self.database, self.on_import)

        self.take_tables()

    def display_window(self):
        self.root = ctk.CTk()
        self.root.title("Database Application")

        window_width = 428
        window_height = 380
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=10, pady=10, fill='both', expand=True)

        file = ctk.CTkLabel(frame, text="Select Excel file:", font=("Arial", 13, "bold"))
        file.grid(row=0,  pady=(15, 10), padx=(60, 1))

        self.file_entry = ctk.CTkEntry(frame, font=("Arial", 12), width=180, height=25)
        self.file_entry.grid(row=0, column=1, pady=(15, 10), padx=(0, 20))

        browse_button = ctk.CTkButton(frame, text="Search", font=("Arial", 13, "bold"), width=150, height=30,
                                      border_color="#000080", border_width=2, command=self.browse)
        browse_button.grid(row=1, column=0, columnspan=3, pady=(5, 5), padx=(5, 5))

        table = ctk.CTkLabel(frame, text="Select database table:", font=("Arial", 13, "bold"))
        table.grid(row=2, column=0, pady=(10, 10), padx=(25, 1))

        self.tb_combobox = ctk.CTkComboBox(frame, values=self.tables, font=("Arial", 12), width=180, height=25)
        self.tb_combobox.grid(row=2, column=1, pady=(10, 10), padx=(0, 20))

        import_button = ctk.CTkButton(frame, text="Import data", font=("Arial", 14, "bold"), width=180, height=40,
                                      command=self.import_data)
        import_button.grid(row=3, column=0, pady=(10, 5), padx=(20, 1))

        restore_button = ctk.CTkButton(frame, text="Restore database", font=("Arial", 14, "bold"), width=180,
                                       height=40, command=self.restore)
        restore_button.grid(row=3, column=1, pady=(10, 5), padx=(5, 20))

        check_errors_button = ctk.CTkButton(frame, text="Check errors", font=("Arial", 14, "bold"), width=180,
                                            height=40, command=self.check_errors)
        check_errors_button.grid(row=4, column=0, pady=(5, 5), padx=(20, 1))

        check_history_button = ctk.CTkButton(frame, text="Check history", font=("Arial", 14, "bold"), width=180,
                                             height=40, command=self.check_history)
        check_history_button.grid(row=4, column=1, pady=(5, 5), padx=(5, 20))

        save_button = ctk.CTkButton(frame, text="Save history", font=("Arial", 14, "bold"), width=370, height=40,
                                    command=self.save_history)
        save_button.grid(row=6, columnspan=5, pady=(5, 5), padx=(20, 20))

        return_button = ctk.CTkButton(frame, text="Back to menu", font=("Arial", 14, "bold"), width=370, height=40,
                                      command=self.go_to_main_window)
        return_button.grid(row=7, columnspan=5, pady=(5, 15), padx=(20, 20))

        self.root.mainloop()

    def take_tables(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            self.tables = [table[0] for table in cursor.fetchall()]
            cursor.close()

    def browse(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki Excel", "*.xlsx;*.xls")])
        if file_path:
            self.file_path.set(file_path)
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def on_import(self, df, table_name):
        self.manager_import.import_data_df(df, table_name)

    def import_data(self):
        file_path = self.file_path.get()
        table_name = self.tb_combobox.get()

        if not file_path or not table_name:
            messagebox.showerror("Error", "Please select an Excel file and a table.")
            return

        self.manager_validation.check_data(file_path, table_name)

        errors_found = self.manager_validation.errors_found
        if not errors_found:
            self.manager_import.import_data(file_path, table_name)

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

    def check_history(self):
        main_directory = os.path.dirname(os.path.abspath(__file__))
        his_folder = os.path.join(main_directory, "history")

        if not os.path.exists(his_folder):
            messagebox.showerror("Error", "History folder does not exist.")
            return

        file_path = filedialog.askopenfilename(initialdir=his_folder, title="Select a file",
                                               filetypes=(("Excel files", "*.xlsx;*.xls"),))
        if file_path:
            os.startfile(file_path)

    def restore(self):
        self.manager_import.restore_initial_state()

    def save_history(self):
        self.manager_import.save_history()

    def go_to_main_window(self):
        self.root.destroy()
        self.main_window.deiconify()
