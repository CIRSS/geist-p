from geist.tools.utils import get_content

def geist_load(datastore, dataset, inputfile, inputformat, isinputpath, config={}):
    """
    Import data into a dataset
    :param datastore: a string. Backend datastores, i.e., rdflib, duckdb
    :param dataset: a string. Dataset to load an object: (1) A string indicates the name of the dataset stored on disk OR (2) a DuckPyConnection object OR a GeistGraph object for dataset in memory
    :param inputfile: a string. File to be loaded
    :param inputformat: a string. Format of the file to be loaded
    :param isinputpath: bool. True if the inputfile is the file path, otherwise the inputfile is the content
    :param config: a dictionary with the 'colnames' key (when datastore=rdflib and inputformat='csv') OR the 'table' key (when datastore=duckdb)
                   the 'inmemory' key is required when datastore=rdflib, inmemory=False by default
    """
    content = get_content(inputfile, isinputpath)
    if datastore == 'rdflib':
        # Import data into a RDF dataset
        from geist.datastore.rdflib import rdflib_load
        colnames = None if 'colnames' not in config else config['colnames']
        inmemory = False if 'inmemory' not in config else config['inmemory']
        datasetname = None if 'datasetname' not in config else config['datasetname']
        conn = rdflib_load(dataset=dataset, inputfile=content, inputformat=inputformat, colnames=colnames, inmemory=inmemory, datasetname=datasetname)
    elif datastore == 'duckdb':
        # Import data into a SQL dataset
        from geist.datastore.duckdb import duckdb_load
        if 'table' not in config:
            raise ValueError("Please specify the value of 'table' in config")
        conn = duckdb_load(dataset=dataset, inputfile=content, inputformat=inputformat, table=config['table'])
    elif datastore == 'clingo':
        # Import data into an ASP dataset
        from geist.datastore.clingo import clingo_load
        predicate = 'isfirstcol' if 'predicate' not in config else config['predicate']
        programname = 'base' if 'programname' not in config else config['programname']
        inmemory = False if 'inmemory' not in config else config['inmemory']
        conn = clingo_load(dataset=dataset, inputfile=content, inputformat=inputformat, predicate=predicate, programname=programname, inmemory=inmemory)
    else:
        raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
    return conn
