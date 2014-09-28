import math
from numpy.core.records import record
import random

__author__ = 'pok'


class MutliTagging():
    def __init__(self):
        pass

    def datareader(self, path):
        """
        This function mainly reads the arff file into memory.
            Param:
                path->file path
            Return:
                res->the list of records.
        """

        f = open(path, 'r')
        data = f.read()
        data = data.split('\n')
        data_tmp = []
        for idx in range(len(data)):
            if str(data[idx]).find('@data') >= 0:
                data_tmp = data[idx + 1:]
                break
        res = []
        for record in data_tmp:
            record = record.split(',')
            record = map(float, record)
            res.append(record)
        return res

    def bigraph(self, data, tag_index):
        """
        This function mainly transpose the list data to bigraph.
            Param:
                data->the list of data
                tag_index->the index of the first in record's attribute
            return:
                graph->the bigraph
        """

        graph = []
        for idx in range(len(data)):
            record = data[idx]
            record = record[tag_index:]
            tag_count = sum(record)
            for tag_idx in range(len(record)):
                if record[tag_idx] != 0:
                    graph.append((idx, len(data) + tag_idx, 1.0 / tag_count))
        return graph

    def bgll(self, graph, node_count, min_mod, max_pass):
        """
        This function mainly detects the community of the graph.
            Param:
                graph->the graph for detecting
                node_count->the number of the node
                min_mod->the min threshold of the di-modularity
                max_pass->the max pass of the algorithm run
            Return:
                comm->the belonging of the record
        """

        #the belonging of the node
        bl = [i for i in range(node_count)]
        #the node's weight in community
        _in = [0.0] * node_count
        #the node's weight in graph
        _tot = []
        #total weight of a node, just a copy of _tot
        k = []
        #the total weight of the graph
        m = []

        #inital the in-param
        network = [[0.0] * node_count for n in range(node_count)]
        for node, tag, weight in graph:
            network[node][tag] = weight
        for node in network:
            k.append(sum(node))
        _tot = k[:]
        m = sum(k)
        #inital the in-param

        def modularity():
            """
            This function mainly computes the modularity of the network
                Return:
                    mod->the modularity value
            """

            q = 0.0
            for idx in range(0, node_count):
                if _tot[idx] > 0.0:
                    q += (_in[idx] / m - math.pow(_tot[idx] / m, 2))
            return q

        def modularity_gain(n, c, dnodecomm):
            """
            This function mainly computes the modularity gain of a node moving
                Param:
                    n->node id
                    c->community id
                    dnodecomm->the weight between the node and the community
                Return:
                    gain->modularity gain
            """

            totc = _tot[c]
            degc = k[n]
            return dnodecomm - (totc * degc) / m

        def neigh_comm(n):
            """
            This function mainly computes the weight between the node and it's neighbour community
                Param:
                    n->node id
                Return:
                    nc->the map of the weight between the node and it's neighbour community
                        nc=>{cid,weight}
            """

            nc = {bl[n]: 0.0}
            for idx in range(0, node_count):
                neigh = idx
                ncomm = bl[neigh]
                nei_weight = network[n][idx]
                if (neigh != n) & (nei_weight > 0.0):
                    if ncomm in nc:
                        nc[ncomm] += nei_weight
                    else:
                        nc[ncomm] = nei_weight
            return nc

        def insert(n, c, dnodecomm):
            """
            This function mainly get the effect of insert the node into community
                Param:
                    n->node id
                    c->community id
                    dnodecomm->the weight between the node and the community
            """

            _tot[c] += k[n]
            _in[c] += 2 * dnodecomm + network[n][n]
            bl[n] = c

        def remove(n, c, dnodecomm):
            """
            This function mainly get the effect of remove the node off community
                Param:
                    n->node id
                    c->community id
                    dnodecomm->the weight between the node and the community
            """

            _tot[c] -= k[n]
            _in[c] -= 2 * dnodecomm + network[n][n]
            bl[n] = -1

        def detect():
            """
            This function mainly detect the community of the graph.
            """

            _pass_done = 0
            _improve = True
            new_mod = modularity()
            cur_mod = -999999999.0
            rl = random.sample(range(0, node_count), node_count)
            while _improve & (_pass_done < max_pass) & (new_mod - cur_mod > min_mod):
                cur_mod = new_mod
                _improve = False
                _pass_done += 1
                for node_tmp in rl:
                    n = node_tmp
                    nc = bl[n]
                    ncomm = neigh_comm(n)
                    remove(n, nc, ncomm[nc])
                    best_c = nc
                    best_l = 0.0
                    best_incre = 0.0
                    for c in ncomm:
                        incre = modularity_gain(n, c, ncomm[c])
                        if incre > best_incre:
                            best_incre = incre
                            best_c = c
                            best_l = ncomm[c]
                    insert(n, best_c, best_l)
                    if best_c != nc:
                        _improve = True
                new_mod = modularity()
            print new_mod

        detect()
        return bl


def test():
    m = MutliTagging()
    data = m.datareader('/home/pok/PycharmProjects/Mutlitagging/data/Corel5k-train.arff')
    graph = m.bigraph(data, -374)
    bl = m.bgll(graph, len(data) + 374, 0.0001, 20)
    blm = {}
    for i in range(len(bl)):
        if bl[i] in blm:
            tmp = blm[bl[i]]
            tmp.append(i)
            blm[bl[i]] = tmp
        else:
            blm[bl[i]] = [i]
    for i in blm:
        print blm[i]
    print len(blm)

if __name__ == '__main__':
    test()