from geist.tools.utils import get_content

def geist_query(datastore, dataset, inputfile, isinputpath, hasoutput, config={}):
    """
    Perform a query on a dataset.
    :param datastore: a string. Backend datastores, i.e., rdflib, duckdb
    :param dataset: a string. Name of the dataset to be queried
    :param inputfile: a string. File containing the query
    :param isinputpath: bool. True if the inputfile is the file path, otherwise the inputfile is the content
    :param hasoutput: bool. True to store the query results as a CSV file or print them out
    :param config: a dictionary with 'outputroot' and 'outputfile' keys
                   by default, outputroot='./', outputfile=None
    :return res: a Pandas data frame containing the query results
    """
    outputroot = './' if 'outputroot' not in config else config['outputroot']
    outputfile = None if 'outputfile' not in config else config['outputfile']
    content = get_content(inputfile, isinputpath)
    if datastore == 'rdflib':
        # Perform a SPARQL query on a dataset
        from geist.datastore.rdflib import rdflib_query
        res = rdflib_query(dataset=dataset, inputfile=content, hasoutput=hasoutput, outputroot=outputroot, outputfile=outputfile)
        conn = None # This field is a placeholder only
    elif datastore == 'duckdb':
        # Perform a SQL query on a dataset
        from geist.datastore.duckdb import duckdb_query
        (res, conn) = duckdb_query(dataset=dataset, inputfile=content, hasoutput=hasoutput, outputroot=outputroot, outputfile=outputfile)
    elif datastore == 'clingo':
        # Perform a Clingo query on a dataset
        from geist.datastore.clingo import clingo_query
        predicate = None if 'predicate' not in config else config['predicate']
        programname = 'base' if 'programname' not in config else config['programname']
        (res, conn) = clingo_query(dataset=dataset, inputfile=content, hasoutput=hasoutput, outputroot=outputroot, outputfile=outputfile, predicate=predicate, programname=programname)
    else:
        raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
    return res, conn
