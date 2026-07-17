"""Optional Streamlit OIDC gate with a clearly labelled local-dev identity."""

from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Identity:
    owner_id: str
    email: str
    name: str
    authenticated: bool


def auth_required() -> bool:
    return os.environ.get("CONTRACTGUARD_AUTH_REQUIRED", "false").lower() in {"1", "true", "yes"}


def auth_configured() -> bool:
    try:
        auth = st.secrets.get("auth")
        return bool(auth and auth.get("redirect_uri") and auth.get("cookie_secret"))
    except (FileNotFoundError, KeyError):
        return False


def current_identity() -> Identity:
    user = getattr(st, "user", None)
    if user is not None and getattr(user, "is_logged_in", False):
        claims = user.to_dict() if hasattr(user, "to_dict") else dict(user)
        owner_id = str(claims.get("sub") or claims.get("email") or "").strip()
        if not owner_id:
            raise ValueError("The identity provider did not return a stable subject or email claim.")
        return Identity(
            owner_id=owner_id,
            email=str(claims.get("email") or ""),
            name=str(claims.get("name") or claims.get("email") or "User"),
            authenticated=True,
        )
    local_id = os.environ.get("CONTRACTGUARD_LOCAL_OWNER_ID", "local-demo")
    return Identity(owner_id=local_id, email="", name="Local workspace", authenticated=False)


def require_identity() -> Identity:
    if auth_required() and not auth_configured():
        st.error("Authentication is required but OIDC is not configured. Add the [auth] secrets before accepting production documents.")
        st.stop()
    identity = current_identity()
    if auth_required() and not identity.authenticated:
        st.markdown("## Sign in to ContractGuard")
        st.write("Your reviews are private to your account and cannot be opened by another signed-in user.")
        st.button("Continue with secure sign-in", on_click=st.login, type="primary")
        st.stop()
    return identity
