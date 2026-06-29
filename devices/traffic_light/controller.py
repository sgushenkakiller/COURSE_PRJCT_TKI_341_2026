from devices.traffic_light.light import LightState


class TrafficLightController:
    def __init__(self) -> None:
        self._state = LightState.RED

    @property
    def state(self) -> LightState:
        return self._state

    def set_red(self) -> None:
        self._state = LightState.RED

    def set_yellow(self) -> None:
        self._state = LightState.YELLOW

    def set_green(self) -> None:
        self._state = LightState.GREEN

    def turn_off(self) -> None:
        self._state = LightState.OFF

    def reset(self) -> None:
        self._state = LightState.RED