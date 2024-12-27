#!/usr/bin/env bash

# ------------------------------------------------------------------------------

bash_cell 'ex1: create a DuckDB dataset in memory using geist.Connection and export as a Pandas data frame' << END_CELL

python3 << END_PYTHON

import geist

csv_str = """
v1,v2,v3
1,2,3
7,8,9
"""

# create a Connection object
connection = geist.Connection(datastore='duckdb', dataset=':memory:')
connection.create(inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})

# query the dataset
df = connection.export(hasoutput=False, config={'table': 'df'})
# show exported data
print(df)

# close the connection
connection.close()

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex2: create a DuckDB dataset in memory using create and export as a Pandas data frame' << END_CELL

python3 << END_PYTHON

import geist

csv_str = """
v1,v2,v3
1,2,3
7,8,9
"""

# create a Connection object
conn = geist.create(datastore='duckdb', dataset=':memory:', inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})
connection = geist.Connection(datastore='duckdb', dataset=':memory:', conn=conn)

# query the dataset
df = connection.export(hasoutput=False, config={'table': 'df'})
# show exported data
print(df)

# close the connection
connection.close()

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex3: create and store a DuckDB dataset using Connection and query it' << END_CELL

python3 << END_PYTHON

from geist import Connection

csv_str = """
v1,v2,v3
1,2,3
7,8,9
"""

# create a Connection object
connection = Connection(datastore='duckdb', dataset='ex3')
connection.create(inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})

# query the dataset
res = connection.query(
    inputfile="SELECT * FROM df WHERE v1=7;",
    isinputpath=False,
    hasoutput=False
)
print(res)

# close the connection
connection.close()

END_PYTHON

echo "Stored Geist Datasets:"
find .geistdata/ -type f | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex4: create and store a DuckDB dataset using create and query it' << END_CELL

python3 << END_PYTHON

import geist

csv_str = """
v1,v2,v3
1,2,3
7,8,9
"""

# create a DuckDB dataset directly
conn = geist.create(datastore='duckdb', dataset='ex4', inputfile=csv_str, inputformat='csv', isinputpath=False, config={'table': 'df'})
# use the above connection to initialize a Connection object
connection = geist.Connection(datastore='duckdb', dataset='ex3', conn=conn)

# query the dataset
res = connection.query(
    inputfile="SELECT * FROM df WHERE v1=7;",
    isinputpath=False,
    hasoutput=False
)
print(res)

# close the connection
connection.close()

END_PYTHON

echo "Stored Geist Datasets:"
find .geistdata/ -type f | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex5: connect to the dataset created in ex3 and ex4 and delete it' << END_CELL

python3 << END_PYTHON

from geist import Connection

# connect to a Connection object
connection_ex3 = Connection.connect(datastore='duckdb', dataset='ex3')
connection_ex4 = Connection.connect(datastore='duckdb', dataset='ex4')

# close the connection and delete the connected dataset
connection_ex3.destroy()
connection_ex4.destroy()

END_PYTHON

echo "Stored Geist Datasets:"
find .geistdata/ -type f | sort

END_CELL

# ------------------------------------------------------------------------------
