from geist.tools.utils import get_content

def geist_create(datastore, dataset, inputfile, inputformat, isinputpath, config={}):
    """
    Create a new dataset.
    :param datastore: a string. Backend datastores, i.e., rdflib, duckdb
    :param dataset: a string. Name of the dataset to be created
    :param inputfile: a string. File to be loaded
    :param inputformat: a string. Format of the file to be loaded
    :param isinputpath: bool. True if the inputfile is the file path, otherwise the inputfile is the content
    :param config: a dictionary with 'colnames' and 'infer' keys (when datastore=rdflib) OR the 'table' key (when datastore=duckdb)
                   by default, colnames=None, infer='none', table='df'
    """
    content = get_content(inputfile, isinputpath)
    if datastore == 'rdflib':
        # Create a new RDF dataset using RDFLib
        from geist.datastore.rdflib import rdflib_create
        rdflib_create(
            dataset=dataset, 
            inputfile=content, 
            inputformat=inputformat, 
            colnames=None if 'colnames' not in config else config['colnames'], 
            infer='none' if 'infer' not in config else config['infer']
        )
    elif datastore == 'duckdb':
        # Create a new SQL dataset using DuckDB
        from geist.datastore.duckdb import duckdb_create
        duckdb_create(
            dataset=dataset, 
            inputfile=content, 
            inputformat=inputformat, 
            table='df' if 'table' not in config else config['table']
        )
    else:
        raise ValueError("Invalid datastore. Only rdflib and duckdb are supported for now.")
    return

