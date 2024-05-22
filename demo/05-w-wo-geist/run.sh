#!/usr/bin/env bash

# ------------------------------------------------------------------------------

bash_cell 'relocate datasets' << END_CELL

# move fish.duckdb and student.duckdb to the .geistdata/duckdb/ folder
mkdir -p .geistdata/duckdb
mv data/fish.duckdb .geistdata/duckdb/
mv data/student.duckdb .geistdata/duckdb/

# move citation.pkl to the .geistdata/rdflib/ folder
mkdir .geistdata/rdflib
mv data/citation.pkl .geistdata/rdflib/

# fish.duckdb contains table named edges with startnode, edge, endnode columns
# student.duckdb contains table named student with sid, sname, advisor columns
# citation.pkl contains two predicates, i.e., :writtenBy and :cites

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex1: without geist' << END_CELL

python3 << END_PYTHON

import duckdb

# create a connection to a file called fish.duckdb
conn = duckdb.connect(".geistdata/duckdb/fish.duckdb")

# query the database
res = conn.sql("""
SELECT startnode, edge, endnode FROM edges LIMIT 5;
""").df()

# Print all edges in the format of "startnode -- edge --> endnode"
for _, row in res.iterrows():
    print("{startnode} -- {edge} --> {endnode}".format(startnode=row["startnode"], edge=row["edge"], endnode=row["endnode"]))

# close the connection
conn.close()

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex1: with geist' << END_CELL

geist report << __END_TEMPLATE__

{% query "fish", datastore="duckdb", isfilepath=False as edges %}
    SELECT startnode, edge, endnode FROM edges LIMIT 5;
{% endquery %}

{%- for _, row in edges.iterrows() %}
    {{ row["startnode"] }} -- {{ row["edge"] }} --> {{ row["endnode"] }}
{% endfor -%}

__END_TEMPLATE__

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex2: without geist' << END_CELL

python3 << END_PYTHON

import duckdb, pickle, json
import pandas as pd
from io import StringIO
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer

def query2df(rdf_graph, query):
    """
    This function is to run query on a RDF graph
    :param rdf_graph: a RDF Graph object supported by RDFLib
    :param query: string. A query to be applied to the given RDF graph
    :return res: a Pandas data frame. Results of the query
    """
    file = StringIO()
    JSONResultSerializer(rdf_graph.query(query)).serialize(file)
    res_json = json.loads(file.getvalue())
    bindings = res_json["results"]["bindings"]
    colnames = res_json["head"]["vars"]
    if bindings:
        # type: uri, literal, or bnode
        res_df = pd.DataFrame(bindings).apply(lambda row: row.apply(lambda x: "<"+x["value"]+">" if x["type"] == "uri" else x["value"] if x["type"] == "literal" else "_:"+x["value"]), axis=1)[colnames]
    else:
        res_df = pd.DataFrame(columns=colnames)
    return res_df[colnames]

print("""
**************************************************************
*                    Dr. Adams's students                    *
**************************************************************
""")

# create a connection to a file called student.duckdb
conn = duckdb.connect(".geistdata/duckdb/student.duckdb")

# query the database
res1 = conn.sql("""
SELECT sid, sname FROM student WHERE advisor = 'Dr. Adams';
""").df()

# close the duckdb connection
conn.close()

with open(".geistdata/rdflib/citation.pkl", mode='rb') as f:
    graph_object = pickle.load(f)
rdf_graph, infer = graph_object["rdf_graph"], graph_object["infer"]

# Print all edges in the format of "sid: sname"
for _, row in res1.iterrows():
    print("{sname} (student ID is {sid}) has published the following papers:".format(sid=row["sid"], sname=row["sname"]))

    res2 = query2df(rdf_graph, """
        PREFIX : <http://demo.com/>
        PREFIX student: <http://demo.com/student#>
        PREFIX paper: <http://demo.com/paper#>

        SELECT ?pid (COUNT(DISTINCT ?pid1) AS ?num_of_citations)
        WHERE {{
            ?pid :writtenBy student:{sid} .

            OPTIONAL {{ ?pid1 :cites ?pid . }}
        }} 
        GROUP BY ?pid
        ORDER BY ?pid
    """.format(sid=str(row["sid"])))
    
    for _, row in res2.iterrows():
        print("- {pid} has {count} citations.".format(pid=row["pid"].replace("http://demo.com/paper#", ""), count=row["num_of_citations"]))

    print()

rdf_graph.close()

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex2: with geist' << END_CELL

geist report << __END_TEMPLATE__

**************************************************************
*                    Dr. Adams's students                    *
**************************************************************

{% query "student", datastore="duckdb", isfilepath=False as students %}
    SELECT sid, sname FROM student WHERE advisor = 'Dr. Adams';
{% endquery %}

{%- for _, row1 in students.iterrows() %}
{{ row1["sname"] }} (student ID is {{ row1["sid"] }}) has published the following papers:
{% query "citation", datastore="rdflib", isfilepath=False as citations %}
    PREFIX : <http://demo.com/>
    PREFIX student: <http://demo.com/student#>
    PREFIX paper: <http://demo.com/paper#>

    SELECT ?pid (COUNT(DISTINCT ?pid1) AS ?num_of_citations)
    WHERE {
        ?pid :writtenBy student:{{ row1["sid"] }} .

        OPTIONAL { ?pid1 :cites ?pid . }
    }
    GROUP BY ?pid
    ORDER BY ?pid
{% endquery %}
{%- map mappings="data/mappings.json", isfilepath=False as mapped_citations %} {{ citations | df2json }} {% endmap %}
{% for _, row2 in mapped_citations.iterrows() %}
    - {{ row2["pid"] }} has {{ row2["num_of_citations"] }} citations.
{% endfor %}

{% endfor %}

__END_TEMPLATE__

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'move datasets back' << END_CELL

mv .geistdata/duckdb/* data/
mv .geistdata/rdflib/citation.pkl data/
rm -rf .geistdata

END_CELL

# ------------------------------------------------------------------------------