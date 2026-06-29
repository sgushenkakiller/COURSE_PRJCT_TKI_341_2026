from typing import Optional

from entities.rfid_card import RFIDCard


class RFIDParser:
    def parse(self, uid: Optional[str]) -> Optional[RFIDCard]:
        if uid is None:
            return None

        uid = uid.strip().upper()

        if not uid:
            return None

        return RFIDCard(
            uid=uid,
            owner_id="",
            issue_date="",
            expiration_date="",
        )
