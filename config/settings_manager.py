import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")


def load_settings():

    defaults = {
        "exclude_minor": False,
        "practices": [],
        "pac_staff": []
    }

    if not SETTINGS_FILE.exists():
        return defaults

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return defaults


def save_settings_file(settings):

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            settings,
            f,
            indent=4
        )