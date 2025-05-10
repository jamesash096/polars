import streamlit as st

st.set_page_config(
    page_title="Polars v Pandas", 
    layout="wide", 
    page_icon="./icons/polars_logo.png"
)

st.header("Code Syntax")
pandas_column, polars_column = st.columns(2)

##CODE SNIPPETS FOR PANDAS
pandas_column.subheader("Pandas")
pandas_column.markdown("In Pandas, you need multiple intermediate steps and often use functions like .reset_index() to adjust the DataFrame after grouping.")
pandas_code = '''
# Step 1: Filtering the dataframe based on values greater than 2
filtered_df = df[df['A'] > 2]

# Step 2: Group by 'C' and calculate sum of 'A' and mean of 'B'
grouped_df = filtered_df.groupby('C').agg({
    'A': 'sum',
    'B': 'mean'
}).reset_index()

# Step 3: Sort the results by the sum of 'A'
sorted_df = grouped_df.sort_values(by='A', ascending=False)
'''
pandas_column.code(pandas_code, language='python')
pandas_column.divider()

pandas_column.subheader("Filtering")
pandas_filter_code = '''filtered_df = df[df['A'] > 2]'''
pandas_column.code(pandas_filter_code, language='python')
pandas_column.markdown('''In Pandas, filtering is done using df[df['A'] > 2], which can be less readable, especially in larger codebases where the logic might get buried under many other lines.''')
pandas_column.divider()

pandas_column.subheader("Grouping and Aggregation")
pandas_grouping_code = '''grouped_df = filtered_df.groupby('C').agg({
    'A': 'sum',
    'B': 'mean'
}).reset_index()'''
pandas_column.code(pandas_grouping_code, language='python')
pandas_column.markdown('''In Pandas, aggregation after grouping is done with a dictionary (i.e., {'A': 'sum', 'B': 'mean'}). This can become cumbersome when performing more complex aggregations or when the number of columns increases''')
pandas_column.divider()

pandas_column.subheader("Sorting")
pandas_sorting_code = '''sorted_df = grouped_df.sort_values(by='A', ascending=False)'''
pandas_column.code(pandas_sorting_code, language='python')
pandas_column.markdown('''Sorting in Pandas is done with the sort_values() function, and it requires specifying the column name ('A') and the sorting order''')

##CODE SNIPPETS FOR POLARS
polars_column.subheader("Polars")
polars_column.markdown("Polars provides a more intuitive and concise way to perform multiple aggregations after grouping, without the need for dictionary-based syntax")
polars_code = '''
# Doing the same thing in Polars, but it feels more intuitive
result = df.filter(pl.col('A') > 2)
    .groupby('C')
    .agg([
        pl.col('A').sum().alias('sum_A'),
        pl.col('B').mean().alias('mean_B')
    ])
    .sort('sum_A', reverse=True)

# Adding some comments here for better alignment for the pages
# Adding some comments here for better alignment for the pages

'''
polars_column.code(polars_code, language='python')
polars_column.divider()

polars_column.subheader("Filtering")
polars_filter_code = '''df.filter(pl.col('A') > 2)'''
polars_column.code(polars_filter_code, language='python')
polars_column.markdown('''In Polars, filtering is done using the more explicit filter() method, and pl.col('A') makes it clear that you are referring to a column. This is part of the fluent style that Polars uses, where each transformation is specified clearly and in sequence.''')
polars_column.divider()

polars_column.subheader("Grouping and Aggregation")
polars_grouping_code = '''.groupby('C')
.agg([
    pl.col('A').sum().alias('sum_A'),
    pl.col('B').mean().alias('mean_B')])'''
polars_column.code(polars_grouping_code, language='python')
polars_column.markdown('''In Polars, the aggregation is done using agg() with a list of expressions. These expressions are more intuitive because they explicitly reference columns using pl.col(). This is clearer and easier to extend.''')
polars_column.divider()

polars_column.subheader("Sorting")
polars_sorting_code = '''.sort('sum_A', reverse=True)'''
polars_column.code(polars_sorting_code, language='python')
polars_column.markdown('''In Polars, sorting is done with .sort(), and the sorting column is specified directly ('sum_A'). The reverse=True argument is more explicit and clearly indicates that the sorting is in descending order''')
