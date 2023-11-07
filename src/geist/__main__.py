#!/usr/bin/env python3

import click, jinja2, pickle, json, os, sys, ast, re
from jinja2_simple_tags import StandaloneTag, ContainerTag
from io import StringIO
import pandas as pd
import pygraphviz as pgv
from rdflib import Graph
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics, RDFS_OWLRL_Semantics
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer

DATA_DIR = ".geistdata/"
PASTEL_COLORS = ["#b3e2cd", "#fdccac", "#cbd5e8", "#f4cae4", "#e6f5c9", "#fff2ae", "#f1e2cc", "#cccccc"]
TAGS = ["use", "template", "create", "load", "query", "destroy", "graph", "graph2", "component", "map", "html", "img", "table", "include", "import", "macro", "block", "extends", "call", "filter", "set", "for", "if", "elif", "else"]

@click.group()
def cli():
    global outputroot
    outputroot = './'
    pass

def escape_quotes(txt):
    return txt.replace("'", "\'").replace('"', '\"')

def update_outputroot(dir):
    # Update the global variable outputroot
    if not dir.endswith('/'):
        dir = dir + '/'
    globals()["outputroot"] = dir
    return

def get_full_path(dir, file):
    # If file is an absolute path
    if file.startswith('~') or file.startswith('/'):
        path = file
    else: # Relative path
        path = dir + file
    return path

def ensure_dir_exists(file_path, output=True):
    """
    This function is to (1) get the full file path; and (2) ensure the directory of the given file path exists
    :param file_path: a string. An absolute file path or a relative file path
    :param output: a bool value to denote if the given file path is an output file path (default: True) or not (e.g., the path where we store the RDF dataset)
    :return file_path: a string. A full file path.
    """
    if output:
        file_path = get_full_path(outputroot, file_path)
    dir_path = os.path.split(file_path)[0]
    if (dir_path != '') and (not os.path.isdir(dir_path)):
        os.makedirs(dir_path)
    return file_path

def process_str_for_html(cell):
    """
    This function is to preprocess a string to be displayed within an HTML document
    :param cell: a string
    :return cell_prpcessed: a string
    """
    return cell.replace("<", "&lt").replace(">", "&gt")

def json2df(json_str):
    """
    This function is to convert a JSON string to a Pandas data frame
    :param json_str: a JSON string
    :return df: a Pandas data frame
    """
    return pd.read_json(StringIO(json_str))

def json2dict(json_str):
    """
    This function is to convert a JSON string to a dictionary
    :param json_str: a JSON string
    :return df: a dictionary
    """
    return json.loads(json_str)

def dict2df(dict):
    """
    This function is to convert a dictionary to a Pandas data frame
    :param json_str: a dictionary
    :return df: a Pandas data frame
    """
    return pd.DataFrame(dict)

def df2htmltable(df):
    """
    This function is to convert a Pandas data frame to an HTML table
    :param df: a Pandas data frame
    :return html_table: an HTML table
    """
    header = "".join("<th>{header}</th>".format(header=process_str_for_html(header)) for header in df.columns)
    content = ""
    for _, row in df.iterrows():
        content = content + "\n\t\t\t<tr>" + "".join("<td>{cell}</td>".format(cell=process_str_for_html(cell)) for cell in row.tolist())
    html_table = '''
        <table>
            <tr>{header}</tr>
        {content}
        </table>
    '''.format(header=header, content=content)
    return html_table

def map_df(df, mappings=None):
    """
    This function is to replace the original text in a Pandas data frame with the shorter ones based on the given mappings
    :param df: a Pandas data frame
    :param mappings: file of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text.
    :return df: a Pandas data frame
    """
    if mappings:
        with open(mappings, mode='r', encoding='utf-8') as fin:
            mappings = json.loads(fin.read())
        df = df.replace(mappings, regex=True)
    return df

