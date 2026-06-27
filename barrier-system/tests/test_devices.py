import pytest

from communication.command_result import CommandResult
from communication.commands import Command
from devices.barrier_driver import BarrierDriver
from devices.modem import Modem, ModemMessage
from devices.operator_panel import Display, Keyboard, OperatorPanel
from devices.rfid_reader import RFIDParser, RFIDScanner
from devices.traffic_light import TrafficLightController, LightState
from entities.barrier_state import BarrierState
from entities.reader_state import ReaderState


def test_barrier_driver_open():
    driver = BarrierDriver()
    result = driver.execute(Command.OPEN_BARRIER)
    assert result == CommandResult.SUCCESS
    assert driver.state() == BarrierState.OPEN
    assert driver.opened()


def test_barrier_driver_close():
    driver = BarrierDriver()
    driver.execute(Command.OPEN_BARRIER)
    result = driver.execute(Command.CLOSE_BARRIER)
    assert result == CommandResult.SUCCESS
    assert driver.state() == BarrierState.CLOSED
    assert driver.closed()


def test_barrier_driver_deny():
    driver = BarrierDriver()
    driver.execute(Command.OPEN_BARRIER)
    result = driver.execute(Command.DENY_ACCESS)
    assert result == CommandResult.SUCCESS
    assert driver.closed()


def test_barrier_driver_unsupported():
    driver = BarrierDriver()
    result = driver.execute(Command.HEARTBEAT)
    assert result == CommandResult.UNSUPPORTED


def test_traffic_light_default_red():
    tl = TrafficLightController()
    assert tl.state == LightState.RED


def test_traffic_light_green():
    tl = TrafficLightController()
    tl.set_green()
    assert tl.state == LightState.GREEN


def test_traffic_light_reset():
    tl = TrafficLightController()
    tl.set_green()
    tl.reset()
    assert tl.state == LightState.RED


def test_rfid_parser_valid():
    parser = RFIDParser()
    card = parser.parse("card-abc")
    assert card is not None
    assert card.uid == "CARD-ABC"


def test_rfid_parser_empty():
    parser = RFIDParser()
    assert parser.parse(None) is None
    assert parser.parse("") is None
    assert parser.parse("   ") is None


def test_rfid_scanner_initial_state():
    scanner = RFIDScanner()
    assert scanner.state == ReaderState.READY


def test_rfid_scanner_disable():
    scanner = RFIDScanner()
    scanner.disable()
    assert scanner.state == ReaderState.DISABLED
    assert scanner.read_uid() is None


def test_modem_send_when_connected():
    modem = Modem()
    modem.connect()
    msg = ModemMessage(recipient="admin", subject="Alert", body="Test alert")
    assert modem.send(msg) is True
    assert len(modem.outbox) == 1


def test_modem_send_when_disconnected():
    modem = Modem()
    msg = ModemMessage(recipient="admin", subject="Alert", body="Test")
    assert modem.send(msg) is False
    assert len(modem.outbox) == 0


def test_operator_panel():
    display = Display()
    keyboard = Keyboard()
    panel = OperatorPanel(display=display, keyboard=keyboard)
    panel.show_message("ACCESS GRANTED")
    assert panel.display.text == "ACCESS GRANTED"
    panel.clear()
    assert panel.display.text == ""


def test_keyboard_press_and_read():
    kb = Keyboard()
    kb.press("OPEN")
    assert kb.read() == "OPEN"
    assert kb.read() is None
