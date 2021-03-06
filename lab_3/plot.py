from matplotlib import pylab

x1 = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35]
y1 = [0.083, 0.215,	0.402, 0.712, 1.203, 2.076,	3.418]

x2 = [0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700]
y2 = [0.146, 0.308, 0.479, 0.646, 0.833, 1.031, 1.247, 1.478, 1.725, 1.967, 2.343, 2.693, 3.258, 3.897]

x3 = [0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700, 0.750, 0.800, 0.850, 0.900, 0.950, 1.000, 1.050, 1.100, 1.150, 1.200, 1.250, 1.300, 1.350, 1.400, 1.450, 1.500, 1.550, 1.600, 1.650, 1.700, 1.750, 1.800, 1.850, 1.900]
y3 = [0.119, 0.224, 0.335, 0.472, 0.581, 0.710, 0.847, 0.981, 1.090, 1.242, 1.391, 1.549, 1.687, 1.857, 1.992, 2.195, 2.270, 2.506, 2.707, 2.942, 3.071, 3.313, 3.606, 3.791, 4.163, 4.300, 4.740, 5.229, 5.576, 6.238, 6.575, 7.069, 8.388, 9.121, 10.516, 11.800, 15.837, 24.012]

x4 = [0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700, 0.750, 0.800, 0.850, 0.900, 0.950, 1.000, 1.050, 1.100, 1.150, 1.200, 1.250, 1.300, 1.350, 1.400, 1.450, 1.500, 1.550, 1.600, 1.650, 1.700, 1.750, 1.800, 1.850, 1.900, 1.950]
y4 = [0.132, 0.258, 0.392, 0.530, 0.679, 0.818, 0.966, 1.126, 1.304, 1.473, 1.658, 1.826, 2.041, 2.246, 2.471, 2.727, 2.997, 3.319, 3.707, 4.172, 4.609, 5.420, 6.307, 7.293, 11.769, 16.255, 31.617, 72.805, 105.794, 134.484, 161.967, 213.838, 246.601, 283.930, 312.260, 357.494, 386.600, 431.428, 466.966]

x5 = [0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700, 0.750, 0.800, 0.850, 0.900, 0.950, 1.000, 1.050, 1.100, 1.150, 1.200, 1.250, 1.300, 1.350, 1.400, 1.450, 1.500, 1.550, 1.600, 1.650, 1.700, 1.750, 1.800, 1.850, 1.900, 1.950]
y5 = [0.122, 0.243, 0.367, 0.500, 0.636, 0.758, 0.898, 1.046, 1.190, 1.330, 1.494, 1.662, 1.812, 2.027, 2.178, 2.380, 2.588, 2.800, 3.061, 3.332, 3.510, 3.849, 4.249, 4.519, 5.065, 5.468, 6.415, 7.074, 8.853, 11.191, 16.803, 32.368, 87.969, 134.012, 183.332, 264.867, 325.028, 380.301, 445.050]

pylab.plot(x1[:5], y1[:5], 'k-', label='Min means [rand 2lvl]')
pylab.plot(x2[:5], y2[:5], 'k--', label='Min means [deter 2lvl]')
pylab.plot(x3[:5], y3[:5], 'k-.', label='Min means [deter 3lvl]')
pylab.legend(loc='upper left')
pylab.title(f'Minimum of means count of clients to $\lambda$')
pylab.xlabel('$\lambda$')
pylab.ylabel('Clients')
pylab.show()

_y3 = [val for val in y4 if val < 4]
pylab.plot(x1, y1, 'k-', label='Min means [rand 2lvl]')
pylab.plot(x2, y2, 'k--', label='Min means [deter 2lvl]')
pylab.plot(x3[:len(_y3)], _y3, 'k-.', label='Min means [deter 3lvl]')
pylab.legend(loc='upper left')
pylab.title(f'Minimum of means count of clients to $\lambda$')
pylab.xlabel('$\lambda$')
pylab.ylabel('Clients')
pylab.show()


pylab.plot(x3, y3, 'k-', label='Min means [1 chunk]')
pylab.plot(x4, y4, 'k--', label='Min means [3 chunk]')
pylab.plot(x5, y5, 'k-.', label='Min means [5 chunk]')
pylab.legend(loc='upper left')
pylab.title(f'Minimum of means count of clients to $\lambda$')
pylab.xlabel('$\lambda$')
pylab.ylabel('Clients')
pylab.show()
