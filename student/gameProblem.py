
'''
	Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search

class GameProblem(SearchProblem):

	# Object attributes, can be accessed in the methods below
	
	MAP=None
	POSITIONS=None
	INITIAL_STATE=None
	GOAL=None
	CONFIG=None
	AGENT_START=None
	SHOPS=[]
	CUSTOMERS=[]
	MAXBAGS = 0

	MOVES = ('West','North','East','South')

	# ---- HELPER FUNCTIONS ----
	def getPosition(self, state):
		return state[0]

	def getActiveOrders(self,state):
		return state[1]

	def getPizzasHeld(self,state):
		return state[2]

	def westpos(self,pos):
		return (pos[0]-1,pos[1])

	def northpos(self,pos):
		return (pos[0],pos[1]-1)

	def eastpos(self,pos):
		return (pos[0]+1,pos[1])

	def southpos(self,pos):
		return (pos[0],pos[1]+1)

	def validpos(self,pos):
		'''returns true if pos within grid bounds. else, returns false
		'''
		if pos[0] >= 0 and pos[0] < self.CONFIG['map_size'][0] and pos[1] >= 0 and pos[1] < self.CONFIG['map_size'][1]:
			return True
		else:
			return False

	def blocked(self,pos):
		'''returns true if pos is a blocked building. else, returns false
		'''
		if pos in self.POSITIONS["building"]:
			return True
		else:
			return False

	def numActiveOrders(self,state):
		''' returns the total number of pizzas requested
		'''
		return sum(state[1])

	def numPizzasAtLoc(self,state,loc):
		''' returns the number of pizzas currently requested at a specific location
		'''
		if loc in self.CUSTOMERS:
			return self.getActiveOrders(state)[self.CUSTOMERS.index(loc)]
		else:
			return 0

   # --------------- Common functions to a SearchProblem -----------------

	def actions(self, state):
		'''Returns a LIST of the actions that may be executed in this state
		'''
		# Possible Actions: Move (W,N,E,S), Load, Unload
		actions = []
		pos = self.getPosition(state)
		piz = self.getPizzasHeld(state)
		# if at a restaurant and num pizzas held < 2 and there are active orders, add 'Load' to list
		if pos in self.SHOPS and piz < 2 and self.numActiveOrders(state) > 0:
			actions.append('Load')
		# if at a delivery loc and we have at least the num pizzas requested at that location, add 'Unload' to list
		if pos in self.CUSTOMERS and piz >= self.numPizzasAtLoc(state,pos):
			actions.append('Unload')
		# if not off grid and not blocked, add direction
		p = self.westpos(pos)
		if self.validpos(p) and not self.blocked(p):
			actions.append('West')
		p = self.northpos(pos)
		if self.validpos(p) and not self.blocked(p):
			actions.append('North')
		p = self.eastpos(pos)
		if self.validpos(p) and not self.blocked(p):
			actions.append('East')
		p = self.southpos(pos)
		if self.validpos(p) and not self.blocked(p):
			actions.append('South')
		print('Found possible actions',actions,'for state',state)
		return actions
	

	def result(self, state, action):
		'''Returns the state reached from this state when the given action is executed
		'''
		if action is 'Load':
			newPizzasHeld = min(self.MAXBAGS,self.numActiveOrders(state))
			print('self.MAXBAGS:',self.MAXBAGS,'numactiveorders:',self.numActiveOrders(state))
			next_state = (state[0],state[1],newPizzasHeld)
		if action is 'Unload':
			loc = self.getPosition(state)
			pizzasDelivered = self.numPizzasAtLoc(state,loc)
			active_orders = list(state[1])
			active_orders[self.CUSTOMERS.index(loc)] = active_orders[self.CUSTOMERS.index(loc)] - pizzasDelivered
			next_state = (state[0],tuple(active_orders),state[2]-pizzasDelivered)
		# Movement
		pos = self.getPosition(state)
		if action is 'West':
			next_state = (self.westpos(pos),state[1],state[2])
		if action is 'North':
			next_state = (self.northpos(pos),state[1],state[2])
		if action is 'East':
			next_state = (self.eastpos(pos),state[1],state[2])
		if action is 'South':
			next_state = (self.southpos(pos),state[1],state[2])
		print('Given state',state,'and action',action,'next state is',next_state)
		return next_state


	def is_goal(self, state):
		'''Returns true if state is the final state
		'''
		if state == self.GOAL:
			return True

	def cost(self, state, action, state2):
		'''Returns the cost of applying `action` from `state` to `state2`.
		   The returned value is a number (integer or floating point).
		   By default this function returns `1`.
		'''
		return 1

	def heuristic(self, state):
		'''Returns the heuristic for `state`
		'''
		# if order locs empty, MD from agent loc to (0,0)
		# else if pizzas held, MD to order loc + MD order loc to (0,0)
		# else, MD to restaurant + MD to order loc + MD order loc to (0,0)
		return 0


	def setup (self):
		'''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
		   This values are later stored as globals that are used when calling the search algorithm.
		   final state is optional because it is only used inside the is_goal() method

		   It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
		'''

		print('\nMAP: ', self.MAP, '\n')
		print('POSITIONS: ', self.POSITIONS, '\n')
		print('CONFIG: ', self.CONFIG, '\n')

		# initialize SHOPS, global variable that holds locations of restaurants
		if "pizza" in self.POSITIONS:
			for i in range(len(self.POSITIONS["pizza"])):
				self.SHOPS.append(self.POSITIONS["pizza"][i])
		print("SHOPS:", self.SHOPS)

		# initialize CUSTOMERS, the positions of clients and active_orders, the tuple of number of active
		# orders (number pizzas requested at that location), where the indices correspond with indices of 
		# CUSTOMERS
		active_orders = [] # build list and later convert to tuple
		if "customer1" in self.POSITIONS:
			for i in range(len(self.POSITIONS["customer1"])):
				self.CUSTOMERS.append(self.POSITIONS["customer1"][i])
				active_orders.append(1)
		if "customer2" in self.POSITIONS:
			for i in range(len(self.POSITIONS["customer2"])):
				self.CUSTOMERS.append(self.POSITIONS["customer2"][i])
				active_orders.append(2)
		if "customer3" in self.POSITIONS:
			for i in range(len(self.POSITIONS["customer3"])):
				self.CUSTOMERS.append(self.POSITIONS["customer3"][i])
				active_orders.append(3)
		print("CUSTOMERS:", self.CUSTOMERS)

		# initialize MAXBAGS, the maximum number of pizzas that can be held by agent at one time
		self.MAXBAGS = 2

		# define state as tuple (starting position (X/column,Y/row) tuple, 
		# tuple of active orders (location (X,Y), number pizzas requested), num of pizzas holding)
		# note that state must consist of immutable type due to search algorithm implementation details
		initial_state = (self.AGENT_START,tuple(active_orders),0)
		final_state= (self.AGENT_START,tuple(0 for i in range(len(active_orders))),0)
		algorithm= simpleai.search.astar
		#algorithm= simpleai.search.breadth_first
		#algorithm= simpleai.search.depth_first
		#algorithm= simpleai.search.limited_depth_first

		return initial_state,final_state,algorithm

	def printState (self,state):
		'''Return a string to pretty-print the state '''
		pps='(Row,Col)=('+str(state[0])+'\n'
		pps=pps+'Orders: '+str(state[1])+', Num Pizzas Holding: '+str(state[2])
		return (pps)

	def getPendingRequests (self,state):
		''' Return the number of pending requests in the given position (0-N). 
			MUST return None if the position is not a customer.
			This information is used to show the proper customer image.
		'''
		return self.numPizzasAtLoc(state,state[0])

	# -------------------------------------------------------------- #
	# --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
	# -------------------------------------------------------------- #

	def getAttribute (self, position, attributeName):
		'''Returns an attribute value for a given position of the map
		   position is a tuple (x,y)
		   attributeName is a string
		   
		   Returns:
			   None if the attribute does not exist
			   Value of the attribute otherwise
		'''
		tileAttributes=self.MAP[position[0]][position[1]][2]
		if attributeName in tileAttributes.keys():
			return tileAttributes[attributeName]
		else:
			return None

	def getStateData (self,state):
		stateData={}
		pendingItems=self.getPendingRequests(state)
		if pendingItems >= 0:
			stateData['newType']='customer{}'.format(pendingItems)
		return stateData
		
	# THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
	def initializeProblem(self,map,positions,conf,aiBaseName):
		self.MAP=map
		self.POSITIONS=positions
		self.CONFIG=conf
		self.AGENT_START = tuple(conf['agent']['start'])

		initial_state,final_state,algorithm = self.setup()
		if initial_state == False:
			print ('-- INITIALIZATION FAILED')
			return True
	  
		self.INITIAL_STATE=initial_state
		self.GOAL=final_state
		self.ALGORITHM=algorithm
		super(GameProblem,self).__init__(self.INITIAL_STATE)
			
		print ('-- INITIALIZATION OK')
		return True
		
	# END initializeProblem 

