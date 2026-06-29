from interfaces.access_controller_interface import AccessControllerInterface

from entities.access_request import AccessRequest
from entities.direction import Direction

from devices.rfid_reader.scanner import RFIDScanner
from devices.rfid_reader.parser import RFIDParser

from uuid import uuid4


class RFIDReader:
    def __init__(
        self,
        scanner: RFIDScanner,
        parser: RFIDParser,
        controller: AccessControllerInterface,
        reader_id: str = "reader-01",
    ) -> None:
        self._scanner = scanner
        self._parser = parser
        self._controller = controller
        self._reader_id = reader_id

    def scan(self, direction: Direction = Direction.ENTRY, uid: str | None = None) -> None:
        raw_uid = uid if uid is not None else self._scanner.read_uid()

        card = self._parser.parse(raw_uid)

        if card is None:
            return

        request = AccessRequest(
            request_id=str(uuid4()),
            uid=card.uid,
            reader_id=self._reader_id,
            direction=direction,
        )

        self._controller.process_request(request)
