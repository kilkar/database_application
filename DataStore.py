class DataStore:
    def __init__(self):
        self.imported_data = {}

    def check_if_table_exists(self, table_name):
        return True if table_name in self.imported_data else False

    def get_items(self):
        return self.imported_data.items()

    def clear(self):
        self.imported_data.clear()

    def append_row(self, table_name, row):
        self.imported_data[table_name].append(row)

    def create_key_for_db(self, table_name):
        self.imported_data[table_name] = []

    def get_imported_data(self):
        return self.imported_data
