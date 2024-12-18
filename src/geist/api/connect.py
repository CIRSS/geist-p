from geist.api.create import geist_create
from geist.api.destroy import geist_destroy
from geist.api.export import geist_export
from geist.api.graph import geist_graph
from geist.api.load import geist_load
from geist.api.query import geist_query
from geist.datastore.rdflib import load_rdf_dataset
from geist.datastore.duckdb import load_sql_dataset
import duckdb

class Connection:
    def __init__(self, datastore, dataset, conn=None):
        # Initialize the connection to the dataset
        self.datastore = datastore
        self.dataset = dataset
        self.conn = conn
    
    @classmethod
    def connect(cls, datastore, dataset):
        """
        Create a new Connection instance to connect to a dataset.
        :param datastore: a string. Backend datastores, i.e., rdflib, duckdb
        :param dataset: a string. Name of the dataset. You can pass ':memory:' to create
                        a dataset existing only in memory, and open a connection to it.
        :return connection: a Connection object.
        """
        if datastore == 'rdflib':
            # Connect to an RDF dataset using RDFLib
            if dataset == ':memory:':
                conn = None
            else:
                (rdf_graph, infer) = load_rdf_dataset(dataset)
                conn = {"rdf_graph": rdf_graph, "infer": infer}
        elif datastore == 'duckdb':
            if dataset == ':memory:':
                conn = duckdb.connect(dataset)
            else:
                conn = load_sql_dataset(dataset)
        else:
            raise ValueError("Invalid datastore. Only rdflib and duckdb are supported for now.")
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
        (data, _) = geist_export(
            datastore=self.datastore,
            dataset=self.conn,
            hasoutput=hasoutput,
            config=config
        )
        return data

    def graph(self, hasoutput, config={}):
        G = geist_graph(
            datastore=self.datastore, 
            dataset=self.conn, 
            hasoutput=hasoutput, 
            config=config
        )
        return G

    def load(self, inputfile, inputformat, isinputpath, config={}):
        config['inmemory'] = True if self.dataset == ':memory:' else False
        self.conn = geist_load(
            datastore=self.datastore, 
            dataset=self.conn, 
            inputfile=inputfile, 
            inputformat=inputformat, 
            isinputpath=isinputpath, 
            config=config)
        return
    
    def query(self, inputfile, isinputpath, hasoutput, config={}):
        (res, _) = geist_query(
            datastore=self.datastore, 
            dataset=self.conn, 
            inputfile=inputfile, 
            isinputpath=isinputpath, 
            hasoutput=hasoutput, 
            config=config
        )
        return res
