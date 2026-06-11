# Stripe monthly statement consolidation

## An automated data pipeline designed to seamlessly merge fragmented, multi-year  Stripe financial reports into a single, standardised master dataset.

------
### Built With: ###

- ![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)
- ![pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
- <a href="https://apache/org"><img src="https://arrow.apache.org/img/arrow-logo_horizontal_black-txt_white-bg.png" alt="pyarrow" height="25"></a> 
- ![plotly](https://img.shields.io/badge/-Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
- ![Matplotlib](https://img.shields.io/badge/-Matplotlib-000000?style=flat&logo=python)
- ![Jupyter Notebook](https://img.shields.io/badge/Jupyter%20Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)
-  📁 Glob
-------

### The Problem: ###

As our non-profit expanded, managing our historical financial data from Stripe became problematic over time due to two major challenges:

- Fragmented Storage:
The data is spread across multiple separate CSV files and organised into different structures by year (for example: 2021_06_to_2021_12, 2023, etc). This fragmentation made it incredibly difficult to perform multi-year financial analysis or reporting.

- Schema Drift (different formats):
In 2023, Stripe decided to update its reporting export format.
  - _The Old format_: Used column headers like "id", "amount", "Created UTC" and specific Donorbox metadata strings ("donorbox_recurring_donation (metadata)).
  - _The New format_: Standardised to snake_case headers like "balance_transaction_id",  "customer_facing_amount", "created_utc", and structured metadata brackets ("payment_metadata[donorbox_recurring_donation]).

### Impact: ### 

Because of these mismatched column names and shifting date formats, a standard, straightforward merge or append of all files would fail or result in corrupted or missing data.

We also had files located in various different folders and largely disorganised datasets with missing data creating issues with finding and locating the files. We needed a place where all the data is consolidated.

-------
## The solution: Automated normalisation and consolidation of old and new formats (Technical guide) ##

This script acts as an automated ETL (Extract, Transform, Load) pipeline that consolidates fragmented, multi-format financial data into a single analysis ready dataset. This allows us to analyse the data in one place and create visuals for various different stakeholders.

It accomplishes this through three core phases:

1) Targeted Extraction:
   - It dynamically identifies and loops through annual folders using file pattern matching (glob.glob).
   - To optimise memory usage, it isolates and extracts only the relevant financial and metadata columns, ignoring unnecessary data fields.
  
2) Schema Normalisation (Transformation):
   - Historical grouping: It manually maps and groups hardcoded legacy data structures (2021-2023)
   - Column alignment: It programmatically maps and renames legacy column headers to match the modern Stripe format. For example, standardising "amount" and "customer_facing_amount" into just "amount".
   - Data Type safety: It handles mixed date formats across the years by converting the "created_utc" strings into proper queryable datetime objects.

3) Consolidated Loading:
   - It securely stiches all dataframes together sequentially across time horizons.
   - It exports the unified dataset into a Parquet file (full_data.parquet) utilising Snappy compression. This ensures significantly faster query performance and drastically lower storage overhead compared to a massive raw CSV file.
  
  ## The solution (non-tech guide) ##

  This script acts as a bridge between the old and the new reporting standards/format. It automates the extraction, transformation , and consolidation of all monthly CSV statements into a single and high performance master file ("full_data.parquet"). This allows us to analyse the data in one place and create visuals for various different stakeholders.

  It provides 4 features/solutions:

  1) **integrates old and new formats.**
  2) **multi year parsing** seamlessly integrates annual folders and monthly statement files since 2021.
  3) **Data integrity** converts text based timestamps into clean and uniform datetime parameters ("UTC") to ensure chronological audit accuracy.
  4) **Optimised storage and loading** Saves the final consolidated ledger into a compressed ".parquet" format which drastically reduces storage size whilst speeding up analytical loading time.

---------

## Results: ##

  1) The data is clean and easy to read in one file.
  2) Every time a statement is downloaded into the statements file it is automatically added to the dataset.
  3) The script automatically recognises any CSV regardless of month or year and adds it to the consolidated ledger.
  4) The data can be easily used to provide data visualisations and insight into donor/payment activity. 

## Additional Information: ##

 1) I created a "basic_dashboard.py" file showing two visual charts using plotly:
   - The first is a line chart showing "monthly consolidated revenue trends" over the months and years.
   - The second is a pie chart that shows the distribution of currencies and amounts per currency.
 2) I created a "professional_dashboard.py" file showing three visual charts using plotly geared towards business presentations:
   - Trend Analysis: A scatter graph showing monthly Gross Revenue vs. Net Income (Line/Area).
   - Revenue Predictability: A bar chart showcasing total baseline   predictability.
   - Revenue Breakdown: A donut chart displaying the revenue breakdown by category with custom colors and radial percentage labels.
 3) I created a "views.ipynb" file showing multiple matplotlib visual charts such as:
   - Polished overhead cost distributions (histogram chart): charting fee frequencies.
   - Fee consumption visualisations (horizontal bar chart): which isolates the top 10 donors with the vertical axis inverted to represent the highest fees paid.
   - Seasonal Processing Matrix (vertical bar chart): illustrating total funds raised per month over the years.
   - Cumulative Operational Financial Ledger (line chart): showcases total financial growth performance over time.

All these visuals have helped us to track information useful to the fund raising and tracking of donations.

## Disclaimer: ##

1) No private details or data are shown.
2) Column titles are based on readily available Stripe statements that come standard for all.
3) Stripe frequently updates report schemas. Future structural shifts might break column mappings.
4) Currency mixing. The script combines numbers without currency conversion.
5) This is an ongoing project relevant to my work.