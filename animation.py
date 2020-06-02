import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D


def adjust_limits(filename):
	fig_tmp = plt.figure()

	data = [[], []]
	data[0], data[1] = np.loadtxt(filename, delimiter=' ', unpack=True)

	ax_tmp = fig_tmp.add_subplot(111)
	ax_tmp.plot(data[0], data[1])

	xlim = ax_tmp.get_xlim()
	ylim = ax_tmp.get_ylim()

	plt.close()

	return xlim, ylim


def adjust_limits3D(filename):
	fig_tmp = plt.figure()

	data = [[], [], []]
	biological_system = [[], [], [], []]
	data[0], data[1], data[2] = np.loadtxt(filename, delimiter=' ', unpack=True)
	biological_system[0], biological_system[1], biological_system[2], biological_system[3] = np.loadtxt(
		'biological_system_parameters.tmp', delimiter=' ', unpack=True)

	ax_tmp = fig_tmp.gca(projection='3d')
	ax_tmp.plot(data[0], data[1], data[2])
	ax_tmp.plot(biological_system[0] / 10, biological_system[1] / 10, biological_system[2] / 10)

	xlim = ax_tmp.get_xlim()
	ylim = ax_tmp.get_ylim()
	zlim = ax_tmp.get_zlim()

	plt.close()

	return xlim, ylim, zlim


def create_animation():
	animation_progress_window = tk.Tk()
	animation_progress_window.title('Animation progress')

	progress_bar_label = tk.Label(animation_progress_window, text='Progress of rendering the animation', width=50)
	progress_bar_label.grid(row=0)

	progress_bar = ttk.Progressbar(animation_progress_window, orient='horizontal', mode='determinate')
	progress_bar['maximum'] = 100
	progress_bar.grid(row=1, sticky=tk.NSEW)
	
	animation_rendering_status = tk.Label(animation_progress_window, text='Rendering...')
	animation_rendering_status.grid(row=2, sticky=tk.NSEW)
	
	style.use('ggplot')
	sns.set_palette(sns.color_palette("hls", 2))

	fig = plt.figure(figsize=(16, 10))

	trajectory = np.loadtxt('trajectory.txt', delimiter=' ', unpack=True)
	energy = np.loadtxt('energy.txt', delimiter=' ', unpack=True)
	velocity = np.loadtxt('velocity.txt', delimiter=' ', unpack=True)
	biological_system = np.loadtxt('biological_system_parameters.tmp', delimiter=' ', unpack=True)

	ax1 = fig.add_subplot(2, 2, (1, 3), projection='3d')
	obj1, = ax1.plot(trajectory[0], trajectory[1], trajectory[2])

	ax1.plot(biological_system[0] / 10, biological_system[1] / 10, biological_system[2] / 10, 'o', markersize=1)

	trajectory_xlim, trajectory_ylim, trajectory_zlim = adjust_limits3D('trajectory.txt')
	ax1.set_xlim(trajectory_xlim)
	ax1.set_ylim(trajectory_ylim)
	ax1.set_zlim(trajectory_zlim)

	ax1.set_xlabel('x[nm]')
	ax1.set_ylabel('y[nm]')
	ax1.set_zlabel('z[nm]')
	ax1.set_title('Particle trajectory')

	ax2 = fig.add_subplot(2, 2, 2)
	obj2, = ax2.plot(energy[0], energy[1])

	energy_xlim, energy_ylim = adjust_limits('energy.txt')
	ax2.set_xlim(energy_xlim)
	ax2.set_ylim(energy_ylim)

	ax2.set_xlabel('t[ns]')
	ax2.set_ylabel('E[eV]')
	ax2.set_title('Particle total energy vs time')

	ax3 = fig.add_subplot(2, 2, 4)
	obj3, = ax3.plot(velocity[0], velocity[1])

	velocity_xlim, velocity_ylim = adjust_limits('velocity.txt')
	ax3.set_xlim(velocity_xlim)
	ax3.set_ylim(velocity_ylim)

	ax3.set_xlabel('t[ns]')
	ax3.set_ylabel('v[m/s]')
	ax3.set_title('Particle velocity vs time')

	def init():
		obj1.set_data([], [])
		obj1.set_3d_properties([])

		obj2.set_data([], [])

		obj3.set_data([], [])
		return obj1, obj2, obj3,

	def animate(i):
		nonlocal step
		j = i * step

		progress_bar['value'] = i * 100 / frames_num
		progress_bar.update()

		obj1.set_data(trajectory[0, :j], trajectory[1, :j])
		obj1.set_3d_properties(trajectory[2, :j])

		obj2.set_data(energy[0, :j], energy[1, :j])

		obj3.set_data(velocity[0, :j], velocity[1, :j])
		return obj1, obj2, obj3,

	frames_num = 100
	step = math.ceil(len(energy[0]) / frames_num)

	ani = animation.FuncAnimation(fig, animate, init_func=init, frames=frames_num, blit=True)
	Writer = animation.writers['ffmpeg']
	writer = Writer(fps=10, metadata=dict(artist='Me'))

	ani.save('animation.mp4', writer=writer)

	animation_rendering_status['text'] = 'Rendering has finished!'
	animation_rendering_status.update()

	animation_progress_window.destroy()
	animation_progress_window.mainloop()
