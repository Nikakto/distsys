import numpy
from matplotlib import pylab

from lab_1.abstract import AbstractServer

QUANTUMS = 5000
RUNS = 10


# ======================================================================================================================
# Main lab
# ======================================================================================================================

class ServerReceiver(AbstractServer):

    def __init__(self, poisson_lambda, client_message_probability=0.25, equality=False):
        super().__init__(client_message_probability=client_message_probability, equality=equality)
        self.equality = equality
        self.poisson_lambda = poisson_lambda

    def client_new(self):
        return numpy.random.poisson(self.poisson_lambda)


class ServerRepeater(AbstractServer):

    def __init__(self, client_message_probability=0.25, equality=False):
        super().__init__(client_message_probability=client_message_probability, equality=equality)
        self.equality = equality

    def client_new(self):
        return 0


def _servers_section(poisson_lambda, p_receiver, p_repeater):

    section = {
        'leafs': [ServerReceiver(poisson_lambda=poisson_lambda, client_message_probability=p_receiver) for i in range(2)],
        'server': ServerRepeater(client_message_probability=p_repeater),
    }

    return section


def _servers_section_mean_clients_count(section):

    leafs_mean = sum(server.stats_mean_clients_count for server in section['leafs'])
    return section['server'].stats_mean_clients_count + leafs_mean


def _servers_moment(servers, end=False):

    clients_0, clients_1 = servers[0].moment(end=end), servers[1].moment(end=end)

    if clients_0 and clients_1:
        servers[0].clients.extend(clients_0)
        servers[1].clients.extend(clients_1)

    return clients_0 or clients_1


def server_emulating(poisson_lambda, p_receiver, p_repeater):

    print('lambda=%f; p_receiver=%f; p_repeater=%f' % (poisson_lambda, p_receiver, p_repeater))

    # 2 lists of 2 ServerPoison
    sections = [_servers_section(poisson_lambda, p_receiver, p_repeater) for i in range(2)]

    for moment in range(QUANTUMS):

        end = (moment == QUANTUMS - 1)

        _servers_moment([section['server'] for section in sections], end=end)
        for section in sections:
            new_clients = _servers_moment(section['leafs'], end=end)
            section['server'].clients.extend(new_clients)

    mean_count = sum(_servers_section_mean_clients_count(section) for section in sections)
    return mean_count


if __name__ == '__main__':

    POISON_LAMBDAS = list(numpy.arange(0.05, 0.40, 0.05))
    P_RECEIVERS = [0.860, 0.880, 0.740, 0.665, 0.615, 0.485, 0.51]
    P_REPEATERS = [0.855, 0.810, 0.830, 0.735, 0.560, 0.37, 0.31]

    RUNS_DATA = zip(POISON_LAMBDAS, P_RECEIVERS, P_REPEATERS)

    min_means = []
    for poison_lambda, p_receiver, p_repeater in RUNS_DATA:
        min_mean_lambda = sum(server_emulating(poison_lambda / 4, p_receiver, p_repeater) for run in range(RUNS)) / RUNS
        min_means.append(min_mean_lambda)

    with open('random', 'w') as f:
        f.write(', '.join('%.3f' % v for v in POISON_LAMBDAS))
        f.write('\n')
        f.write(', '.join('%.3f' % v for v in min_means))

    pylab.plot(POISON_LAMBDAS, min_means, 'k-', label='Min means')
    pylab.legend(loc='upper left')
    pylab.title(f'Minimum of means count of clients to $\lambda$')
    pylab.xlabel('$\lambda$')
    pylab.ylabel('Clients')
    pylab.show()
