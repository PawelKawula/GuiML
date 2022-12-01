import re
from copy import deepcopy
from importlib import import_module

from gi.repository import Gtk


class Template(Gtk.Template):
    def __init__(self, *, filename):
        super().__init__(filename=filename)
        self.filename = filename

    def __call__(self, cls):
        for attr in [
            re.search(r'id=".*"', l).group().replace("id=", "").replace('"', "")
            for l in open(self.filename)
            if len(re.findall(r"id=", l))
        ]:
            setattr(cls, attr, Gtk.Template.Child())
        return super().__call__(cls)
