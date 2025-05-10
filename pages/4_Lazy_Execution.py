import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
import sys

st.set_page_config(
    page_title="Polars v Pandas", 
    layout="wide", 
    page_icon="./icons/polars_logo.png"
)

st.title("Lazy Execution")
st.markdown("So How is Polars able to pull this off when Pandas struggles this much? <span style='font-weight:bold'> Lazy Execution </span>", unsafe_allow_html=True)
st.markdown("It is a feature that enables deferred computation for DataFrame operations, allowing the library to optimize query execution. Instead of executing operations immediately, Polars builds a logical plan that represents the steps to be executed later. This plan is only evaluated when a result is explicitly requested (e.g., using .collect() to gather the results of a computation).")
st.markdown("Lazy execution is particularly beneficial when dealing with complex queries or large datasets where multiple operations can be combined and optimized before execution. It ensures minimal resource usage and maximum performance, making Polars a powerful choice for data processing.")
st.markdown("Consider here, a 3 GB datafile of the Indian National Stock Exchange dataset and its subsequent filtered output")

polars_column, pandas_column = st.columns(2)

file_path = "combined_data3gb.csv"

lazy_df = pl.scan_csv(file_path)

# Show data size
polars_column.subheader("Polars Gets It Done Fast")
polars_size_gb = lazy_df.collect().estimated_size() / (1024 ** 3)  # Convert bytes to GB
polars_column.markdown(f"Polars DataFrame size: <span style='font-weight:bold'> {polars_size_gb:.2f} GB </span>", unsafe_allow_html=True)

# Transformations
transformed_lazy_df = (
    lazy_df
    .filter(pl.col("close") > 50)
    .group_by("company")
    .agg([
        pl.col("volume").sum().alias("total_volume"),
        pl.col("close").mean().alias("average_close"),
    ])
    .sort("company")
)


polars_column.table(transformed_lazy_df.collect())

##PANDAS TRYNG TO RUN
try:
    # Creating a Pandas DataFrame
    pandas_column.subheader("Pandas Will Take Some Time (Or Crash)")
    pandas_df = pd.read_csv(file_path)

    pandas_size_gb = round(sys.getsizeof(pandas_df)/1000000000, 1)
    pandas_column.markdown(f"Pandas DataFrame size: <span style='font-weight:bold'> {pandas_size_gb:.2f} GB </span>", unsafe_allow_html=True)

    # Transformations
    filtered_df = pandas_df[pandas_df["close"] > 50]
    grouped_df = filtered_df.groupby("company").agg(
        total_volume=("volume", "sum"),
        average_close=("close", "mean")
    )
    pandas_column.table(grouped_df)
except MemoryError as e:
    pandas_column.markdown("Pandas workflow failed due to memory error:", e)