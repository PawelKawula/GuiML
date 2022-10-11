class SettingsController:
    def __init__(self, model, view):
        self.model, self.view = model, view

    def on_ok_clicked(self, button):
        print("ok clicked")

    def on_close_clicked(self, button):
        print("cancel clicked")
        self.destroy()

    def on_apply_clicked(self, button):
        print("apply clicked")

    def run(self):
        self.view.dialog.run()

    def destroy(self):
        self.view.dialog.destroy()
