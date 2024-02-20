import json, re, os
import pandas as pd

TAGS = ["use", "template", "create", "load", "query", "destroy", "graph", "graph2", "component", "map", "html", "img", "table", "include", "import", "macro", "block", "extends", "call", "filter", "set", "for", "if", "elif", "else"]

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
        file_path = get_full_path(globals()["outputroot"], file_path)
    dir_path = os.path.split(file_path)[0]
    if (dir_path != '') and (not os.path.isdir(dir_path)):
        os.makedirs(dir_path)
    return file_path

def update_outputroot(dir):
    # Update the global variable outputroot
    if not dir.endswith('/'):
        dir = dir + '/'
    globals()["outputroot"] = dir
    return

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

def map_df(df, mappings=None, on=None):
    """
    This function is to replace the original text in a Pandas data frame on selected columns (if provides) with the shorter ones based on the given mappings
    :param df: a Pandas data frame
    :param mappings: file of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text.
    :param on: a column or a list of selected columns. All columns will be selected by default (None)
    :return df: a Pandas data frame
    """
    if on:
        if isinstance(on, str):
            on = [on]
        elif not isinstance(on, list):
            raise ValueError("on must be a string or a list of string")
    if mappings:
        with open(mappings, mode='r', encoding='utf-8') as fin:
            mappings = json.loads(fin.read())
        if not on: # None
            df = df.replace(mappings, regex=True)
        else:
            df[on] = df[on].replace(mappings, regex=True)
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
        rendered_content = globals()["environment"].from_string("""{content}""").render({params_assign})
        return rendered_content'''.format(params_def=params_def, content=content, params_assign=params_assign)
            else:
                render_func = '''
    def render(self):
        rendered_content = globals()["environment"].from_string("""{content}""").render()
        return rendered_content'''.format(content=content)
            # Generate a template class and add its extension
            templates = templates + '''
class {tag_cap}Extension(StandaloneTag):
    tags = {{"{tag_low}"}}
{render_func}
globals()["environment"].add_extension({tag_cap}Extension)'''.format(tag_cap=tag_cap, tag_low=tag_low, render_func=render_func)
        return templates

