from gi.repository import Gtk

# Add default value for model and view
class SplitView(Gtk.Dialog):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        area = self.get_content_area()

        self.output_choose_combo = Gtk.ComboBoxText()
        self.output_choose_combo.set_entry_text_column(0)
        area.add(self.output_choose_combo)

        for column in self.model.columns:
            self.output_choose_combo.append_text(column)

        self.first_split_method_button = Gtk.RadioButton.new_with_label_from_widget(
            None, self.model.split_methods[0]
        )
        area.add(self.first_split_method_button)

        for split_method in self.model.split_methods[1:]:

            validation_split_method_radio = Gtk.RadioButton.new_from_widget(
                self.first_split_method_button
            )
            validation_split_method_radio.set_label(split_method)
            area.add(validation_split_method_radio)

        self.validation_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL, 0, 100, 1
        )
        self.validation_scale.set_value(75)
        area.add(self.validation_scale)

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.show_all()
