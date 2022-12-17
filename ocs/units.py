from ocs import socketio
import asyncio
import datetime
from ocs import models

class Door:
    """ Базовый класс двери в комнату """
    def __init__(self) -> None:
        pass

    def open(self):
        socketio.emit('send_success_message')

    def close(self):
        async def async_coroutine():
            await asyncio.sleep(5)
            socketio.emit('door_closed_message')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coroutine = async_coroutine()
        loop.run_until_complete(coroutine)
        

class OrganizationUnit:
    """ Базовый класс юнита в организации """
    def __init__(self, access_level) -> None:
        self.door = Door()
        self.access_level = access_level
        self.employees_list = dict()

    def update_list(self, user: models.Users, direction: str) -> None:
        if direction == 'in':
            current_user = dict()
            current_user['username'] = user.username
            current_user['time_of_arrival'] = datetime.datetime.now().strftime("%H:%M:%S")
            self.employees_list[user.id] = current_user
        if direction == 'out':
            self.employees_list.pop(user.id)
            
    def get_state(self):
        return self.employees_list

    def is_user_inside(self, user):
        if user.id in self.employees_list:
            return True
        return False

class Main(OrganizationUnit):
    """
        Класс основной комнаты (фактически - вся организация)
    """
    def __init__(self) -> None:
        super().__init__(access_level=1)

    class ServerRoom(OrganizationUnit):
        """ Класс серверной комнаты """
        def __init__(self) -> None:
            super().__init__(access_level=6)

    class AccountingRoom(OrganizationUnit):
        """ Класс комнаты бухгалтерии """
        def __init__(self) -> None:
            super().__init__(access_level=4)

class Organization:
    def __init__(self) -> None:
        self.main = Main()
    
    def get_state(self) -> dict:
        result = dict()
        for unit in units:
            current_unit = units[unit]
            result[unit] = current_unit.get_state()
        return result



def get_current_unit(unit_type: str) -> OrganizationUnit:
    if unit_type not in units:
        raise KeyError

    return units[unit_type]

main = Main()
server_room = main.ServerRoom()
accounting_room = main.AccountingRoom()

units = {
    'main_room': main,
    'server_room': server_room,
    'accounting_room': accounting_room
}

organization = Organization()
