from enum import Enum


class Protocol(Enum):
    INTERNAL = "internal"

    API = "api"

    TCP = "tcp"

    SERIAL = "serial"

    MQTT = "mqtt"

    HTTP = "http"

    HTTPS = "https"