def format_cell(cell):
    """
    This function is to format a cell in a Pandas data frame to a string of N-Triples
    :param cell: a cell in a Pandas data frame
    :return cell: a string of N-Triples
    """
    if cell.startswith("<") or cell.startswith("_:") or cell.startswith('"'):
        return cell
    else:
        return '"' + cell + '"'        

def df2nt(df, colnames_of_triples):
    """
    This function is to convert a Pandas data frame to a string of N-Triples
    :param df: a Pandas data frame
    :param colnames_of_triples: a list of list. [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] where these items are column names
    :return nt: a string of N-Triples
    """
    nt = ""
    for colnames_of_triple in colnames_of_triples:
        nt += df.apply(lambda row: "{s} {p} {o} .\n".format(s=format_cell(row[colnames_of_triple[0]]), p=format_cell(row[colnames_of_triple[1]]), o=format_cell(row[colnames_of_triple[2]])), axis=1).str.cat(sep='')
    return nt

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
        nt = df2nt(pd.read_csv(StringIO(input_file)), ast.literal_eval(colnames_of_triples))
        rdf_graph.parse(data=nt, format="nt")
    else:
        rdf_graph.parse(data=input_file, format=input_format)
    rdf_graph = infer_rdf_graph(rdf_graph, infer)
    return rdf_graph

def load_rdf_dataset(dataset):
    data_path = DATA_DIR + dataset + ".pkl"
    if not os.path.isfile(data_path):
        raise ValueError("Please create the RDF dataset ({dataset}) before loading it. Run `geist create --help` for detailed information".format(dataset=dataset))
    with open(data_path, mode='rb') as f:
        geist_graph_object = pickle.load(f)
    rdf_graph, infer = geist_graph_object["rdf_graph"], geist_graph_object["infer"]
    return rdf_graph, infer

def delete_rdf_dataset(**kwargs):
    dataset = kwargs["dataset"] if "dataset" in kwargs else "kb"
    data_path = DATA_DIR + dataset + ".pkl"
    if not os.path.isfile(data_path):
        if "quiet" in kwargs and kwargs["quiet"]:
            return
        raise ValueError("Nothing to be removed. Can NOT find {data_path}".format(data_path=data_path))
    os.remove(data_path)
    return

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
        res_df = pd.DataFrame(bindings).apply(lambda row: row.apply(lambda x: "<"+x["value"]+">" if x["type"] == "uri" else '"'+x["value"]+'"' if x["type"] == "literal" else "_:"+x["value"]), axis=1)
    else:
        res_df = pd.DataFrame(columns=colnames)
    return res_df[colnames]

