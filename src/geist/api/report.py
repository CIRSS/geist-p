import json, re, os
from geist.tools.utils import set_tags, ensure_dir_exists, get_content, update_outputroot, include_filepaths, generate_template_class, map_df, export_mermaid
from geist.tools.filters import head, csv2df, dict2df, json2df, json2dict, df2json, df2htmltable, escape_quotes, process_str_for_html, clingo_list_arguments
from jinja2 import nodes, Environment, FileSystemLoader
from jinja2.compiler import CodeGenerator, Frame
from jinja2_simple_tags import StandaloneTag, ContainerTag

class CustomCodeGenerator(CodeGenerator):
    def visit_AssignBlock(self, node: nodes.AssignBlock, frame: Frame) -> None:
        self.push_assign_tracking()
        block_frame = frame.inner()
        # This is a special case.  Since a set block always captures we
        # will disable output checks. This way one can use set blocks
        # toplevel even in extended templates.
        block_frame.require_output_check = False
        block_frame.symbols.analyze_node(node)
        self.enter_frame(block_frame)
        self.buffer(block_frame)
        self.blockvisit(node.body, block_frame)
        self.newline(node)

        # Ref: https://github.com/dldevinc/jinja2-simple-tags/issues/7
        # This added block of code makes it possible to return any object instead of a string for a ContainerTag
        self.writeline(f"if len({block_frame.buffer}) == 1 and not isinstance({block_frame.buffer}[0], str):")
        self.indent()
        self.newline()
        self.visit(node.target, frame)
        self.write(f" = {block_frame.buffer}[0]")
        self.outdent()
        self.writeline("else:")
        self.indent()
        self.newline()

        self.visit(node.target, frame)
        self.write(" = (Markup if context.eval_ctx.autoescape else identity)(")
        if node.filter is not None:
            self.visit_Filter(node.filter, block_frame)
        else:
            self.write(f"concat({block_frame.buffer})")
        self.write(")")
        self.outdent()
        self.pop_assign_tracking(frame)
        self.leave_frame(block_frame)

class CreateExtension(ContainerTag):
    tags = {"create"}
    
    def render(self, dataset="kb", datastore="rdflib", inputformat="json-ld", colnames=None, infer="none", isfilepath=True, table="df", predicate="isfirstcol", name="base", caller=None):
        content = get_content(environment.from_string(str(caller())).render(), isfilepath)
        if datastore == "rdflib":
            from geist.datastore.rdflib import rdflib_create
            rdflib_create(dataset, content, inputformat, colnames, infer)
        elif datastore == "duckdb":
            from geist.datastore.duckdb import duckdb_create
            conn = duckdb_create(dataset, content, inputformat, table)
            conn.close()
        elif datastore == "clingo":
            from geist.datastore.clingo import clingo_create
            inputformat = "lp" if inputformat == "json-ld" else inputformat
            clingo_create(dataset, content, inputformat, predicate, name)
        else:
            raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
        return ""

class LoadExtension(ContainerTag):
    tags = {"load"}
    
    def render(self, dataset="kb", datastore="rdflib", inputformat="json-ld", colnames=None, isfilepath=True, table="df", predicate="isfirstcol", programname="base", caller=None):
        content = get_content(environment.from_string(str(caller())).render(), isfilepath)
        if datastore == "rdflib":
            from geist.datastore.rdflib import rdflib_load
            rdflib_load(dataset, content, inputformat, colnames, False, None)
        elif datastore == "duckdb":
            from geist.datastore.duckdb import duckdb_load
            conn = duckdb_load(dataset, content, inputformat, table)
            conn.close()
        elif datastore == "clingo":
            from geist.datastore.clingo import clingo_load
            inputformat = "lp" if inputformat == "json-ld" else inputformat
            clingo_load(dataset, content, inputformat, predicate, programname, False)
        else:
            raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
        return ""

class QueryExtension(ContainerTag):
    tags = {"query"}

    def render(self, dataset="kb", datastore="rdflib", isfilepath=True, predicate=None, programname='base', rformat="lp", caller=None):
        res = '{}'
        content = get_content(environment.from_string(str(caller())).render(), isfilepath)
        if datastore == "rdflib":
            from geist.datastore.rdflib import load_rdf_dataset, query2df
            (rdf_graph, _) = load_rdf_dataset(dataset)
            res = query2df(rdf_graph, content)
        elif datastore == "duckdb":
            from geist.datastore.duckdb import load_sql_dataset
            conn = load_sql_dataset(dataset)
            res = conn.sql(content).df()
            conn.close()
        elif datastore == "clingo":
            from geist.datastore.clingo import load_asp_dataset, query2dicts, format_dicts
            conn = load_asp_dataset(dataset, name="base")
            dicts = query2dicts(conn, content, programname, predicate)
            res = format_dicts(dicts, rformat)
        else:
            raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
        return res

