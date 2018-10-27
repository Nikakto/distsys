import numpy
from matplotlib import pylab
from mpl_toolkits.mplot3d import Axes3D


from lab_1.abstract import AbstractServer

QUANTUMS = 2000


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


def server_emulating(poisson_lambda, p_receivers, p_repeaters):

    def _emulation(p_receiver, p_repeater):

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

    results = []

    for p_receiver in p_receivers:
        result_row = []
        results.append(result_row)

        for p_repeater in p_repeaters:
            result = _emulation(p_receiver, p_repeater)
            result_row.append(result)

    return results


if __name__ == '__main__':

    POISON_LAMBDAS = list(numpy.arange(0.05, 0.40, 0.05))
    P_RECEIVERS = list(numpy.arange(0.05, 1.00, 0.05))
    P_REPEATERS = list(numpy.arange(0.05, 1.00, 0.05))

    min_means, min_means_x, min_means_y = [], [], []

    results = [(poison_lambda, server_emulating(poison_lambda/4, P_RECEIVERS, P_REPEATERS)) for poison_lambda in POISON_LAMBDAS]

    for poison_lambda, result in results:

        print('\n\nMATRIX', 'lambda = %.2f' % poison_lambda, '; column - p_repeaters; rows - p_receiver')
        print(' '*8 + ('{:7.2f} ' * len(P_REPEATERS)).format(*P_REPEATERS))
        for index, row_data in enumerate(result):

            print('{:7.2f} '.format(P_RECEIVERS[index]), end='')
            print(('{:7.2f} ' * len(row_data)).format(*row_data))

        matrix = numpy.asmatrix(result)
        min_mean_x, min_mean_y = numpy.unravel_index(matrix.argmin(), matrix.shape)

        min_means.append(result[3][3])
        min_means_x.append(min_mean_x)
        min_means_y.append(min_mean_y)

    pylab.plot(POISON_LAMBDAS, min_means, 'k-', label='Min means')
    pylab.legend(loc='upper left')
    pylab.title(f'Minimum of means count of clients to $\lambda$')
    pylab.xlabel('$\lambda$')
    pylab.ylabel('Clients')
    pylab.show()

    pylab.plot(POISON_LAMBDAS, [P_REPEATERS[index] for index in min_means_x], 'k-', label='P receivers')
    pylab.plot(POISON_LAMBDAS, [P_RECEIVERS[index] for index in min_means_y], 'k*', label='P repeaters')
    pylab.legend(loc='upper left')
    pylab.title(f'P of (receiver and repeater) to $\lambda$')
    pylab.xlabel('$\lambda$')
    pylab.ylabel('P')
    pylab.show()
