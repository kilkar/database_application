import customtkinter as ctk
from DatabaseConnector import DatabaseConnector


class LoginWindow:

    def __init__(self):
        self.db_connector = DatabaseConnector()
        self.root = ctk.CTk()
        self.connection = None
        self.entry_host = None
        self.entry_login = None
        self.entry_password = None
        self.entry_database = None
        self.host_error = None
        self.login_error = None
        self.password_error = None
        self.database_error = None

    def validate(self):
        go_to_database_connector = True

        if not self.entry_host.get():
            self.host_error.configure(text="Host field is required")
            go_to_database_connector = False
        else:
            self.host_error.configure(text="")
        if not self.entry_login.get():
            self.login_error.configure(text="Login field is required")
            go_to_database_connector = False
        else:
            self.login_error.configure(text="")
        if not self.entry_password.get():
            self.password_error.configure(text="Password field is required")
            go_to_database_connector = False
        else:
            self.password_error.configure(text="")
        if not self.entry_database.get():
            self.database_error.configure(text="Database field is required")
            go_to_database_connector = False
        else:
            self.database_error.configure(text="")

        if go_to_database_connector:
            self.db_connector.connect_to_database(self.root, self.entry_host, self.entry_login, self.entry_password,
                                                  self.entry_database)
            
    def display_window(self):
        self.root.title("Database Application")

        window_width = 305
        window_height = 390
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=13, pady=14, fill='both', expand=True)

        host_label = ctk.CTkLabel(frame, text="Host:", font=("Arial", 14, "bold"))
        host_label.grid(row=0, column=0, padx=(20, 5), pady=(20, 5))
        self.entry_host = ctk.CTkEntry(frame)
        self.entry_host.grid(row=0, column=1, padx=(10, 5), pady=(20, 5))
        self.host_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.host_error.grid(row=1, column=1, padx=5, pady=(2, 2), sticky="w")

        login_label = ctk.CTkLabel(frame, text="Login:", font=("Arial", 14, "bold"))
        login_label.grid(row=2, column=0, padx=(20, 5), pady=(5, 5))
        self.entry_login = ctk.CTkEntry(frame)
        self.entry_login.grid(row=2, column=1, padx=(10, 5), pady=(2, 5))
        self.login_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.login_error.grid(row=3, column=1, padx=5, pady=(2, 2), sticky="w")

        password_label = ctk.CTkLabel(frame, text="Password:", font=("Arial", 14, "bold"))
        password_label.grid(row=4, column=0, padx=(20, 5), pady=5)
        self.entry_password = ctk.CTkEntry(frame, show="*")
        self.entry_password.grid(row=4, column=1, padx=(10, 5), pady=5)
        self.password_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.password_error.grid(row=5, column=1, padx=5, pady=(2, 2), sticky="w")

        database_label = ctk.CTkLabel(frame, text="Database:", font=("Arial", 14, "bold"))
        database_label.grid(row=6, column=0, padx=(20, 5), pady=5)
        self.entry_database = ctk.CTkEntry(frame)
        self.entry_database.grid(row=6, column=1, padx=(10, 5), pady=5)
        self.database_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.database_error.grid(row=7, column=1, padx=5, pady=(2, 2), sticky="w")

        login_button = ctk.CTkButton(frame, text="Connect", font=("Arial", 14, "bold"), command=self.validate)
        login_button.grid(row=8, columnspan=2, pady=(5, 10), padx=(65, 20))

        self.root.mainloop()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_database(self):
        return self.db_connector.get_database()
