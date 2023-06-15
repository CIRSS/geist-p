#!/usr/bin/env bash

# ------------------------------------------------------------------------------

bash_cell 'jinja installation info' << END_CELL

pip show Jinja2

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'imported jinja module info' << END_CELL

python3 << END_PYTHON

import jinja2

print(jinja2)

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'jinja hello world' << END_CELL

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment()
hello_template = environment.from_string("Hello {{ name }}!")
hello_world = hello_template.render(name="World")
print(hello_world)

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'jinja hello world from external template' << END_CELL

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
hello_template = environment.get_template("hello.jinja")
hello_world = hello_template.render(name="World")
print(hello_world)

END_PYTHON

END_CELL
