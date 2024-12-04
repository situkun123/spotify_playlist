# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import inspect
import textwrap
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv

load_dotenv()

# meta data
key = os.environ.get("DUCK_KEY")
db_name = 'my_db'

def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

class DuckDB:
    def __init__(self):
        try:
            self.conn = duckdb.connect(f"md:{db_name}?motherduck_token={key}&saas_mode=true")
        except:
            raise Exception("Could not connect to duckdb")

def middle_bar_chart(df, col_names):
    '''col_names = ['x', 'daily', 'daily30s', 'monthly']'''
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(name=col_names[1], x=df[col_names[0]].to_list(), y=df[col_names[1]]),
        secondary_y=False
    )
    fig.add_trace(
        go.Bar(name=col_names[2], x=df[col_names[0]].to_list(), y=df[col_names[2]]),
        secondary_y=False
    )
    fig.add_trace(
        go.Line(name=col_names[3], x=df[col_names[0]].to_list(),
                y=df[col_names[3]]),
        secondary_y=True
    )
    fig.update_layout(
        barmode='group',
        width=950,
        height=470,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig

def middle_scatter_chart(df, x, y, size, color):
    fig = px.scatter(df,
                     x=x,
                     y=y,
                     size=size,
                     color=color)
    fig.update_layout(
        width=950,
        height=470,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig

if __name__ == "__main__":
    output = DuckDB()
    # data = output.conn.sql("SELECT * FROM playlist_summary_external_modified").to_df()
    # data.to_parquet("playlist_summary_external_modified.parquet")