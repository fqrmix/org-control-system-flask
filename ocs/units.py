from ocs import socketio
import asyncio
import datetime

class Door:
    def __init__(self) -> None:
        pass

    def open(self):
        socketio.emit('send_success_message')

        async def async_coroutine():
            await asyncio.sleep(5)
            self.close()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coroutine = async_coroutine()
        loop.run_until_complete(coroutine)
          
    def close(self):
        socketio.emit('door_closed_message')

class OrganizationUnit:
    def __init__(self, access_level) -> None:
        self.door = Door()
        self.access_level = access_level
        self.employees_list = dict()

    def update_list(self, user, direction: str) -> None:
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
    def __init__(self) -> None:
        super().__init__(access_level=1)

    class ServerRoom(OrganizationUnit):
        def __init__(self) -> None:
            super().__init__(access_level=4)

    class AccountingRoom(OrganizationUnit):
        def __init__(self) -> None:
            super().__init__(access_level=6)

def get_current_unit(unit_type: str) -> OrganizationUnit:
    units = {
        'main_room': main,
        'server_room': server_room,
        'accounting_room': accounting_room
    }
    if unit_type not in units:
        raise KeyError

    return units[unit_type]

main = Main()
server_room = main.ServerRoom()
accounting_room = main.AccountingRoom()
