from geist.tools.utils import get_content, _require_dependency

def geist_create(datastore, dataset, inputfile, inputformat, isinputpath, config={}):
    """
    Create a new dataset.
    :param datastore: a string. Backend datastores, i.e., rdflib, duckdb, or clingo
    :param dataset: a string. Name of the dataset to be created
    :param inputfile: a string. File to be loaded
    :param inputformat: a string. Format of the file to be loaded
    :param isinputpath: bool. True if the inputfile is the file path, otherwise the inputfile is the content
    :param config: a dictionary with 'colnames' and 'infer' keys (when datastore=rdflib) OR the 'table' key (when datastore=duckdb)
                   OR 'predicate' and 'programname' keys (when datastore=clingo)
                   by default, colnames=None, infer='none', table='df'
    """
    content = get_content(inputfile, isinputpath)
    if datastore == 'rdflib':
        # Create a new RDF dataset using RDFLib
        _require_dependency('rdflib')
        from geist.datastore.rdflib import rdflib_create
        conn = rdflib_create(
            dataset=dataset, 
            inputfile=content, 
            inputformat=inputformat, 
            colnames=None if 'colnames' not in config else config['colnames'], 
            infer='none' if 'infer' not in config else config['infer']
        )
    elif datastore == 'duckdb':
        # Create a new SQL dataset using DuckDB
        _require_dependency('duckdb')
        from geist.datastore.duckdb import duckdb_create
        conn = duckdb_create(
            dataset=dataset, 
            inputfile=content, 
            inputformat=inputformat, 
            table='df' if 'table' not in config else config['table']
        )
    elif datastore == 'clingo':
        # Create a new ASP dataset using Clingo
        _require_dependency('clingo')
        from geist.datastore.clingo import clingo_create
        conn = clingo_create(
            dataset=dataset,
            inputfile=content,
            inputformat=inputformat,
            predicate='isfirstcol' if 'predicate' not in config else config['predicate'],
            programname='base' if 'programname' not in config else config['programname']
        )
    else:
        raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
    return conn