def connected_components(graph, edges):
    """
    This function is to find the connected components in a graph
    :param graph: a Pandas data frame
    :param edges: a list of list. [[start_node1, end_node1], [start_node2, end_node2], ...] or [[start_node1, end_node1, label1], [start_node2, end_node2, label2], ...] where these items are column names
    :return components: a dict, where the key is the index of a component and the value is a connected component
    """

    # Transform the dataframe to two/three columns: start_node and end_node (and label if exists)
    graph_transformed = pd.DataFrame()
    for edge in edges:
        if len(edge) != 2 and len(edge) != 3:
            raise ValueError("Each edge should have two or three items, i.e., [start_node, end_node] or [start_node, end_node, label].")
        if len(edge) == 2:
            graph_per_edge = graph[edge].rename(columns={edge[0]: "start_node", edge[1]: "end_node"})
        else: # len(edge) == 3
            graph_per_edge = graph[edge].rename(columns={edge[0]: "start_node", edge[1]: "end_node", edge[2]: "label"})
        graph_transformed = pd.concat([graph_transformed, graph_per_edge], axis=0)
    graph_transformed.drop_duplicates(inplace=True)
    start_nodes, end_nodes = set(graph_transformed["start_node"]), set(graph_transformed["end_node"])
    nodes = start_nodes.union(end_nodes)
    start2end, end2start = {}, {}
    for start_node in start_nodes:
        start2end[start_node] = set(graph_transformed[graph_transformed["start_node"] == start_node]["end_node"])
    for end_node in end_nodes:
        end2start[end_node] = set(graph_transformed[graph_transformed["end_node"] == end_node]["start_node"])

    nodes_components = []
    for node in nodes:
        flag = False
        connected_nodes = start2end.get(node, set()).union(end2start.get(node, set()))
        connected_nodes.add(node)

        for nodes_component in nodes_components:
            if connected_nodes.intersection(nodes_component):
                nodes_component.update(connected_nodes)
                flag = True
                break
        if not flag:
            nodes_components.append(connected_nodes)

        # Merge connected components
        flags = [False] * len(nodes_components)
        for idx1, nodes_component_1 in enumerate(nodes_components):
            for idx2, nodes_component_2 in enumerate(nodes_components):
                if (idx1 == idx2) or flags[idx1] or flags[idx2]:
                    continue
                if nodes_component_1.intersection(nodes_component_2):
                    nodes_components[idx1].update(nodes_component_2)
                    flags[idx2] = True
        merged_nodes_components = []
        for idx, flag in enumerate(flags):
            if not flag:
                merged_nodes_components.append(nodes_components[idx])
        nodes_components = merged_nodes_components
    
    components = {}
    if len(nodes_components) == 1:
        components[0]=graph_transformed.to_dict()
    else:
        for idx, nodes_component in enumerate(nodes_components):
            components[idx] = graph_transformed[graph_transformed["start_node"].isin(nodes_component) | graph_transformed["end_node"].isin(nodes_component)].to_dict()
    return components

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

    graph2_env = jinja2.Environment()
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

def _create(dataset, inputfile, inputformat, colnames, infer):
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

def _load(dataset, inputfile, inputformat, colnames):
    """Import data into a RDF dataset"""
    if inputformat == "csv" and (not colnames):
        raise ValueError("Please provide the column names of triples for the CSV file, i.e., --colnames")
    (rdf_graph, infer) = load_rdf_dataset(dataset)
    rdf_graph = rdf_graph + create_rdf_graph(inputfile, inputformat, colnames, infer)
    geist_graph_object = {"rdf_graph": rdf_graph, "infer": infer}
    with open(DATA_DIR + dataset + ".pkl", "wb") as f:
        pickle.dump(geist_graph_object, f)
    return

def _graph(rdf_graph, rankdir, mappings):
    """Convert a RDF graph object to a Graphviz graph object"""
    query = """
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        """
    res = query2df(rdf_graph, query)
    res = map_df(res, mappings)
    G = visualize_query_results(query_res=res, edges=[['s', 'o', 'p']], rankdir=rankdir, same_color=True)
    return G

def _graph2(rdf_graph, rankdir, mappings, **kwargs):
    """Convert a RDF graph object to a Graphviz graph object"""
    query = """
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        """
    res = query2df(rdf_graph, query)
    res = map_df(res, mappings)
    gv = visualize_query_results_without_pygraphviz(query_res=res, edges=[['s', 'o', 'p']], rankdir=rankdir, same_color=True, **kwargs)
    return gv

def get_content(data, isfilepath):
    """
    This function is to retrieve the content of the given file path or the input string itself.
    :param data: a string. It can be a file path or content of the file
    :param isfilepath: a bool value to denote if the given data is a file path or not (default: True, which is a file path)
    :return content: a string
    """
    if isfilepath:
        with open(data.strip(), mode='r', encoding='utf-8') as fin:
            content = fin.read()
    else:
        content = data.strip()
    return content

class CreateExtension(ContainerTag):
    tags = {"create"}
    
    def render(self, dataset="kb", inputformat="json-ld", colnames=None, infer="none", isfilepath=True, caller=None):
        _create(dataset, get_content(environment.from_string(str(caller())).render(), isfilepath), inputformat, colnames, infer)
        return ""

