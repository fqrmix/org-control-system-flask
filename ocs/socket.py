class SocketBalancer:
    """ Класс для балансировки пользователей socket.io """
    def __init__(self) -> None:
        self.socket_list = dict()
        self.while_started = False

    def popout_socket_connection(self, socket_id) -> bool:
        try:
            self.socket_list.pop(socket_id)
            return True
        except KeyError:
            return False

    def add_socket_connection(self, socket_id) -> bool:
        self.socket_list[socket_id] = True
        return self.socket_list[socket_id]

socket_balancer = SocketBalancer()
