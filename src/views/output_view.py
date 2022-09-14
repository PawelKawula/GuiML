#!/usr/bin/env python3

from gi.repository import Gtk


class OutputView(Gtk.Dialog):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.columns = columns
        self.output_choose_combo = Gtk.ComboBoxText()
        self.output_choose_combo.set_entry_text_column(0)
        area = self.get_content_area()

        for column in columns:
            self.output_choose_combo.append_text(column)

        self.validation_split_method_radio_time = Gtk.RadioButton.new_with_label_from_widget(None, "Time-Based")
        self.validation_split_method_radio_rand = Gtk.RadioButton.new_from_widget(self.validation_split_method_radio_time)
        self.validation_split_method_radio_rand.set_label("Random")
        self.validation_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        self.validation_scale.set_value(75)

        self.method_radio = Gtk.ComboBoxText()
        self.method_radio.set_entry_text_column(0)
        self.method_radio.append_text("Deep Learning")
        self.method_radio.append_text("Random Forrest Regression")

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        area.add(self.output_choose_combo)
        area.add(self.validation_split_method_radio_time)
        area.add(self.validation_split_method_radio_rand)
        area.add(self.validation_scale)
        area.add(self.method_radio)
        self.show_all()

    def get_ins_out(self):
        response = self.run()
        if response == Gtk.ResponseType.OK:
            selection = self.output_choose_combo.get_active_text()
            print(f"selection: {selection}")
            return [x for x in self.columns if x != selection], selection
        else:
            return None, None
