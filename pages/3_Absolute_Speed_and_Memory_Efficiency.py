import streamlit as st
import pandas as pd
import polars as pl
import time
import os
import sys
import glob

st.set_page_config(
    page_title="Polars v Pandas", 
    layout="wide", 
    page_icon="./icons/polars_logo.png"
)

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Streamlit UI
st.title('Speed & Memory Efficiency: Polars vs Pandas')

st.markdown("""This application compares the performance of **Polars** and **Pandas** for the following operations on the Indian National Stock Exchange dataset listed below""")
st.markdown('- Aggregation & Group By \n- Searching \n- Sorting')

percent_complete = 0
polars_column, pandas_column = st.columns(2)
hide_button_code = st.empty()
compute_executions = hide_button_code.button("Execute the computations", type='primary')

pandas_container = st.container()
polars_container = st.container()
polars_progress_text = "Loading data and performing required computations using Polars...Please wait"
pandas_progress_text = "Loading data and performing required computation using Pandas...Yeah, this is going to take a long, long time..."

file_paths = glob.glob("archive/*.csv")

if compute_executions:
    hide_button_code.empty()
# Function to calculate file size in GB
    def get_file_size_in_gb(file_path):
        return os.path.getsize(file_path) / (1024 ** 3)  # Convert bytes to GB

    # Function to lazily scan files up to a given size limit and measure reading time
    def scan_files_upto_limit(file_paths, size_limit_gb):
        total_size_gb = 0
        lazy_frames = []
        start_time = time.time()  # Start timing the reading process
        for file_path in file_paths:
            file_size_gb = get_file_size_in_gb(file_path)
            if total_size_gb + file_size_gb > size_limit_gb:
                break
            total_size_gb += file_size_gb

            # Extract company name from filename
            company_name = os.path.basename(file_path).replace(".csv", "")

            print(f"Scanning file: {file_path}, Size: {file_size_gb:.2f} GB, Total Size: {total_size_gb:.2f} GB")
            lazy_df = pl.scan_csv(file_path)
            
            # Avoid adding columns or doing operations during scanning
            lazy_df = lazy_df.with_columns([
                pl.col("volume").cast(pl.Float64),  # Ensure 'volume' is Float64
                pl.col("open").cast(pl.Float64),    # Ensure 'open' is Float64
                pl.lit(company_name).alias("Stock_Name")  # Add company name as a column
            ])
            lazy_frames.append(lazy_df)
        reading_time = time.time() - start_time  # Total reading time
        return pl.concat(lazy_frames) if lazy_frames else None, reading_time

    # Function to measure time for operations
    def measure_operations_lazy(lazy_df):
        results = {}

        # Focus only on 'Stock_Name', 'volume', and 'date'
        selected_df = lazy_df.select(["Stock_Name", "volume", "date"])
        selected_df_final = selected_df.collect()

        # Group By & Aggregation
        start_time = time.time()
        groupby_result = selected_df.group_by("date").agg(pl.sum("volume").alias("Total Volume"))
        groupby_result = groupby_result.collect()
        results["Group By & Aggregation Time (s)"] = round(time.time() - start_time, 2)

        # Search
        start_time = time.time()
        search_result = selected_df.filter(pl.col("volume") > 1000)
        search_result = search_result.collect()
        results["Search Time (s)"] = round(time.time() - start_time, 2)

        # Sorting
        start_time = time.time()
        sorted_result = selected_df.sort("date")
        sorted_result = sorted_result.collect()
        results["Sorting Time (s)"] = round(time.time() - start_time, 2)

        return results, selected_df_final

    # Track results for each dataset size
    results = []
    #data_table_display_polars = st.empty()
    data_table_display_pandas = st.empty()

    polars_column.subheader("Performance Metrics for Dataset Sizes For Polars:")
    data_table_display_polars = polars_column.empty()
    polars_progress_bar = polars_column.progress(0, text=polars_progress_text)
    with st.spinner("Performing computations...Please wait"):
        # Measure for 1GB dataset
        while percent_complete < 100:
            lazy_df_1gb, reading_time_1gb = scan_files_upto_limit(file_paths, 1)
            if lazy_df_1gb is not None:
                result_1gb, result_df_1gb = measure_operations_lazy(lazy_df_1gb)
                results_1gb_final = {'Data Size (GB)':'1 GB','Reading Time(s)':reading_time_1gb}
                results_1gb_final.update(result_1gb)
                results.append(results_1gb_final)
                
                data_table_display_polars.table(results)

                one_gig_df_value = round((result_df_1gb.estimated_size('mb')) / 1000, 1)
                one_gig_data_string = f"The estimated memory used for <span style='font-weight:bold'> 1 GB </span> Polars Dataframe is <span style='font-weight:bold'> {one_gig_df_value} GB </span>"
                polars_column.markdown(one_gig_data_string, unsafe_allow_html=True)
            
            percent_complete += 33
            polars_progress_bar.progress(percent_complete, text=polars_progress_text)

            # Measure for 2GB dataset
            lazy_df_2gb, reading_time_2gb = scan_files_upto_limit(file_paths, 2)
            if lazy_df_2gb is not None:
                result_2gb, result_df_2gb = measure_operations_lazy(lazy_df_2gb)
                results_2gb_final = {'Data Size (GB)':'2 GB','Reading Time(s)':reading_time_2gb}
                results_2gb_final.update(result_2gb)
                results.append(results_2gb_final)
                
                data_table_display_polars.empty()
                data_table_display_polars.table(results)

                two_gig_df_value = round((result_df_2gb.estimated_size('mb')) / 1000, 1)
                two_gig_data_string = f"The estimated memory used for <span style='font-weight:bold'> 2 GB </span> Polars Dataframe is <span style='font-weight:bold'> {two_gig_df_value} GB </span>"
                polars_column.markdown(two_gig_data_string, unsafe_allow_html=True)
            
            percent_complete += 33
            polars_progress_bar.progress(percent_complete, text=polars_progress_text)

            # Measure for 3GB dataset
            lazy_df_3gb, reading_time_3gb = scan_files_upto_limit(file_paths, 3)
            if lazy_df_3gb is not None:
                result_3gb, result_df_3gb = measure_operations_lazy(lazy_df_3gb)
                results_3gb_final = {'Data Size (GB)':'3 GB','Reading Time(s)':reading_time_3gb}
                results_3gb_final.update(result_3gb)
                results.append(results_3gb_final)
                
                data_table_display_polars.empty()
                data_table_display_polars.table(results)

                three_gig_df_value = round((result_df_3gb.estimated_size('mb')) / 1000, 1)
                three_gig_data_string = f"The estimated memory used for <span style='font-weight:bold'> 3 GB </span> Polars Dataframe is <span style='font-weight:bold'> {three_gig_df_value} GB </span>"
                polars_column.markdown(three_gig_data_string, unsafe_allow_html=True)
                #st.table(results)
            
            percent_complete += 34
            polars_progress_bar.progress(percent_complete, text=polars_progress_text)

        percent_complete = 0
        polars_progress_bar.empty()

        # Convert results to a DataFrame
        results_df = pd.DataFrame(results)

        # Display the results
        #st.subheader("Performance Metrics for Dataset Sizes For Polars:")
        #st.table(results_df)

    ####CODE FOR PANDAS####

    # Function to read files up to a given size limit and measure reading time
    def read_files_upto_limit_pandas(file_paths, size_limit_gb):
        chunk_size = 5000
        total_size_gb = 0
        dfs = []
        start_time = time.time()  # Start timing the reading process
        for file_path in file_paths:
            file_size_gb = get_file_size_in_gb(file_path)
            if total_size_gb + file_size_gb > size_limit_gb:
                break
            total_size_gb += file_size_gb

            # Extract company name from filename
            company_name = os.path.basename(file_path).replace(".csv", "")

            print(f"Reading file: {file_path}, Size: {file_size_gb:.2f} GB, Total Size: {total_size_gb:.2f} GB")
            df_chunks = pd.read_csv(file_path, chunksize=chunk_size)
            
            for chunks in df_chunks:
                # Ensure 'volume' and 'open' columns are Float64 and add 'Stock_Name' column
                chunks["volume"] = chunks["volume"].astype("float64")
                chunks["open"] = chunks["open"].astype("float64")
                chunks["Stock_Name"] = company_name

                dfs.append(chunks)

        reading_time = time.time() - start_time  # Total reading time
        return pd.concat(dfs, ignore_index=True), reading_time

    # Function to measure time for operations
    def measure_operations_pandas(df):
        results = {}

        # Focus only on 'Stock_Name', 'volume', and 'date'
        selected_df = df.loc[:, ["Stock_Name", "volume", "date"]]
        _ = st.empty()

        # Group By & Aggregation
        start_time = time.time()
        selected_df.groupby("date")["volume"].sum()
        results["Group By & Aggregation Time (s)"] = round(time.time() - start_time, 2)

        # Search
        start_time = time.time()
        selected_df[selected_df["volume"] > 1000]
        results["Search Time (s)"] = round(time.time() - start_time, 2)

        # Sorting
        start_time = time.time()
        selected_df.sort_values("date")
        results["Sorting Time (s)"] = round(time.time() - start_time, 2)

        return results, selected_df

    # Track results for each dataset size
    results = []
    df_hide_container = st.empty()

    pandas_column.subheader("Performance Metrics for Dataset Sizes For Pandas:")
    data_table_display_pandas = pandas_column.empty()
    pandas_progress_bar = pandas_column.progress(0, text=polars_progress_text)
    # Measure for 1GB dataset
    #with pandas_column:
    with st.spinner("Performing computations...Please wait"):
        while percent_complete < 100:
            df_1gb, reading_time_1gb = read_files_upto_limit_pandas(file_paths, 1)
            if df_1gb is not None:
                result_1gb, result_1gb_df = measure_operations_pandas(df_1gb)
                results_1gb_final = {'Data Size (GB)':'1 GB','Reading Time(s)':reading_time_1gb}
                results_1gb_final.update(result_1gb)
                results.append(results_1gb_final)

                data_table_display_pandas.table(results)

                one_gig_pd_size = round(sys.getsizeof(result_1gb_df)/1000000000, 1)
                one_gig_data_string_pandas = f"The estimated memory used for <span style='font-weight:bold'> 1 GB </span> Pandas Dataframe is <span style='font-weight:bold'> {one_gig_pd_size} GB </span>"
                pandas_column.markdown(one_gig_data_string_pandas, unsafe_allow_html=True)
                
            percent_complete += 33
            pandas_progress_bar.progress(percent_complete, text=pandas_progress_text)

            # Measure for 2GB dataset
            df_2gb, reading_time_2gb = read_files_upto_limit_pandas(file_paths, 2)
            if df_2gb is not None:
                result_2gb, result_2gb_df = measure_operations_pandas(df_2gb)
                results_2gb_final = {'Data Size (GB)':'2 GB','Reading Time(s)':reading_time_2gb}
                results_2gb_final.update(result_2gb)
                results.append(results_2gb_final)

                data_table_display_pandas.empty()
                data_table_display_pandas.table(results)

                two_gig_pd_size = round(sys.getsizeof(result_2gb_df)/1000000000, 1)
                two_gig_data_string_pandas = f"The estimated memory used for <span style='font-weight:bold'> 2 GB </span> Pandas Dataframe is <span style='font-weight:bold'> {two_gig_pd_size} GB </span>"
                pandas_column.markdown(two_gig_data_string_pandas, unsafe_allow_html=True)

            percent_complete += 33
            pandas_progress_bar.progress(percent_complete, text=pandas_progress_text)

            # Measure for 3GB dataset
            df_3gb, reading_time_3gb = read_files_upto_limit_pandas(file_paths, 3)
            if df_3gb is not None:
                result_3gb, result_3gb_df = measure_operations_pandas(df_3gb)
                results_3gb_final = {'Data Size (GB)':'3 GB','Reading Time(s)':reading_time_3gb}
                results_3gb_final.update(result_3gb)
                results.append(results_3gb_final)

                data_table_display_pandas.empty()
                data_table_display_pandas.table(results)

                three_gig_pd_size = round(sys.getsizeof(result_3gb_df)/1000000000, 1)
                three_gig_data_string_pandas = f"The estimated memory used for <span style='font-weight:bold'> 3 GB </span> Pandas Dataframe is <span style='font-weight:bold'> {three_gig_pd_size} GB </span>"
                pandas_column.markdown(three_gig_data_string_pandas, unsafe_allow_html=True)
            percent_complete += 34
            pandas_progress_bar.progress(percent_complete, text=pandas_progress_text)
        percent_complete = 0
        pandas_progress_bar.empty()

        results_df_pandas = pd.DataFrame(results)
    