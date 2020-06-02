import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D


def create_graphs():
	trajectory = np.loadtxt('trajectory.txt', delimiter=' ', unpack=True)
	biological_system = np.loadtxt('biological_system_parameters.tmp', delimiter=' ', unpack=True)
	energy = np.loadtxt('energy.txt', delimiter=' ', unpack=True)
	velocity = np.loadtxt('velocity.txt', delimiter=' ', unpack=True)

	plt.rcParams.update({'font.size': 14})
	style.use('ggplot')
	sns.set_palette(sns.color_palette("hls", 2))
	# Figure 1 "Particle trajectory" -------------------------------------------------
	fig = plt.figure(1)
	ax = fig.gca(projection='3d')

	ax.plot(trajectory[0], trajectory[1], trajectory[2])
	ax.plot(biological_system[0] / 10, biological_system[1] / 10, biological_system[2] / 10, 'o', markersize='1')

	ax.set_xlabel('x[nm]')
	ax.set_ylabel('y[nm]')
	ax.set_zlabel('z[nm]')
	plt.title('Particle trajectory')
	# -----------------------------------------
	# Figure 2 "Particle total energy and velocity vs time" --------------------------
	fig, (ax1, ax2) = plt.subplots(2, sharex=True)
	ax1.plot(energy[0], energy[1])

	ax1.set_ylabel('E[eV]')
	ax1.set_title('Particle total energy vs time')

	ax2.plot(velocity[0], velocity[1])

	ax2.set_xlabel('t[ns]')
	ax2.set_ylabel('v[m/s]')
	ax2.set_title('Particle velocity vs time')
	# -----------------------------------------
	plt.show()