class LoadExtension(ContainerTag):
    tags = {"load"}
    
    def render(self, dataset="kb", inputformat="json-ld", colnames=None, isfilepath=True, caller=None):
        _load(dataset, get_content(environment.from_string(str(caller())).render(), isfilepath), inputformat, colnames)
        return ""

class QueryExtension(ContainerTag):
    tags = {"query"}

    def render(self, dataset="kb", isfilepath=True, caller=None):
        (rdf_graph, _) = load_rdf_dataset(dataset)
        res = query2df(rdf_graph, get_content(environment.from_string(str(caller())).render(), isfilepath))
        return res.to_json()

class DestroyExtension(StandaloneTag):
    tags = {"destroy"}
    
    def render(self, dataset="kb", quiet=False):
        delete_rdf_dataset(dataset=dataset, quiet=quiet)
        return ""

class GraphExtension(StandaloneTag):
    tags = {"graph"}

    def render(self, dataset="kb", rankdir="TB", mappings=None):
        (rdf_graph, _) = load_rdf_dataset(dataset)
        G = _graph(rdf_graph, rankdir, mappings)
        return G.string()

class Graph2Extension(StandaloneTag):
    tags = {"graph2"}

    def render(self, dataset="kb", rankdir="TB", mappings=None, **kwargs):
        (rdf_graph, _) = load_rdf_dataset(dataset)
        gv = _graph2(rdf_graph, rankdir, mappings, **kwargs)
        return gv

class ComponentExtension(ContainerTag):
    tags = {"component"}

    def render(self, isfilepath=True, edges=[["s", "o", "p"]], caller=None):
        graph = json2df(get_content(environment.from_string(str(caller())).render(), isfilepath))
        components = connected_components(graph, edges)
        return json.dumps(components)

class MapExtension(ContainerTag):
    tags = {"map"}

    def render(self, isfilepath=True, mappings=None, caller=None):
        df = json2df(get_content(environment.from_string(str(caller())).render(), isfilepath))
        df = map_df(df, mappings)
        return df.to_json()

class UseExtension(StandaloneTag):
    tags = {"use"}

    def render(self, filepath):
        return ""

class HtmlExtension(ContainerTag):
    tags = {"html"}

    def render(self, path="report.html", caller=None):
        report = '''
<!DOCTYPE html>
<html>
{content}
</html>
'''.format(content=environment.from_string(str(caller())).render())
        path = ensure_dir_exists(path)
        with open(path, 'w') as fout:
            fout.write(report)
        return report

class ImgExtension(ContainerTag):
    tags = {"img"}

    def render(self, src, caller=None, **kwargs):
        path = ensure_dir_exists(src)
        report = environment.from_string(str(caller())).render()
        # Extract extension from src
        ext = src.split('.')[-1]
        params_assign = " ".join(['{param_k}={param_v}'.format(param_k=param_k, param_v=param_v) for param_k, param_v in kwargs.items()])
        if ext == 'gv' or ext == 'dot':
            with open(path, 'w') as fout:
                fout.write(report)
            # Code to be embeded in an HTML file
            code = '<pre><code {params_assign}>{report}</code></pre>'.format(params_assign=params_assign, report=report)
        else:
            # Save as an image
            graph = pgv.AGraph(string=report)
            graph.draw(path, format=ext, prog='dot')
            # Code to be embeded in an HTML file
            code = '<img src="{src}" {params_assign}>'.format(src=src, params_assign=params_assign)
        return code

class TableExtension(ContainerTag):
    tags = {"table"}

    def render(self, mappings=None, caller=None):
        json_str = environment.from_string(str(caller())).render()
        df = json2df(json_str)
        df = map_df(df, mappings)
        code = df2htmltable(df)
        return code

