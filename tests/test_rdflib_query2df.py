"""Unit tests for geist.datastore.rdflib.query2df.

Restores coverage of the SPARQL-result -> DataFrame conversion, the layer the
retired Go geist exercised in pkg/geist/tests/sparql_result_test.go (TestResultSet_*).
The empty-group case is a regression test for the rdflib >= 7 KeyError fix
(see LOG / Sessions 2026-06-18).

These are environment-dependent (the verdict turns on the installed rdflib's
GROUP BY semantics), so they should run against the pinned/repro environment.
"""
import pytest
from rdflib import Graph
from geist.datastore.rdflib import query2df


@pytest.fixture
def graph():
    g = Graph()
    g.parse(
        data="""
            @prefix ex: <http://example.org/> .
            ex:a a ex:Item ; ex:name "Alice" ; ex:tag ex:t1 ; ex:tag ex:t2 .
            ex:b a ex:Item ; ex:name "Bob"   ; ex:tag ex:t3 .
        """,
        format="turtle",
    )
    return g


def test_columns_and_rows(graph):
    """Vars become columns; literals and URIs are rendered; rows preserved."""
    df = query2df(
        graph,
        "SELECT ?item ?name WHERE { ?item a ex:Item ; ex:name ?name } ORDER BY ?name",
    )
    assert list(df.columns) == ["item", "name"]
    assert len(df) == 2
    assert df["name"].tolist() == ["Alice", "Bob"]
    assert df["item"].tolist() == ["<http://example.org/a>", "<http://example.org/b>"]


def test_empty_group_by_returns_empty_frame(graph):
    """A GROUP BY whose WHERE matches nothing yields one all-unbound binding
    ([{}]) in rdflib >= 7; query2df must return an empty frame with the SELECT
    vars as columns, not raise KeyError. Regression for the 2026-06-18 fix."""
    df = query2df(
        graph,
        "SELECT ?item (COUNT(?x) AS ?n) WHERE { ?item ex:nonexistent ?x } GROUP BY ?item",
    )
    assert list(df.columns) == ["item", "n"]
    assert len(df) == 0


def test_resultset_vars_rows_columns():
    """Faithful port of the retired Go geist's sparql_result_test.go
    (TestResultSet_Vars / _Row / _Rows / _Column), expressed against query2df's
    DataFrame (the Python analog of geist's Go ResultSet).

    Documented divergence: Go's Row()/Column() returned a URI value raw
    ('http://tmcphill.net/data#x'); geist-p renders URIs wrapped ('<...#x>').
    The test asserts geist-p's actual behavior and records the difference."""
    g = Graph()
    g.parse(
        data="""
            @prefix d: <http://tmcphill.net/data#> .
            d:x d:p "seven" .
            d:y d:p "eight" .
        """,
        format="turtle",
    )
    df = query2df(g, "SELECT ?s ?o WHERE { ?s d:p ?o } ORDER BY ?s")
    # Variables() -> columns
    assert list(df.columns) == ["s", "o"]
    # Row(0), Row(1)  -- URI wrapped in <> (diverges from Go's raw value)
    assert df.iloc[0].tolist() == ["<http://tmcphill.net/data#x>", "seven"]
    assert df.iloc[1].tolist() == ["<http://tmcphill.net/data#y>", "eight"]
    # Column(0), Column(1)
    assert df["s"].tolist() == ["<http://tmcphill.net/data#x>", "<http://tmcphill.net/data#y>"]
    assert df["o"].tolist() == ["seven", "eight"]


def test_partial_unbound_rows_are_kept(graph):
    """A row with some projected vars unbound (here ?name, projected outside the
    GROUP BY) but an aggregate bound must be kept, not dropped as empty."""
    df = query2df(
        graph,
        "SELECT ?name (COUNT(?tag) AS ?n) WHERE { ?item a ex:Item ; ex:tag ?tag } GROUP BY ?item",
    )
    assert list(df.columns) == ["name", "n"]
    assert len(df) == 2
    assert set(df["n"]) == {"1", "2"}
