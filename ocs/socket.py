class SocketBalancer:
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
        self.last_socket_id = socket_id
        return self.socket_list[socket_id]

socket_balancer = SocketBalancer()
