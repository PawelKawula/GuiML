from datetime import datetime

from gi.repository import Gtk

from ..template import Template
from .. import constants


class ArgumentCalendar(Gtk.Button):
    def __init__(self, parent):
        self.parent = parent
        self.connect("clicked", self.on_button_clicked)
        self.date = None

    def on_button_clicked(self):
        calendar_dialog = DatetimeDialog(self.parent)
        response = calendar_dialog.run()
        calendar_dialog.destroy()
        if response != int(Gtk.ResponseType.OK):
            self.date = calendar_dialog.get_datetime()

    def get(self):
        return self.date


@Template(filename=constants.DATETIME_FILE)
class DatetimeDialog(Gtk.Dialog):
    __gtype_name__ = "datetime_dialog"

    def __init__(self, parent):
        super().__init__(parent=parent, transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
        )

    def get_datetime(self):
        date = list(self.calendar.get_date())
        time = [
            s.get_value()
            for s in [self.hours_spin, self.min_spin, self.sec_spin]
        ]
        return datetime(*(date + time))
