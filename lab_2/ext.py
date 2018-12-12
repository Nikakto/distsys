import numpy
from matplotlib import pylab

from lab_1.abstract import AbstractServer

QUANTUMS = 1000
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


def _servers_section(poisson_lambda, p_receiver, p_repeater, sections=None):

    section = {
        'server': ServerRepeater(client_message_probability=p_repeater),
    }

    if sections:
        section['leafs'] = [section['server'] for section in sections]
    else:
        section['leafs'] = [ServerReceiver(poisson_lambda=poisson_lambda, client_message_probability=p_receiver)
                            for i in range(2)]

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


def server_emulating(poisson_lambda, p_receivers, p_repeaters_low, p_repeaters_medium):

    def _emulation(p_receiver, p_repeater_low, p_repeater_medium):

        print('lambda=%f; p_receiver=%f; p_repeater_low=%f; p_repeater_medium=%f'
              % (poisson_lambda, p_receiver, p_repeater_low, p_repeater_medium))

        # 2 lists of 2 ServerPoison
        sections_receiver = [_servers_section(poisson_lambda, p_receiver, p_repeater_low) for i in range(4)]
        sections_repeater = [_servers_section(poisson_lambda, None, p_repeater_medium, sections_receiver[i*2:((i+1)*2)])
                             for i in range(2)]

        for moment in range(QUANTUMS):

            end = (moment == QUANTUMS - 1)

            _servers_moment([section['server'] for section in sections_repeater], end=end)
            _servers_moment([section['server'] for section in sections_receiver], end=end)

            for section in sections_receiver:
                new_clients = _servers_moment(section['leafs'], end=end)
                section['server'].clients.extend(new_clients)

        mean_count = sum(_servers_section_mean_clients_count(section) for section in sections_receiver)
        mean_count += sum(section['server'].stats_mean_clients_count for section in sections_repeater)
        return mean_count

    results = []

    for p_receiver in p_receivers:
        result_row = []
        results.append(result_row)

        for p_repeater_low in p_repeaters_low:

            result_column = []
            result_row.append(result_column)

            for p_repeater_medium in p_repeaters_medium:
                result = _emulation(p_receiver, p_repeater_low, p_repeater_medium)
                result_column.append(result)

    return results


if __name__ == '__main__':

    POISON_LAMBDAS = list(numpy.arange(0.05, 0.75, 0.05))
    P_RECEIVERS = list(numpy.arange(0.70, 1.00, 0.05))
    P_REPEATERS_LOW = list(numpy.arange(0.70, 1.00, 0.05))
    P_REPEATERS_MEDIUM = list(numpy.arange(0.35, 0.70, 0.05))

    min_means, min_means_x, min_means_y, min_means_z = [], [], [], []

    results = []

    for poison_lambda in POISON_LAMBDAS:

        min_means_run = []
        min_means_x_run = []
        min_means_y_run = []
        min_means_z_run = []

        for run in range(RUNS):

            print('\n\nRUN:', run+1, '\n\n')

            result = server_emulating(poison_lambda / 8, P_RECEIVERS, P_REPEATERS_LOW, P_REPEATERS_MEDIUM)

            matrix = numpy.array(result)
            min_mean_x, min_mean_y, min_mean_z = numpy.unravel_index(matrix.argmin(), matrix.shape)

            min_means_run.append(result[min_mean_x][min_mean_y][min_mean_z])
            min_means_y_run.append(P_RECEIVERS[min_mean_x])
            min_means_z_run.append(P_REPEATERS_LOW[min_mean_y])
            min_means_x_run.append(P_REPEATERS_MEDIUM[min_mean_z])

            # print('\n\nMATRIX', 'lambda = %.2f' % poison_lambda, '; column - p_repeaters; rows - p_receiver')
            # print(' '*8 + ('{:7.2f} ' * len(P_REPEATERS)).format(*P_REPEATERS))
            # for index, row_data in enumerate(result):
            #
            #     print('{:7.2f} '.format(P_RECEIVERS[index]), end='')
            #     print(('{:7.2f} ' * len(row_data)).format(*row_data))

            # if run < 1:
            #
            #     with open('matrix_%.2f' % poison_lambda, 'w') as f:
            #
            #         f.write('MATRIX' + 'lambda = %.2f' % poison_lambda + '; column - p_repeaters; rows - p_receiver\n')
            #         f.write(' ' * 8 + ('{:7.2f}\t' * len(P_REPEATERS)).format(*P_REPEATERS))
            #
            #         for index, row_data in enumerate(result):
            #             f.write('\n{:7.2f}\t'.format(P_RECEIVERS[index]))
            #             f.write(('{:7.2f}\t' * len(row_data)).format(*row_data))

        file_name = 'lamba_%.2f.txt' % (poison_lambda, )

        results.append([
            min_means.append(sum(min_means_run) / RUNS),
            min_means_x.append(sum(min_means_x_run) / RUNS),
            min_means_y.append(sum(min_means_y_run) / RUNS),
            min_means_z.append(sum(min_means_z_run) / RUNS),
        ])

        with open(file_name, 'w') as f:
            f.write(
                f'min means: {sum(min_means_run) / RUNS}\n'
                f'receiver: {sum(min_means_x_run) / RUNS}\n'
                f'repeater low: {sum(min_means_y_run) / RUNS}\n'
                f'repeater med: {sum(min_means_z_run) / RUNS}\n'
            )

    pylab.plot(POISON_LAMBDAS, min_means, 'k-', label='Min means')
    pylab.legend(loc='upper left')
    pylab.title(f'Minimum of means count of clients to $\lambda$')
    pylab.xlabel('$\lambda$')
    pylab.ylabel('Clients')
    pylab.savefig('Minimum of means.png')
    pylab.show()

    pylab.plot(POISON_LAMBDAS, min_means_x, 'k-', label='P receivers')
    pylab.plot(POISON_LAMBDAS, min_means_y, 'k--', label='P repeaters_low')
    pylab.plot(POISON_LAMBDAS, min_means_z, 'k*', label='P repeaters_medium')
    # pylab.legend(loc='upper left')
    pylab.title(f'P of (receiver and repeater) to $\lambda$')
    pylab.xlabel('$\lambda$')
    pylab.ylabel('P')
    pylab.savefig('P of (receiver and repeater).png')
    pylab.show()
