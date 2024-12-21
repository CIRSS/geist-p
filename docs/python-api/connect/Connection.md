**Connection** class can interact with a dataset with `create`, `close`, `destroy`, `export`, `graph`, `load`, and `query` methods.

## What is a *Connection* class?

A *Connection* class has three attributes:

|Name       |Type    |Description                                | Default   |
|---------- |------- |------------------------------------------ |---------- |
|datastore  |string  |A backend datastore, i.e., `rdflib` or `duckdb`|`[required]` |
|dataset    |string  |Name of the dataset. Note that `:memory:` is a reserved value for datasets that exist only in memory|`[required]` |
|conn       |object  |A `DuckPyConnection` object OR a `GeistGraph` object |`None`       |

## How to instantiate a *Connection* class?

If the dataset exists, the *Connection* class can be instantiated using its **connect** method:

```py
# create a Connection object to an existing dataset named test
connection = geist.Connection.connect(datastore='duckdb', dataset='test')
```

If the dataset does not exist, there are two approaches to create and connect:

??? example "Approach 1: use the **create** function, then initialize the **Connection class**"

    ??? info "create function"

        --8<-- "python-api/create.md"

    ```py
    import geist

    csv_str = """
    v1,v2,v3
    1,2,3
    7,8,9
    """

    # create a Connection object
    conn = geist.create(datastore='duckdb', dataset=':memory:', inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})
    connection = geist.Connection(datastore='duckdb', dataset=':memory:', conn=conn)
    ```

??? example "Approach 2: use the **create** method of the **Connection class**"

    ??? info "create method of the Connection class"

        --8<-- "python-api/connect/create.md"

    ```py
    import geist

    csv_str = """
    v1,v2,v3
    1,2,3
    7,8,9
    """

    # create a Connection object
    connection = geist.Connection(datastore='duckdb', dataset=':memory:')
    connection.create(inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})
    ```

## How to interact with a *Connection* class?

Once a *Connection* class is instantiated, we can interact with it using `close`, `destroy`, `export`, `graph`, `load`, and `query` methods.

??? info "**close** method"

    --8<-- "python-api/connect/close.md"

??? info "**destroy** method"

    --8<-- "python-api/connect/destroy.md"

??? info "**export** method"

    --8<-- "python-api/connect/export.md"

??? info "**graph** method"

    --8<-- "python-api/connect/graph.md"

??? info "**load** method"

    --8<-- "python-api/connect/load.md"

??? info "**query** method"

    --8<-- "python-api/connect/query.md"

