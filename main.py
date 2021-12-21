# NYU 2021 AI Project 2 (Final) -- Constraint Satisfaction Problems: Map Coloring
#  by: Kora S. Hughes & Jorge A. Velasquez

import fileinput
import os
import copy

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

    # def num_unassigned_n():
    #     for node in self.adj

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
                    if self.adjacency[i][j] == 1 and self.map[self.order[i]] == self.map[self.order[j]]:
                        return False
        return True

    def valid_adjacent_reigons(self):
        """ returns false if adjacent reigon has no options """
        for reigon, color in self.map.items():
            color_lst = []
            i = self.order.index(reigon)  # adj index of this reigon
            for adj_reigon in self.adjacency[i]:
                if self.map[adj_reigon] != "":  # if adjacent reigon has color we save it
                    color_lst.append(self.map[adj_reigon])
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
            n1.color_options = self.colors[self.order[i]];
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

def num_unassigned_n(node, map):
    ret_val = 0;
    for n_node in node.adj:
        if map.map[n_node].new_color == "":
            ret_val += 1;
    return ret_val;

# Params: node_list
# node
def get_node(node_list, map):
    curr_min_node = [];
    curr_min_moves = 0;
    # minumum remaining value heuristic
    for node in node_list:
        if node.color != "":
            legal_moves = len(node.color_options);
            if legal_moves == curr_min_moves:
                curr_min_node.append(node);
            elif legal_moves < curr_min_moves:
                curr_min_node.clear();
                curr_min_moves = legal_moves;
                curr_min_node.append(node);
    # degree heuristic
    if len(curr_min_node) == 0:
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
        # node_result = False;
        # # needs
        # while (not node_result):
        #     curr_node = get_node();
        #     node_result = back_track(curr_node);
        curr_node = get_node(map.export_nodes);
        for color in curr_node.color:
            new_map = map.deepcopy()
            new_map.map[curr_node.name] = color;
            result = back_track(new_map);
            if result[0]:
                return result;

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

        # the actual calculations
        # TODO: compute answer here
        new_map = back_track(new_map);

        if new_map[0] != True:
            print("Solution not found");
        else:
            # write/show output
            f = open("Outputs/output"+str(file_i+1)+".txt", "w")  # create file if it doesnt exist
            f.write(str(new_map))
            f.close()
        
    print("\n...end")