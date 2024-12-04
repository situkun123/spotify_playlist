import pandas as pd
import streamlit as st
from streamlit.logger import get_logger
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import DuckDB, middle_bar_chart, middle_scatter_chart

LOGGER = get_logger(__name__)
im = Image.open("Spotify_icon.ico")
def run():
    st.set_page_config(
        page_title="Spotify Playlist",
        page_icon=im,
        layout="wide",
    )

    st.title("Spotify Playlist Analysis", )
    conn = DuckDB().conn

    # getting data from duckdb
    df_main = pd.read_parquet('playlist_summary_external_modified.parquet')
    df_genre = conn.sql('''SELECT * FROM rpt_top_genre''').to_df()
    df_mood = conn.sql('''SELECT * FROM rpt_top_mood''').to_df()

    # lite processing
    df_genre_top_5 = df_genre[['genre', 'no_playlist']].sort_values('no_playlist', ascending=False).head(5)
    df_genre_top_5_fig = px.pie(df_genre_top_5,
                                values='no_playlist',
                                names='genre',
                                title="Top 5 Genre Playlist",
                                width=375,
                                height=375,)

    df_mood_top_5 = df_mood[['mood', 'no_playlist']].sort_values('no_playlist', ascending=False).head(5)
    df_mood_top_5_fig = px.pie(df_mood_top_5,
                                values='no_playlist',
                                names='mood',
                               title="Top 5 Mood Playlist",
                               width=375,
                                height=375,)

    df_stream30s_cohort = df_main['stream30s_cohort'].value_counts().reset_index()
    df_stream30s_cohort_fig = px.pie(df_stream30s_cohort,
                               values='count',
                               names='stream30s_cohort',
                               title="Playlist Stream30s Cohort",
                               width=375,
                               height=375, )

    # bar_chart
    # genre dfs
    df_genre_total = df_genre[['genre', 'total_stream', 'total_stream30s', 'total_monthly_stream30s']]
    df_genre_avg = df_genre[['genre', 'avg_streams', 'avg_stream30s', 'avg_monthly_stream30s']]
    # mood dfs
    df_mood_total = df_mood[['mood', 'total_stream', 'total_stream30s', 'total_monthly_stream30s']]
    df_mood_avg = df_mood[['mood', 'avg_streams', 'avg_stream30s', 'avg_monthly_stream30s']]
    # middle figs -- bar
    df_genre_total_fig = middle_bar_chart(df_genre_total, ['genre', 'total_stream', 'total_stream30s', 'total_monthly_stream30s'])
    df_genre_avg = middle_bar_chart(df_genre_avg, ['genre', 'avg_streams', 'avg_stream30s', 'avg_monthly_stream30s'])
    df_mood_total_fig = middle_bar_chart(df_mood_total, ['mood', 'total_stream', 'total_stream30s', 'total_monthly_stream30s'])
    df_mood_avg_fig = middle_bar_chart(df_mood_avg, ['mood', 'avg_streams', 'avg_stream30s', 'avg_monthly_stream30s'])


    # display
    # top containers for pie chart
    top_container = st.container()


    with top_container:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(df_genre_top_5_fig, theme=None)
        with col2:
            st.plotly_chart(df_mood_top_5_fig, theme=None)
        with col3:
            st.plotly_chart(df_stream30s_cohort_fig, theme=None)

    middle_container = st.container()
    with middle_container:
        col1, col2 = st.columns(2)
        with col1:
            col_1_1, col_1_2, col_1_3= st.columns(3)
            with col_1_2:
                view = st.radio(
                    label='View',
                    options=["Total", "Average"],
                    horizontal = True
                )
            with col_1_3:
                mood_genre = st.radio(
                    label='Metric',
                    options=["Genre", "Mood"],
                    horizontal = True
                )
            if view == "Total" and mood_genre == "Genre":
                st.plotly_chart(df_genre_total_fig, theme=None)
            elif view == "Average" and mood_genre == "Genre":
                st.plotly_chart(df_genre_avg, theme=None)
            elif view == "Total" and mood_genre == "Mood":
                st.plotly_chart(df_mood_total_fig, theme=None)
            elif view == "Average" and mood_genre == "Mood":
                st.plotly_chart(df_mood_avg_fig, theme=None)

        with col2:
            col_2_1, col_2_2 , col_2_3, col_2_4= st.columns(4)
            with col_2_2:
                streams = st.slider("weighted_streams_metric", min_value=df_main['weighted_streams_metric'].min(), max_value=df_main['weighted_streams_metric'].max(), value=1.0)
            with col_2_3:
                au = st.slider("weighted_au_metric", min_value=df_main['weighted_au_metric'].min(), max_value=df_main['weighted_au_metric'].max(), value=1.0)
            df_main_processed = df_main[(df_main['weighted_au_metric'] <= au) & (df_main['weighted_streams_metric'] <= streams)]
            with col_2_4:
                st.write(f"Number of Playlists: \n {len(df_main_processed)}")
            # middle figs -- scatter
            scatter_chart =middle_scatter_chart(df_main_processed, 'weighted_au_metric', 'weighted_streams_metric', 'n_tracks', 'genre_1')

            st.plotly_chart(scatter_chart, theme=None)



    # middle charts
    # st.plotly_chart(df_genre_total_fig, theme=None)
    # st.plotly_chart(df_genre_avg, theme=None)

    # detailed table
    st.header("Detailed Table")
    st.write(df_genre)


if __name__ == "__main__":
    run()