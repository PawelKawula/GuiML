#!/usr/bin/env python


from controllers import file_handler


class FileChooserModel:
    def __init__(self, filters={"Csv files": "text/csv", "Any files": "*"}):
        self.filters = filters
        self.filename = None

    def set_filename(self, filename):
        self.filename = filename