class DestroyExtension(StandaloneTag):
    tags = {"destroy"}
    
    def render(self, dataset="kb", datastore="rdflib", quiet=False):
        if datastore == "rdflib":
            from geist.datastore.rdflib import rdflib_destroy
            rdflib_destroy(dataset=dataset, quiet=quiet)
        elif datastore == "duckdb":
            from geist.datastore.duckdb import duckdb_destroy
            duckdb_destroy(dataset=dataset, quiet=quiet)
        elif datastore == "clingo":
            from geist.datastore.clingo import clingo_destroy
            clingo_destroy(dataset=dataset, quiet=quiet)
        else:
            raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
        return ""

class GraphExtension(StandaloneTag):
    tags = {"graph"}

    def render(self, dataset="kb", datastore="rdflib", rankdir="TB", mappings=None, on=None, samecolor=True):
        res = ""
        if datastore == "rdflib":
            from geist.datastore.rdflib import load_rdf_dataset, _graph
            (rdf_graph, _) = load_rdf_dataset(dataset)
            res = _graph(rdf_graph, rankdir, mappings, on, samecolor)
        else:
            raise ValueError("Invalid datastore. Only rdflib is supported for now.")
        return res

class Graph2Extension(StandaloneTag):
    tags = {"graph2"}

    def render(self, dataset="kb", datastore="rdflib", rankdir="TB", mappings=None, on=None, **kwargs):
        gv = ""
        if datastore == "rdflib":
            from geist.datastore.rdflib import load_rdf_dataset, _graph2
            (rdf_graph, _) = load_rdf_dataset(dataset)
            gv = _graph2(rdf_graph, rankdir, mappings, on, **kwargs)
        else:
            raise ValueError("Invalid datastore. Only rdflib is supported for now.")
        return gv

class ComponentExtension(ContainerTag):
    tags = {"component"}

    def render(self, isfilepath=True, edges=[["s", "o", "p"]], caller=None):
        from geist.tools.utils import connected_components
        graph = json2df(get_content(environment.from_string(str(caller())).render(), isfilepath))
        components = connected_components(graph, edges)
        return json.dumps(components)

class MapExtension(ContainerTag):
    tags = {"map"}

    def render(self, isfilepath=True, mappings=None, on=None, caller=None):
        df = json2df(get_content(environment.from_string(str(caller())).render(), isfilepath))
        df = map_df(df, mappings, on)
        return df

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
        if ext == 'gv' or ext == 'dot' or ext == 'mermaid' or ext == 'mmd':
            with open(path, 'w') as fout:
                fout.write(report)
            # Code to be embeded in an HTML file
            code = '<pre><code {params_assign}>{report}</code></pre>'.format(params_assign=params_assign, report=report)
            if ext == 'mermaid' or ext == 'mmd':
                code = f'<pre class="mermaid">{report}</pre><script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";mermaid.initialize({{ startOnLoad: true }});</script>'
        elif ext == 'png' or ext == 'svg' or ext == 'pdf':
            # Save as an image
            export_mermaid(report, ext, path)
            # Code to be embeded in an HTML file
            code = '<img src="{src}" {params_assign}>'.format(src=src, params_assign=params_assign)
        else:
            raise ValueError("Invalid src. Only gv, dot, mermaid, mmd, png, svg, and pdf are supported for now.")
        return code

class TableExtension(ContainerTag):
    tags = {"table"}

    def render(self, mappings=None, on=None, caller=None):
        json_str = environment.from_string(str(caller())).render()
        df = json2df(json_str)
        df = map_df(df, mappings, on)
        code = df2htmltable(df)
        return code    

def geist_report(inputfile, isinputpath=False, outputroot='./', suppressoutput=True, args={}):
    """
    Expand a report using dataset(s).
    :param inputfile: a string. Report to be expanded
    :param isinputpath: bool. True if the inputfile is the file path, otherwise the inputfile is the content (default: False)
    :param outputroot: a string. Path of the directory to store the expanded report (default: current directory)
    :param suppressoutput: bool. True to suppress output (default: True)
    :return report: a string. The expanded report
    """
    TAGS = set_tags()
    update_outputroot(outputroot)
    content = get_content(inputfile, isinputpath)

    # Create a new global environment
    global environment
    environment = Environment(
        loader=FileSystemLoader("./"), 
        trim_blocks=True, 
        extensions=[CreateExtension, LoadExtension, QueryExtension, DestroyExtension, GraphExtension, Graph2Extension, ComponentExtension, MapExtension, UseExtension, HtmlExtension, ImgExtension, TableExtension],
        cache_size=0 # recompile templates all the time
    )
    for filter in ["head", "csv2df", "dict2df", "json2df", "json2dict", "df2json", "df2htmltable", "escape_quotes", "process_str_for_html", "clingo_list_arguments"]:
        environment.filters[filter] = globals()[filter]
    environment.code_generator_class = CustomCodeGenerator

    # Define custom tags based on files with the "use" tag
    file_paths = include_filepaths(content)
    if file_paths:
        if isinputpath:
            curr_dir = os.path.dirname(inputfile)
            file_paths = [f"{curr_dir}/{file_path}" for file_path in file_paths] 
        templates = generate_template_class(file_paths, TAGS)
        exec(templates, globals())

    # Render the report
    template = environment.from_string(content)
    report = template.render(args)

    if not suppressoutput:
        print(report)

    return report
