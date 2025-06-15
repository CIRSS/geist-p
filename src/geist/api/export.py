def geist_export(datastore, dataset, hasoutput, config={}):
    """
    Export a dataset.
    :param datastore: a string. Backend datastores, i.e., rdflib, duckdb, or clingo
    :param dataset: a string represents the name of the dataset to be exported OR a GeistGraph object OR a DuckPyConnection object
    :param hasoutput: bool. True to export as a file or print it out
    :param config: a dictionary with 'outputroot', 'outputfile', 'outputformat', and 'table' keys
                   the 'table' key is required when datastore=duckdb
    :return data: an RDF graph object (when datastore=rdflib) OR a Pandas data frame (when datastore=duckdb)
    """
    outputroot = './' if 'outputroot' not in config else config['outputroot']
    outputfile = None if 'outputfile' not in config else config['outputfile']
    if datastore == 'rdflib':
        # Export an RDF dataset
        from geist.datastore.rdflib import rdflib_export
        data = rdflib_export(
            dataset=dataset, 
            hasoutput=hasoutput, 
            outputroot=outputroot, 
            outputfile=outputfile, 
            outputformat='nt' if 'outputformat' not in config else config['outputformat']
        )
        conn = None # This field is a placeholder only
    elif datastore == 'duckdb':
        # Export a SQL dataset
        from geist.datastore.duckdb import duckdb_export
        (data, conn) = duckdb_export(
            dataset=dataset, 
            table='df' if 'table' not in config else config['table'], 
            hasoutput=hasoutput, 
            outputroot=outputroot, 
            outputfile=outputfile, 
            outputformat='csv' if 'outputformat' not in config else config['outputformat']
        )
    elif datastore == 'clingo':
        # Export an ASP dataset
        from geist.datastore.clingo import clingo_export
        (data, conn) = clingo_export(
            dataset=dataset,
            predicate=None if 'predicate' not in config else config['predicate'],
            hasoutput=hasoutput, 
            outputroot=outputroot,
            outputfile=outputfile,
            outputformat='lp' if 'outputformat' not in config else config['outputformat']
        )
    else:
        raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
    return data, conn
