from dataset_property import NAME, DATASET_SIZE
NUM_NODES_SUB = 100
import pdb

def node_attr_classifier(d):
    if d < 100:
        return int(d/5)
    else:
        return 20


def is_in_subgraph(number):
    if (number < 0):
        return False
    if (number < NUM_NODES_SUB):
        return True
    else:
        return False

def match_from_sub_to_whole(sub_index):
    if (sub_index < NUM_NODES_SUB):
        return sub_index
    else:
        raise ValueError("This node is not in the subgraph")

def match_from_whole_to_sub(whole_index):
    if not is_in_subgraph(whole_index):
        raise ValueError("This node is not in the subgraph")
    return whole_index

if __name__ == '__main__':
    graph_file_open = open("./" + NAME + "-original/out.soc-sign-bitcoinalpha", 'r')
    edge_file = open("./" + NAME + "/edge.txt", 'w')
    node_attr_file = open("./" + NAME + "/node_attr.txt", 'w')
    node_degree_count = {node: 0 for node in range(DATASET_SIZE)}
    for line in graph_file_open.readlines():
        items = line.strip().split('\t')
        node1 = int(items[0])
        node2 = int(items[1])
        attr = int(items[2])
        node_degree_count[node1 - 1] += 1
        node_degree_count[node2 - 1] += 1
        edge_file.write(str(node1 - 1) + ',' + str(node2 - 1) + ',' + str(attr - 1) + '\n')
    edge_file.close()
    for i in range(DATASET_SIZE):
        node_attr_file.write(str(i) + ',' + str(node_attr_classifier(node_degree_count[i])) + '\n')
    node_attr_file.close()

    new_edge_file = open("./" + NAME + "/edge.txt", 'r')
    new_node_attr_file = open("./" + NAME + "/node_attr.txt", 'r')
    sub_edge_file = open("./" + NAME + "/edge_sub.txt", 'w')
    sub_node_attr_file = open("./" + NAME + "/node_attr_sub.txt", 'w')
    for line in new_node_attr_file.readlines():
        items = line.strip().split(',')
        node = int(items[0])
        attr = int(items[1])
        if is_in_subgraph(node):
            sub_node_attr_file.write(str(match_from_whole_to_sub(node)) + ',' + str(attr) + '\n')
    new_node_attr_file.close()
    sub_node_attr_file.close()

    for line in new_edge_file.readlines():
        items = line.strip().split(',')
        node1 = int(items[0])
        node2 = int(items[1])
        attr = int(items[2])
        if (is_in_subgraph(node1) and is_in_subgraph(node2)):
            sub_edge_file.write(str(match_from_whole_to_sub(node1)) + ',' + str(match_from_whole_to_sub(node2)) + ',' + str(attr) + '\n')
    new_edge_file.close()
    sub_edge_file.close()

    ground_truth_file = open("./" + NAME + "/ground_truth.txt", 'w')
    for i in range(NUM_NODES_SUB):
        ground_truth_file.write(str(match_from_sub_to_whole(i)) + ',' + str(i) + '\n')
    ground_truth_file.close()
