class DoorOpeningError(Exception):
    """
        Base door opening exception
        *args - reason
    """
    def __init__(self, *args: object) -> None:
            self.reason = args[0]
    
    def __str__(self) -> str:
            return f"DoorOpeningError! Reason: {self.reason}"

class IncorrectPassword(DoorOpeningError):
    def __init__(self) -> None:
        super().__init__('Был введен неверный пин!')

class UnknownUser(DoorOpeningError):
    def __init__(self) -> None:
        super().__init__('На камере находится человек, незарегистрированный в организации!')

class AccessError(DoorOpeningError):
    def __init__(self) -> None:
        super().__init__('У пользователя недостаточный уровень доступа для открытия двери!')

class AlreadyInside(DoorOpeningError):
    def __init__(self) -> None:
         super().__init__('Пользователь уже находится внутри здания!')
