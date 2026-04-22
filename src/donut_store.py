import json
import os
import shutil

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SOURCE_FILE = os.path.join(_PROJECT_DIR, 'data', 'donuts.json')
_RUNTIME_FILE = '/tmp/led_matrix_donuts.json'

def init_donuts():
    """Copy donuts.json to /tmp before rgbmatrix drops privileges.
    After privilege drop, edit /tmp/led_matrix_donuts.json to update counts."""
    try:
        shutil.copy2(_SOURCE_FILE, _RUNTIME_FILE)
        os.chmod(_RUNTIME_FILE, 0o666)
    except (FileNotFoundError, PermissionError):
        # Create a default file in /tmp if source doesn't exist
        try:
            with open(_RUNTIME_FILE, 'w') as f:
                json.dump({'michael_owes': 0, 'tyler_owes': 0}, f)
            os.chmod(_RUNTIME_FILE, 0o666)
        except OSError:
            pass

def load_donuts():
    try:
        with open(_RUNTIME_FILE, 'r') as f:
            data = json.load(f)
        return data.get('michael_owes', 0), data.get('tyler_owes', 0)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return 0, 0
