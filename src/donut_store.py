import json
import os

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONUT_FILE = os.path.join(_PROJECT_DIR, 'data', 'donuts.json')

def init_donuts():
    """Make data/donuts.json accessible after rgbmatrix drops to UID 1.
    Must be called before Matrix init while still running as root."""
    data_dir = os.path.join(_PROJECT_DIR, 'data')
    for d in [os.path.expanduser('~'), _PROJECT_DIR, data_dir]:
        try:
            st = os.stat(d)
            if not (st.st_mode & 0o001):
                os.chmod(d, st.st_mode | 0o001)
        except OSError:
            pass

def load_donuts():
    try:
        with open(DONUT_FILE, 'r') as f:
            data = json.load(f)
        return data.get('michael_owes', 0), data.get('tyler_owes', 0)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return 0, 0
