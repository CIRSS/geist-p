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

bash_cell create_dataset_test << END_CELL

../../geist create -d test -ifile data/tro.jsonld

ls -l .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell add_command << END_CELL

../../geist add --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell add_dataset_test << END_CELL

../../geist add -d test -ifile data/tro.jsonld

ls -l .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_command << END_CELL

../../geist destroy --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_dataset_test << END_CELL

../../geist destroy -d test

ls -l .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_dataset_kb << END_CELL

../../geist create -ifile data/tro.jsonld

ls -l .geistdata

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_command << END_CELL

../../geist export --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_dataset_kb << END_CELL

../../geist export

END_CELL

# ------------------------------------------------------------------------------

bash_cell graph_command << END_CELL

../../geist graph --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell graph_dataset_kb_png << END_CELL

../../geist graph -m data/mappings.json -ofile products/kb -oformat png

END_CELL

# ------------------------------------------------------------------------------

bash_cell graph_dataset_kb_gv << END_CELL

../../geist graph -m data/mappings.json -ofile products/kb -oformat gv

END_CELL

# ------------------------------------------------------------------------------

bash_cell query_command << END_CELL

../../geist query --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell query_dataset_kb << END_CELL

../../geist query --file data/query

END_CELL

# ------------------------------------------------------------------------------
