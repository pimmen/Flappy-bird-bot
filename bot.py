import os.path
import json
from itertools import chain

class Bot:
	def __init__(self):
		self.num_games = 0
		self.dump_interval = 25

		self.rewards = {'good': 1, 'bad': -1000}
		self.learning_rate = 0.7
		self.discount = 1.0
		self.actions = []
		self.prev_state = "40_420_0"
		self.prev_action = 0

		if not os.path.isfile('qvalues.json'):
			print('No file present')
			self.initialize_qvalues()

		self.qvalues = self.load_qvalues()

	def load_qvalues(self):
		qvalues = {}

		json_file = open('qvalues.json')
		qvalues = json.load(json_file)
		json_file.close()
			
		return qvalues

	def choose_action(self, diff_to_path, dist_to_path, vertical_velocity):
		state = self.evaluate_state(diff_to_path, dist_to_path, vertical_velocity)
		
		self.actions.append([self.prev_state, self.prev_action, state])
		self.prev_state = state

		if state in self.qvalues.keys():
			if self.qvalues[state][0] >= self.qvalues[state][1]:
				self.prev_action = 0
				return 0
			else:
				self.prev_action = 1
				return 1

	def evaluate_state(self, diff_to_path, dist_to_path, vertical_velocity):
		if dist_to_path < 140:
			dist_to_path = int(dist_to_path) - (int(dist_to_path) % 10)
		else:
			dist_to_path = int(dist_to_path) - (int(dist_to_path) % 70)

		if diff_to_path < 180:
			diff_to_path = int(diff_to_path) - (int(diff_to_path) % 10)
		else:
			diff_to_path = int(diff_to_path) - (int(diff_to_path) % 60)

		return str(int(diff_to_path)) + '_' + str(int(dist_to_path)) + '_' + str(int(vertical_velocity))

	def update_scores(self):
		history = list(reversed(self.actions))

		high_death = True if int(history[0][2].split('_')[0]) > 120 else False

		t = 1
		for exp in history:
			state = exp[0]
			act = exp[1]
			res_state = exp[2]
			if state not in self.qvalues.keys():
				self.qvalues[state] = {}

			if t == 1 or t==2:
				self.qvalues[state][act] = (1- self.learning_rate) * (self.qvalues[state][act]) + (self.learning_rate) * ( self.rewards['bad'] + (self.discount)*max(self.qvalues[res_state]) )

			elif high_death and act:
				self.qvalues[state][act] = (1- self.learning_rate) * (self.qvalues[state][act]) + (self.learning_rate) * ( self.rewards['bad'] + (self.discount)*max(self.qvalues[res_state]) )
				high_death = False

			else:
				self.qvalues[state][act] = (1- self.learning_rate) * (self.qvalues[state][act]) + (self.learning_rate) * ( self.rewards['good'] + (self.discount)*max(self.qvalues[res_state]) )
			t += 1

		self.num_games = self.num_games + 1
		self.dump_qvalues()
		self.actions = []

	def dump_qvalues(self):

		if self.num_games % self.dump_interval == 0:
			json_file = open('qvalues.json', 'w')
			json.dump(self.qvalues, json_file)
			json_file.close()

			print('Updated qvalues file')
	
	def initialize_qvalues(self):
		qvalues = {}

		for x in chain(list(range(-40,140,10)), list(range(140,421,70))):
			for y in chain(list(range(-300,180,10)), list(range(180,421,60))):
				for v in range(-10,11):
					qvalues[str(y)+'_'+str(x)+'_'+str(v)] = [0,0]

		json_file = open('qvalues.json','w')
		json.dump(qvalues, json_file)
		json_file.close()


		



























