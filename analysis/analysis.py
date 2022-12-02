import pandas as pd


def tidy_table(df, listy_cols):
    """Shape df with list-containing cells into 'tidy' format"""
    for listy_col in listy_cols:
        s = df[listy_col].apply(pd.Series).stack().reset_index(level=1, drop=True)
        s.name = listy_col.rstrip('s')
        df = df.drop(listy_col, axis=1).join(s)
    return df
