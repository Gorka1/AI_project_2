# NYU 2021 AI Project 2 (Final) -- Constraint Satisfaction Problems: Map Coloring
#  by: Kora S. Hughes & Jorge A. Velasquez

import fileinput
import os
import copy
import math

# Backtracking Algorithm for CSPs

class Node:
    def __init__(self, new_name, new_color):
        self.name = new_name
        self.adj = []
        self.color = new_color
        self.color_options = ""     # treat this as list

    def __str__(self):
        out = self.name
        out += ": " + self.color
        out += ", " + str(self.adj)
        return out

    def is_valid(self):
        return self.color in self.color_options

    def __repr__(self) -> str:
        return str(self);

# Note: regions = variables & colors = constraints
class ColorMap:
    def __init__(self, constraints, adjacency, order):
        """ init map information:
        constraints = dict of key=reigon, value=possible colors
        adjacent list = nested binary list of reigon adjacency in order
        order = ordered list of reigons to read adjacency map"""
        # keys: region name, value: color
        self.map = {key: "" for key, value in constraints.items()}
        # empty string as value is easy to check later on (default/unassigned state)
        self.colors = constraints.copy()  # list of chars
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
                    if self.adjacency[i][j] == 1 and self.map[self.order[i]] == self.map[self.order[j]]:
                        return False
        return True

    def valid_adjacent_reigons(self):
        """ returns false if adjacent reigon has no options """
        for reigon, color in self.map.items():
            color_lst = []
            i = self.order.index(reigon)  # adj index of this reigon
            j = 0  # index of subreigon
            for adj_reigon in self.adjacency[i]:
                if adj_reigon == "1" and self.map[self.order[j]] != "":  # if adjacent reigon has color we save it
                    color_lst.append(self.map[self.order[j]])
                j += 1
            color_count = 0
            for temp_color in color_lst:  # for each adjacent color
                if temp_color in self.colors[reigon]:  # if color is in constrains we inc
                    color_count += 1
            # if adj colors in constraints >= num constraints there are no moves
            if color_count >= len(self.colors[reigon]):
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
            n1.color_options = self.colors[self.order[i]]
            for j in range(len(self.order)):
                if (self.adjacency[i][j] == "1"):
                    n1.adj.append(self.order[j])
            node_lst.append(n1)
        return node_lst

    def import_node(self, n1):
        self.map[n1.name] = n1.color

    def import_node_lst(self, lst):
        for n1 in lst:
            assert type(n1) == Node
            self.import_node(n1)

def num_unassigned_n(node, map):
    ret_val = 0;
    for n_node in node.adj:
        if map.map[n_node] == "":
            ret_val += 1;
    return ret_val;

# Params: node_list
# node
def get_node(node_list, map):
    curr_min_node = [];
    curr_min_moves = math.inf;
    # minumum remaining value heuristic
    for node in node_list:
        if node.color == "":
            legal_moves = len(node.color_options);
            if legal_moves == curr_min_moves:
                curr_min_node.append(node);
            elif legal_moves < curr_min_moves:
                curr_min_node.clear();
                curr_min_moves = legal_moves;
                curr_min_node.append(node);

    if len(curr_min_node) == 0:
        return None;
    # degree heuristic
    if len(curr_min_node) == 1:
        return curr_min_node[0];
    else:
        curr_ret_node = curr_min_node[0];
        for node in curr_min_node:
            curr_value = num_unassigned_n(node, map);
            if curr_value < num_unassigned_n(curr_ret_node, map):
                curr_ret_node = node;
        return curr_ret_node;

# Returns a tuple (was an answer found, the answer found)
def back_track(map):
    if map.is_valid():
        return (True, map);
    elif not map.valid_adjacent_reigons():
        return (False, map);
    else:
        # getting the next node according to heuristics
        curr_node = get_node(map.export_nodes(), map);
        # if getting the node somehow failed, something bad happened, chances are this map isn't even good in the first place
        if curr_node == None:
            return (False, map);
        # looping through the possible options of the current node
        for color in curr_node.color_options:
            new_map = copy.deepcopy(map);
            new_map.map[curr_node.name] = color;
            result = back_track(new_map);
            if result[0]:
                return result;
    return (False, map);

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

        # testing prints
        # new_map.show_adj_map()
        # for temp_node in new_map.export_nodes():
        #     print("Node:", str(temp_node))
        # print(str(new_map))
        print("Start map nodes: ", new_map.export_nodes())

        # the actual calculations
        # TODO: compute answer here
        new_map_tuple = back_track(new_map);

        print("Final map nodes: ", new_map_tuple[1].export_nodes())

        if new_map_tuple[0] != True:
            print("Solution not found");
        else:
            # write/show output
            f = open("Outputs/output"+str(file_i+1)+".txt", "w")  # create file if it doesnt exist
            f.write(str(new_map_tuple[0]))
            f.close()
        
    print("\n...end")