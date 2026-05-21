"""User-Agent header'idan brauzer/OS/qurilma ma'lumotlarini ajratish."""
from __future__ import annotations

from user_agents import parse


def parse_ua(ua_string: str) -> dict:
    """User-Agent qatorini parse qiladi.

    Qaytaradi: {browser, browser_version, os, os_version, device, is_mobile, is_bot}
    """
    if not ua_string:
        return {
            "browser": "Unknown",
            "browser_version": "",
            "os": "Unknown",
            "os_version": "",
            "device": "Unknown",
            "is_mobile": False,
            "is_bot": False,
        }

    ua = parse(ua_string)
    return {
        "browser": ua.browser.family or "Unknown",
        "browser_version": ua.browser.version_string or "",
        "os": ua.os.family or "Unknown",
        "os_version": ua.os.version_string or "",
        "device": ua.device.family or "Other",
        "is_mobile": ua.is_mobile or ua.is_tablet,
        "is_bot": ua.is_bot,
    }
