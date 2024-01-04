The `component` tag finds connected components in a graph. It will return a dict where the key is the index of a component (e.g., 0, 1, 2, ...) and the value is a connected component. By default, the given string is a file path. However, it can be updated by setting the `isfilepath` field to False. Here are parameters of the `component` tag:

|Name           | Description |
|---------------|-------------|
|`isfilepath`   |A bool value to denote if the given data is a file path or not (by default: True, which denotes the given data is a file path) |
|`edges`        |A list of list. [[start_node1, end_node1], [start_node2, end_node2], ...] or [[start_node1, end_node1, label1], [start_node2, end_node2, label2], ...] where these items are column names |

