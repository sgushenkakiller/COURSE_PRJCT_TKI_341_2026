import signal
import sys
import time

from config.settings import Settings

from core.access_controller import AccessController
from core.audit import AuditLogger
from core.database import AccessRepository
from core.policy_engine import PolicyEngine
from core.security_monitor import SecurityMonitor

from devices.barrier_driver import BarrierDriver
from devices.modem import Modem
from devices.operator_panel import OperatorPanel, Display, Keyboard
from devices.rfid_reader import RFIDReader, RFIDScanner, RFIDParser
from devices.traffic_light import TrafficLightController

from entities.administrator import Administrator
from entities.barrier_state import BarrierState
from entities.direction import Direction
from entities.operator import Operator
from entities.policy_result import PolicyResult
from entities.rfid_card import RFIDCard
from entities.user import User

from security import (
    AuthenticationService,
    AuthorizationService,
    CryptoService,
    IntegrityService,
    SessionService,
)

from services.access_service import AccessService
from services.administration_service import AdministrationService
from services.operator_service import OperatorService
from services.user_service import UserService

from api.access_api import AccessAPI
from api.admin_api import AdminAPI
from api.monitor_api import MonitorAPI
from api.operator_api import OperatorAPI

settings = Settings()
_running = True


def handle_signal(signum, frame):
    global _running
    print("\n[SYSTEM] Получен сигнал завершения. Остановка...")
    _running = False


def seed_demo_data(repository: AccessRepository) -> None:
    admin_user = Administrator(
        identifier="admin-001",
        full_name="Системный Администратор",
        access_level=3,
        department="IT",
        superuser=True,
        can_modify_policy=True,
        can_manage_users=True,
    )
    repository.add_user(admin_user)

    operator_user = Operator(
        identifier="operator-001",
        full_name="Оператор КПП",
        access_level=2,
        department="Охрана",
        console_id="console-01",
        shift="день",
        can_override=True,
    )
    repository.add_user(operator_user)

    regular_user = User(
        identifier="user-001",
        full_name="Иванов Иван Иванович",
        access_level=1,
        department="Разработка",
    )
    repository.add_user(regular_user)

    blocked_user = User(
        identifier="user-002",
        full_name="Петров Пётр Петрович",
        access_level=1,
        department="Маркетинг",
        blocked=True,
    )
    repository.add_user(blocked_user)

    valid_card = RFIDCard(
        uid="CARD-A1B2C3",
        owner_id="user-001",
        issue_date="2024-01-01",
        expiration_date="2026-12-31",
        active=True,
    )
    repository.add_card(valid_card)

    blocked_card = RFIDCard(
        uid="CARD-X9Y8Z7",
        owner_id="user-002",
        issue_date="2024-01-01",
        expiration_date="2026-12-31",
        active=False,
    )
    repository.add_card(blocked_card)

    print("[INIT] Тестовые данные загружены:")
    print(f"       Пользователи: {len(repository.get_users())}")
    print(f"       Карты: {len(repository.get_cards())}")


def print_banner() -> None:
    print("=" * 60)
    print("  Киберимунная RFID Система Контроля Доступа (Шлагбаум)")
    print(f"  Версия: {settings.APP_VERSION}")
    print("=" * 60)


def simulate_access_cycle(
    access_api: AccessAPI,
    uid: str,
    direction: str,
    label: str,
) -> None:
    print(f"\n[RFID] Считана карта: {uid} ({label}, направление={direction})")
    response = access_api.process_card_read(uid=uid, reader_id=settings.READER_ID, direction=direction)
    result = response.payload.get("result", "unknown")
    reason = response.payload.get("reason", "")
    barrier_state = access_api.get_barrier_state().payload.get("barrier_state", "?")
    print(f"       Решение: {result.upper()} — {reason}")
    print(f"       Состояние шлагбаума: {barrier_state}")


