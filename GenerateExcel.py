import tkinter as tk
import pandas as pd
from tkinter import ttk, filedialog, messagebox


class GenerateExcel:

    def __init__(self, connection, database, main_window=None):
        self.connection = connection
        self.database = database
        self.main_window = main_window
        self.tables = []
        self.root = None
        self.tb_combobox = None
        self.take_tables()

    def display_window(self):
        self.root = tk.Tk()
        self.root.title("Database Application")
        window_width = 250
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=23)

        table = ttk.Label(frame, text="Choose table:")
        table.pack(pady=5)

        self.tb_combobox = ttk.Combobox(frame)
        self.tb_combobox['values'] = self.tables
        self.tb_combobox.pack(pady=10)

        generate_button = ttk.Button(frame, text="Generate Excel file", command=self.generate_excel)
        generate_button.pack(pady=10)

        return_button = ttk.Button(frame, text="Back to menu", command=self.go_to_main_window)
        return_button.pack(pady=5)

        self.root.mainloop()

    def take_tables(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            self.tables = [table[0] for table in cursor.fetchall()]
            cursor.close()

    def generate_excel(self):
        table_selected = self.tb_combobox.get()
        if not table_selected:
            tk.messagebox.showerror("Error", "Table has not been chosen.")
            return
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE {self.database}.{table_selected}")
        columns = [column[0] for column in cursor.fetchall()]
        cursor.close()

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if not file_path:
            return
        try:
            data = {column: [] for column in columns}
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)

            tk.messagebox.showinfo("Info", "The Excel file was generated successfully.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while generating the Excel file: {str(e)}")

    def go_to_main_window(self):
        self.root.destroy()
        self.main_window.deiconify()
