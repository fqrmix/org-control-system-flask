class DoorError(Exception):
    """
        Base door opening exception
        *args - reason
    """
    def __init__(self, *args: object) -> None:
            self.reason = args[0]
    
    def __str__(self) -> str:
            return f"DoorOpeningError! Reason: {self.reason}"

class IncorrectPassword(DoorError):
    def __init__(self) -> None:
        super().__init__('Был введен неверный пин!')

class UnknownUser(DoorError):
    def __init__(self) -> None:
        super().__init__('На камере находится человек, незарегистрированный в организации!')

class AccessError(DoorError):
    def __init__(self) -> None:
        super().__init__('У пользователя недостаточный уровень доступа для открытия двери!')

class AlreadyInside(DoorError):
    def __init__(self) -> None:
         super().__init__('Пользователь уже находится внутри здания/комнаты!')

class NotInside(DoorError):
    def __init__(self) -> None:
         super().__init__('Пользователь не находится внутри здания/комнаты!')
