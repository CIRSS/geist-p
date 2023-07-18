#!/usr/bin/env bash

# ------------------------------------------------------------------------------

bash_cell create_command << END_CELL

../../geist create --help

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_two_triples_dataset_infer_none << END_CELL

# Two triples: 1) a is a subclass of b, 2) foo's type is a
../../geist create -ifile data/two_triples.jsonld --infer none

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_two_triples_dataset_infer_none << END_CELL

../../geist export | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_dataset << END_CELL

../../geist destroy

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_empty_dataset_infer_rdfs << END_CELL

../../geist create -ifile data/empty.jsonld --infer rdfs

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_empty_dataset_infer_rdfs << END_CELL

../../geist export | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_two_triples_infer_rdfs << END_CELL

# Two triples: 1) a is a subclass of b, 2) foo's type is a
# Expand two triples with rdfs => expected output: 1) a is a subclass of b, 2) foo's type is a, 3) foo's type is b
../../geist load -ifile data/two_triples.jsonld

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_two_triples_infer_rdfs << END_CELL

../../geist export | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_dataset << END_CELL

../../geist destroy

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_empty_dataset_infer_owl << END_CELL

../../geist create -ifile data/empty.jsonld --infer owl

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_empty_dataset_infer_owl << END_CELL

../../geist export | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_two_triples_infer_owl << END_CELL

../../geist load -ifile data/two_triples.jsonld

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_two_triples_infer_owl << END_CELL

../../geist export | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_dataset << END_CELL

../../geist destroy

END_CELL

# ------------------------------------------------------------------------------

bash_cell create_empty_dataset_infer_rdfs_owl << END_CELL

../../geist create -ifile data/empty.jsonld --infer rdfs_owl

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_empty_dataset_infer_rdfs_owl << END_CELL

../../geist export | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell load_two_triples_infer_rdfs_owl << END_CELL

../../geist load -ifile data/two_triples.jsonld

END_CELL

# ------------------------------------------------------------------------------

bash_cell export_two_triples_infer_rdfs_owl << END_CELL

../../geist export | sort

END_CELL

# ------------------------------------------------------------------------------

bash_cell destroy_dataset << END_CELL

../../geist destroy

END_CELL

# ------------------------------------------------------------------------------

