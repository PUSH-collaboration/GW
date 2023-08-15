import numpy as np
import pandas as pd

def load_meta(path, skiprows=0):

    df = pd.read_csv(path, sep="|", engine="python", skiprows=skiprows)

    ### Drop non-data columns, rows that read_csv creates because of markdown format

    # Drop first, last columns (read_csv is cranky that there are '|' separators,
    # but nothing to the left/right, respectively)
    df = df.drop([df.columns[0], df.columns[-1]], axis=1)
    # Drop second row in the file (first in the dataframe)
    # which is all '-----'
    df = df.drop(0, axis=0)

    ### Cleanup column names
    df.columns = df.columns.str.strip()

    ### Cleanup string values
    str_cols = ["Series", "EOS"]
    for sc in str_cols:
        df[sc] = np.char.strip(df[sc].values.astype(str))

    ### Cleanup numeric columns
    for c in df.columns.values:
        if c not in str_cols:
            df[c] = df[c].apply(pd.to_numeric, errors="coerce")

    ### Set useful multi-index
    df.index = pd.MultiIndex.from_arrays([df["Series"], df["Mass"], df["EOS"]])
    df.index.names = ["Series", "Mass", "EOS"]

    df.drop(["Series", "Mass", "EOS"], axis=1, inplace=True)

    return df
