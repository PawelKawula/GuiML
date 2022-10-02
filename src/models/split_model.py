from controllers.file_handler import get_columns_from_csv

# Add default value for model and view
class SplitModel:
    def __init__(self, columns, split_methods=["Random", "Time-Based"]):
        self.columns = columns
        self.split_methods = split_methods
