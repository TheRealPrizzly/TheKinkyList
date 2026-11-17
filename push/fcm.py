"""Send push notifications through Firebase Cloud Messaging (the HTTP v1 API).

Configured by FCM_SERVICE_ACCOUNT_FILE: the JSON key of a Firebase service account
(Firebase console → Project settings → Service accounts → Generate new private key).
Without it, push is off and nothing is sent.
"""

import logging
import threading

from django.conf import settings

log = logging.getLogger(__name__)

SCOPE = "https://www.googleapis.com/auth/firebase.messaging"
SEND_URL = "https://fcm.googleapis.com/v1/projects/{project}/messages:send"
TIMEOUT = 10  # seconds

_lock = threading.Lock()
_session = None


class InvalidToken(Exception):
    """Firebase no longer knows this token: the app was uninstalled or the token rotated."""


def is_configured():
    return bool(settings.FCM_SERVICE_ACCOUNT_FILE)


def _authorized_session():
    """One session per process; it refreshes its access token by itself."""
    global _session
    with _lock:
        if _session is None:
            from google.auth.transport.requests import AuthorizedSession
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                settings.FCM_SERVICE_ACCOUNT_FILE, scopes=[SCOPE]
            )
            _session = AuthorizedSession(credentials)
        return _session


def build_message(token, title, body, url):
    return {
        "token": token,
        "notification": {"title": title, "body": body},
        # Read by static/js/push.js: tapping the notification opens this page.
        "data": {"url": url},
        "android": {
            "priority": "high",
            "notification": {"icon": "ic_stat_heart", "color": "#E11D48", "sound": "default"},
        },
        "apns": {"payload": {"aps": {"sound": "default"}}},
    }


def send(token, title, body, url):
    """Send one notification. Raises InvalidToken when the device is gone; logs other failures."""
    session = _authorized_session()
    response = session.post(
        SEND_URL.format(project=session.credentials.project_id),
        json={"message": build_message(token, title, body, url)},
        timeout=TIMEOUT,
    )
    if response.ok:
        return
    error = _error_code(response)
    if response.status_code == 404 or error == "UNREGISTERED":
        raise InvalidToken(token)
    log.warning("FCM send failed (%s %s): %s", response.status_code, error, response.text[:500])


def _error_code(response):
    try:
        details = response.json()["error"].get("details", [])
    except (ValueError, KeyError, AttributeError):
        return ""
    return next((d.get("errorCode", "") for d in details if "errorCode" in d), "")
