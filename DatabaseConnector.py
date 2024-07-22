from tkinter import messagebox
import mysql.connector


class DatabaseConnector:

    def __init__(self):
        self.connection = None
        self.database = None

    def connect_to_database(self, root, entry_host, entry_login, entry_password, entry_database):
        try:
            self.connection = mysql.connector.connect(
                host=entry_host.get(),
                user=entry_login.get(),
                password=entry_password.get(),
                database=entry_database.get()
            )
            self.database = entry_database.get()
            messagebox.showinfo("Connected", "Connected to {} database".format(entry_database.get()))
            root.destroy()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Error: {}".format(error))

    def get_connection(self):
        return self.connection

    def get_database(self):
        return self.database
