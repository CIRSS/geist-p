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

# fish.duckdb is a dataset for Hamming numbers containing the "edges" table with "startnode", "label", and "endnode" columns
# student.duckdb is a dataset for student records containing the "student" table with "sid", "sname", and "advisor" columns
# citation.pkl is a dataset for papers and citations containing two predicates, i.e., :writtenBy and :cites

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex1: without geist' << END_CELL

python3 << END_PYTHON

import duckdb

# create a connection to a file called fish.duckdb
fish_graph = duckdb.connect(".geistdata/duckdb/fish.duckdb")

# query the database
edges = fish_graph.sql("""
SELECT startnode, label, endnode FROM edges LIMIT 5;
""").df()

# print all edges in the format of "startnode -- label --> endnode"
for _, edge in edges.iterrows():
    print("{startnode} -- {label} --> {endnode}".format(startnode=edge["startnode"], label=edge["label"], endnode=edge["endnode"]))

# close the connection
fish_graph.close()

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex1: with geist CLI' << END_CELL

geist report << __END_TEMPLATE__

{% query "fish", datastore="duckdb", isfilepath=False as edges %}
    SELECT startnode, label, endnode FROM edges LIMIT 5;
{% endquery %}

{%- for _, edge in edges.iterrows() %}
    {{ edge["startnode"] }} -- {{ edge["label"] }} --> {{ edge["endnode"] }}
{% endfor -%}

__END_TEMPLATE__

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex1: with geist report Python API' << END_CELL

python3 << END_PYTHON

from geist import report

template = """
{% query "fish", datastore="duckdb", isfilepath=False as edges %}
    SELECT startnode, label, endnode FROM edges LIMIT 5;
{% endquery %}

{%- for _, edge in edges.iterrows() %}
    {{ edge["startnode"] }} -- {{ edge["label"] }} --> {{ edge["endnode"] }}
{% endfor -%}

"""

print(report(inputfile=template, isinputpath=False))


END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex1: with geist Python API' << END_CELL

python3 << END_PYTHON

import geist

# connect to the fish dataset in DuckDB and create a Connection object
fish_graph = geist.Connection.connect(datastore="duckdb", dataset="fish")

# query the dataset
edges = fish_graph.query(
    inputfile="SELECT startnode, label, endnode FROM edges LIMIT 5;",
    isinputpath=False,
    hasoutput=False
)

# print all edges in the format of "startnode -- label --> endnode"
for _, edge in edges.iterrows():
    print("{startnode} -- {label} --> {endnode}".format(startnode=edge["startnode"], label=edge["label"], endnode=edge["endnode"]))

# close the connection
fish_graph.close()

END_PYTHON

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
students = duckdb.connect(".geistdata/duckdb/student.duckdb")

# query the database
adams_students = students.sql("""
SELECT sid, sname FROM student WHERE advisor = 'Dr. Adams';
""").df()

# close the duckdb connection
students.close()

with open(".geistdata/rdflib/citation.pkl", mode='rb') as f:
    citations = pickle.load(f)["rdf_graph"]

# print all edges in the format of "sid: sname"
for _, student in adams_students.iterrows():
    print("{sname} (student ID is {sid}) has published the following papers:".format(sid=student["sid"], sname=student["sname"]))

    papers_and_citation_counts = query2df(citations, """
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
    """.format(sid=str(student["sid"])))
    
    for _, paper in papers_and_citation_counts.iterrows():
        print("- {pid} has {count} citations.".format(pid=paper["pid"].replace("http://demo.com/paper#", ""), count=paper["num_of_citations"]))

    print()

citations.close()

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex2: with geist CLI' << END_CELL

geist report << __END_TEMPLATE__

**************************************************************
*                    Dr. Adams's students                    *
**************************************************************

{% query "student", datastore="duckdb", isfilepath=False as adams_students %}
    SELECT sid, sname FROM student WHERE advisor = 'Dr. Adams';
{% endquery %}

{%- for _, student in adams_students.iterrows() %}
{{ student["sname"] }} (student ID is {{ student["sid"] }}) has published the following papers:
{% query "citation", datastore="rdflib", isfilepath=False as papers_and_citation_counts %}
    PREFIX : <http://demo.com/>
    PREFIX student: <http://demo.com/student#>
    PREFIX paper: <http://demo.com/paper#>

    SELECT ?pid (COUNT(DISTINCT ?pid1) AS ?num_of_citations)
    WHERE {
        ?pid :writtenBy student:{{ student["sid"] }} .

        OPTIONAL { ?pid1 :cites ?pid . }
    }
    GROUP BY ?pid
    ORDER BY ?pid
{% endquery %}
{%- map mappings="data/mappings.json", isfilepath=False as mapped_papers_and_citation_counts %} {{ papers_and_citation_counts | df2json }} {% endmap %}
{% for _, paper in mapped_papers_and_citation_counts.iterrows() %}
    - {{ paper["pid"] }} has {{ paper["num_of_citations"] }} citations.
{% endfor %}

{% endfor %}

__END_TEMPLATE__

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'ex2: with geist Python API' << END_CELL

python3 << END_PYTHON

import geist

print("""
**************************************************************
*                    Dr. Adams's students                    *
**************************************************************
""")

# connect to datasets and create Connection objects
students = geist.Connection.connect(datastore="duckdb", dataset="student")
citations = geist.Connection.connect(datastore="rdflib", dataset="citation")

# query the student dataset
adams_students = students.query(
    inputfile="SELECT sid, sname FROM student WHERE advisor = 'Dr. Adams';",
    isinputpath=False,
    hasoutput=False
)
# print all edges in the format of "sid: sname"
for _, student in adams_students.iterrows():
    print("{sname} (student ID is {sid}) has published the following papers:".format(sid=student["sid"], sname=student["sname"]))

    papers_and_citation_counts = citations.query(
        inputfile="""
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
        """.format(sid=str(student["sid"])),
        isinputpath=False,
        hasoutput=False)
    
    for _, paper in papers_and_citation_counts.iterrows():
        print("- {pid} has {count} citations.".format(pid=paper["pid"].replace("http://demo.com/paper#", ""), count=paper["num_of_citations"]))

    print()

# close the connections
students.close()
citations.close()

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'move datasets back' << END_CELL

mv .geistdata/duckdb/* data/
mv .geistdata/rdflib/citation.pkl data/
rm -rf .geistdata

END_CELL

# ------------------------------------------------------------------------------