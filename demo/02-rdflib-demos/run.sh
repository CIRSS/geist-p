#!/usr/bin/env bash

# ------------------------------------------------------------------------------

bash_cell available_commands << END_CELL

geist --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_command << END_CELL

geist create --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_stdin << END_CELL

geist create rdflib -d test -iformat nt << __END_INPUT__

<http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://example.com/drewp> <http://example.com/says> "Hello World" .

__END_INPUT__

geist export rdflib -d test | sort

geist destroy rdflib -d test

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_file << END_CELL

geist create rdflib -d test -ifile data/tro.jsonld

ls -R .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_command << END_CELL

geist load --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_dataset_test << END_CELL

geist load rdflib -d test -ifile data/tro.jsonld

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_command << END_CELL

geist destroy --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_dataset_test << END_CELL

geist destroy rdflib -d test

ls -R .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_dataset_kb << END_CELL

geist create rdflib -ifile data/tro.jsonld

ls -R .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_command << END_CELL

geist export --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_dataset_kb << END_CELL

geist export rdflib | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell graph_command << END_CELL

geist graph --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell graph_dataset_kb << END_CELL

geist graph rdflib -m data/mappings.json -oroot products -ofile kb -oformat none -oformat png -oformat gv

END_CELL

# ------------------------------------------------------------------------------

bash_cell query_command << END_CELL

geist query --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell file_query_dataset_kb << END_CELL

geist query rdflib --inputfile data/query

END_CELL

# ------------------------------------------------------------------------------

bash_cell stdin_query_dataset_kb << END_CELL

geist query rdflib << __END_QUERY__

SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o
}
ORDER BY ?s ?p ?o

__END_QUERY__

geist destroy rdflib -d kb

END_CELL

# ------------------------------------------------------------------------------

bash_cell query_dataset_to_newkb << END_CELL

geist create rdflib -d kb -ifile data/tro.jsonld

geist query rdflib -d kb --outputfile products/qres.csv << __END_QUERY__

SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o .
    FILTER ( ?p = trov:sha256 ) .
}
ORDER BY ?s ?p ?o

__END_QUERY__

geist create rdflib -d newkb -ifile products/qres.csv -iformat csv --colnames "[['s','p','o']]"

geist query rdflib -d newkb << __END_QUERY__

SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o
}
ORDER BY ?s ?p ?o

__END_QUERY__

geist destroy rdflib -d newkb
geist destroy rdflib -d kb

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_command << END_CELL

geist report --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_create_kb << END_CELL

geist report << END_TEMPLATE

{% create datastore="rdflib", inputformat="nt", isfilepath=False %}
    <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
    <http://example.com/drewp> <http://example.com/says> "Hello World" .
{% endcreate %}

{% query datastore="rdflib", isfilepath=False as all_triples %}
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o
    }
    ORDER BY ?s ?p ?o
{% endquery %}

{% for _, row in all_triples.iterrows() %}
    Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
{% endfor %}

{% destroy datastore="rdflib" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_create_test << END_CELL

geist report << END_TEMPLATE

{% create "test", datastore="rdflib", inputformat="csv", colnames="[['s', 'p', 'o']]", isfilepath=False %}
s,p,o
<http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
<http://example.com/drewp>,<http://example.com/says>,"Hello World"
{% endcreate %}

{% query "test", datastore="rdflib", isfilepath=False as all_triples %}
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o
    }
    ORDER BY ?s ?p ?o
{% endquery %}

{% for _, row in all_triples.iterrows() %}
    Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
{% endfor %}

{% destroy "test", datastore="rdflib" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_create_kb_file << END_CELL

geist report -oroot products << END_TEMPLATE

{% create datastore="rdflib", inputformat="csv", colnames="[['s', 'p', 'o']]" %} data/kb.csv {% endcreate %}

{% query datastore="rdflib" as all_triples %} data/query {% endquery %}

{%- html "report.html" %}
<body>
    <u>List</u>
    {% for _, row in all_triples.iterrows() %}
        {%- set s = row["s"] | process_str_for_html %}
        {%- set p = row["p"] | process_str_for_html %}
        {%- set o = row["o"] | process_str_for_html %}
        <li>Subject: {{ s }}, Predicate: {{ p }}, Object: {{ o }}.</li>
    {% endfor -%}<br>
    <u>Visualization</u><br>
    {% img src="rdf.svg" %}
        {% graph datastore="rdflib" %}
    {% endimg %}
</body>
{%- endhtml %}

{% destroy datastore="rdflib" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_with_nested_rules << END_CELL

geist report << END_TEMPLATE

{%- use "templates.geist" %}

{%- create "kb1", datastore="rdflib", inputformat="nt", isfilepath=False %}
    <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
    <http://example.com/drewp> <http://example.com/says> "Hello World" .
    <http://example.com/drewp> <http://example.com/says> "What a Nice Day" .
    <http://example.com/drewp> <http://example.com/feels> "Happy" .
{% endcreate %}

{%- create "kb2", datastore="rdflib", inputformat="nt", isfilepath=False %}
    <http://example.com/test> <http://example.com/p1> <http://example.com/says>.
    <http://example.com/test> <http://example.com/p2> <http://example.com/feels>.
{% endcreate %}

{%- query "kb1", datastore="rdflib", isfilepath=False as all_triples %}
    SELECT ?s ?o
    WHERE {
        ?s ?p ?o
        FILTER (?p IN ({% query "kb2", datastore="rdflib", isfilepath=False as res %}
                            SELECT ?p 
                            WHERE {?s <http://example.com/p1> ?p}
                        {% endquery %}
                        {{", ".join(res["p"])}}))
    }
    ORDER BY ?s ?o
{% endquery %}

{% for _, row in all_triples.iterrows() %}
    {% format_output row["s"], row["o"] %}.
{%- endfor %}

{%- query_with_args %}

{%- destroy "kb1", datastore="rdflib" %}
{%- destroy "kb2", datastore="rdflib" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------
