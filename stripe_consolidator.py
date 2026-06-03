"""
The script automatically consolidates Stripe monthly finanacial statements into a single Pandas dataframe for easier readibility.

Supports:
* Old stripe export format (2021-2023)
* New Stripe export format (2024 onwards)

Any future year folders will be picked up automatically
"""
import glob
import os
import re
import pandas as pd

def str_to_datetime(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """
    converting a named series to datetime from str
    args:
        df: pd.Dataframe
        name: str
    returns:
        pd.DataFrame
    """
    if name in df.columns:
        df[name] = pd.to_datetime(df[name], format="mixed", errors="raise")
    
    return df 

def new_format_data(filepaths: str, column_names: list) -> pd.DataFrame:
    """
    create a list of dataframes in the new format specifying the filepath and column names str
    args:
        filepath: str
        column_names: list columns in the dataframe
    returns:
        df of all data
    """
    if not filepaths:
        return pd.DataFrame()
    
    data = [pd.read_csv(file, sep=",", usecols=column_names) for file in filepaths]
    
    return pd.concat(data, axis=0, ignore_index=True)

def old_format_data(filepath: str, column_names: list) -> pd.DataFrame:
    """
    create a list of dataframes in the old format specifying the filepath and column names str
    """
    data_2021 = [
        pd.read_csv("../stripe-statements/2021_06_to_2021_12/June_2021.csv", usecols=column_names),
        pd.read_csv("../stripe-statements/2021_06_to_2021_12/July_2021.csv", usecols=column_names),
        pd.read_csv("../stripe-statements/2021_06_to_2021_12/August_2021.csv", usecols=column_names),
        pd.read_csv("../stripe-statements/2021_06_to_2021_12/September_2021.csv", usecols=column_names),
        pd.read_csv("../stripe-statements/2021_06_to_2021_12/October_2021.csv", usecols=column_names),
        pd.read_csv("../stripe-statements/2021_06_to_2021_12/November_2021.csv", usecols=column_names),
        pd.read_csv("../stripe-statements/2021_06_to_2021_12/December_2021.csv", usecols=column_names),
    ]
    data_2022 = [pd.read_csv(file,sep=",", usecols=column_names) for file in filepath]
    dfs_may_2023 = [
        pd.read_csv("../stripe-statements/2023/January 2023.csv", usecols=column_names),
        pd.read_csv("../stripe-statements/2023/February 2023.csv", usecols=column_names), 
        pd.read_csv("../stripe-statements/2023/March 2023.csv", usecols=column_names),
        pd.read_csv("../stripe-statements/2023/April 2023.csv", usecols=column_names)   
    ]

    df = pd.concat([
        pd.concat(data_2021, axis=0),
        pd.concat(data_2022, axis=0),
        pd.concat(dfs_may_2023, axis=0)
    ], axis=0, ignore_index=True)
    
    return df


def main():
    base_dir = "../stripe-statements"
    
    # 2022 filepath
    filepath_2022 = glob.glob(f"{base_dir}../stripe-statements/2022/*.csv")

    # old column names
    column_names = [
        "donorbox_name (metadata)",
        "Description",
        "Created (UTC)",
        "Amount",
        "Fee",
        "Customer ID",
        "donorbox_recurring_donation (metadata)",
        "id",
        "Currency",
        "donorbox_email (metadata)"
    ]

    # required column names    
    column_names_new = [
        "customer_name",
        "description",
        "created_utc",
        "customer_facing_amount",
        "fee",
        "customer_id",
        "payment_metadata[donorbox_recurring_donation]",
        "balance_transaction_id",
        "currency",
        "customer_email"
    ]
    
    # map new column names to old fmt dataframe
    df_old_fmt = old_format_data(filepath=filepath_2022, column_names=column_names)
    df_old_fmt.rename(columns={
        "id": "balance_transaction_id",
        "Description": "description",
        "Created (UTC)":"created_utc",
        "Amount": "amount",
        "Currency":"currency",
        "Fee":"fee",
        "Customer ID":"customer_id",
        "donorbox_name (metadata)":"customer_name",
        "donorbox_email (metadata)":"customer_email",
        "donorbox_recurring_donation (metadata)":"payment_metadata[donorbox_recurring_donation]"
    },inplace=True)
    
    # automatically loops through all folders starting from 2024 onwards
    all_dfs = [df_old_fmt]
    
    if os.path.exists(base_dir):
        for item in sorted(os.listdir(base_dir)):
            if re.match(r"^\d{4}$", item):
                year = int(item)
                if year >= 2024:
                    year_folder_files = glob.glob(f"{base_dir}/{item}/*.csv")
                    if year_folder_files:
                        print(f"Processing new format folder:{item}")
                        df_year = new_format_data(year_folder_files, column_names_new)
                        df_year.rename(columns={"customer_facing_amount": "amount"}, inplace=True)
                        all_dfs.apenned(df_year)
    
    # get new fmt data + add new filepaths every year
    filepath_2024 = glob.glob("../stripe-statements/2024/*.csv")
    df_2024_fmt = new_format_data(filepath_2024, column_names=column_names_new)
    df_2024_fmt.rename(columns={"customer_facing_amount":"amount"},inplace=True)

    filepath_2025 = glob.glob("../stripe-statements/2025/*.csv")
    df_2025_fmt = new_format_data(filepath_2025, column_names=column_names_new)
    df_2025_fmt.rename(columns={"customer_facing_amount":"amount"},inplace=True)
    
    filepath_2026 = glob.glob("../stripe-statements/2026/*.csv")
    df_2026_fmt = new_format_data(filepath_2026, column_names=column_names_new)
    df_2026_fmt.rename(columns={"customer_facing_amount":"amount"},inplace=True)

    # save all data
    df = pd.concat([df_old_fmt, df_2024_fmt, df_2025_fmt, df_2026_fmt], axis=0)
    df=str_to_datetime(df, name="created_utc")
    df.to_parquet("full_data.parquet", index=False, engine="pyarrow", compression="snappy")

if __name__ == "__main__":
    
    main()