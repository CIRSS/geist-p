from geist.api.create import geist_create
from geist.api.destroy import geist_destroy
from geist.api.export import geist_export
from geist.api.graph import geist_graph
from geist.api.load import geist_load
from geist.api.query import geist_query
from geist.tools.utils import _require_dependency

class Connection:
    def __init__(self, datastore, dataset, conn=None):
        # Initialize the connection to the dataset
        self.datastore = datastore
        self.dataset = dataset
        self.conn = conn # a DuckPyConnection object or a GeistGraph object or a Control object
    
    @classmethod
    def connect(cls, datastore, dataset):
        """
        Create a new Connection instance to connect to a dataset.
        :param datastore: a string. Backend datastores, i.e., rdflib, duckdb, or clingo
        :param dataset: a string. Name of the dataset. You can pass ':memory:' to create
                        a dataset existing only in memory, and open a connection to it.
        :return connection: a Connection object.
        """
        if datastore == 'rdflib':
            _require_dependency('rdflib')
            from geist.datastore.rdflib import load_rdf_dataset
            # Connect to an RDF dataset using RDFLib
            if dataset == ':memory:':
                conn = None
            else:
                (rdf_graph, infer) = load_rdf_dataset(dataset)
                conn = {"rdf_graph": rdf_graph, "infer": infer}
        elif datastore == 'duckdb':
            _require_dependency('duckdb')
            from geist.datastore.duckdb import load_sql_dataset
            if dataset == ':memory:':
                import duckdb
                conn = duckdb.connect(dataset)
            else:
                conn = load_sql_dataset(dataset)
        elif datastore == 'clingo':
            _require_dependency('clingo')
            from geist.datastore.clingo import load_asp_dataset
            if dataset == ':memory:':
                import clingo
                conn = clingo.control.Control()
            else:
                conn = load_asp_dataset(dataset)
        else:
            raise ValueError("Invalid datastore. Only rdflib, duckdb, and clingo are supported for now.")
        connection = cls(datastore, dataset, conn)
        return connection

    def create(self, inputfile, inputformat, isinputpath, config={}):
        if self.conn:
            raise ValueError('You have already connected to an existing dataset')
        self.conn = geist_create(
            datastore=self.datastore,
            dataset=self.dataset,
            inputfile=inputfile, 
            inputformat=inputformat,
            isinputpath=isinputpath,
            config=config
        )
        return

    def close(self):
        if self.conn and self.datastore == 'duckdb':
            self.conn.close()
        self.datastore = None
        self.dataset = None
        self.conn = None
        return
    
    def destroy(self):
        if self.dataset and self.dataset != ':memory:':
            geist_destroy(
                datastore=self.datastore,
                dataset=self.dataset,
                quiet=False
            )
        self.close()
        return
    
    def export(self, hasoutput, config={}):
        if not self.conn:
            raise ValueError('You have not connected to any dataset yet. Please use the connect method first.')
        (data, _) = geist_export(
            datastore=self.datastore,
            dataset=self.conn,
            hasoutput=hasoutput,
            config=config
        )
        return data

    def graph(self, hasoutput, config={}):
        if not self.conn:
            raise ValueError('You have not connected to any dataset yet')
        G = geist_graph(
            datastore=self.datastore, 
            dataset=self.conn, 
            hasoutput=hasoutput, 
            config=config
        )
        return G

    def load(self, inputfile, inputformat, isinputpath, config={}):
        if not self.conn:
            raise ValueError('You have not connected to any dataset yet. Please use the connect method first.')
        config['inmemory'] = True if self.dataset == ':memory:' else False
        config['datasetname'] = None if self.dataset == ':memory' else self.dataset # Add dataset name to save as a file
        self.conn = geist_load(
            datastore=self.datastore, 
            dataset=self.conn, 
            inputfile=inputfile, 
            inputformat=inputformat, 
            isinputpath=isinputpath, 
            config=config)
        return
    
    def query(self, inputfile, isinputpath, hasoutput, config={}):
        if not self.conn:
            raise ValueError('You have not connected to any dataset yet. Please use the connect method first.')
        (res, _) = geist_query(
            datastore=self.datastore, 
            dataset=self.conn, 
            inputfile=inputfile, 
            isinputpath=isinputpath, 
            hasoutput=hasoutput, 
            config=config
        )
        return res