def include_filepaths(data):
    """
    This function is to retrive file paths of the included files through matching the pattern {% use filepath %}
    :param data: a string, which might contains multiple included files
    :return file_paths: a list of file paths
    """
    blocks = re.findall(r"{%[+\-\s]?\s*use.*?\s*[+\-\s]?%}", data)
    file_paths = []
    for block in blocks:
        file_path = re.search(r"{%[+\-\s]?\s*use\s+([^\s]*?)\s*[+\-\s]?%}", block).groups()[0].replace('"', "").replace("'", "")
        file_paths.append(file_path)
    return file_paths

def generate_template_class(file_paths):
    """
    This function is to generate {Tag}Extension class based on the give file paths
    :param file_paths: a list of file paths
    :return templates: a string of Python code to define template classes and add them as extensions
    """
    templates = ""
    for file_path in file_paths:
        with open(file_path, mode='r', encoding='utf-8') as fin:
            macros = fin.read()
        blocks = re.findall(r"{%\s*template.*?{%\s*endtemplate\s*%}", macros, re.DOTALL)
        for block in blocks:
            # Parse tag, params, and content
            (tag, params, content) = re.search(r"{%\s*template\s*([a-zA-Z\d_]+)\s*([a-zA-Z\d_ ]*).*?%}(.*?){%\s*endtemplate\s*%}", block, re.DOTALL).groups()
            # Validate tag
            tag_cap, tag_low = tag.capitalize(), tag.lower()
            if tag_low.startswith("end"):
                raise ValueError("The tag name (i.e., {tag}) cannot start with 'end'.".format(tag=tag))
            if tag_low.startswith("end") or (tag_low in TAGS):
                raise ValueError("Duplicate tag names (i.e., {tag}). \nPlease make sure your tag is not one of the reserved tages [template, create, load, query, destroy, include, import, macro, block, extends, call, filter, set, for, if, elif, else].".format(tag=tag))
            TAGS.append(tag_low)
            # Generate render function
            params = params.strip().split()
            params_def, params_assign = ", ".join(params), ", ".join(['{param}={param}'.format(param=param) for param in params])
            if params:
                render_func = '''
    def render(self, {params_def}):
        rendered_content = environment.from_string("""{content}""").render({params_assign})
        return rendered_content'''.format(params_def=params_def, content=content, params_assign=params_assign)
            else:
                render_func = '''
    def render(self):
        rendered_content = environment.from_string("""{content}""").render()
        return rendered_content'''.format(content=content)
            # Generate a template class and add its extension
            templates = templates + '''
class {tag_cap}Extension(StandaloneTag):
    tags = {{"{tag_low}"}}
{render_func}
environment.add_extension({tag_cap}Extension)'''.format(tag_cap=tag_cap, tag_low=tag_low, render_func=render_func)
        return templates

