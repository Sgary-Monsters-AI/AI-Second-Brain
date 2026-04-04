#!/usr/bin/env python3
"""
Substack Authentication Checker

Verifies that Substack credentials are configured correctly.

Usage:
    python3 check_auth.py

Supports two auth methods:
1. Cookie auth (preferred): SUBSTACK_COOKIE + SUBSTACK_PUBLICATION_URL
2. Password auth: SUBSTACK_EMAIL + SUBSTACK_PASSWORD + SUBSTACK_PUBLICATION_URL
"""

import os
import sys


def check_environment():
    """Check environment variables and determine auth method."""
    print("Checking environment variables...\n")

    publication_url = os.environ.get("SUBSTACK_PUBLICATION_URL")
    cookie = os.environ.get("SUBSTACK_COOKIE")
    email = os.environ.get("SUBSTACK_EMAIL")
    password = os.environ.get("SUBSTACK_PASSWORD")

    # Check publication URL (always required)
    if publication_url:
        print(f"  [OK] SUBSTACK_PUBLICATION_URL = {publication_url}")
    else:
        print("  [MISSING] SUBSTACK_PUBLICATION_URL")
        return None, []

    # Check cookie auth
    if cookie:
        # Mask the cookie value
        masked = cookie[:20] + "..." if len(cookie) > 20 else cookie
        print(f"  [OK] SUBSTACK_COOKIE = {masked}")
        return "cookie", []

    # Check password auth
    missing = []
    if email:
        print(f"  [OK] SUBSTACK_EMAIL = {email}")
    else:
        print("  [MISSING] SUBSTACK_EMAIL")
        missing.append("SUBSTACK_EMAIL")

    if password:
        print("  [OK] SUBSTACK_PASSWORD = ****")
    else:
        print("  [MISSING] SUBSTACK_PASSWORD")
        missing.append("SUBSTACK_PASSWORD")

    if not missing:
        return "password", []

    return None, missing


def test_authentication(auth_method):
    """Attempt to authenticate with Substack."""
    try:
        from substack import Api
    except ImportError:
        print("\n[ERROR] python-substack not installed")
        print("Run: pip install python-substack")
        return False

    print(f"\nTesting authentication ({auth_method} method)...")

    try:
        if auth_method == "cookie":
            api = Api(
                cookies_string=os.environ["SUBSTACK_COOKIE"],
                publication_url=os.environ["SUBSTACK_PUBLICATION_URL"],
            )
        else:
            api = Api(
                email=os.environ["SUBSTACK_EMAIL"],
                password=os.environ["SUBSTACK_PASSWORD"],
                publication_url=os.environ["SUBSTACK_PUBLICATION_URL"],
            )

        user_id = api.get_user_id()
        print(f"  [OK] Authenticated successfully")
        print(f"  [OK] User ID: {user_id}")

        # Try to get publication info
        try:
            pubs = api.get_publications()
            if pubs:
                print(f"  [OK] Found {len(pubs)} publication(s)")
        except Exception:
            pass

        return True

    except Exception as e:
        print(f"  [FAILED] Authentication error: {e}")
        return False


def main():
    print("=" * 50)
    print("Substack Authentication Check")
    print("=" * 50)

    auth_method, missing = check_environment()

    if auth_method is None:
        print("\n" + "=" * 50)
        print("SETUP REQUIRED")
        print("=" * 50)
        print("\nOption 1 - Cookie auth (recommended):")
        print("  1. Log into Substack in Chrome")
        print("  2. DevTools (Cmd+Opt+I) > Application > Cookies > substack.com")
        print("  3. Copy the 'substack.sid' cookie value")
        print("  4. Add to ~/.zshrc:")
        print('     export SUBSTACK_COOKIE="substack.sid=YOUR_VALUE"')
        print("\nOption 2 - Password auth:")
        print('  export SUBSTACK_EMAIL="your-email"')
        print('  export SUBSTACK_PASSWORD="your-password"')
        print("\nAlso required:")
        print('  export SUBSTACK_PUBLICATION_URL="https://yourpub.substack.com"')
        print("\nThen run: source ~/.zshrc")
        sys.exit(1)

    print()

    if test_authentication(auth_method):
        print("\n" + "=" * 50)
        print("ALL CHECKS PASSED")
        print("=" * 50)
        print("\nYou're ready to publish to Substack!")
        sys.exit(0)
    else:
        print("\n" + "=" * 50)
        print("AUTHENTICATION FAILED")
        print("=" * 50)
        if auth_method == "cookie":
            print("\nPossible issues:")
            print("1. Cookie expired - get a fresh one from browser")
            print("2. Wrong cookie format - should be 'substack.sid=VALUE'")
            print("3. Publication URL doesn't match your account")
        else:
            print("\nPossible issues:")
            print("1. Wrong email/password")
            print("2. Account requires CAPTCHA - try cookie auth instead")
            print("3. Publication URL doesn't match your account")
        sys.exit(1)


if __name__ == "__main__":
    main()
