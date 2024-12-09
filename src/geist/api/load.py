from geist.tools.utils import get_content

def geist_load(datastore, dataset, inputfile, inputformat, isinputpath, config={}):
    """
    Import data into a dataset
    :param datastore: a string. Backend datastores, i.e., rdflib, duckdb
    :param dataset: a string. Name of the dataset to load an object, e.g., a Pandas data frame
    :param inputfile: a string. File to be loaded
    :param inputformat: a string. Format of the file to be loaded
    :param isinputpath: bool. True if the inputfile is the file path, otherwise the inputfile is the content
    :param config: a dictionary with the 'colnames' key (when datastore=rdflib and inputformat='csv') OR the 'table' key (when datastore=duckdb)
    """
    content = get_content(inputfile, isinputpath)
    if datastore == 'rdflib':
        # Import data into a RDF dataset
        from geist.datastore.rdflib import rdflib_load
        colnames = None if 'colnames' not in config else config['colnames']
        rdflib_load(dataset=dataset, inputfile=content, inputformat=inputformat, colnames=colnames)
    elif datastore == 'duckdb':
        # Import data into a SQL dataset
        from geist.datastore.duckdb import duckdb_load
        if 'table' not in config:
            raise ValueError("Please specify the value of 'table' in config")
        duckdb_load(dataset=dataset, inputfile=content, inputformat=inputformat, table=config['table'])
    else:
        raise ValueError("Invalid datastore. Only rdflib and duckdb are supported for now.")
    return
