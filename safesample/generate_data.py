import networkx as nx
import sys
import sqlparse
import random
from argparse import ArgumentParser

def getPrettySQL(sql):
    return sqlparse.format(sql,  reindent=True, keyword_case='upper')


def generateSQL(unary, binary, names, output_file, unary_dist=None, binary_dist=None):
    """
    Given the necessary information about relationships, generates SQL database useable by our open world implementation

    Args:
        unary: ([[Node]]) A list of lists of node_indexes, each inner list represents 1 unary relation
        binary: ([Graph]) A list of graphs, each graph represents 1 binary relation (an edge between 2 nodes means it will have an entry)
        names: ([string]) A list of strings each representing the name of a relation to be used (unary, then binary)
        output_file: target file to write to
        unary_dist: function -> [0,1] Probabilities for unary relations drawn from here. Default is Uniform(0.9,1)
        binary_dist: function -> [0,1] Probabilities for binary relations draw from here. Default is Uniform(0.9,1)
    """

    # Make sure we didn't mess anything up
    assert (len(unary) + len(binary)) == len(names)

    sql = ''
    # generate drop statements
    for name in names:
        sql += "drop table if exists %s;\n" % name

    # Create unary tables
    for name in names[:len(unary)]:
        sql += "create table %s (\n\tid\tserial,\n\tv0\tinteger,\n\tp\tdouble precision\n);\n" % name

    # Create binary tables
    for name in names[len(unary):]:
        sql += "create table %s (\n\tid\tserial,\n\tv0\tinteger,\n\tv1\tinteger,\n\tp\tdouble precision\n);\n" % name

    # Insert into unary tables

    # First need to decide on our distribution, if it was not provided
    if unary_dist is None:
        unary_dist = lambda: random.uniform(0.8, 1)

    # Now, we do the insertion randomly generating probabilities as we go
    for name, rel in zip(names[:len(unary)], unary):
        sql += 'INSERT INTO %s (v0, p) VALUES\n' % name
        sql += ',\n'.join(["(%d, %f)" % (x, unary_dist()) for x in rel]) + '\n;\n'

    # Insert into binary tables

    # Again, need to decide on our distribution
    if binary_dist is None:
        binary_dist = lambda: random.uniform(0.8, 1)

    # Now, we do the insertion randomly generating probabilities as we go
    for name, rel in zip(names[len(unary):], binary):
        sql += 'INSERT INTO %s (v0, v1, p) VALUES\n' % name
        # Bidirectional edges always exist, but can have different probablities
        sql += ',\n'.join(["(%d, %d, %f),\n(%d, %d, %f)" % (e1, e2, binary_dist(), e2, e1, binary_dist()) for e1, e2 in rel.edges()]) + '\n;\n'

    with open(output_file, 'w') as f:
        # s = getPrettySQL(sql)
        f.write(sql)


def generateUnaryRel(graph, dist=None):
    """
    Generates a unary relation from our graph by first sampling a value from dist (must return a number between 1 and N, where N is the number of nodes in the graph), and then sampling that many nodes from the graph with replacement
    Args:
        graph: nx.Graph we want to sample from
        dist: Distribution to sample number of entries from (default is uniform(1,n))
    Returns:
        [Node] representing the variables that will be included in this relation
    """
    if dist is None:
        dist = lambda: random.randint(1, len(graph.nodes()))

    count = dist()
    return random.sample(graph.nodes(), count)

def parse_args(args):
    parser = ArgumentParser("Randomly generate a probabilistic SQL database based on power law graphs")
    parser.add_argument('domain', metavar='N', type=int)
    parser.add_argument('num_unary', metavar='NUM_UNARY', type=int)
    parser.add_argument('num_binary', metavar='NUM_BINARY', type=int)
    parser.add_argument('output_file', metavar='OUT')
    return parser.parse_args(args)

def main(domain, num_unary, num_binary, output_file):
    assert num_unary + num_binary <= 10
    names = 'PQRSTUVXYZ'[:(num_unary + num_binary)]
    empty_graph = nx.empty_graph(domain)

    unary_rels = []
    binary_rels = []

    for i in range(num_unary):
        unary_rels.append(generateUnaryRel(empty_graph))
    for i in range(num_binary):
        binary_rels.append(nx.powerlaw_cluster_graph(domain, domain/4, 0.2))

    generateSQL(unary_rels, binary_rels, names, output_file)

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    sys.exit(main(**vars(args)))
    
