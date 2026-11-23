
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="South Korea Top 50 Analysis",
    page_icon="🎵",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0B1120;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111C33;
}

h1, h2, h3 {
    color: #60A5FA;
}

[data-testid="stMetric"] {
    background-color: #17243B;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #263B5A;
}

.stTabs [data-baseweb="tab"] {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎵 South Korea Top 50 Playlist Analysis")

st.subheader(
    "Comeback Momentum, Chart Re-Entry, "
    "and Fandom Intensity Analysis"
)

st.markdown("""
An interactive analytical dashboard exploring
song comeback frequency, chart retention,
rank recovery, momentum, and chart-based
fandom intensity indicators.
""")

st.divider()

# --------------------------------------------------
# LOAD DATASETS
# --------------------------------------------------

@st.cache_data
def load_data():

    frequency = pd.read_csv(
        "outputs/song_comeback_frequency.csv"
    )

    retention = pd.read_csv(
        "outputs/song_comeback_retention.csv"
    )

    momentum = pd.read_csv(
        "outputs/song_momentum_summary.csv"
    )

    fandom = pd.read_csv(
        "outputs/fandom_intensity_scores.csv"
    )

    artist = pd.read_csv(
        "outputs/artist_comeback_performance.csv"
    )

    album = pd.read_csv(
        "outputs/album_comeback_advantage.csv"
    )

    recovery = pd.read_csv(
        "outputs/song_rank_recovery.csv"
    )

    return (
        frequency,
        retention,
        momentum,
        fandom,
        artist,
        album,
        recovery
    )


try:

    (
        frequency,
        retention,
        momentum,
        fandom,
        artist,
        album,
        recovery
    ) = load_data()

except Exception as error:

    st.error(
        f"Unable to load project datasets: {error}"
    )

    st.info(
        "Run the analysis scripts from the main "
        "project directory before starting the dashboard."
    )

    st.stop()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

artist_options = sorted(
    frequency["artist"].dropna().unique().tolist()
)

selected_artists = st.sidebar.multiselect(
    "Select Artists",
    artist_options
)

min_comebacks = int(
    frequency["reentry_count"].min()
)

max_comebacks = int(
    frequency["reentry_count"].max()
)

comeback_range = st.sidebar.slider(
    "Comeback Frequency",
    min_comebacks,
    max_comebacks,
    (min_comebacks, max_comebacks)
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_frequency = frequency[
    frequency["reentry_count"].between(
        comeback_range[0],
        comeback_range[1]
    )
].copy()

if selected_artists:

    filtered_frequency = filtered_frequency[
        filtered_frequency["artist"].isin(
            selected_artists
        )
    ]

filtered_keys = filtered_frequency[
    "song_artist_key"
].unique()

filtered_retention = retention[
    retention["song_artist_key"].isin(
        filtered_keys
    )
]

filtered_momentum = momentum[
    momentum["song_artist_key"].isin(
        filtered_keys
    )
]

filtered_fandom = fandom[
    fandom["song_artist_key"].isin(
        filtered_keys
    )
]

# --------------------------------------------------
# PROJECT KPIs
# --------------------------------------------------

st.header("📊 Project Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Songs Analysed",
    f"{len(filtered_frequency):,}"
)

col2.metric(
    "Comeback Events",
    f"{filtered_frequency['reentry_count'].sum():,}"
)

col3.metric(
    "Artists Represented",
    f"{filtered_frequency['artist'].nunique():,}"
)

col4.metric(
    "Average Retention",
    f"{filtered_retention['average_retention_days'].mean():.2f} days"
    if not filtered_retention.empty
    else "N/A"
)

st.divider()

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Song Analysis",
    "Artist Analysis",
    "Momentum & Retention",
    "Fandom Proxy",
    "Album Comparison"
])

# --------------------------------------------------
# TAB 1: OVERVIEW
# --------------------------------------------------

