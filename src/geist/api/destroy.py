def geist_destroy(datastore, dataset, quiet=False):
    """
    Delete a dataset.
    :param datastore: a string. Backend datastores, i.e., rdflib, duckdb, or clingo
    :param dataset: a string. Name of the dataset to be removed
    :param quiet: bool. True to suppress error messages if the provided dataset does not exist
    """
    if datastore == 'rdflib':
        # Delete an RDF dataset
        from geist.datastore.rdflib import rdflib_destroy
        rdflib_destroy(dataset=dataset, quiet=quiet)
    elif datastore == 'duckdb':
        # Delete a SQL dataset
        from geist.datastore.duckdb import duckdb_destroy
        duckdb_destroy(dataset=dataset, quiet=quiet)
    elif datastore == 'clingo':
        from geist.datastore.clingo import clingo_destroy
        clingo_destroy(dataset=dataset, quiet=quiet)
    else:
        raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
    return
