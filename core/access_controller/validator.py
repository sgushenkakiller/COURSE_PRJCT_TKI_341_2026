from entities.access_request import AccessRequest


class RequestValidator:

    def validate(self, request: AccessRequest) -> bool:

        if not request.request_id:
            return False

        if not request.uid:
            return False

        if not request.reader_id:
            return False

        return True