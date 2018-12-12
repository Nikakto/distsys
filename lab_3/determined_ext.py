import numpy
from matplotlib import pylab

from lab_1.abstract import AbstractServer

EVERY_MOMENTS = 5
QUANTUMS = 5000
RUNS = 10


# ======================================================================================================================
# Main lab
# ======================================================================================================================


class ServerDetermined(AbstractServer):

    def moment(self, can_return=True, end=False):

        result = []

        clients_added = self.client_add()
        self.clients_new.append(len(clients_added))
        self.clients_total.append(len(self.clients))

        for client in self.clients:
            client.live_time += 1

        if can_return and self.clients:
            client = self.clients.pop()
            self.clients_live_time.append(client.live_time)
            result.append(client)

        # final moment - add live time of all clients in system
        if end:
            [self.clients_live_time.append(client.live_time) for client in self.clients]

        return result


class ServerReceiver(ServerDetermined):

    def __init__(self, poisson_lambda, client_message_probability=0.25, equality=False):
        super().__init__(client_message_probability=client_message_probability, equality=equality)
        self.equality = equality
        self.poisson_lambda = poisson_lambda

    def client_new(self):
        return numpy.random.poisson(self.poisson_lambda)


class ServerRepeater(ServerDetermined):

    def __init__(self, client_message_probability=0.25, equality=False):
        super().__init__(client_message_probability=client_message_probability, equality=equality)
        self.equality = equality

    def client_new(self):
        return 0


def _servers_section(poisson_lambda, sections=None):

    section = {
        'server': ServerRepeater(),
    }

    if sections:
        section['leafs'] = [section['server'] for section in sections]
    else:
        section['leafs'] = [ServerReceiver(poisson_lambda=poisson_lambda) for i in range(2)]

    return section


def _servers_section_mean_clients_count(section):

    leafs_mean = sum(server.stats_mean_clients_count for server in section['leafs'])
    return section['server'].stats_mean_clients_count + leafs_mean


def _servers_moment(servers, first=False, end=False):

    if first:
        servers[1].moment(can_return=False, end=end)
        return servers[0].moment(end=end)
    else:
        servers[0].moment(can_return=False, end=end)
        return servers[1].moment(end=end)


def server_emulating(poisson_lambda):

    print('lambda=%f;' % poisson_lambda)

    # 2 lists of 2 ServerPoison
    sections_receiver = [_servers_section(poisson_lambda) for i in range(4)]
    sections_repeater = [_servers_section(poisson_lambda, sections_receiver[i * 2:((i + 1) * 2)]) for i in range(2)]

    first = True
    for moment in range(QUANTUMS):

        if moment % EVERY_MOMENTS:
            first = not first

        end = (moment == QUANTUMS - 1)

        _servers_moment([section['server'] for section in sections_repeater], first=first, end=end)
        _servers_moment([section['server'] for section in sections_receiver], first=first, end=end)

        for section in sections_receiver:
            new_clients = _servers_moment(section['leafs'], first=first, end=end)
            section['server'].clients.extend(new_clients)

    mean_count = sum(_servers_section_mean_clients_count(section) for section in sections_receiver)
    mean_count += sum(section['server'].stats_mean_clients_count for section in sections_repeater)
    return mean_count


if __name__ == '__main__':

    POISON_LAMBDAS = list(numpy.arange(0.05, 2.00, 0.05))

    min_means = []
    for poison_lambda in POISON_LAMBDAS:
        min_mean_lambda = sum(server_emulating(poison_lambda / 8) for run in range(RUNS)) / RUNS
        min_means.append(min_mean_lambda)

    with open(f'determined_ext_{EVERY_MOMENTS}', 'w') as f:
        f.write(', '.join('%.3f' % v for v in POISON_LAMBDAS))
        f.write('\n')
        f.write(', '.join('%.3f' % v for v in min_means))

    pylab.plot(POISON_LAMBDAS, min_means, 'k-', label='Min means')
    pylab.legend(loc='upper left')
    pylab.title(f'Minimum of means count of clients to $\lambda$')
    pylab.xlabel('$\lambda$')
    pylab.ylabel('Clients')
    pylab.show()
