import os
from pathlib import Path

from gi.repository import Gtk

SRC_PATH = Path(os.path.realpath(__file__)).parent.parent
PROJECT_ROOT = SRC_PATH.parent
GLADE_ROOT = PROJECT_ROOT / "glade"

GLADE_FILE = str(GLADE_ROOT / "project.glade")
ABOUT_FILE = str(GLADE_ROOT / "about.glade")
FILE_CHOOSER_FILE = str(GLADE_ROOT / "file_chooser.glade")
RESULT_FILE = str(GLADE_ROOT / "result.glade")
RESULT_ADD_FILE = str(GLADE_ROOT / "result_add.glade")
LEARN_DIALOG_FILE = str(GLADE_ROOT / "learn_dialog.glade")
SETTINGS_FILE = str(GLADE_ROOT / "settings.glade")
SETTINGS_TAB_FILE = str(GLADE_ROOT / "settings_tab.glade")
SPLITS_FILE = str(GLADE_ROOT / "splits.glade")
DATETIME_FILE = str(GLADE_ROOT / "datetime.glade")

MARGINS = {
    "margin_top": 20,
    "margin_bottom": 20,
    "margin_left": 10,
    "margin_right": 10,
}
