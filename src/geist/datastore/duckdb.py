import click, duckdb, os
from geist.tools.filters import csv2df, json2df
from geist.tools.utils import ensure_dir_exists, update_outputroot

DATA_DIR = ".geistdata/duckdb/"

def create_sql_dataset(data_path, inputfile, inputformat, table):
    conn = duckdb.connect(data_path)
    df = inputfile2df(inputfile, inputformat)
    conn.sql(f'CREATE TABLE {table} AS SELECT * FROM df;')
    return conn

def load_sql_dataset(dataset):
    if isinstance(dataset, str):
        if dataset == ':memory:':
            raise ValueError(":memory: is a reserved value for data stored in memory. Please specify another dataset name OR pass the DuckDBPyConnection object directly.")
        data_path = DATA_DIR + dataset + ".duckdb"
        if not os.path.isfile(data_path):
            raise ValueError("Please create the SQL dataset ({dataset}) before loading it. Run `geist create duckdb --help` for detailed information".format(dataset=dataset))
        conn = duckdb.connect(data_path)
    else: # For Python API Connection class
        conn = dataset
    return conn

def inputfile2df(inputfile, inputformat):
    if inputformat == 'csv':
        df = csv2df(inputfile)
    elif inputformat == 'json':
        df = json2df(inputfile)
    else:
        raise ValueError("Invalid input format. Only csv and json are supported for now.")
    return df

def table2df(conn, table='df'):
    """Export a table from a DuckDB connection as a Pandas data frame"""
    return conn.sql(f"SELECT * FROM {table}").df()

@click.group()
def cli():
    pass

@cli.group()
def sql_duckdb():
    pass

def duckdb_create(dataset, inputfile, inputformat, table):
    """Create a new SQL dataset using DuckDB"""
    if dataset == ':memory:':
        data_path = dataset
    else:
        data_path = DATA_DIR + dataset + '.duckdb'
        ensure_dir_exists(data_path, output=False)
    conn = create_sql_dataset(data_path, inputfile, inputformat, table)
    return conn

def duckdb_load(dataset, inputfile, inputformat, table):
    """Import data into a SQL dataset"""    
    conn = load_sql_dataset(dataset)
    locals()[table+"2add"] = inputfile2df(inputfile, inputformat)
    conn.sql(f'INSERT INTO {table} SELECT * FROM {table}2add;')
    return conn

def duckdb_query(dataset, inputfile, hasoutput, outputroot, outputfile):
    """Perform a SQL query on a dataset"""
    update_outputroot(outputroot)
    conn = load_sql_dataset(dataset)
    res = conn.sql(inputfile).df()
    if hasoutput:
        if outputfile is None:
            print(res.to_markdown())
        else:
            outputfile = ensure_dir_exists(outputfile)
            res.to_csv(outputfile, index=False)
    return res, conn

def duckdb_destroy(**kwargs):
    """Delete a SQL dataset"""
    dataset = kwargs["dataset"] if "dataset" in kwargs else "kb"
    data_path = DATA_DIR + dataset + ".duckdb"
    if not os.path.isfile(data_path):
        if "quiet" in kwargs and kwargs["quiet"]:
            return
        raise ValueError("Nothing to be removed. Can NOT find {data_path}".format(data_path=data_path))
    os.remove(data_path)
    return

def duckdb_export(dataset, table, hasoutput, outputroot, outputfile, outputformat):
    """Export a data frame"""
    update_outputroot(outputroot)
    conn = load_sql_dataset(dataset)
    df = table2df(conn=conn, table=table)
    if hasoutput:
        if outputfile is None:
            print(df.to_markdown())
        else:
            outputfile = ensure_dir_exists(outputfile)
            if outputformat == 'csv':
                df.to_csv(outputfile, index=False)
            elif outputformat == 'json':
                df.to_json(outputfile, orient='records')
    return df, conn



if __name__ == '__main__':
    cli()
