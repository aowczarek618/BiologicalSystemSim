import json
import os
import threading
from shutil import copyfile
from tkinter import *
from tkinter import filedialog

import numpy as np

import animation as a
import graph as g
import simulation as s


def read_file_to_list(biological_system_filepath):
	biological_system_parameters = open(biological_system_filepath, 'r')
	biological_system = []

	for atom in biological_system_parameters.readlines():
		atom = atom.split()
		atom = list(map(float, atom))
		biological_system.append(atom)
	biological_system = np.array(biological_system)
	biological_system_parameters.close()

	return biological_system


def make_output_files():
	trajectory = open("trajectory.txt", "w")
	energy = open("energy.txt", "w")
	velocity = open("velocity.txt", "w")
	trajectory.close()
	energy.close()
	velocity.close()


def write_data_to_output_files(particle_pos, time, total_energy, particle_velocity):
	trajectory = open("trajectory.txt", "a")
	energy = open("energy.txt", "a")
	velocity = open("velocity.txt", "a")
	trajectory.write("{} {} {}\n".format(particle_pos[0] * 1e9, particle_pos[1] * 1e9, particle_pos[2] * 1e9))
	energy.write("{} {}\n".format(time * 1e9, total_energy * 6.24150913e18))
	velocity.write("{} {}\n".format(time * 1e9, particle_velocity))
	trajectory.close()
	energy.close()
	velocity.close()


def main():
	root = Tk()
	root.title("Simulator")
	biological_system_filepath = ''
	particle_filepath = ''
	stop_sim = False

	def get_filename_dat():
		return filedialog.askopenfilename(parent=root,
		                                  defaultextension='.dat',
		                                  filetypes=[('dat file', '.dat'), ('All files', '.*')])

	def get_filename_json():
		return filedialog.askopenfilename(parent=root,
		                                  defaultextension='.json',
		                                  filetypes=[('Json file', '.json'), ('All files', '.*')])

	def get_atoms_parameters():
		nonlocal biological_system_filepath
		biological_system_filepath = get_filename_dat()

	def get_particle_parameters():
		nonlocal particle_filepath
		particle_filepath = get_filename_json()

	def play():
		def run():
			nonlocal stop_sim
			file = open(particle_filepath, 'r')
			particle_parameters = json.loads(file.read())

			particle = s.Particle(pos=np.array(particle_parameters['pos']),
			                      velocity=np.array(particle_parameters['velocity']),
			                      mass=particle_parameters['mass'], charge=particle_parameters['charge'])
			biological_system = read_file_to_list(biological_system_filepath)
			make_output_files()
			time = 0
			time_step = float(time_step_spinbox.get())
			while not stop_sim:
				if time == 0:
					particle_pos, time, initial_total_energy, particle_velocity = s.simulation_step(particle,
					                                                                                biological_system,
					                                                                                time,
					                                                                                time_step)
				particle_pos, time, energy, particle_velocity = s.simulation_step(particle, biological_system, time,
				                                                                  time_step)
				if energy > 0:
					stop_sim = True
				else:
					write_data_to_output_files(particle_pos, time, energy, particle_velocity)
				if stop_sim:
					stop_simulation()
					break

		thread = threading.Thread(target=run, daemon=True)
		thread.start()

	def start_simulation():
		nonlocal stop_sim
		stop_sim = False
		v.set('Simulation is running!')
		statement['bg'] = 'red'
		statement['fg'] = 'white'
		play()

	def stop_simulation():
		nonlocal stop_sim
		stop_sim = True
		v.set('Simulation is stopped!')
		statement['bg'] = 'blue'
		statement['fg'] = 'white'

	def draw_graphs():
		copyfile(biological_system_filepath, 'biological_system_parameters.tmp')
		g.create_graphs()
		os.remove('biological_system_parameters.tmp')

	def draw_animation():
		copyfile(biological_system_filepath, 'biological_system_parameters.tmp')
		a.create_animation()
		os.remove('biological_system_parameters.tmp')

	start = Button(root, text='Start simulation', command=start_simulation, width=50)
	start.grid(row=0, column=0, columnspan=2, sticky=NSEW)

	finish = Button(root, text='Stop simulation', command=stop_simulation)
	finish.grid(row=1, column=0, columnspan=2, sticky=NSEW)

	biological_system_parameters = Button(root, text='Biological system parameters', command=get_atoms_parameters)
	biological_system_parameters.grid(row=2, column=0, columnspan=2, sticky=NSEW)

	particle_parameters_button = Button(root, text='Particle parameters', command=get_particle_parameters)
	particle_parameters_button.grid(row=3, column=0, columnspan=2, sticky=NSEW)

	graphs = Button(root, text='Graphs', command=draw_graphs)
	graphs.grid(row=4, column=0, columnspan=2, sticky=NSEW)

	animation = Button(root, text='Animation', command=draw_animation)
	animation.grid(row=5, column=0, columnspan=2, sticky=NSEW)

	time_step_label = Label(root, text='Time step: ')
	time_step_label.grid(row=6, column=0, sticky=NSEW)

	time_step_spinbox = Spinbox(root, values=tuple(np.geomspace(1e-18, 1e-10, 9)))
	time_step_spinbox.grid(row=6, column=1)

	exit_button = Button(root, text='Exit', command=root.destroy)
	exit_button.grid(row=7, column=0, columnspan=2, sticky=NSEW)

	v = StringVar()
	statement = Label(root, textvariable=v)
	statement.grid(row=8, column=0, columnspan=2, sticky=NSEW)

	root.mainloop()


if __name__ == '__main__':
	main()
