"""
The script automatically consolidates Stripe monthly finanacial statements into a single Pandas dataframe.
"""
import glob
import pandas as pd


def new_format_data(filepath: str, column_names: str) -> pd.DataFrame:
    """
    create a list of dataframes in the new format specifying the filepath and column names str
    """

    data = [pd.read_csv(file, sep=",", usecols=column_names) for file in filepath]

    df = pd.concat([
        pd.concat(data, axis=0),
    ], axis=0)
    
    return df


def old_format_data(filepath: str, column_names: list) -> pd.DataFrame:
    """
    create a list of dataframes in the old format specifying the filepath and column names str
    """

    data_2022 = [pd.read_csv(file,sep=",", usecols=column_names) for file in filepath]
    dfs_may_2023 = [
        pd.read_csv("data/2023/January 2023.csv", usecols=column_names),
        pd.read_csv("data/2023/February 2023.csv", usecols=column_names), 
        pd.read_csv("data/2023/March 2023.csv", usecols=column_names),
        pd.read_csv("data/2023/April 2023.csv", usecols=column_names)   
    ]

    df = pd.concat([
        pd.concat(data_2022, axis=0),
        pd.concat(dfs_may_2023, axis=0)
    ], axis=0)
    
    return df


def main():
    
    # 2022 filepath
    filepath_2022 = glob.glob("data/2022/*.csv")

    # old column names
    column_names = [
        "id",
        "Description",
        "Created (UTC)",
        "Amount",
        "Currency",
        "Fee",
        "Customer ID",
        "donorbox_name (metadata)",
        "donorbox_email (metadata)",
        "donorbox_recurring_donation (metadata)"
    ]

    # required column names    
    column_names_new = [
        "balance_transaction_id",
        "description",
        "created_utc",
        "customer_facing_amount",
        "currency",
        "fee",
        "customer_id",
        "customer_name",
        "customer_email",
        "payment_metadata[donorbox_recurring_donation]"
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
    
    # get new fmt data
    filepath_2024 = glob.glob("data/2024/*.csv")
    df_2024_fmt = new_format_data(filepath_2024, column_names=column_names_new)

    filepath_2025 = glob.glob("data/2025/*.csv")
    df_2025_fmt = new_format_data(filepath_2025, column_names=column_names_new)
    
    filepath_2026 = glob.glob("data/2026/*.csv")
    df_2026_fmt = new_format_data(filepath_2026, column_names=column_names_new)

    # save all data
    df = pd.concat([df_old_fmt, df_2024_fmt, df_2025_fmt, df_2026_fmt], axis=0)
    df.to_csv("full_data.csv", index=False)

if __name__ == "__main__":
    
    main()