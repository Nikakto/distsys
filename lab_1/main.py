import numpy
from matplotlib import pylab

from lab_1.abstract import AbstractServer

QUANTUMS = 10000

# ======================================================================================================================
# Main lab
# ======================================================================================================================


class ServerPoison(AbstractServer):

    def __init__(self, poisson_lambda, client_message_probability=0.25, equality=False):
        super().__init__(client_message_probability=client_message_probability, equality=equality)
        self.equality = equality
        self.poisson_lambda = poisson_lambda

    def client_new(self):
        return numpy.random.poisson(self.poisson_lambda)


def server_emulating(server, moments=QUANTUMS):

    # quantum of times
    for i in range(moments):
        end = (i == moments - 1)
        server.moment(end=end)

    # stats
    print('mean clients per moment:', server.stats_mean_clients_new)
    print('mean live time:', server.stats_mean_clients_live_time)
    print('mean count of clients:', server.stats_mean_clients_count)


def plot(x_values, servers_a, servers_b, lamda=True):

    # mean live time
    pylab.axhline(y=QUANTUMS / 2, color='k', linestyle=':', label='throttling')
    pylab.plot(x_values, [server.stats_mean_clients_live_time for server in servers_a], 'k-', label='A')
    pylab.plot(x_values, [server.stats_mean_clients_live_time for server in servers_b], 'k--', label='B')
    pylab.legend(loc='upper left')
    pylab.title(f'Mean client\'s live time in system (quantums = {QUANTUMS})')
    pylab.xlabel('$\lambda$' if lamda else '$\sigma$')
    pylab.ylabel('$Time _{quantums}$')
    pylab.show()

    # mean count of clients
    pylab.plot(x_values, [server.stats_mean_clients_count for server in servers_a], 'k-', label='A')
    pylab.plot(x_values, [server.stats_mean_clients_count for server in servers_b], 'k--', label='B')
    pylab.legend(loc='upper left')
    pylab.title(f'Mean client\'s count in system (quantums = {QUANTUMS})')
    pylab.xlabel('$\lambda$' if lamda else '$\sigma$')
    pylab.ylabel('Count')
    pylab.show()

    # stablity

    def stability(servers):

        one, two, three = 0, int(len(servers_b) / 2), -2
        moments_start, moments_end = 0, 150
        _slice = slice(moments_start, moments_end)

        label = '$\lambda$' if lamda else '$\sigma$'
        pylab.plot(range(moments_start, moments_end), servers[one].clients_total[_slice], 'k*',
                   label='%s = %f.2' % (label, x_values[one]))

        pylab.plot(range(moments_start, moments_end), servers[two].clients_total[_slice], 'k--',
                   label='%s = %f.2' % (label, x_values[two]))

        pylab.plot(range(moments_start, moments_end), servers[three].clients_total[_slice], 'k-',
                   label='%s = %f.2' % (label, x_values[three]))

        pylab.legend(loc='upper left')
        pylab.title(f'Clients in system per moment (quantums = {QUANTUMS})')
        pylab.xlabel('Quantum (slot)')
        pylab.ylabel('Count')
        pylab.show()

    stability(servers_a)
    stability(servers_b)

# ======================================================================================================================
# Extra
# ======================================================================================================================


class ServerLogNorm(AbstractServer):

    client_message_probality = 0.25

    def __init__(self, lognormal_sigma, client_message_probability=0.25, equality=False):
        super().__init__(client_message_probability=client_message_probability, equality=equality)
        self.lognormal_sigma = lognormal_sigma

    def client_new(self):
        count = int(numpy.random.lognormal(mean=-1, sigma=self.lognormal_sigma))
        return count if count else 0


# ======================================================================================================================
# Runner
# ======================================================================================================================


if __name__ == '__main__':

    # POISON

    POISON_LAMBDAS = list(numpy.arange(0.05, 0.55, 0.05))

    print('\n\nPOISON A')
    servers_poison_a = []
    for poisson_lambda in POISON_LAMBDAS:

        print('\nlamda:', poisson_lambda)
        server = ServerPoison(poisson_lambda, client_message_probability=0.25, equality=False)
        server.title = f'$\lambda = {poisson_lambda:.2f}$'
        server_emulating(server)
        servers_poison_a.append(server)

    print('\n\nPOISON B')
    servers_poison_b = []
    for poisson_lambda in POISON_LAMBDAS:

        print('\nlamda:', poisson_lambda)
        server = ServerPoison(poisson_lambda, client_message_probability=0.25, equality=True)
        server.title = f'$\lambda = {poisson_lambda:.2f}$'
        server_emulating(server)
        servers_poison_b.append(server)

    # POISON PLOT
    plot(POISON_LAMBDAS, servers_poison_a, servers_poison_b)

    # LOGNORM

    LOGNORM_SIGMAS = list(numpy.arange(0.5, 1.5, 0.1))

    print('\n\nLOGNORM A')
    servers_lognormal_a = []
    for sigma in LOGNORM_SIGMAS:

        print('\nsigma:', sigma)
        server = ServerLogNorm(sigma, client_message_probability=0.25, equality=False)
        server.title = f'$\sigma = {numpy.round(sigma, 1):.2f}$'
        server_emulating(server)
        servers_lognormal_a.append(server)

    print('\n\nLOGNORM B')
    servers_lognormal_b = []
    for sigma in LOGNORM_SIGMAS:

        print('\nsigma:', sigma)
        server = ServerLogNorm(sigma, client_message_probability=0.25, equality=True)
        server.title = f'$\sigma = {numpy.round(sigma, 1):.2f}$'
        server_emulating(server)
        servers_lognormal_b.append(server)

    # POISON PLOT
    plot(LOGNORM_SIGMAS, servers_lognormal_a, servers_lognormal_b, lamda=False)
