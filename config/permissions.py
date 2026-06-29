from core.database.permissions import Permission


ROLE_PERMISSIONS: dict[str, list[Permission]] = {
    "user": [Permission.USER],
    "operator": [Permission.USER, Permission.OPERATOR],
    "administrator": [Permission.USER, Permission.OPERATOR, Permission.ADMINISTRATOR],
}
