from geist.tools.utils import update_outputroot, ensure_dir_exists, map_df, df2nt
from geist.tools.filters import csv2df, escape_quotes
import click, pickle, json, os, ast
from jinja2 import Environment
from io import StringIO
import pandas as pd
import pygraphviz as pgv
from rdflib import Graph
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics, RDFS_OWLRL_Semantics
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer

DATA_DIR = ".geistdata/rdflib/"
PASTEL_COLORS = ["#b3e2cd", "#fdccac", "#cbd5e8", "#f4cae4", "#e6f5c9", "#fff2ae", "#f1e2cc", "#cccccc"]

@click.group()
def cli():
    pass

@cli.group()
def rdflib():
    pass

def infer_rdf_graph(rdf_graph, infer):
    if infer == "rdfs":
        # RDFS_Semantics: implementing the RDFS semantics
        DeductiveClosure(RDFS_Semantics).expand(rdf_graph)
    elif infer == "owl":
        # OWLRL_Semantics: implementing the OWL 2 RL
        DeductiveClosure(OWLRL_Semantics).expand(rdf_graph)
    elif infer == "rdfs_owl":
        # RDFS_OWLRL_Semantics: implementing a combined semantics of RDFS semantics and OWL 2 RL
        DeductiveClosure(RDFS_OWLRL_Semantics).expand(rdf_graph)
    return rdf_graph

def create_rdf_graph(input_file, input_format, colnames_of_triples, infer):
    """
    This function is to load a file with a given format as a RDF Graph object supported by RDFLib
    :param input_file: String. Path of the file
    :param input_format: Defaults to json-ld. It must be one of [xml, n3, turtle, nt, pretty-xml, trix, trig, nquads, json-ld, hext, csv]
    :param infer: Inference to perform on update [none, rdfs, owl, rdfs_owl] (default "none")
    :return rdf_graph: a RDF Graph object supported by RDFLib
    """
    if input_format not in ["xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig", "nquads", "json-ld", "hext", "csv"]:
        raise ValueError("Only supports [xml, n3, turtle, nt, pretty-xml, trix, trig, nquads, json-ld, hext, csv], but '" + str(input_format) + "' was given.")
    if infer not in ["none", "rdfs", "owl", "rdfs_owl"]:
        raise ValueError("Only [none, rdfs, owl, rdfs_owl] are supported.")
    # Parse the file (e.g., a JSON-LD file) with RDFLib
    rdf_graph = Graph()
    if input_format == "csv":
        if not colnames_of_triples:
            raise ValueError("Please provide the column names of triples for the CSV file.")
        nt = df2nt(csv2df(input_file), ast.literal_eval(colnames_of_triples))
        rdf_graph.parse(data=nt, format="nt")
    else:
        rdf_graph.parse(data=input_file, format=input_format)
    rdf_graph = infer_rdf_graph(rdf_graph, infer)
    return rdf_graph

def load_rdf_dataset(dataset):
    data_path = DATA_DIR + dataset + ".pkl"
    if not os.path.isfile(data_path):
        raise ValueError("Please create the RDF dataset ({dataset}) before loading it. Run `geist create rdflib --help` for detailed information".format(dataset=dataset))
    with open(data_path, mode='rb') as f:
        geist_graph_object = pickle.load(f)
    rdf_graph, infer = geist_graph_object["rdf_graph"], geist_graph_object["infer"]
    return rdf_graph, infer

def query2df(rdf_graph, query):
    """
    This function is to run query on a RDF graph
    :param rdf_graph: a RDF Graph object supported by RDFLib
    :param query: string. A query to be applied to the given RDF graph
    :return res: a Pandas data frame. Results of the query
    """
    file = StringIO()
    JSONResultSerializer(rdf_graph.query(query)).serialize(file)
    res_json = json.loads(file.getvalue())
    bindings = res_json["results"]["bindings"]
    colnames = res_json["head"]["vars"]
    if bindings:
        # type: uri, literal, or bnode
        res_df = pd.DataFrame(bindings).apply(lambda row: row.apply(lambda x: "<"+x["value"]+">" if x["type"] == "uri" else x["value"] if x["type"] == "literal" else "_:"+x["value"]), axis=1)
    else:
        res_df = pd.DataFrame(columns=colnames)
    return res_df[colnames]

