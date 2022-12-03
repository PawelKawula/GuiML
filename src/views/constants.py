import os
from pathlib import Path

from gi.repository import Gtk

SRC_PATH = Path(os.path.realpath(__file__)).parent.parent
PROJECT_ROOT = SRC_PATH.parent

GLADE_FILE = str(PROJECT_ROOT / "project.glade")
ABOUT_FILE = str(PROJECT_ROOT / "about.glade")
FILE_CHOOSER_FILE = str(PROJECT_ROOT / "file_chooser.glade")
RESULT_FILE = str(PROJECT_ROOT / "result.glade")
LEARN_DIALOG_FILE = str(PROJECT_ROOT / "learn_dialog.glade")
SETTINGS_FILE = str(PROJECT_ROOT / "settings.glade")
SETTINGS_TAB_FILE = str(PROJECT_ROOT / "settings_tab.glade")
SPLITS_FILE = str(PROJECT_ROOT / "splits.glade")

MARGINS = {
    "margin_top": 20,
    "margin_bottom": 20,
    "margin_left": 10,
    "margin_right": 10,
}
