""" Creation of Graph Structure """

from collections import defaultdict
import random

##Creating Graph Structure
class Graph:
    def __init__(self):
    #A Graph has a set of nodes
        self.nodes = set()
        #The set of Edges is a dictionary with {key:value} with key as
        # a node and value as a set of its neighbours
        self.edges = defaultdict(set)
        #Every cost-weight of an edge is saved in a dictionary
        # {key:value} with key as a pair-tuple (nodei,nodej) and as
        # value the cost of the edge nodei-nodej
        self.distances = {}

    def __str__(self):
        return '\nThe Nodes of the Graph are: ' + str(self.nodes) +
        '\n' + \
        '\nThe Edges of the Graph are: ' + str(self.edges.items()) +
        '\n' + \
        '\nThe Distances of the Graph are: ' + str(self.distances)
    
    def addnode(self, value):
        # A new node added to the set of nodes
        self.nodes.add(value)

    def addedge(self, from_node, to_node, distance):
        # To add an edge we add a neighbour to list of neighbours of 
        # the node:from_node to dictionary Graph.edges
        self.edges[from_node].add(to_node)
        self.edges[to_node].add(from_node) #For non-directed Graph

        # To add or change a cost of an edge we add or change the
        # value of the edge:(from_node,to_node) in the dictionary
        Graph.distances
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance #For nondirected Graph

    def Path(self,start,end): # Detects a path between two nodes

    if start == end: return 1 # If start is end...

    remaining_nodes = self.nodes.copy() # A set that we remove
    every node we have visited. Contains every node that we have not
    visited yet

    visited = set([start]) # Contains every node we have
    visited

    current_node = start # Starting from the start node

    while 1 :
    # Access every neighbour of the current node
    for neighbour in self.edges[current_node]:
    if neighbour in remaining_nodes: # If we have not
    visited it before
    visited.add(neighbour) # Add it to visited set

    # Remove the current node so we won't access it again
    in the future
    remaining_nodes.remove(current_node)
    # if we access all nodes that we could access
    if not remaining_nodes&visited: break
    # Access randomly a node from the set of nodes we have
    not access yet
    # and they are neighbours of previous nodes we accessed
    before
    current_node =
    random.sample(visited&remaining_nodes,1)[0]

    if current_node == end: # If we access the end we stop
    return 1 # Return true

    return 0 # If we have visited all nodes that we could and
    we did not access the end return false
    - 62 -

    def Connected(self): # Check if the Graph is a Connected
    Graph
    strongconnection = 0
    random_node = random.sample(self.nodes,1)[0]
    for node in self.nodes:
    if self.Path(random_node,node) and
    self.Path(node,random_node):
    strongconnection = strongconnection + 1
    if not(self.Path(random_node,node) or
    self.Path(node,random_node)):
    return 'The graph is not connected. Two nodes that
    are not connected are:'+str(random_node)+' '+str(node)
    # If the connections between all nodes are |V| means that
    every node is connected to all other nodes
    if strongconnection == len(self.nodes):
    return 'The Graph is strongly connected'
    else: return 'The Graph is weakly connected'
