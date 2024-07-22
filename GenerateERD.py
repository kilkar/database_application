from tkinter import filedialog, messagebox
import pydot


class GenerateERD:
    def __init__(self, connection):
        self.connection = connection

    def generate(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()[0]
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        new_graph = pydot.Dot(graph_type='digraph', rankdir='LR')  # Changed to directed graph and left-to-right layout

        tb_columns = {}
        foreign_keys = {}

        for table in tables:
            table_name = table[0]
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = cursor.fetchall()
            tb_columns[table_name] = columns

            cursor.execute(f"""
                SELECT column_name, referenced_table_name, referenced_column_name
                FROM information_schema.key_column_usage
                WHERE table_name = %s AND table_schema = %s AND referenced_table_name IS NOT NULL
            """, (table_name, database))
            foreign_keys[table_name] = cursor.fetchall()

        for table_name, columns in tb_columns.items():
            label = f"{{{table_name}|"
            for column in columns:
                column_name = column[0]
                column_type = column[1]
                column_key = column[3]
                info = []

                if column_key == "PRI":
                    info.append("PK")
                if column_key == "UNI":
                    info.append("UNIQUE")
                if column[2] == "NO":
                    info.append("NOT NULL")

                # Check if the column is a foreign key
                if any(fk[0] == column_name for fk in foreign_keys[table_name]):
                    info.append("FK")

                if info:
                    label += f"{column_name}: {column_type} ({', '.join(info)})\l"
                else:
                    label += f"{column_name}: {column_type}\l"
            label += "}"

            node = pydot.Node(table_name, shape='record', label=label)
            new_graph.add_node(node)

        for table_name, fkey in foreign_keys.items():
            for fk in fkey:
                target_table = fk[1]
                edge = pydot.Edge(table_name, target_table, arrowhead='normal')
                new_graph.add_edge(edge)

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            new_graph.write_png(file_path)
            messagebox.showinfo("Info", f"The ERD diagram has been generated and saved to a file {file_path}.")
        else:
            messagebox.showerror("Error", "Failed to generate ERD diagram")
