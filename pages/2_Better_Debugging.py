import streamlit as st

st.set_page_config(
    page_title="Polars v Pandas", 
    layout="wide", 
    page_icon="./icons/polars_logo.png"
)

st.title("Error Debugging")
st.markdown('''
Here are examples comparing Pandas and Polars error messages to demonstrate how Polars often provides clearer, more specific feedback
''')

pandas_column, polars_column = st.columns(2)

##Code Snippets for Pandas
pandas_column.header("Pandas Shortcomings")
pandas_column.subheader("Missing column")
ms_column_code = '''
import pandas as pd
df = pd.DataFrame({"A": [1, 2, 3]})
df["B"]  # Accessing a non-existent column

KeyError: 'B'
'''
pandas_column.code(ms_column_code, language='python')
pandas_column.markdown('''The error message doesn't indicate the available columns, leaving the user unsure about what went wrong.''')
pandas_column.divider()

pandas_column.subheader("Operation Mismatch")
op_mismatch_code = '''
df = pd.DataFrame({"A": ["1", "2", "three"]})
df["A"].mean()  # Attempting mean on non-numeric data

TypeError: can only concatenate str (not "int") to str
'''
pandas_column.code(op_mismatch_code, language='python')
pandas_column.markdown('''The error message is generic and doesn't directly indicate that the issue arises from a non-numeric column.''')
pandas_column.divider()

pandas_column.subheader("Shape Mismatch")
shape_mismatch_code ='''
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df["C"] = [5, 6, 7]  # Assigning a list with mismatched length

ValueError: Length of values (3) does not match length of index (2)
'''
pandas_column.code(shape_mismatch_code, language='python')
pandas_column.markdown('''The error message mentions the mismatch but doesn't explicitly help users locate the issue in large datasets.''')
pandas_column.divider()

pandas_column.subheader("Method Usage Error")
method_usage_code = '''
df = pd.DataFrame({"A": [1, 2, 3]})
df.mean(axis="invalid")  # Invalid axis argument

ValueError: No axis named invalid for object type DataFrame
'''
pandas_column.code(method_usage_code, language='python')
pandas_column.markdown('''The error is vague and doesn't clarify the acceptable values for axis.''')
pandas_column.divider()

##CODE SNIPPETS FOR POLARS
polars_column.header("Polars's Elaboration")
polars_column.subheader("Missing column")
ms_column_code_polars = '''
import polars as pl
df = pl.DataFrame({"A": [1, 2, 3]})
df["B"]  # Accessing a non-existent column

KeyError: 'B' not found. Available columns: ['A']
'''
polars_column.code(ms_column_code_polars, language='python')
polars_column.markdown('''Polars clearly states the missing column and lists the available columns, helping the user debug faster.''')
polars_column.divider()

polars_column.subheader("Operation Mismatch")
op_mismatch_code_polars = '''
df = pl.DataFrame({"A": ["1", "2", "three"]})
df["A"].mean()  # Attempting mean on non-numeric data

ComputeError: Cannot compute mean; column 'A' has non-numeric data type Utf8.
'''
polars_column.code(op_mismatch_code_polars, language='python')
polars_column.markdown('''Polars specifies the exact problem (column type mismatch) and identifies the column causing the issue.''')
polars_column.divider()

polars_column.subheader("Shape Mismatch")
shape_mismatch_code_polars ='''
df = pl.DataFrame({"A": [1, 2], "B": [3, 4]})
df = df.with_column(pl.Series("C", [5, 6, 7]))  # Assigning a mismatched length column

ShapeError: Cannot add column 'C' with length 3 to DataFrame with length 2.
'''
polars_column.code(shape_mismatch_code_polars, language='python')
polars_column.markdown('''Polars explicitly mentions the column being added and the mismatch, making it easier to trace the issue.''')
polars_column.divider()

polars_column.subheader("Method Usage Error")
method_usage_code_polars = '''
df = pl.DataFrame({"A": [1, 2, 3]})
df.mean(axis="invalid")  # Invalid axis argument

ComputeError: Invalid axis 'invalid'. Use axis=0 for column-wise, or axis=1 for row-wise.
'''
polars_column.code(method_usage_code_polars, language='python')
polars_column.markdown('''Polars provides a clear explanation and lists acceptable values, reducing user confusion.''')
polars_column.divider()
