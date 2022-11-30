from gi.repository import Gtk

from views import constants, utils
from views.template import Template
from common import file_handler


@Template(filename=constants.RESULT_FILE)
class ResultView(Gtk.Dialog):
    __gtype_name__ = "result_dialog"
    def __init__(self, parent, ml_model, **learn_kwargs):
        super().__init__()
        self.parent = parent
        self.ml_config = parent.get_ml_config()
        self.splits_config = parent.get_splits_config()
        self.ml_model = ml_model(self.ml_config.get_tdf(), **learn_kwargs)
        self.populate()

        self.show()

    @Gtk.Template.Callback()
    def on_ok(self, item):
        self.destroy()

    def populate(self):
        tdf, split_kwargs = self.ml_config.get_tdf(), self.splits_config.dump_dict_copy()
        tdf = file_handler.get_values(
            tdf, valid=True, ml_model=self.ml_model, **split_kwargs
        )
        store = file_handler.get_store(tdf, valid=True)
        utils.view_trees(self.items_view, store, **split_kwargs)