with tab1:

    st.header("Comeback Performance Overview")

    top_songs = filtered_frequency.sort_values(
        "reentry_count",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_songs,
        x="reentry_count",
        y="song",
        color="reentry_count",
        orientation="h",
        title="Top 10 Songs by Comeback Frequency",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Project Highlights")

    st.write(
        "The analysis identifies recurring chart "
        "entries and compares their retention, "
        "rank recovery, and momentum."
    )

    if not filtered_frequency.empty:

        top_song = filtered_frequency.sort_values(
            "reentry_count",
            ascending=False
        ).iloc[0]

        st.success(
            f"Leading song in current selection: "
            f"{top_song['song']} by {top_song['artist']} "
            f"({top_song['reentry_count']} comebacks)"
        )

# --------------------------------------------------
# TAB 2: SONG ANALYSIS
# --------------------------------------------------

with tab2:

    st.header("Song-Level Comeback Analysis")

    song_table = filtered_frequency.merge(
        filtered_retention[
            [
                "song_artist_key",
                "average_retention_days"
            ]
        ],
        on="song_artist_key",
        how="left"
    )

    song_table = song_table.sort_values(
        "reentry_count",
        ascending=False
    )

    st.dataframe(
        song_table[
            [
                "song",
                "artist",
                "reentry_count",
                "average_retention_days"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    search_song = st.text_input(
        "Search for a song"
    )

    if search_song:

        results = song_table[
            song_table["song"].str.contains(
                search_song,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

# --------------------------------------------------
# TAB 3: ARTIST ANALYSIS
# --------------------------------------------------

with tab3:

    st.header("Artist-Level Comeback Performance")

    filtered_artist = artist[
        artist["artist"].isin(
            filtered_frequency["artist"].unique()
        )
    ]

    top_artists = filtered_artist.sort_values(
        "total_comeback_events",
        ascending=False
    ).head(15)

    fig = px.bar(
        top_artists,
        x="total_comeback_events",
        y="artist",
        orientation="h",
        color="average_fandom_proxy_score",
        title="Top Artists by Comeback Events",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        filtered_artist.sort_values(
            "total_comeback_events",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# TAB 4: MOMENTUM & RETENTION
# --------------------------------------------------

with tab4:

    st.header("Momentum and Retention Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            filtered_retention,
            x="average_retention_days",
            nbins=25,
            title="Average Retention Distribution",
            color_discrete_sequence=["#60A5FA"]
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.histogram(
            filtered_momentum,
            x="average_momentum_score",
            nbins=25,
            title="Momentum Score Distribution",
            color_discrete_sequence=["#A78BFA"]
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Rank Recovery Analysis")

    recovery_filtered = recovery[
        recovery["song_artist_key"].isin(
            filtered_keys
        )
    ]

    st.dataframe(
        recovery_filtered,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# TAB 5: FANDOM PROXY
# --------------------------------------------------

with tab5:

    st.header("Fandom Intensity Proxy Analysis")

    fig = px.bar(
        filtered_fandom.sort_values(
            "fandom_intensity_score",
            ascending=False
        ).head(15),
        x="fandom_intensity_score",
        y="song",
        color="fandom_category",
        orientation="h",
        title="Top 15 Songs by Fandom Proxy Score",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        filtered_fandom[
            [
                "song",
                "artist",
                "reentry_count",
                "fandom_intensity_score",
                "fandom_category"
            ]
        ].sort_values(
            "fandom_intensity_score",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Fandom intensity is a custom chart-based proxy. "
        "It does not measure actual fanbase size or engagement."
    )

# --------------------------------------------------
# TAB 6: ALBUM COMPARISON
# --------------------------------------------------

with tab6:

    st.header("Album vs Single Comeback Advantage")

    fig = px.bar(
        album,
        x="album_type",
        y="average_retention_days",
        color="album_type",
        title="Average Retention by Album Type",
        text="average_retention_days",
        color_discrete_sequence=["#60A5FA", "#A78BFA"]
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        album,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "South Korea Top 50 Playlist Analysis | "
    "Research and Data Analytics Project"
)

st.caption(
    "All findings are based on the available chart "
    "dataset and the project's defined analytical methods."
)
