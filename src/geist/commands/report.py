import click, json, sys
from geist.commands.cli import cli
from geist.tools.utils import ensure_dir_exists, get_content, update_outputroot, include_filepaths, generate_template_class, map_df
from geist.tools.filters import head, json2df, json2dict, dict2df, df2json, df2htmltable, escape_quotes, process_str_for_html
from jinja2 import nodes, Environment, FileSystemLoader
from jinja2.compiler import CodeGenerator, Frame
from jinja2_simple_tags import StandaloneTag, ContainerTag
import pygraphviz as pgv

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
    
    def render(self, dataset="kb", datastore="rdflib", inputformat="json-ld", colnames=None, infer="none", isfilepath=True, table="df", caller=None):
        content = get_content(environment.from_string(str(caller())).render(), isfilepath)
        if datastore == "rdflib":
            from geist.datastore.rdflib import rdflib_create
            rdflib_create(dataset, content, inputformat, colnames, infer)
        elif datastore == "duckdb":
            from geist.datastore.duckdb import duckdb_create
            duckdb_create(dataset, content, inputformat, table)
        else:
            raise ValueError("Invalid datastore. Only rdflib and duckdb are supported for now.")
        return ""

class LoadExtension(ContainerTag):
    tags = {"load"}
    
    def render(self, dataset="kb", datastore="rdflib", inputformat="json-ld", colnames=None, isfilepath=True, table="df", caller=None):
        content = get_content(environment.from_string(str(caller())).render(), isfilepath)
        if datastore == "rdflib":
            from geist.datastore.rdflib import rdflib_load
            rdflib_load(dataset, content, inputformat, colnames)
        elif datastore == "duckdb":
            from geist.datastore.duckdb import duckdb_load
            duckdb_load(dataset, content, inputformat, table)
        else:
            raise ValueError("Invalid datastore. Only rdflib and duckdb are supported for now.")
        return ""

class QueryExtension(ContainerTag):
    tags = {"query"}

    def render(self, dataset="kb", datastore="rdflib", isfilepath=True, caller=None):
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
        else:
            raise ValueError("Invalid datastore. Only rdflib and duckdb are supported for now.")
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
        else:
            raise ValueError("Invalid datastore. Only rdflib and duckdb are supported for now.")
        return ""

class GraphExtension(StandaloneTag):
    tags = {"graph"}

    def render(self, dataset="kb", datastore="rdflib", rankdir="TB", mappings=None, on=None, samecolor=True):
        res = ""
        if datastore == "rdflib":
            from geist.datastore.rdflib import load_rdf_dataset, _graph
            (rdf_graph, _) = load_rdf_dataset(dataset)
            G = _graph(rdf_graph, rankdir, mappings, on, samecolor)
            res = G.string()
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

    def render(self, mappings=None, on=None, caller=None):
        json_str = environment.from_string(str(caller())).render()
        df = json2df(json_str)
        df = map_df(df, mappings, on)
        code = df2htmltable(df)
        return code



@cli.command()
@click.option('--file', '-f', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file containing the report template to expand')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the expanded report (default: current directory)')
@click.option('--suppressoutput', '-so', default=False, help='Suppress output or not (default: False)')
def report(file, outputroot, suppressoutput):
    """Expand a report using a dataset"""
    update_outputroot(outputroot)

    global environment
    environment = Environment(
        loader=FileSystemLoader("./"), 
        trim_blocks=True, 
        extensions=[CreateExtension, LoadExtension, QueryExtension, DestroyExtension, GraphExtension, Graph2Extension, ComponentExtension, MapExtension, UseExtension, HtmlExtension, ImgExtension, TableExtension]
    )
    for filter in ["head", "json2df", "json2dict", "dict2df", "df2json", "df2htmltable", "escape_quotes", "process_str_for_html"]:
        environment.filters[filter] = globals()[filter]
    environment.code_generator_class = CustomCodeGenerator

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