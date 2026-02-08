from geist.tools.utils import _require_dependency

def geist_graph(datastore, dataset, hasoutput, config={}):
    """
    Visualize a dataset
    :param datastore: a string. Backend datastores, only rdflib is supported for now
    :param dataset: a string. Name of the dataset to be visualized
    :param hasoutput: bool. True to export as a file or print it out
    :param config: a dictionary with 'rankdir', 'mappings', 'on', 'samecolor', 'outputroot', 'outputfile', and 'outputformat' keys
    :return g: a Mermaid string
    """
    if datastore == 'rdflib':
        # Visualize an RDF dataset
        _require_dependency('rdflib')
        from geist.datastore.rdflib import rdflib_graph
        if 'rankdir' in config and config['rankdir'] not in ['TB', 'BT', 'LR', 'RL']:
            raise ValueError("rankdir must be one of ['TB', 'BT', 'LR', 'RL']")
        g = rdflib_graph(
            dataset=dataset, 
            rankdir='TB' if 'rankdir' not in config else config['rankdir'], 
            mappings=None if 'mappings' not in config else config['mappings'], 
            on=None if 'on' not in config else config['on'], 
            samecolor=True if 'samecolor' not in config else config['samecolor'], 
            hasoutput=hasoutput, 
            outputroot='./' if 'outputroot' not in config else config['outputroot'], 
            outputfile='res' if 'outputfile' not in config else config['outputfile'], 
            outputformats=['none'] if 'outputformats' not in config else config['outputformats']
        )
    else:
        raise ValueError("Invalid datastore. Only rdflib is supported for now.")
    return g
