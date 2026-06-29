import os


class Settings:

    APP_NAME: str = "Cyberimmune RFID Barrier Control System"
    APP_VERSION: str = "1.0.0"

    BARRIER_ID: str = os.getenv("BARRIER_ID", "barrier-01")
    READER_ID: str = os.getenv("READER_ID", "reader-01")

    MIN_ACCESS_LEVEL: int = int(os.getenv("MIN_ACCESS_LEVEL", "1"))
    OPERATOR_ACCESS_LEVEL: int = int(os.getenv("OPERATOR_ACCESS_LEVEL", "2"))
    ADMIN_ACCESS_LEVEL: int = int(os.getenv("ADMIN_ACCESS_LEVEL", "3"))

    LOOP_INTERVAL: float = float(os.getenv("LOOP_INTERVAL", "0.5"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    SEED_DATA: bool = os.getenv("SEED_DATA", "true").lower() == "true"
