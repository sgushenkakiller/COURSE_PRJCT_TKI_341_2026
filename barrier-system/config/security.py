import os


class SecurityConfig:

    CRYPTO_ALGORITHM: str = os.getenv("CRYPTO_ALGORITHM", "sha256")
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))
    MAX_FAILED_ATTEMPTS: int = int(os.getenv("MAX_FAILED_ATTEMPTS", "5"))
