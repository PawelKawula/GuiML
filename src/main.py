from views.main_view import MainView
from models.main_model import MainModel
from controllers.main_controller import MainController
from gi.repository import Gtk

model = MainModel()
view = MainView(model)
controller = MainController(model, view)
view.register_listener(controller)

Gtk.main()
