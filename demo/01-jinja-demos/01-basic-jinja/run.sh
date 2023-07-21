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

bash_cell 'jinja hello world from external template' << 'END_CELL'

print_template templates/hello.jinja

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
hello_template = environment.get_template("hello.jinja")
hello_world = hello_template.render(name="World")
print(hello_world)

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'jinja hello world with built-in filter' << 'END_CELL'

print_template templates/hello_all_caps_name.jinja

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
hello_template = environment.get_template("hello_all_caps_name.jinja")
hello_world = hello_template.render(name="World")
print(hello_world)

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'jinja hello world with variable assignment' << 'END_CELL'

print_template templates/hello_assigned_variable.jinja

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
hello_template = environment.get_template("hello_assigned_variable.jinja")
hello_world = hello_template.render()
print(hello_world)

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'jinja hello world with variable assignment and trimmed block' << 'END_CELL'

print_template templates/hello_assigned_variable_trimblock.jinja

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
hello_template = environment.get_template("hello_assigned_variable_trimblock.jinja")
hello_world = hello_template.render()
print(hello_world)

END_PYTHON

END_CELL


# ------------------------------------------------------------------------------

bash_cell 'jinja hello world with block trimming default' << 'END_CELL'

print_template templates/hello_assigned_variable.jinja

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"), trim_blocks=True)
hello_template = environment.get_template("hello_assigned_variable.jinja")
hello_world = hello_template.render()
print(hello_world)

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'jinja hello world using global function' << 'END_CELL'

print_template templates/hello_global_functions.jinja

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"),
    trim_blocks=True)

def get_greeting():
    return 'Hello'
environment.globals['get_greeting'] = get_greeting

environment.globals['get_name'] = lambda: 'Planet'

hello_template = environment.get_template("hello_global_functions.jinja")
hello_world = hello_template.render()
print(hello_world)

END_PYTHON

END_CELL

# ------------------------------------------------------------------------------

bash_cell 'jinja nested template expansion' << 'END_CELL'

print_template templates/hello_nested_outer_template.jinja
print_template templates/hello_nested_inner_template.jinja

python3 << END_PYTHON

import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"),
    trim_blocks=True)

def get_name():
    inner_template = environment.get_template("hello_nested_inner_template.jinja")
    return inner_template.render()

environment.globals['get_name'] = get_name
environment.globals['get_greeting'] = lambda: 'Hello'

hello_template = environment.get_template("hello_nested_outer_template.jinja")
hello_world = hello_template.render()
print(hello_world)

END_PYTHON

END_CELL

