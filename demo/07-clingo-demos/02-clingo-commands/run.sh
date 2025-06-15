#!/usr/bin/env bash

# ------------------------------------------------------------------------------

bash_cell available_commands << END_CELL

geist --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_command << END_CELL

geist create clingo --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_stdin << END_CELL

geist create clingo -d test -iformat lp << __END_INPUT__

friends(a, b).
friends(a, c).

__END_INPUT__

geist export clingo -d test | sort

geist destroy clingo -d test

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_file_lp << END_CELL

geist create clingo -d test -ifile data/friends.lp -iformat lp

geist export clingo -d test | sort

geist destroy clingo -d test

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_file_csv << END_CELL

geist create clingo -d test -ifile data/friends.csv -iformat csv -pred friends

geist export clingo -d test | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_command << END_CELL

geist load clingo --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_dataset_test << END_CELL

geist load clingo -d test -ifile data/new_friends.lp -iformat lp

geist export clingo -d test | sort

ls -R .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_command << END_CELL

geist destroy --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_dataset_test << END_CELL

geist destroy clingo -d test

ls -R .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_dataset_kb << END_CELL

geist create clingo -ifile data/friends.lp

ls -R .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_command << END_CELL

geist export clingo --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_dataset_kb << END_CELL

geist export clingo | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell query_command << END_CELL

geist query clingo --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell file_query_dataset_kb << END_CELL

geist query clingo --inputfile data/query

END_CELL

# ------------------------------------------------------------------------------

bash_cell stdin_query_dataset_kb << END_CELL

geist query clingo << __END_QUERY__

friends(X, Z) :- friends(X, Y), friends(Y, Z), X < Z.
friends(Y, Z) :- friends(X, Y), friends(X, Z), Y < Z.

__END_QUERY__

geist destroy clingo -d kb

END_CELL

# ------------------------------------------------------------------------------

bash_cell query_dataset_to_newkb << END_CELL

geist create clingo -d kb -ifile data/friends.lp

geist query clingo -d kb --outputfile products/qres -pred friends_of_b << __END_QUERY__

friends_of_b(X) :- friends(X, b).
friends_of_b(X) :- friends(b, X).

__END_QUERY__

geist create clingo -d newkb -ifile products/qres#friends_of_b.csv -iformat csv -pred friends_of_b

geist export clingo -d newkb

geist destroy clingo -d newkb
geist destroy clingo -d kb

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_command << END_CELL

geist report --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_create_kb << END_CELL

geist report << END_TEMPLATE

{% create datastore="clingo", inputformat="lp", isfilepath=False %}
    friends(a, b).
    friends(a, c).
{% endcreate %}

{% query datastore="clingo", oformat="df", isfilepath=False as expanded_friends %}
    friends(X, Z) :- friends(X, Y), friends(Y, Z), X < Z.
    friends(Y, Z) :- friends(X, Y), friends(X, Z), Y < Z.
{% endquery %}

{% for _, row in expanded_friends["friends"].iterrows() %}
    {{ row.iloc[0] }} and {{ row.iloc[1] }} are friends.
{% endfor %}

{% destroy datastore="clingo" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_create_kb_file << END_CELL

geist report -oroot products << END_TEMPLATE

{% create datastore="clingo", inputformat="lp" %} data/friends.lp {% endcreate %}

{% query datastore="clingo", oformat="df" as expanded_friends %} data/query {% endquery %}

{%- html "report.html" %}
<body>
    <u>Friends:</u>
    {% for _, row in expanded_friends["friends"].iterrows() %}
        {%- set p1 = row.iloc[0] | process_str_for_html %}
        {%- set p2 = row.iloc[1] | process_str_for_html %}
        <li>{{ p1 }}, {{ p2 }}</li>
    {% endfor -%}<br>
</body>
{%- endhtml %}

{% destroy datastore="clingo" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_with_nested_rules_interact_using_lp << END_CELL

geist report << END_TEMPLATE

{%- create "kb1", datastore="clingo", inputformat="lp", isfilepath=False %}
    friends(a, b).
    friends(a, c).
{% endcreate %}

{%- create "kb2", datastore="clingo", inputformat="lp", isfilepath=False %}
    flag1(a).
    flag1(b).
    flag2(b).
    flag2(c).
{% endcreate %}

{%- load "kb1", datastore="clingo", inputformat="lp", isfilepath=False %}
    {% query "kb2", datastore="clingo", predicate="select", oformat="lp", isfilepath=False as selected_person %}
        select(X) :- flag1(X), flag2(X).
    {% endquery %}
    {{ selected_person }}
{% endload %}

{% query "kb1", datastore="clingo", predicate="friends_of_selected_person", isfilepath=False as friends_of_selected_person %}
    friends_of_selected_person(X) :- friends(X, Y), select(Y).
    friends_of_selected_person(X) :- friends(Y, X), select(Y).
{% endquery %}
{{ friends_of_selected_person }}

{%- destroy "kb1", datastore="clingo" %}
{%- destroy "kb2", datastore="clingo" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_with_nested_rules_interact_using_df << END_CELL

geist report << END_TEMPLATE

{%- create "kb1", datastore="clingo", inputformat="lp", isfilepath=False %}
    friends(a, b).
    friends(a, c).
{% endcreate %}

{%- create "kb2", datastore="clingo", inputformat="lp", isfilepath=False %}
    flag1(a).
    flag1(b).
    flag2(b).
    flag2(c).
{% endcreate %}

{%- load "kb1", datastore="clingo", inputformat="csv", predicate="select", isfilepath=False %}
    {% query "kb2", datastore="clingo", predicate="select", oformat="df", isfilepath=False as selected_person %}
        select(X) :- flag1(X), flag2(X).
    {% endquery %}
    {{ selected_person.to_string(index=False) }}
{% endload %}

{% query "kb1", datastore="clingo", predicate="friends_of_selected_person", isfilepath=False as friends_of_selected_person %}
    friends_of_selected_person(X) :- friends(X, Y), select(Y).
    friends_of_selected_person(X) :- friends(Y, X), select(Y).
{% endquery %}
{{ friends_of_selected_person }}

{%- destroy "kb1", datastore="clingo" %}
{%- destroy "kb2", datastore="clingo" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------

bash_cell report_with_nested_queries_interact_using_lp << END_CELL

geist report << END_TEMPLATE

{%- create "kb1", datastore="clingo", inputformat="lp", isfilepath=False %}
    friends(a, b).
    friends(a, c).
{% endcreate %}

{%- create "kb2", datastore="clingo", inputformat="lp", isfilepath=False %}
    flag1(a).
    flag1(b).
    flag2(a).
    flag2(b).
    flag2(c).
{% endcreate %}

{%- query "kb1", datastore="clingo", predicate="friends_of_selected_person", isfilepath=False %}
    {% query "kb2", datastore="clingo", predicate="select", oformat="lp", isfilepath=False as selected_person %}
        select(X) :- flag1(X), flag2(X).
    {% endquery %}
    {{ selected_person }}
    % friends_of_selected_person(X, Y): X is a friend of the selected person Y
    friends_of_selected_person(X, Y) :- friends(X, Y), select(Y).
    friends_of_selected_person(X, Y) :- friends(Y, X), select(Y).
{% endquery %}
{{ friends_of_selected_person }}

{%- destroy "kb1", datastore="clingo" %}
{%- destroy "kb2", datastore="clingo" %}

END_TEMPLATE

END_CELL

# ------------------------------------------------------------------------------