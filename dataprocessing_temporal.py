from dataset_property import DATASET_SIZE, LEFT_SIZE, RIGHT_SIZE
NUM_NODES_SUB = 90
COUNT_ONE = LEFT_SIZE
RATIO = 2/3
INITIAL_RATIO = 0.9
import pdb

def node_attr_classifier_left(d):
    if d < 500:
        return int(d/5)
    elif d < 1000:
        return 100 + int((d-500)/10)
    else:
        return 150

def node_attr_classifier_right(d):
    return 151 + node_attr_classifier_left(d)

def is_in_subgraph(number):
    if (number < 0):
        return False
    if (number < NUM_NODES_SUB*RATIO):
        return True
    elif (number < LEFT_SIZE):
        return False
    elif (number < LEFT_SIZE + NUM_NODES_SUB*(1-RATIO)):
        return True
    else:
        return False

def match_from_sub_to_whole(sub_index):
    if (sub_index < NUM_NODES_SUB*RATIO):
        return sub_index
    elif (sub_index < NUM_NODES_SUB):
        return int(sub_index - NUM_NODES_SUB*RATIO + LEFT_SIZE)

def match_from_whole_to_sub(whole_index):
    if not is_in_subgraph(whole_index):
        raise ValueError("This node is not in the subgraph")
    if (whole_index < NUM_NODES_SUB*RATIO):
        return whole_index
    elif (whole_index < LEFT_SIZE + NUM_NODES_SUB*(1-RATIO)):
        return int(whole_index - LEFT_SIZE + NUM_NODES_SUB*RATIO)


if __name__ == '__main__':
    graph_file_open = open("./movielens-1m-original/out.movielens-1m", 'r')
    node_attr_file = open("./movielens-1m-temporal/node_attr.txt", 'w')
    edge_file = open("./movielens-1m-temporal/edge.txt", 'w')
    node_degree_count_left = {node: 0 for node in range(LEFT_SIZE)}
    node_degree_count_right = {node: 0 for node in range(RIGHT_SIZE)}
    all_possible_timestamp_set = set()

    for line in graph_file_open.readlines():
        items = line.strip().split(' ')
        node1 = int(items[0])
        node2 = int(items[1])
        attr = int(items[2])
        time = int(items[3])
        all_possible_timestamp_set.add(int(time))
        node_degree_count_left[node1 - 1] += 1
        node_degree_count_right[node2 - 1] += 1
        edge_file.write(str(node1 - 1) + ',' + str(node2 + LEFT_SIZE - 1) + ',' + str(attr - 1) + ',' + str(time) + '\n')
    for i in range(LEFT_SIZE):
        node_attr_file.write(str(i) + ',' + str(node_attr_classifier_left(node_degree_count_left[i])) + '\n')
    for j in range(RIGHT_SIZE):
        node_attr_file.write(str(j + LEFT_SIZE) + ',' + str(node_attr_classifier_right(node_degree_count_right[j])) + '\n')
    edge_file.close()
    node_attr_file.close()
    graph_file_open.close()


    new_node_attr_file = open("./movielens-1m-temporal/node_attr.txt", 'r')
    sub_node_attr_file = open("./movielens-1m-temporal/node_attr_sub.txt", 'w')
    for line in new_node_attr_file.readlines():
        items = line.strip().split(',')
        node = int(items[0])
        attr = int(items[1])
        if is_in_subgraph(node):
            sub_node_attr_file.write(str(match_from_whole_to_sub(node)) + ',' + str(attr) + '\n')
    new_node_attr_file.close()
    sub_node_attr_file.close()


    all_possible_timestamp_list = []
    for item in all_possible_timestamp_set:
        all_possible_timestamp_list.append(item)
    all_possible_timestamp_list.sort()

    timestamp_to_line_counter = {timestamp: [] for timestamp in all_possible_timestamp_list}
    graph_file_open = open("./movielens-1m-temporal/edge.txt", 'r')
    all_lines = graph_file_open.readlines()
    line_counter = 0
    for line in all_lines:
        items = line.strip().split(',')
        time = int(items[3])
        timestamp_to_line_counter[time].append(line_counter)
        line_counter += 1
    graph_file_open.close()

    temporal_edge_file = open("movielens-1m-temporal/edge_sorted.txt", 'w')
    for timestamp in all_possible_timestamp_list:
        for line_counter in timestamp_to_line_counter[timestamp]:
            temporal_edge_file.write(all_lines[line_counter])
    temporal_edge_file.close()
    
    temporal_edge_file = open("movielens-1m-temporal/edge_sorted.txt", 'r')
    temporal_edge_file_sub = open("movielens-1m-temporal/edge_sorted_sub.txt", 'w')
    temporal_edge_file_initial = open("movielens-1m-temporal/edge_sorted_initial.txt", 'w')
    temporal_edge_file_initial_sub = open("movielens-1m-temporal/edge_sorted_initial_sub.txt", 'w')
    temporal_lines = temporal_edge_file.readlines()

    for line in temporal_lines:
        items = line.strip().split(',')
        node1 = int(items[0])
        node2 = int(items[1])
        attr = int(items[2])
        time = int(items[3]) 
        if (is_in_subgraph(node1) and is_in_subgraph(node2)):
            temporal_edge_file_sub.write(str(match_from_whole_to_sub(node1)) + ',' + str(match_from_whole_to_sub(node2)) + ',' + str(attr) + ',' + str(time) + '\n')

    upper = int(INITIAL_RATIO * len(temporal_lines))
    for i in range(upper):
        temporal_edge_file_initial.write(temporal_lines[i])
        items = temporal_lines[i].strip().split(',')
        node1 = int(items[0])
        node2 = int(items[1])
        attr = int(items[2])
        time = int(items[3])
        if (is_in_subgraph(node1) and is_in_subgraph(node2)):
            temporal_edge_file_initial_sub.write(str(match_from_whole_to_sub(node1)) + ',' + str(match_from_whole_to_sub(node2)) + ',' + str(attr) + ',' + str(time) + '\n')

    temporal_edge_file.close()
    temporal_edge_file_sub.close()
    temporal_edge_file_initial.close()
    temporal_edge_file_initial_sub.close()

    ground_truth_file = open("./movielens-1m-temporal/ground_truth.txt", 'w')
    for i in range(NUM_NODES_SUB):
        ground_truth_file.write(str(match_from_sub_to_whole(i)) + ',' + str(i) + '\n')
    ground_truth_file.close()