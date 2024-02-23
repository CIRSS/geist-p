#!/usr/bin/env bash

# ------------------------------------------------------------------------------

bash_cell 'create duckdb fish' << END_CELL

geist destroy duckdb -d fish --quiet
geist destroy rdflib -d fish --quiet
geist destroy rdflib -d subfish --quiet

geist create duckdb -d fish -ifile data/fish.csv -t edges
geist query duckdb -d fish << END_QUERY
    SHOW tables;
END_QUERY

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'report demo' << END_CELL

geist report -oroot products << END_TEMPLATE

{%- use "templates.geist" %}

{% query "fish", datastore="duckdb", isfilepath=False as edges %}
    {% query_duckdb_edges %}
{% endquery %}
{% set edgesdf = edges | json2df %}

{% create "fish", datastore="rdflib", inputformat="nt", isfilepath=False %}
    {%- for _, row in edgesdf.iterrows() %}
        {% format_triples row.startnode, row.edge, row.endnode %}
    {% endfor -%}
{% endcreate %}

{% query "fish", datastore="rdflib", isfilepath=False as res %}
    {% query_rdflib_subfish %}
{% endquery %}
{% set subgraph = res | json2df %}
{% create "subfish", datastore="rdflib", inputformat="nt", isfilepath=False %}
    {% for _, row in subgraph.iterrows() %}
        {% format_subfish row.node1, row.node2, row.node3 %}
    {% endfor %}
{% endcreate %}

{%- html "report.html" %}
{%- head "Geist" %}
<body>
    <h1>Geist Demo for SciPy 2024</h1>
    Suppose we have a <strong>Hamming numbers</strong> (let's call it a <strong>Fish</strong> Graph) dataset stored in DuckDB, which contains a table named <i>edges</i>. The fish dataset was generated based on the following rules:
    <li>The initial starting node is 1.</li>
    <li>The edge can be either 2 or 3 or 5.</li>
    <li>Start node times edge equals to the end node.</li>

    Below shows the first 5 rows of the fish table:
    {{ edgesdf | head | df2htmltable }}

    <h4>1. Visualization of the Fish Graph</h4>
    {% img src="fish.svg", width="80%%" %}
        {% graph "fish", datastore="rdflib", rankdir="LR", mappings="data/mappings.json" %}
    {% endimg %}

    <h4>2. Visualization of the subgraph extracted from the Fish Graph</h4>
    Find all nodes that can be reached from node 5 by following either edge 2 or 3.
    {% img src="subfish.svg", width="80%" %}
        {% graph "subfish", datastore="rdflib", rankdir="LR", mappings="data/mappings.json" %}
    {% endimg %}
</body>
{%- style  %}
{%- endhtml %}

{% destroy "fish", datastore="duckdb" %}
{% destroy "fish", datastore="rdflib" %}
{% destroy "subfish", datastore="rdflib" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------
