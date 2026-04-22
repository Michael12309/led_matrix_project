import json
import os

DONUT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'donuts.json')

def load_donuts():
    try:
        with open(DONUT_FILE, 'r') as f:
            data = json.load(f)
        return data.get('michael_owes', 0), data.get('tyler_owes', 0)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return 0, 0
