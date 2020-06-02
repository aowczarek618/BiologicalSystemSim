import numba
import numpy as np

spec = [
	('pos', numba.float64[:]),
	('velocity', numba.float64[:]),
	('mass', numba.float64),
	('charge', numba.float64)
]


@numba.jitclass(spec)
class Particle:
	def __init__(self, pos, velocity, mass, charge):
		self.pos = pos
		self.velocity = velocity
		self.mass = mass
		self.charge = charge


@numba.njit
def coulomb_potential(x, y, z, atom, r1, r2, r3):
	distance = np.sqrt((x - atom[0] * 1e-10 + VIBRATION_AMPLITUDE * np.sin(2 * np.pi * r1)) ** 2 + (
				y - atom[1] * 1e-10 + VIBRATION_AMPLITUDE * np.sin(2 * np.pi * r2)) ** 2 + (
				                   z - atom[2] * 1e-10 + VIBRATION_AMPLITUDE * np.sin(2 * np.pi * r3)) ** 2)
	potential_value = COULOMB_CONSTANT * atom[3] * ELEMENTARY_CHARGE / distance
	return potential_value


@numba.njit
def gradient(f, x, y, z, h, atom, r1, r2, r3):
	rise = np.array([f(x + h, y, z, atom, r1, r2, r3) - f(x - h, y, z, atom, r1, r2, r3),
	                 f(x, y + h, z, atom, r1, r2, r3) - f(x, y - h, z, atom, r1, r2, r3),
	                 f(x, y, z + h, atom, r1, r2, r3) - f(x, y, z - h, atom, r1, r2, r3)])
	return rise / (2 * h)


@numba.njit
def vector_length(vector):
	return np.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)


@numba.njit
def simulation_step(particle, biological_system, time, time_step):
	# Calculating gradient of potential ---------------------------
	gradient_of_potential = np.array([0., 0., 0.])
	potential_energy = 0
	for i in range(biological_system.shape[0]):
		atom = biological_system[i, :]
		r1, r2, r3 = np.random.rand(3)
		gradient_of_potential += gradient(coulomb_potential, particle.pos[0], particle.pos[1], particle.pos[2],
		                                  ARGUMENT_RISE, atom, r1, r2, r3)
		potential_energy += coulomb_potential(particle.pos[0], particle.pos[1], particle.pos[2],
		                                      atom, r1, r2, r3) * particle.charge
	# -------------------------------------------------------------
	# Simulation step----------------------------------------------
	particle.velocity -= time_step * particle.charge / particle.mass * gradient_of_potential
	particle.pos += time_step * particle.velocity
	kinetic_energy = particle.mass * vector_length(particle.velocity) ** 2 / 2
	total_energy = kinetic_energy + potential_energy
	time += time_step
	# -------------------------------------------------------------
	return particle.pos, time, total_energy, vector_length(particle.velocity)


# constants ---------------------------
VIBRATION_AMPLITUDE = 1e-11
COULOMB_CONSTANT = 8.9875517873681764e9
BOLTZMANN_CONSTANT = 1.38064852e-23
ELEMENTARY_CHARGE = 1.6021766208e-19
ELECTRON_MASS = 9.10938356e-31
ARGUMENT_RISE = 1e-20  # parameter to counting a gradient
# -------------------------------------
