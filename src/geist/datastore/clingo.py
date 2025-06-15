from io import StringIO
import pandas as pd
import click, pickle, os
from geist.tools.filters import csv2df, json2df
from geist.tools.utils import ensure_dir_exists, update_outputroot
from clingo.control import Control

DATA_DIR = ".geistdata/clingo/"
fact_data = {}

def dict2facts(dict):
    facts = ""
    for predicate, arguments in dict.items():
        for argument in arguments:
            facts = facts + predicate + "(" + ",".join(argument) + ").\n"
    return facts

def dict2dfs(dict):
    dfs = {}
    for predicate, arguments in dict.items():
        dfs[predicate] = pd.DataFrame(columns=[f"arg{k+1}" for k in range(len(arguments[0]))], data=arguments)
    return dfs

def query2dict(ctl, query=None, name="base"):
    global fact_data
    fact_data = {}
    if query:
        ctl.add(name, [], query)
        ctl.ground(parts=[(name, [])])
    ctl.solve(on_model=collect_fact_data)
    return fact_data

def build_program(inputfile, inputformat, predicate="isfirstcol"):
    if inputformat == "lp":
        program = inputfile #StringIO(inputfile).read()
    elif inputformat == "json":
        program = dict2facts(dict)
    elif inputformat == "csv":
        df = csv2df(inputfile)
        if predicate == "isfirstcol":
            predicate, arguments = df.columns[0], df.columns[1:]
            program = "\n".join(df[predicate] + "(" + df[arguments].apply(lambda row: ", ".join(row.astype(str)), axis=1) + ").")
        else: # predicate itself is the predicate
            program = "\n".join(predicate + "(" + df.apply(lambda row: ", ".join(row.astype(str)), axis=1) + ").")        
    else:
        raise ValueError("Invalid input format. Only csv and lp are supported for now.")
    # if hasattr(program, "read"):
    #     program = program.read()
    return program

def add_and_ground_program(program, name="base", ctl=None):
    if not ctl:
        ctl = Control()
    ctl.add(name, [], program)
    ctl.ground(parts=[(name, [])])
    return ctl

def create_asp_dataset(inputfile, inputformat, predicate="isfirstcol", name="base"):
    program = build_program(inputfile, inputformat, predicate)
    conn = add_and_ground_program(program, name, None)
    return conn 

def collect_fact_data(model):
    for atom in model.symbols(shown=True):
        predicate = atom.name
        fact_data.setdefault(predicate, []).append([str(argument) for argument in atom.arguments])

def load_asp_dataset(dataset, name="base"):
    if isinstance(dataset, str):
        if dataset == ':memory:':
            raise ValueError(":memory: is a reserved value for data stored in memory. Please specify another dataset name OR pass the Control object directly.")
        data_path = DATA_DIR + dataset + ".pkl"
        if not os.path.isfile(data_path):
            raise ValueError("Please create the ASP dataset ({dataset}) before loading it. Run `geist create clingo --help` for detailed information".format(dataset=dataset))
        with open(data_path, mode='rb') as f:
            facts = dict2facts(pickle.load(f))
        conn = add_and_ground_program(facts, name, None)
    else: # For Python API Control class
        conn = dataset
    return conn

@click.group()
def cli():
    pass

@cli.group()
def clingo():
    pass

def clingo_create(dataset, inputfile, inputformat, predicate, programname):
    """Create a new ASP dataset using Clingo"""
    conn = create_asp_dataset(inputfile, inputformat, predicate, programname)
    if dataset != ':memory:':
        data_path = DATA_DIR + dataset + '.pkl'
        if os.path.isfile(data_path):
            raise ValueError("Please remove the existing ASP dataset ({dataset}) before loading the new one. Run `geist destroy --help` for detailed information".format(dataset=dataset))
        ensure_dir_exists(data_path, output=False)
        global fact_data
        fact_data = {}
        conn.solve(on_model=collect_fact_data)
        with open(data_path, "wb") as f:
            pickle.dump(fact_data, f)
    return conn

def clingo_load(dataset, inputfile, inputformat, predicate, programname, inmemory):
    """Import data into an ASP dataset"""

    conn = load_asp_dataset(dataset)
    program = build_program(inputfile, inputformat, predicate)
    conn = add_and_ground_program(program, name=programname, ctl=conn)
    
    if not inmemory:
        global fact_data
        fact_data = {}
        conn.solve(on_model=collect_fact_data)
        with open(DATA_DIR + dataset + ".pkl", "wb") as f:
            pickle.dump(fact_data, f)

    return conn

def clingo_query(dataset, inputfile, hasoutput, outputroot, outputfile, outputformat="lp", predicate=None, programname="base"):
    """Perform an ASP query on a dataset"""
    update_outputroot(outputroot)
    conn = load_asp_dataset(dataset)
    raw_res = query2dict(conn, inputfile, programname)
    raw_res = {predicate: raw_res[predicate]} if predicate else raw_res
    if hasoutput and outputformat == "lp" and outputfile:
        outputfile = ensure_dir_exists(outputfile)
        with open(outputfile, "w", encoding="utf8") as fout:
            fout.write(dict2facts(raw_res))
    res = dict2dfs(raw_res)
    for predicate, arguments in res.items():
        if hasoutput:
            if outputfile is None:
                print(f'{dict2facts(raw_res)}')
            else:
                outputfile = ensure_dir_exists(outputfile)
                arguments.to_csv(outputfile.replace(".csv", "") + f"#{predicate}.csv", index=False)
    return res, conn

def clingo_destroy(**kwargs):
    """Delete an ASP dataset"""
    dataset = kwargs["dataset"] if "dataset" in kwargs else "kb"
    data_path = DATA_DIR + dataset + ".pkl"
    if not os.path.isfile(data_path):
        if "quiet" in kwargs and kwargs["quiet"]:
            return
        raise ValueError("Nothing to be removed. Can NOT find {data_path}".format(data_path=data_path))
    os.remove(data_path)
    return

def clingo_export(dataset, predicate, hasoutput, outputroot, outputfile, outputformat, programname="base"):
    """Export facts"""
    return clingo_query(dataset, None, hasoutput, outputroot, outputfile, outputformat, predicate, programname)



if __name__ == '__main__':
    cli()
