import customtkinter as ctk
from GenerateDBSchema import GenerateDBSchema
from GenerateExcel import GenerateExcel
from ImportDataWindow import ImportDataWindow
from ValidateDataWindow import ValidateDataWindow
from EndConnection import EndConnection


class MainWindow:

    def __init__(self, connection, database):
        self.connection = connection
        self.database = database
        self.root = ctk.CTk()
        self.root.title("Database Application")
        self.__import_data = ImportDataWindow(self.connection, self.database, self.root)
        self.__generate_db_schema = GenerateDBSchema(self.connection)
        self.__generate_excel = GenerateExcel(self.connection, self.database, self.root)
        self.__valid_data = ValidateDataWindow(self.connection, self.database, self.root)
        self.__end_connection = EndConnection(self.connection, self.root)

    def display_window(self):
        window_width = 300
        window_height = 360
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=10, pady=10, fill='both', expand=True)

        erd_generate_button = ctk.CTkButton(frame, text="Generate DB schema", font=("Arial", 14, "bold"), width=200,
                                            height=45, command=self.go_to_generate_db_schema)
        erd_generate_button.grid(row=0, pady=(15, 10), padx=(40, 40))

        generate_excel_button = ctk.CTkButton(frame, text="Generate Excel file", font=("Arial", 14, "bold"), width=200,
                                              height=45, command=self.go_to_generate_excel)
        generate_excel_button.grid(row=1, pady=(10, 10), padx=(40, 40))

        import_data_button = ctk.CTkButton(frame, text="Import Data", font=("Arial", 14, "bold"), width=200,
                                           height=45, command=self.go_to_import_data)
        import_data_button.grid(row=2, pady=(10, 10), padx=(40, 40))

        validate_data_button = ctk.CTkButton(frame, text="Validate Data", font=("Arial", 14, "bold"), width=200,
                                             height=45, command=self.go_to_validate_data)
        validate_data_button.grid(row=3, pady=(10, 10), padx=(40, 40))

        end_connection_button = ctk.CTkButton(frame, text="End Connection", font=("Arial", 14, "bold"), width=200,
                                              height=45, command=self.go_to_end_connection)
        end_connection_button.grid(row=4, pady=(10, 10), padx=(40, 40))

        self.root.mainloop()

    def go_to_generate_db_schema(self):
        self.__generate_db_schema.generate()

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
