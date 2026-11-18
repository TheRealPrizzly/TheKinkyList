"""Sign in with Google.

In browsers, "Continue with Google" is a plain link: Google asks the person to choose an account,
then sends them back to /google/callback/ with a one-time code, which we swap for an ID token.
Google blocks that page inside apps, so the Android app signs in with Android's own account
picker instead and posts the ID token to /google/token/.

Either way we keep only the token's "sub", Google's permanent number for that account. We ask
for the "profile" scope only to suggest a display name; we never ask for the email address.

Configured by GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET: the OAuth client of type "Web
application" that Firebase creates when Google sign-in is turned on (see the README). The
Android app requests tokens for that same client, so one client ID checks both.
"""

import base64
import hashlib
import logging
from dataclasses import dataclass
from urllib.parse import urlencode

import requests
from django.conf import settings

log = logging.getLogger(__name__)

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
TIMEOUT = 10  # seconds


class InvalidCredential(Exception):
    """Google didn't confirm who this is: a bad, expired or forged token, or Google unreachable."""


@dataclass(frozen=True)
class Identity:
    sub: str  # Google's permanent number for the account
    name: str  # only used to suggest a display name


def is_configured():
    return bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET)


def authorization_url(redirect_uri, state, code_verifier):
    challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid profile",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "prompt": "select_account",
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def exchange_code(code, redirect_uri, code_verifier):
    """Swap the code from Google's redirect for the person's identity."""
    try:
        response = requests.post(
            TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
                "code_verifier": code_verifier,
            },
            timeout=TIMEOUT,
        )
    except requests.RequestException as error:
        raise InvalidCredential(f"Couldn't reach Google: {error}") from error
    if not response.ok:
        log.warning("Google token exchange failed (%s): %s", response.status_code, response.text[:300])
        raise InvalidCredential(f"Google refused the code ({response.status_code})")
    return verify(response.json().get("id_token", ""))


def verify(token):
    """Check an ID token's signature, issuer, audience and expiry, and return who it's for."""
    from google.auth.exceptions import GoogleAuthError
    from google.auth.transport.requests import Request
    from google.oauth2 import id_token

    if not token or not settings.GOOGLE_CLIENT_ID:
        raise InvalidCredential("No token")
    try:
        claims = id_token.verify_oauth2_token(token, Request(), audience=settings.GOOGLE_CLIENT_ID, clock_skew_in_seconds=10)
    except (ValueError, GoogleAuthError) as error:
        raise InvalidCredential(str(error)) from error
    return Identity(sub=claims["sub"], name=(claims.get("name") or claims.get("given_name") or "").strip())