def visualize_query_results(query_res, edges, rankdir="TB", same_color=False):
    """
    This function is to visualize query results with pygraphviz
    :param query_res: a Pandas data frame.
    :param edges: a list of list. [[start_node1, end_node1, label1], [start_node2, end_node2, label2], ...] where these items are column names
    :param same_color: a bool value to denote if all edges are filled with the same color (default: False)
    :return g: a Graphviz graph
    """
    # Create a directed graph
    G = pgv.AGraph(directed=True, rankdir=rankdir)
    # Add nodes and edges
    for _, row in query_res.iterrows():
        for idx, edge in enumerate(edges):
            if same_color:
                color = PASTEL_COLORS[0]
            else:
                color = PASTEL_COLORS[idx % 8]
            G.add_node(row[edge[0]], shape="box", style="filled, rounded", fillcolor=color)
            G.add_node(row[edge[1]], shape="box", style="filled, rounded", fillcolor=color)
            G.add_edge(row[edge[0]], row[edge[1]], label=row[edge[2]])
    return G

def visualize_query_results_without_pygraphviz(query_res, edges, rankdir="TB", same_color=False, **kwargs):
    """
    This function is to visualize query results without using pygraphviz
    :param query_res: a Pandas data frame.
    :param edges: a list of list. [[start_node1, end_node1, label1], [start_node2, end_node2, label2], ...] where these items are column names
    :param kwargs: a dict. Parameters for Graphviz
    :return g: a string of Graphviz DOT language
    """

    graph2_env = Environment()
    graph2_env.globals['enumerate'] = enumerate
    graph2_env.filters['escape_quotes'] = escape_quotes
    gv = graph2_env.from_string("""
        {% set ns = namespace(params=params, query_res=query_res, edges=edges, same_color=same_color, pastel_colors=pastel_colors) %}
                graph [rankdir={{ rankdir }}{% for param_k, param_v in ns.params.items() %}, {{ param_k }}={{ param_v }}{% endfor %}];
                node[shape=box style="filled, rounded" peripheries=1 fontname=Courier];
        {% for _, row in ns.query_res.iterrows() -%}
            {% for idx, edge in enumerate(ns.edges) -%}
                {% set color = ns.pastel_colors[0] if ns.same_color else ns.pastel_colors[idx % 8] %}
                {{ row[edge[0]] | escape_quotes }} [fillcolor="{{ color }}"];
                {{ row[edge[1]] | escape_quotes }} [fillcolor="{{ color }}"];
                {{ row[edge[0]] | escape_quotes }} -> {{ row[edge[1]] | escape_quotes }} [label={{ row[edge[2]] | escape_quotes }} fontname=Courier]; 
            {% endfor%}
        {% endfor %}
        """).render(rankdir=rankdir,
                    params=kwargs,
                    query_res=query_res,
                    edges=edges,
                    same_color=same_color,
                    pastel_colors=PASTEL_COLORS)
    return 'digraph "" {' + gv + '}'

def _graph(rdf_graph, rankdir, mappings, on, same_color):
    """Convert a RDF graph object to a Graphviz graph object"""
    query = """
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        """
    res = query2df(rdf_graph, query)
    res = map_df(res, mappings, on)
    G = visualize_query_results(query_res=res, edges=[['s', 'o', 'p']], rankdir=rankdir, same_color=same_color)
    return G

