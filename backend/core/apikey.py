"""Sayt API kalitlarini generatsiya qilish."""
import secrets


API_KEY_PREFIX = "vmt_"  # Veb Monitoring Tracking
API_KEY_BYTES = 24  # 32 ta simvol hex emas, secrets.token_urlsafe(24) -> 32 char


def generate_api_key() -> str:
    """Yangi xavfsiz API kalit hosil qiladi.

    Format: vmt_<32-char-urlsafe-token>
    Misol: vmt_aBc1XYz2dEf3GhI4jKl5mNo6pQrStUvW
    """
    return API_KEY_PREFIX + secrets.token_urlsafe(API_KEY_BYTES)
