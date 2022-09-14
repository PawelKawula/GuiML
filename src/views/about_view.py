#!/usr/bin/env python3

from gi.repository import Gtk
from views import constants


@Gtk.Template(filename=constants.ABOUT_FILE)
class AboutDialog(Gtk.Dialog):
    __gtype_name__ = "about_dialog"

    @Gtk.Template.Callback()
    def on_cancel_clicked(self, button):
        self.destroy()
