import requests

from version import APP_VERSION


def check_for_updates():

    repo = "YOURUSERNAME/PAC-Metrics-App"

    url = (
        f"https://api.github.com/repos/"
        f"{repo}/releases/latest"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        latest = data["tag_name"].replace(
            "v",
            ""
        )

        return {
            "current": APP_VERSION,
            "latest": latest,
            "update_available":
                latest != APP_VERSION,
            "release_url":
                data["html_url"]
        }

    except Exception:

        return None