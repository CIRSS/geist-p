#!/usr/bin/env bash

# ------------------------------------------------------------------------------

bash_cell available_commands << END_CELL

../../geist --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_command << END_CELL

../../geist create --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_stdin << END_CELL

../../geist create -d test -iformat nt << __END_INPUT__

<http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://example.com/drewp> <http://example.com/says> "Hello World" .

__END_INPUT__

../../geist export -d test | sort

../../geist destroy -d test

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_file << END_CELL

../../geist create -d test -ifile data/tro.jsonld

ls .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_command << END_CELL

../../geist load --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_dataset_test << END_CELL

../../geist load -d test -ifile data/tro.jsonld

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_command << END_CELL

../../geist destroy --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_dataset_test << END_CELL

../../geist destroy -d test

ls .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_dataset_kb << END_CELL

../../geist create -ifile data/tro.jsonld

ls .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_command << END_CELL

../../geist export --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_dataset_kb << END_CELL

../../geist export | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell graph_command << END_CELL

../../geist graph --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell graph_dataset_kb << END_CELL

../../geist graph -m data/mappings.json -ofile products/kb -oformat none -oformat png -oformat gv

END_CELL

# ------------------------------------------------------------------------------

bash_cell query_command << END_CELL

../../geist query --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell file_query_dataset_kb << END_CELL

../../geist query --file data/query

END_CELL

# ------------------------------------------------------------------------------

bash_cell stdin_query_dataset_kb << END_CELL

../../geist query << __END_QUERY__

SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o
}
ORDER BY ?s ?p ?o

__END_QUERY__

../../geist destroy -d kb

END_CELL

# ------------------------------------------------------------------------------

bash_cell query_dataset_to_newkb << END_CELL

../../geist create -d kb -ifile data/tro.jsonld

../../geist query -d kb --outputfile products/qres.csv << __END_QUERY__

SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o .
    FILTER ( ?p = trov:sha256 ) .
}
ORDER BY ?s ?p ?o

__END_QUERY__

../../geist create -d newkb -ifile products/qres.csv -iformat csv --colnames "[['s','p','o']]"

../../geist query -d newkb << __END_QUERY__

SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o
}
ORDER BY ?s ?p ?o

__END_QUERY__

../../geist destroy -d newkb
../../geist destroy -d kb

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_command << END_CELL

../../geist report --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_create_kb << END_CELL

../../geist report << END_TEMPLATE

{% create inputformat="nt", isfilepath=False %}
    <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
    <http://example.com/drewp> <http://example.com/says> "Hello World" .
{% endcreate %}

{% query isfilepath=False as res %}
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o
    }
    ORDER BY ?s ?p ?o
{% endquery %}
{% set all_triples = res | json2df %}

{% for _, row in all_triples.iterrows() %}
    Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
{% endfor %}

{% destroy %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_create_test << END_CELL

../../geist report << END_TEMPLATE

{% create dataset="test", inputformat="csv", colnames="[['s', 'p', 'o']]", isfilepath=False %}
s,p,o
<http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
<http://example.com/drewp>,<http://example.com/says>,"Hello World"
{% endcreate %}

{% query "test", isfilepath=False as res %}
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o
    }
    ORDER BY ?s ?p ?o
{% endquery %}
{% set all_triples = res | json2df %}

{% for _, row in all_triples.iterrows() %}
    Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
{% endfor %}

{% destroy "test" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_create_kb_file << END_CELL

../../geist report << END_TEMPLATE

{% create inputformat="csv", colnames="[['s', 'p', 'o']]" %} data/kb.csv {% endcreate %}

{% query as res %} data/query {% endquery %}
{% set all_triples = res | json2df %}

{% for _, row in all_triples.iterrows() %}
    Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
{% endfor %}

{% destroy %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_with_nested_rules << END_CELL

../../geist report << END_TEMPLATE

{%- use "templates.geist" %}

{%- create "kb1", inputformat="nt", isfilepath=False %}
    <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
    <http://example.com/drewp> <http://example.com/says> "Hello World" .
    <http://example.com/drewp> <http://example.com/says> "What a Nice Day" .
    <http://example.com/drewp> <http://example.com/feels> "Happy" .
{% endcreate %}

{%- create "kb2", inputformat="nt", isfilepath=False %}
    <http://example.com/test> <http://example.com/p1> <http://example.com/says>.
    <http://example.com/test> <http://example.com/p2> <http://example.com/feels>.
{% endcreate %}

{%- query "kb1", isfilepath=False as res %}
    SELECT ?s ?o
    WHERE {
        ?s ?p ?o
        FILTER (?p IN ({% query "kb2", isfilepath=False as res %}
                            SELECT ?p 
                            WHERE {?s <http://example.com/p1> ?p}
                        {% endquery %}
                        {% set p = res | json2df %}
                        {{", ".join(p["p"])}}))
    }
    ORDER BY ?s ?o
{% endquery %}
{% set all_triples = res | json2df %}

{% for _, row in all_triples.iterrows() %}
    {% format_output row["s"], row["o"] %}.
{%- endfor %}

{%- query_with_args %}

{%- destroy "kb1" %}
{%- destroy "kb2" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------
