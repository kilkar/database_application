import tkinter as tk
from DatabaseConnector import DatabaseConnector


class LoginWindow:

    def __init__(self):
        self.db_connector = DatabaseConnector()
        self.root = tk.Tk()
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

        if len(self.entry_host.get()) == 0:
            self.host_error.config(text="Host field is required")
            go_to_database_connector = False
        else:
            self.host_error.config(text="")
        if len(self.entry_login.get()) == 0:
            self.login_error.config(text="Login field is required")
            go_to_database_connector = False
        else:
            self.login_error.config(text="")
        if len(self.entry_password.get()) == 0:
            self.password_error.config(text="Password field is required")
            go_to_database_connector = False
        else:
            self.password_error.config(text="")
        if len(self.entry_database.get()) == 0:
            self.database_error.config(text="Database name field is required")
            go_to_database_connector = False
        else:
            self.database_error.config(text="")

        if go_to_database_connector:
            self.db_connector.connect_to_database(self.root, self.entry_host, self.entry_login, self.entry_password, 
                                                  self.entry_database)
            
    def display_window(self):
        frame = tk.Frame(self.root)
        self.root.title("Database Application")

        window_width = 300
        window_height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        frame.pack(padx=10, pady=23)

        host = tk.Label(frame, text="Host:")
        host.grid(row=0, column=0)
        self.entry_host = tk.Entry(frame)
        self.entry_host.grid(row=0, column=1)
        self.host_error = tk.Label(frame, text="", fg="red")
        self.host_error.grid(row=1, column=1)

        login = tk.Label(frame, text="Login:")
        login.grid(row=2, column=0)
        self.entry_login = tk.Entry(frame)
        self.entry_login.grid(row=2, column=1)
        self.login_error = tk.Label(frame, text="", fg="red")
        self.login_error.grid(row=3, column=1)

        password = tk.Label(frame, text="Password:")
        password.grid(row=4, column=0)
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.grid(row=4, column=1)
        self.password_error = tk.Label(frame, text="", fg="red")
        self.password_error.grid(row=5, column=1)

        database = tk.Label(frame, text="Database name:  ")
        database.grid(row=6, column=0)
        self.entry_database = tk.Entry(frame)
        self.entry_database.grid(row=6, column=1)
        self.database_error = tk.Label(frame, text="", fg="red")
        self.database_error.grid(row=7, column=1)

        login_button = tk.Button(frame, text="Connect", command=self.validate)
        login_button.grid(row=8, columnspan=2, pady=10)

        default_text = "localhost"
        self.entry_host.insert(0, default_text)

        default_text2 = "root"
        self.entry_login.insert(0, default_text2)

        default_text4 = "orders"
        self.entry_database.insert(0, default_text4)

        self.root.mainloop()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_database(self):
        return self.db_connector.get_database()