@cli.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to create (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as triples')
@click.option('--inputformat', '-iformat', default='json-ld', type=click.Choice(['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig', 'nquads', 'json-ld', 'hext', 'csv']), help='Format of the file to be loaded as triples (default json-ld)')
@click.option('--colnames', default=None, type=str, help='Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] when the input format is csv')
@click.option('--infer', default='none', type=click.Choice(['none', 'rdfs', 'owl', 'rdfs_owl']), help='Inference to perform on update [none, rdfs, owl, rdfs_owl] (default "none")')
def create(dataset, inputfile, inputformat, colnames, infer):
    """Create a new RDF dataset"""
    _create(dataset, inputfile.read(), inputformat, colnames, infer)

@cli.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to create (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as triples')
@click.option('--inputformat', '-iformat', default='json-ld', type=click.Choice(['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig', 'nquads', 'json-ld', 'hext', 'csv']), help='Format of the file to be loaded as triples (default json-ld)')
@click.option('--colnames', default=None, type=str, help='Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] when the input format is csv')
def load(dataset, inputfile, inputformat, colnames):
    """Import data into a RDF dataset"""
    _load(dataset, inputfile.read(), inputformat, colnames)

@cli.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be removed (default "kb")')
@click.option('--quiet', '-q', is_flag=True, show_default=True, default=False, help="Suppress error messages if the provided dataset does not exist")
def destroy(dataset, quiet):
    """Delete an RDF dataset"""
    delete_rdf_dataset(dataset=dataset, quiet=quiet)

@cli.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be exported (default "kb")')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store these exported triples (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store these exported triples (default: None)')
@click.option('--outputformat', '-oformat', default='nt', type=click.Choice(['json-ld', 'n3', 'nquads', 'nt', 'hext', 'pretty-xml', 'trig', 'trix', 'turtle', 'longturtle', 'xml']), help='Format of the exported triples (default nt)')
def export(dataset, outputroot, outputfile, outputformat):
    """Export an RDF graph"""
    update_outputroot(outputroot)
    (rdf_graph, _) = load_rdf_dataset(dataset)
    if outputfile is None:
        print(rdf_graph.serialize(format=outputformat))
    else:
        outputfile = ensure_dir_exists(outputfile)
        rdf_graph.serialize(destination=outputfile, format=outputformat)

@cli.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be queried (default "kb")')
@click.option('--file', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file containing the SPARQL query to execute')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the query results (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the query results (default: None)')
def query(dataset, file, outputroot, outputfile):
    """Perform a SPARQL query on a dataset"""
    update_outputroot(outputroot)
    (rdf_graph, _) = load_rdf_dataset(dataset)
    res = query2df(rdf_graph, file.read())
    if outputfile is None:
        print(res.to_markdown())
    else:
        outputfile = ensure_dir_exists(outputfile)
        res.to_csv(outputfile, index=False)

@cli.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be visualized (default "kb")')
@click.option('--rankdir', '-r', default='TB', type=click.Choice(['TB', 'BT', 'LR', 'RL']), help='Direction of the graph (default TB): TB or BT or LR or RL')
@click.option('--mappings', '-m', default=None, help='File of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text.')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the graph (default: current directory). If the given path (i.e., --outputfile) is a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default='res', type=str, help='Path of the file without extension to store the graph (default: res)')
@click.option('outputformats', '--outputformat', '-oformat', default=['none'], type=click.Choice(['none', 'svg', 'png', 'gv']), multiple=True, help='Format of the graph (default: none): none or svg or png or gv')
def graph(dataset, rankdir, mappings, outputroot, outputfile, outputformats):
    """Visualize a dataset"""
    update_outputroot(outputroot)

    # Load a RDF dataset
    (rdf_graph, _) = load_rdf_dataset(dataset)
    # Convert a RDF graph object to a Graphviz graph object
    G = _graph(rdf_graph, rankdir, mappings)

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

@cli.command()
@click.option('--file', '-f', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file containing the report template to expand')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the expanded report (default: current directory)')
@click.option('--suppressoutput', '-so', default=False, help='Suppress output or not (default: False)')
def report(file, outputroot, suppressoutput):
    """Expand a report using a dataset"""
    update_outputroot(outputroot)

    # Create a global Jinja2 environment
    global environment
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("./"), 
        trim_blocks=True, 
        extensions=[CreateExtension, LoadExtension, QueryExtension, DestroyExtension, GraphExtension, Graph2Extension, ComponentExtension, MapExtension, UseExtension, HtmlExtension, ImgExtension, TableExtension]
    )
    environment.filters['json2df'] = json2df
    environment.filters['json2dict'] = json2dict
    environment.filters['dict2df'] = dict2df
    environment.filters['df2htmltable'] = df2htmltable
    environment.filters['escape_quotes'] = escape_quotes
    environment.filters['process_str_for_html'] = process_str_for_html

    # Define custom tags based on files with the "use" tag
    content = file.read()
    file_paths = include_filepaths(content)
    if file_paths:
        templates = generate_template_class(file_paths)
        exec(templates, globals())

    # Render the report
    template = environment.from_string(content)
    report = template.render()

    if not suppressoutput:
        print(report)


if __name__ == '__main__':
    cli()
