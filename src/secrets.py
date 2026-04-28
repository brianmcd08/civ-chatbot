import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(key: str) -> str:
    """
    Load a secret from Streamlit secrets if available (Streamlit Cloud),
    otherwise fall back to environment variables / .env (local dev).
    """
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        value = os.environ.get(key)
        if value is None:
            raise EnvironmentError(f"Missing secret: {key}")
        return value
