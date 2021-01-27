from . import dialog
reload(dialog)
from .dialog import Dialog

def show_dialog(app):
    _dialog = Dialog()
    app.show_dialog(_dialog)

