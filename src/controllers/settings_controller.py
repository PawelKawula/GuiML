class SettingsController:
    def __init__(self, model, view):
        self.model, self.view = model, view

    def on_ok_clicked(self, button):
        pass

    def on_close_clicked(self, button):
        self.destroy()

    def on_apply_clicked(self, button):
        pass

    def run(self):
        self.view.dialog.run()

    def destroy(self):
        self.view.dialog.destroy()
