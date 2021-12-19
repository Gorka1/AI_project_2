# NYU 2021 AI Project 2 (Final) -- Constraint Satisfaction Problems: Map Coloring
#  by: Kora S. Hughes & Jorge A. Velasquez

import fileinput
import os

# Backtracking Algorithm for CSPs

class Node:
    def __init__(self, new_name, new_color):
        self.name = new_name
        self.adj = []
        self.color = new_color
# Note: regions = variables & colors = constraints
class ColorMap:
    def __init__(self, constraints, adjacency, order):
        """ init map information:
        constraints = dict of key=reigon, value=possible colors
        adjacent list = nested binary list of reigon adjacency in order
        order = ordered list of reigons to read adjacency map"""
        self.map = {key: "" for key, value in constraints.items()}
        # empty string as value is easy to check later on (default/unassigned state)
        self.colors = constraints.copy()
        self.adjacency = adjacency  # nested list of adjacent things
        self.order = order  # order of reigons
        # Note: constraint dict is (key, value) : (region, list of potential values)
    
    def __str__(self):  # output function
        out = "*Map:"
        for region, color in self.map.items():
            out += "\n" + str(region) + " = " + str(color)
        return out
            
    def is_complete(self):
        """ checks if map is completely filled out """
        for region, color in self.map.items():
            if color == "":
                return False
        return True
    
    def is_valid(self):
        """ checks if a map is *correctly* filled out """
        if not self.is_complete():  # are all reigons filled with a color?
            return False
        else:
            # are all regions assigned a correct color based on constraints?
            for region, color in self.map.items():
                if color not in self.colors[region]:
                    return False
            # are all adjacent reigons different colors?
            for i in range(len(self.order)):
                for j in range(len(self.order)):
                    if self.adjacency[i][j] == 1 and \
                            self.map[self.order[i]] == self.map[self.order[j]]:
                        return False
        return True
    
    def is_adjecent(self, r1, r2):
        """ returns whether or not two reigons are adjacent """
#         assert r1 != r2
        i = self.order.index(r1)  # Note: will give value error if not found
        j = self.order.index(r2)
        return bool(int(self.adjacency[i+1, j]))
    
    def show_adj_map(self):
        """ prints formatted view of adjacency """
        max_spacing = 5
        print((" "*(max_spacing-2)), "  ".join(self.order))
        for i in range(len(self.adjacency)):
            spacing = " "*(max_spacing - len(self.order[i]))
            print(self.order[i] + spacing + "   ".join(self.adjacency[i]))

    def export_nodes(self):
        node_lst = []
        for i in range(len(self.order)):
            n1 = Node(self.order[i], self.map[self.order[i]])
            for j in range(len(self.order)):
                if (self.adjacency[i][j] == 1):
                    n1.adj.append(self.order[i])
            node_lst.append(n1)
        return node_lst


def SUV(): # SELECT-UNASSIGNED-VARIABLE
    ...
    
def ODV(): # ORDER-DOMAIN-VALUES
    ...

def min_val():  # minumum remaining value heuristic
    """ takes in a map and constraints and returns a list of regions according to MRV """
    regions = []
    assert len(regions) > 0
    return regions
    
def degree(map, constraints):  # degree heuristic
    """ takes in a map and constraints and returns a list of regions according to Degree Heuristic """ #J: what do you mean by this comment???
    # 
    # lowest_degree_node = None;
    # for node in map.nodes:
    #     if (lowest_degree_node == None) or len(node.values) < lowest_degree_node;
    #     lowest_degree_node = node;
    regions = []
    return regions


if __name__ == '__main__':
    print("start...\n")
    
    input_files = os.listdir(os.getcwd() + "/Inputs")  # get all files in input dir
    for file_i in range(len(input_files)):  # run code on all files in directory
        line_num = 1  # keeping track of what input line maps to what value
        
        num_regions = -1  # used for error checking
        num_colors = -1
        
        temp_colors = {}
        temp_adjacency = []
        temp_order = []
        print("Computing file ", file_i, ":", input_files[file_i])
        for line in fileinput.FileInput(files = "Inputs/"+input_files[file_i]):  # parse input

            line = line.replace('\n', '').replace('\t', '').split(" ")  # formatting
            line = list(filter(lambda x: x != "", line))  # get rid of empty strings - potential spacing edge-case
            if line_num == 1:
                num_regions = int(line[0])
                num_colors = int(line[1])
            elif line_num == 2:  # save reigons (and their order)
                temp_order = line
            elif line_num == 3:  # save colors
                assert len(line) == num_colors
                for region in temp_order:  # assuming the potential values are homogenous among regions
                    temp_colors[region] = line  # fill colors
            else:
                if len(line) > 0:
                    temp_adjacency.append(line)
            line_num += 1
        assert num_regions != -1 and num_colors != -1  # testing
        assert len(temp_adjacency) == len(temp_adjacency[0]) == len(temp_order) == num_regions
        new_map = ColorMap(temp_colors, temp_adjacency, temp_order)
        new_map.show_adj_map()
        
        # the actual calculations
        # TODO: compute answer here

        # write/show output
        print(str(new_map))
#         f = open("Outputs/output"+str(file_i+1)+".txt", "w")  # create file if it doesnt exist
#         f.write(str(new_map))
#         f.close
        
    print("\n...end")