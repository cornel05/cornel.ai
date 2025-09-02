# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.17.2
# ---

# # pandas: nullable data types
# - Old NumPy dtypes like `int32`, `int64`, `float64` do not allow missing values. If you insert `NaN` into an integer column, pandas silently upcasts it to float.
# - Pandas introduced nullable dtypes (`Int8`, `Int16`, `Int32`, `Int64`, `Float32`, `Float64`, `boolean`, `string`) that can hold both regular values and `pd.NA`.

# **Examples**

# ```python
# >>> import pandas as pd
# >>> import numpy as np
# ```

# ```python
# >>> arr = np.array([1, np.nan, 3])
# >>> print(arr)
# [ 1. nan  3.]
# >>> print("arr.dtype:", arr.dtype)
# float64
# >>> s = pd.Series([1, pd.NA, 3], dtype="Int64")
# >>> print(s)
# 0      1
# 1   <NA>
# 2      3
# >>> print("s.dtype:", s.dtype)
# dtype: Int64
# ```

# ```python
# >>> df = pd.DataFrame({
# ...     'A': [1, 2, np.nan],
# ...     'B': [4.0, np.nan, 6.0],
# ...     'C': ['a', 'b', None],
# ...     'D': [True, False, None]
# ... })
# >>> df = df.astype({'A': 'Int64', 'B': 'Float64', 'C': 'string', 'D': 'boolean'})
# >>> print(df)
#        A    B     C      D
# 0      1  4.0     a   True
# 1      2  <NA>    b  False
# 2   <NA>  6.0  <NA>    <NA>
# >>> print(df.dtype)
# A      Int64
# B    Float64
# C     string
# D    boolean
# dtype: object
# ```
