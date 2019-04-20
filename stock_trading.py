"""Trade Comparison application."""
import json
import csv
import pandas as pd


column_map = {
    'Side': 'buy_sell',
    'ExecutionPrice': 'price',
    'Shares': 'quantity',
    'TradeDate': 'trade_date',
    'Symbol': 'symbol'}


def trade_comparison(json_file, csv_file):
    """Simple trade comparison application.
       Writes out HTML output of trades that do not match.
       The following fields are checked:
            -Stock symbol
            -Buy/Sell
            -Number of shares traded
            -Trade date
            -Price

    Args:
        json_file: Set of trades in JSON format.
        csv_file: Set of trades in CSV format.

    Returns:
        None.

    """
    df1 = process_json(json_file)
    df2 = process_csv(csv_file)
    unmatched_df = compare_dataframes(df1, df2, 'symbol')
    with open("unmatched_trades.html", "w") as f:
        f.write(unmatched_df.to_html(index=False))


def filter_data(data, column_list):
    """Filters input dictionary of non-desired fields"""
    filtered_data = [{k:v for k, v in d.items() if k in column_list} \
                     for d in data]
    return filtered_data


def process_json(json_file):
    """
    Processes JSON input data.
    Loads JSON data into Pandas DataFrame.

    Args:
        json_file: JSON input file.

    Returns:
        Pandas DataFrame.
    """
    with open(json_file) as f:
        data = json.load(f)['data']
    filtered_data = filter_data(data, column_map.values())
    return pd.DataFrame(filtered_data)

def process_csv(csv_file):
    """
    Processes CSV input data.
    Maninpulates data to be consistent with JSON.
    Loads CSV data into Pandas DataFrame.

    Args:
        csv_file: CSV input file.

    Returns:
        Pandas DataFrame.
    """
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    filtered_data = filter_data(data, column_map.keys())
    df = pd.DataFrame(filtered_data)
    df.rename(columns=column_map, inplace=True)
    df['buy_sell'] = df['buy_sell'].apply(lambda x: x[0])
    df = df[list(column_map.values())]
    return df

def compare_dataframes(df1, df2, key):
    """
    Compare two DataFrames based on a key value.
    Iterates over df2 and finds rows matching key value.
    Then checks for a match in the resulting DataFrame.
    Based on matches found, use sets to return non-matching rows.

    Args:
        df1:  Pandas DataFrame #1
        df2:  Pandas DataFrame #2
        key:  Column for base comparison

    Returns:
        DataFrame containing unmatched rows.
    """
    m1 = set()
    m2 = set()
    for index, row in df1.iterrows():
        key_value = row[key]
        df2_rows = df2[df2[key] == key_value]
        for index2, row2 in df2_rows.iterrows():
            if all([row[col] == row2[col] for col in column_map.values()]):
                m1.add(index)
                m2.add(index2)
                break
    return get_difference(df1, m1).append(get_difference(df2, m2))

def get_difference(df, matches):
    """Returns DataFrame of unmatched rows."""
    unmatched = set(range(len(df))).difference(matches)
    return df.iloc[sorted(list(unmatched))]
