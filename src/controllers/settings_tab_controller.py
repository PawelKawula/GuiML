import flatdict

from learning.defined_models import learn_models


class SettingsTabController:
    def __init__(self, parent, model, view):
        self.parent = parent
        self.model, self.view = model, view

    def on_save_clicked(self, item):
        self.parent.save_model_configs(self.model.model_name)

    def on_revert_clicked(self, item):
        self.parent.revert_model_configs(self.model.model_name)
