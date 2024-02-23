import click, duckdb, os
from geist.tools.filters import csv2df, json2df
from geist.tools.utils import ensure_dir_exists, update_outputroot

DATA_DIR = ".geistdata/duckdb/"

def load_sql_dataset(dataset):
    data_path = DATA_DIR + dataset + ".duckdb"
    if not os.path.isfile(data_path):
        raise ValueError("Please create the SQL dataset ({dataset}) before loading it. Run `geist create duckdb --help` for detailed information".format(dataset=dataset))
    conn = duckdb.connect(data_path)
    return conn

def inputfile2df(inputfile, inputformat):
    if inputformat == 'csv':
        df = csv2df(inputfile)
    elif inputformat == 'json':
        df = json2df(inputfile)
    else:
        raise ValueError("Invalid input format. Only csv and json are supported for now.")
    return df

@click.group()
def cli():
    pass

@cli.group()
def sql_duckdb():
    pass

def duckdb_create(dataset, inputfile, inputformat, table):
    """Create a new SQL dataset using DuckDB"""
    
    data_path = DATA_DIR + dataset + '.duckdb'
    ensure_dir_exists(data_path, output=False)

    conn = duckdb.connect(data_path)
    df = inputfile2df(inputfile, inputformat)
    conn.sql(f'CREATE TABLE {table} AS SELECT * FROM df;')
    conn.close()
    return

def duckdb_load(dataset, inputfile, inputformat, table):
    """Import data into a SQL dataset"""    
    conn = load_sql_dataset(dataset)
    df = inputfile2df(inputfile, inputformat)
    conn.sql(f'INSERT INTO {table} SELECT * FROM df')
    conn.close()
    return

def duckdb_query(dataset, file, outputroot, outputfile):
    """Perform a SQL query on a dataset"""
    update_outputroot(outputroot)
    conn = load_sql_dataset(dataset)
    res = conn.sql(file.read()).df()
    if outputfile is None:
        print(res.to_markdown())
    else:
        outputfile = ensure_dir_exists(outputfile)
        res.to_csv(outputfile, index=False)
    conn.close()
    return

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

def duckdb_export(dataset, outputroot, outputfile, outputformat, table):
    """Export a table from a SQL dataset"""
    update_outputroot(outputroot)
    conn = load_sql_dataset(dataset)
    res = conn.sql(f"SELECT * FROM {table}").df()
    if outputfile is None:
        print(res.to_markdown())
    else:
        outputfile = ensure_dir_exists(outputfile)
        if outputformat == 'csv':
            res.to_csv(outputfile, index=False)
        elif outputformat == 'json':
            res.to_json(outputfile, orient='records')
    conn.close()
    return



if __name__ == '__main__':
    cli()