def main() -> None:
    global _running

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    print_banner()

    print("\n[INIT] Инициализация репозитория...")
    repository = AccessRepository()

    print("[INIT] Инициализация ядра безопасности...")
    crypto = CryptoService()
    integrity = IntegrityService(crypto)
    session_service = SessionService()
    authentication = AuthenticationService(repository)
    authorization = AuthorizationService()

    print("[INIT] Инициализация Policy Engine...")
    policy_engine = PolicyEngine(repository)

    print("[INIT] Инициализация монитора безопасности...")
    monitor = SecurityMonitor()

    print("[INIT] Инициализация аудита...")
    audit = AuditLogger(repository)

    print("[INIT] Инициализация шлагбаума...")
    barrier = BarrierDriver()

    print("[INIT] Инициализация контроллера доступа...")
    controller = AccessController(
        policy=policy_engine,
        barrier=barrier,
        monitor=monitor,
        audit=audit,
    )

    print("[INIT] Инициализация устройств...")
    scanner = RFIDScanner()
    parser = RFIDParser()
    rfid_reader = RFIDReader(
        scanner=scanner,
        parser=parser,
        controller=controller,
        reader_id=settings.READER_ID,
    )
    traffic_light = TrafficLightController()
    modem = Modem()
    modem.connect()
    display = Display()
    keyboard = Keyboard()
    operator_panel = OperatorPanel(display=display, keyboard=keyboard)

    print("[INIT] Инициализация сервисов...")
    access_service = AccessService(
        controller=controller,
        barrier=barrier,
        monitor=monitor,
        audit=audit,
    )
    administration_service = AdministrationService(
        repository=repository,
        audit=audit,
        monitor=monitor,
    )
    operator_service = OperatorService(
        barrier=barrier,
        repository=repository,
        audit=audit,
        monitor=monitor,
    )
    user_service = UserService(repository=repository)

    print("[INIT] Инициализация API слоя...")
    access_api = AccessAPI(
        access_service=access_service,
        authentication=authentication,
        audit=audit,
    )
    admin_api = AdminAPI(
        administration_service=administration_service,
        authorization=authorization,
        audit=audit,
    )
    monitor_api = MonitorAPI(
        monitor=monitor,
        barrier=barrier,
        session_service=session_service,
        authorization=authorization,
        audit=audit,
    )
    operator_api = OperatorAPI(
        operator_service=operator_service,
        barrier=barrier,
        authorization=authorization,
        audit=audit,
    )

    if settings.SEED_DATA:
        print("\n[INIT] Загрузка демонстрационных данных...")
        seed_demo_data(repository)

    print("\n[SYSTEM] Система запущена. Начало демонстрации работы.\n")

    print("-" * 60)
    print("[DEMO] Сценарий 1: Действительная карта — доступ должен быть разрешён")
    simulate_access_cycle(access_api, "CARD-A1B2C3", "entry", "действительная карта")
    time.sleep(settings.LOOP_INTERVAL)

    print("-" * 60)
    print("[DEMO] Сценарий 2: Недействительная карта — доступ должен быть запрещён")
    simulate_access_cycle(access_api, "CARD-UNKNOWN", "entry", "неизвестная карта")
    time.sleep(settings.LOOP_INTERVAL)

    print("-" * 60)
    print("[DEMO] Сценарий 3: Заблокированная карта — доступ должен быть запрещён")
    simulate_access_cycle(access_api, "CARD-X9Y8Z7", "entry", "заблокированная карта")
    time.sleep(settings.LOOP_INTERVAL)

    print("-" * 60)
    print("[DEMO] Сценарий 4: Повторный проход действительной карты (выезд)")
    simulate_access_cycle(access_api, "CARD-A1B2C3", "exit", "выезд")
    time.sleep(settings.LOOP_INTERVAL)

    print("\n" + "-" * 60)
    print("[DEMO] Статус системы:")
    admin = repository.get_user("admin-001")
    status = monitor_api.get_system_status(admin)
    print(f"       {status.payload}")

    print("\n[DEMO] Журнал аудита:")
    for rec in repository.get_records():
        print(f"       [{rec.timestamp.strftime('%H:%M:%S')}] {rec.event} — {rec.source}: {rec.details}")

    print("\n[DEMO] События безопасности:", monitor.count())
    for evt in monitor.events():
        print(f"       [{evt.severity.value.upper()}] {evt.event_type.value} — {evt.description}")

    print("\n" + "=" * 60)
    print("[SYSTEM] Демонстрация завершена. Система готова к работе.")
    print("         Нажмите Ctrl+C для завершения.")
    print("=" * 60)

    while _running:
        time.sleep(settings.LOOP_INTERVAL)

    print("\n[SYSTEM] Система остановлена.")


if __name__ == "__main__":
    main()
