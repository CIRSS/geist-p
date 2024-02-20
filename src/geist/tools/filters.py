import json
import pandas as pd
from io import StringIO

def json2df(json_str):
    """
    This function is to convert a JSON string to a Pandas data frame
    :param json_str: a JSON string
    :return df: a Pandas data frame
    """
    return pd.read_json(StringIO(json_str))

def json2dict(json_str):
    """
    This function is to convert a JSON string to a dictionary
    :param json_str: a JSON string
    :return df: a dictionary
    """
    return json.loads(json_str)

def dict2df(dict):
    """
    This function is to convert a dictionary to a Pandas data frame
    :param json_str: a dictionary
    :return df: a Pandas data frame
    """
    return pd.DataFrame(dict)

def df2htmltable(df):
    """
    This function is to convert a Pandas data frame to an HTML table
    :param df: a Pandas data frame
    :return html_table: an HTML table
    """
    header = "".join("<th>{header}</th>".format(header=process_str_for_html(header)) for header in df.columns)
    content = ""
    for _, row in df.iterrows():
        content = content + "\n\t\t\t<tr>" + "".join("<td>{cell}</td>".format(cell=process_str_for_html(cell)) for cell in row.tolist())
    html_table = '''
        <table>
            <tr>{header}</tr>
        {content}
        </table>
    '''.format(header=header, content=content)
    return html_table

def process_str_for_html(cell):
    """
    This function is to preprocess a string to be displayed within an HTML document
    :param cell: a string
    :return cell_prpcessed: a string
    """
    return cell.replace("<", "&lt").replace(">", "&gt")

def escape_quotes(txt):
    return txt.replace("'", "\'").replace('"', '\"')
