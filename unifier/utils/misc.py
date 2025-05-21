from IPython.display import display
from IPython.core.display import HTML
import pandas as pd


def display_df(df: pd.DataFrame, max_rows: int = 10, from_ind=0, to_ind=None, **kwargs):
    if to_ind is None:
        to_ind = len(df)
    display(HTML(df.iloc[from_ind:to_ind].to_html(max_rows=max_rows, **kwargs)))
    