import tkinter as tk
from GenerateERD import GenerateERD
from GenerateExcel import GenerateExcel
from ImportDataWindow import ImportDataWindow
from ValidateDataWindow import ValidateDataWindow
from EndConnection import EndConnection


class MainWindow:

    def __init__(self, connection, database):
        self.connection = connection
        self.database = database
        self.root = tk.Tk()
        self.root.title("Database Application")
        self.__import_data = ImportDataWindow(self.connection, self.database, self.root)
        self.__generate_erd = GenerateERD(self.connection)
        self.__generate_excel = GenerateExcel(self.connection, self.database, self.root)
        self.__valid_data = ValidateDataWindow(self.connection, self.database, self.root)
        self.__end_connection = EndConnection(self.connection, self.root)

    def display_window(self):
        window_width = 300
        window_height = 240
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=23)

        erd_generate_button = tk.Button(frame, text="Generate ERD diagram", width=20, command=self.go_to_generate_erd)
        erd_generate_button.grid(row=0, columnspan=2, pady=5)

        generate_excel_button = tk.Button(frame, text="Generate Excel file", width=20,
                                          command=self.go_to_generate_excel)
        generate_excel_button.grid(row=1, columnspan=2, pady=5)

        import_data_button = tk.Button(frame, text="Import Data", width=20, command=self.go_to_import_data)
        import_data_button.grid(row=2, columnspan=2, pady=5)

        validate_data_button = tk.Button(frame, text="Validate Data", width=20, command=self.go_to_validate_data)
        validate_data_button.grid(row=3, columnspan=2, pady=5)

        end_connection_button = tk.Button(frame, text="End Connection", width=20, command=self.go_to_end_connection)
        end_connection_button.grid(row=4, columnspan=2, pady=5)

        self.root.mainloop()

    def go_to_generate_erd(self):
        self.__generate_erd.generate()

    def go_to_generate_excel(self):
        self.root.withdraw()
        self.__generate_excel.display_window()

    def go_to_import_data(self):
        self.root.withdraw()
        self.__import_data.display_window()

    def go_to_validate_data(self):
        self.root.withdraw()
        self.__valid_data.display_window()

    def go_to_end_connection(self):
        self.root.withdraw()
        self.__end_connection.display_window()
