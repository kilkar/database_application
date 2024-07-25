import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox


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
        self.root = ctk.CTk()
        self.root.title("Database Application")
        window_width = 300
        window_height = 270
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=10, pady=10, fill='both', expand=True)

        table = ctk.CTkLabel(frame, text="Choose table", font=("Arial", 18, "bold"))
        table.pack(pady=(20, 10))

        self.tb_combobox = ctk.CTkComboBox(frame, values=self.tables, width=180, height=30)
        self.tb_combobox.pack(pady=10)

        generate_button = ctk.CTkButton(frame, text="Generate Excel file", font=("Arial", 14, "bold"), width=180,
                                        height=40, command=self.generate_excel)
        generate_button.pack(pady=10)

        return_button = ctk.CTkButton(frame, text="Back to menu", font=("Arial", 14, "bold"), width=180, height=40,
                                      command=self.go_to_main_window)
        return_button.pack(pady=10)

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
            messagebox.showerror("Error", "Table has not been chosen.")
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

            messagebox.showinfo("Info", "The Excel file was generated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the Excel file: {str(e)}")

    def go_to_main_window(self):
        self.root.destroy()
        self.main_window.deiconify()