def _graph2(rdf_graph, rankdir, mappings, on, **kwargs):
    """Convert a RDF graph object to a Graphviz graph object"""
    query = """
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        """
    res = query2df(rdf_graph, query)
    res = map_df(res, mappings, on)
    gv = visualize_query_results_without_pygraphviz(query_res=res, edges=[['s', 'o', 'p']], rankdir=rankdir, same_color=True, **kwargs)
    return gv

def rdflib_create(dataset, inputfile, inputformat, colnames, infer):
    """Create a new RDF dataset"""
    data_path = DATA_DIR + dataset + ".pkl"
    if os.path.isfile(data_path):
        raise ValueError("Please remove the existing RDF dataset ({dataset}) before loading the new one. Run `geist destroy --help` for detailed information".format(dataset=dataset))
    if inputformat == "csv" and (not colnames):
        raise ValueError("Please provide the column names of triples for the CSV file, i.e., --colnames")
    rdf_graph = create_rdf_graph(inputfile, inputformat, colnames, infer)
    # Save as a Gesit graph object
    geist_graph_object = {"rdf_graph": rdf_graph, "infer": infer}
    ensure_dir_exists(data_path, output=False)
    with open(data_path, "wb") as f:
        pickle.dump(geist_graph_object, f)
    return

def rdflib_load(dataset, inputfile, inputformat, colnames):
    """Import data into a RDF dataset"""
    if inputformat == "csv" and (not colnames):
        raise ValueError("Please provide the column names of triples for the CSV file, i.e., --colnames")
    (rdf_graph, infer) = load_rdf_dataset(dataset)
    rdf_graph = rdf_graph + create_rdf_graph(inputfile, inputformat, colnames, infer)
    geist_graph_object = {"rdf_graph": rdf_graph, "infer": infer}
    with open(DATA_DIR + dataset + ".pkl", "wb") as f:
        pickle.dump(geist_graph_object, f)
    return

def rdflib_destroy(**kwargs):
    """Delete an RDF dataset"""
    dataset = kwargs["dataset"] if "dataset" in kwargs else "kb"
    data_path = DATA_DIR + dataset + ".pkl"
    if not os.path.isfile(data_path):
        if "quiet" in kwargs and kwargs["quiet"]:
            return
        raise ValueError("Nothing to be removed. Can NOT find {data_path}".format(data_path=data_path))
    os.remove(data_path)
    return

def rdflib_export(dataset, outputroot, outputfile, outputformat):
    """Export an RDF dataset"""
    update_outputroot(outputroot)
    (rdf_graph, _) = load_rdf_dataset(dataset)
    if outputfile is None:
        print(rdf_graph.serialize(format=outputformat))
    else:
        outputfile = ensure_dir_exists(outputfile)
        rdf_graph.serialize(destination=outputfile, format=outputformat)
    return

def rdflib_query(dataset, file, outputroot, outputfile):
    """Perform a SPARQL query on a dataset"""
    update_outputroot(outputroot)
    (rdf_graph, _) = load_rdf_dataset(dataset)
    res = query2df(rdf_graph, file.read())
    if outputfile is None:
        print(res.to_markdown())
    else:
        outputfile = ensure_dir_exists(outputfile)
        res.to_csv(outputfile, index=False)

def rdflib_graph(dataset, rankdir, mappings, on, samecolor, outputroot, outputfile, outputformats):
    """Visualize a dataset"""
    update_outputroot(outputroot)

    # Load a RDF dataset
    (rdf_graph, _) = load_rdf_dataset(dataset)
    # Convert a RDF graph object to a Graphviz graph object
    G = _graph(rdf_graph, rankdir, mappings, on, samecolor)

    # Save the graph
    outputfile = ensure_dir_exists(outputfile)
    for outputformat in set(outputformats):
        if outputformat == 'none':
            print(G.string())
        else:
            output_path = outputfile + '.' + outputformat
            if outputformat == 'gv' or outputformat == 'dot':
                G.write(output_path)
            else: # svg, png
                G.draw(output_path, prog='dot')



if __name__ == '__main__':
    cli()
