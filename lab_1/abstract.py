import random


class AbstractClient:

    live_time = 0

    def __call__(self, message_probability):
        """
        :param message_probability: chance to sending message (if client just created chance is 100%)
        :return: True if client not dead and sending message
        """

        self.live_time += 1
        return random.random() < message_probability or self.live_time == 0


class AbstractServer:

    def __init__(self, client_message_probability=0.25, equality=False):
        """
        :param client_message_probability: chance of clients to sending message
        :param equality: chance og clients to sending message is 1 / count_of_clients
        """

        self.client_message_probability = client_message_probability
        self.equality = equality

        self.clients = []               # current clients on server

        self.clients_new = []           # return count of clients was add to server at the quantum of time
        self.clients_live_time = []     # return live_time of each client. At the end append live time of remain clients
        self.clients_messaging = []     # return count of clients send message at the quantum of time
        self.clients_total = []         # count of total client at the quantum of time

    def client_add(self):
        """
        Call client_new. If return True - add client to clients
        """

        new_clients = [self.client_create() for i in range(self.client_new())]
        self.clients.extend(new_clients)

        return new_clients

    def client_create(self):
        """
        :return: return instance of AbstractClient
        """
        return AbstractClient()

    def client_new(self) -> int:
        """
        :return: int(1) if at this moment new client has connected
        """

        return 1 if random.random() >= 0.5 else 0

    def moment(self, end=False):
        """
        Emulate quantum of time for sending messages by clients
        :return:
        """

        clients_added = self.client_add()
        self.clients_new.append(len(clients_added))

        _client_sending = []
        for client in self.clients:

            if self.equality:
                client_message_probability = 1 / len(self.clients) if self.clients else 1
            else:
                client_message_probability = self.client_message_probability

            _client_sending.append(client) if client(client_message_probability) else None

        self.clients_total.append(len(self.clients))

        if len(_client_sending) == 1:
            client = _client_sending.pop()
            self.clients.remove(client)
            self.clients_live_time.append(client.live_time)

        # final moment - add live time of all clients in system
        if end:
            [self.clients_live_time.append(client.live_time) for client in self.clients]

    @property
    def stats_mean_clients_count(self):
        return sum(self.clients_total) / len(self.clients_total)

    @property
    def stats_mean_clients_live_time(self):
        return sum(self.clients_live_time) / len(self.clients_live_time)

    @property
    def stats_mean_clients_new(self):
        return sum(self.clients_new) / len(self.clients_new)
