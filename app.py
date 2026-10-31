# ============================================================
# REEL INSIGHTS
# End-to-End Exploratory Data Analysis of the Global Movie
# Industry (TMDB)
#
# Technology: Python, Pandas, SQLite, Streamlit
# ============================================================

from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. APP SETUP
# ============================================================

st.set_page_config(
    page_title="Reel Insights",
    page_icon="🎬",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "reel_insights.db"

TABLE_NAMES = {
    "movies",
    "genres",
    "movie_genres",
    "cast",
    "crew",
    "movie_keywords"
}


# ============================================================
# 2. DATABASE HELPER FUNCTIONS
# ============================================================

@st.cache_data(show_spinner=False)
def read_table(table_name):
    """Read a table from the SQLite database."""

    if table_name not in TABLE_NAMES:
        raise ValueError(f"Unknown database table: {table_name}")

    connection = sqlite3.connect(str(DB_PATH))

    try:
        return pd.read_sql_query(
            f'SELECT * FROM "{table_name}"',
            connection
        )
    finally:
        connection.close()


def standardize_columns(df, aliases):
    """
    Standardize column names and handle common naming variations.
    For example, movieId becomes movie_id.
    """

    df = df.copy()

    df.columns = [
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        for column in df.columns
    ]

    rename_columns = {}

    for expected_name, alternatives in aliases.items():

        if expected_name in df.columns:
            continue

        for alternative in alternatives:

            alternative = (
                alternative.strip()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            if alternative in df.columns:
                rename_columns[alternative] = expected_name
                break

    return df.rename(columns=rename_columns)


def to_number(series):
    """Convert a column to numbers safely."""

    return pd.to_numeric(series, errors="coerce")


def show_table(df):
    """Display a table or a message if there are no results."""

    if df is None or df.empty:
        st.info(
            "No results match the current filters. "
            "Try widening your filters in the sidebar."
        )
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


def display_money(value):
    """Format a number as a dollar amount."""

    value = pd.to_numeric(
        pd.Series([value]),
        errors="coerce"
    ).iloc[0]

    if pd.isna(value):
        return "Not available"

    return f"${value:,.0f}"


# ============================================================
# 3. CHECK AND LOAD THE DATABASE
# ============================================================

if not DB_PATH.exists():
    st.error(
        "The SQLite database was not found.\n\n"
        f"Expected location: {DB_PATH}\n\n"
        "Please check that reel_insights.db is inside the data folder."
    )
    st.stop()


try:
    raw_movies = read_table("movies")
    raw_genres = read_table("genres")
    raw_movie_genres = read_table("movie_genres")
    raw_cast = read_table("cast")
    raw_crew = read_table("crew")
    raw_keywords = read_table("movie_keywords")

except Exception as error:
    st.error(
        "Could not load the database tables. "
        f"Database error: {error}"
    )
    st.stop()


# Standardize movie table columns.

movies = standardize_columns(
    raw_movies,
    {
        "movie_id": ["movieid", "id", "film_id"],
        "title": ["movie_title"],
        "release_date": ["releasedate"],
        "original_language": ["originallanguage", "language"],
        "vote_average": ["voteaverage", "rating"],
        "vote_count": ["votecount", "num_votes"]
    }
)


# Standardize genre table columns.

genres = standardize_columns(
    raw_genres,
    {
        "genre_id": ["genreid", "id"],
        "genre_name": ["name", "genre"]
    }
)


# Standardize movie-to-genre relationship columns.

movie_genres = standardize_columns(
    raw_movie_genres,
    {
        "movie_id": ["movieid", "film_id"],
        "genre_id": ["genreid"]
    }
)


# Standardize cast table columns.

cast = standardize_columns(
    raw_cast,
    {
        "movie_id": ["movieid", "film_id"],
        "actor_name": [
            "person_name",
            "name",
            "cast_name",
            "original_name"
        ]
    }
)


# Standardize crew table columns.

crew = standardize_columns(
    raw_crew,
    {
        "movie_id": ["movieid", "film_id"],
        "person_name": [
            "name",
            "crew_name",
            "director_name",
            "original_name"
        ],
        "job": ["role", "department_job"]
    }
)


# Standardize keyword table columns.

movie_keywords = standardize_columns(
    raw_keywords,
    {
        "movie_id": ["movieid", "film_id"],
        "keyword_id": ["keywordid"],
        "keyword_name": ["name", "keyword", "keywords"]
    }
)


# Check that the most important columns exist.

required_movie_columns = ["movie_id", "title"]
missing_movie_columns = [
    column
    for column in required_movie_columns
    if column not in movies.columns
]

if missing_movie_columns:
    st.error(
        "The movies table is missing required columns: "
        + ", ".join(missing_movie_columns)
    )
    st.stop()


# Convert IDs to consistent numeric types for joins.

for df in [movies, movie_genres, cast, crew, movie_keywords]:

    if "movie_id" in df.columns:
        df["movie_id"] = pd.to_numeric(
            df["movie_id"],
            errors="coerce"
        )


for df in [genres, movie_genres]:

    if "genre_id" in df.columns:
        df["genre_id"] = pd.to_numeric(
            df["genre_id"],
            errors="coerce"
        )


# Convert financial and rating columns to numbers.

for column in [
    "budget",
    "revenue",
    "runtime",
    "popularity",
    "vote_average",
    "vote_count"
]:
    if column in movies.columns:
        movies[column] = to_number(movies[column])


# Convert the release date to a real date format.

if "release_date" in movies.columns:
    movies["release_date"] = pd.to_datetime(
        movies["release_date"],
        errors="coerce"
    )


if movies.empty:
    st.error("The movies table in the database is empty.")
    st.stop()


# ============================================================
# 4. APP TITLE AND SIDEBAR NAVIGATION
# ============================================================

st.title("🎬 Reel Insights")

st.caption(
    "An End-to-End Exploratory Data Analysis of the "
    "Global Movie Industry (TMDB)"
)

st.sidebar.title("🎬 Reel Insights")
st.sidebar.write("Explore the global movie industry.")

page = st.sidebar.radio(
    "Choose a page",
    ["Filters", "Dashboard", "Query Explorer"],
    key="navigation_page"
)


# ============================================================
# 5. SHARED FILTERS
# These filters are visible on all pages.
# Streamlit stores widget selections in session_state.
# ============================================================

st.sidebar.divider()
st.sidebar.subheader("Shared Movie Filters")

# Minimum rating filter.

minimum_rating = 0.0

if "vote_average" in movies.columns:

    minimum_rating = st.sidebar.slider(
        "Minimum rating",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.5,
        key="filter_minimum_rating"
    )


# Release year filter.

year_range = None

if "release_date" in movies.columns:

    available_years = (
        movies["release_date"]
        .dropna()
        .dt.year
    )

    if not available_years.empty:

        minimum_year = int(available_years.min())
        maximum_year = int(available_years.max())

        if minimum_year < maximum_year:

            year_range = st.sidebar.slider(
                "Release year range",
                min_value=minimum_year,
                max_value=maximum_year,
                value=(minimum_year, maximum_year),
                step=1,
                key="filter_year_range"
            )

        else:
            year_range = (minimum_year, maximum_year)
            st.sidebar.caption(
                f"Available release year: {minimum_year}"
            )


# Genre filter.

genre_options = ["All genres"]

if "genre_name" in genres.columns:

    available_genres = sorted(
        genres["genre_name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    genre_options += available_genres


selected_genre = st.sidebar.selectbox(
    "Genre",
    genre_options,
    key="filter_genre"
)


# Language filter.

language_options = ["All languages"]

if "original_language" in movies.columns:

    available_languages = sorted(
        movies["original_language"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    language_options += available_languages


selected_language = st.sidebar.selectbox(
    "Original language",
    language_options,
    key="filter_language"
)


# Movie title search.

title_search = st.sidebar.text_input(
    "Search movie title",
    key="filter_title_search"
)

st.sidebar.caption(
    "These filters apply to the Filters, Dashboard, "
    "and Query Explorer pages."
)


# ============================================================
# 6. APPLY THE SHARED FILTERS
# ============================================================

filtered_movies = movies.copy()


# Apply minimum rating.

if "vote_average" in filtered_movies.columns:

    filtered_movies = filtered_movies[
        filtered_movies["vote_average"] >= minimum_rating
    ]


# Apply release year.

if year_range and "release_date" in filtered_movies.columns:

    movie_years = filtered_movies["release_date"].dt.year

    filtered_movies = filtered_movies[
        movie_years.between(
            year_range[0],
            year_range[1]
        )
    ]


# Apply original language.

if (
    selected_language != "All languages"
    and "original_language" in filtered_movies.columns
):

    filtered_movies = filtered_movies[
        filtered_movies["original_language"]
        .astype(str)
        == selected_language
    ]


# Apply title search.

if title_search and "title" in filtered_movies.columns:

    filtered_movies = filtered_movies[
        filtered_movies["title"]
        .astype(str)
        .str.contains(
            title_search,
            case=False,
            na=False
        )
    ]


# Apply selected genre.

if (
    selected_genre != "All genres"
    and "genre_name" in genres.columns
    and "genre_id" in genres.columns
    and "genre_id" in movie_genres.columns
):

    selected_genre_ids = genres.loc[
        genres["genre_name"] == selected_genre,
        "genre_id"
    ].dropna().tolist()

    matching_movie_ids = movie_genres.loc[
        movie_genres["genre_id"].isin(selected_genre_ids),
        "movie_id"
    ].dropna().unique()

    filtered_movies = filtered_movies[
        filtered_movies["movie_id"].isin(matching_movie_ids)
    ]


# The selected movie IDs are used by the Query Explorer SQL queries.

selected_movie_ids = (
    filtered_movies["movie_id"]
    .dropna()
    .tolist()
)


# Filter the related tables to match the selected movies.

filtered_cast = (
    cast[cast["movie_id"].isin(selected_movie_ids)].copy()
    if "movie_id" in cast.columns
    else cast.iloc[0:0].copy()
)

filtered_crew = (
    crew[crew["movie_id"].isin(selected_movie_ids)].copy()
    if "movie_id" in crew.columns
    else crew.iloc[0:0].copy()
)

filtered_keywords = (
    movie_keywords[
        movie_keywords["movie_id"].isin(selected_movie_ids)
    ].copy()
    if "movie_id" in movie_keywords.columns
    else movie_keywords.iloc[0:0].copy()
)

filtered_movie_genres = (
    movie_genres[
        movie_genres["movie_id"].isin(selected_movie_ids)
    ].copy()
    if "movie_id" in movie_genres.columns
    else movie_genres.iloc[0:0].copy()
)


# Join the filtered movie data to the genre tables.

if (
    not filtered_movie_genres.empty
    and "genre_id" in genres.columns
    and "genre_name" in genres.columns
):

    filtered_genre_data = (
        filtered_movie_genres
        .merge(
            genres[["genre_id", "genre_name"]],
            on="genre_id",
            how="left"
        )
        .merge(
            filtered_movies,
            on="movie_id",
            how="inner"
        )
    )

else:
    filtered_genre_data = pd.DataFrame()


# ============================================================
# 7. DATABASE QUERY RUNNER
# The query runner creates a temporary table containing
# the selected movie IDs, without modifying the database.
# ============================================================

def execute_filtered_sql(query, movie_ids):
    """Run a SQL query limited to the selected movie IDs."""

    connection = sqlite3.connect(str(DB_PATH))

    try:

        connection.execute(
            "CREATE TEMP TABLE selected_movie_ids (movie_id)"
        )

        id_rows = []

        for value in movie_ids:

            if pd.isna(value):
                continue

            if hasattr(value, "item"):
                value = value.item()

            id_rows.append((value,))

        connection.executemany(
            """
            INSERT INTO selected_movie_ids (movie_id)
            VALUES (?)
            """,
            id_rows
        )

        result = pd.read_sql_query(query, connection)

        return result

    finally:
        connection.close()


# ============================================================
# 8. FILTERS PAGE
# ============================================================

if page == "Filters":

    st.header("🎞️ Movie Filters")

    st.write(
        "Use the shared filters in the sidebar to explore "
        "different groups of movies."
    )

    metric1, metric2 = st.columns(2)

    metric1.metric(
        "Movies matching filters",
        f"{len(filtered_movies):,}"
    )

    if "vote_average" in filtered_movies.columns:

        filtered_average_rating = filtered_movies[
            "vote_average"
        ].mean()

        metric2.metric(
            "Average rating",
            (
                f"{filtered_average_rating:.2f}"
                if pd.notna(filtered_average_rating)
                else "N/A"
            )
        )

    st.subheader("Filtered Movie Results")

    st.caption(
        "The table previews up to 500 movies. "
        "The download button exports all matching movies."
    )

    show_table(filtered_movies.head(500))

    st.download_button(
        "Download filtered movies as CSV",
        data=filtered_movies.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="filtered_movies.csv",
        mime="text/csv"
    )


# ============================================================
# 9. DASHBOARD PAGE
# ============================================================

elif page == "Dashboard":

    st.header("📊 Movie Industry Dashboard")

    # Four required KPI metrics.

    total_movies = len(filtered_movies)

    total_genres = (
        filtered_genre_data["genre_name"].nunique()
        if (
            not filtered_genre_data.empty
            and "genre_name" in filtered_genre_data.columns
        )
        else 0
    )

    total_actors = (
        filtered_cast["actor_name"].nunique()
        if "actor_name" in filtered_cast.columns
        else 0
    )

    average_rating = (
        filtered_movies["vote_average"].mean()
        if "vote_average" in filtered_movies.columns
        else float("nan")
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Total movies",
        f"{total_movies:,}"
    )

    kpi2.metric(
        "Genres represented",
        f"{total_genres:,}"
    )

    kpi3.metric(
        "Total actors",
        f"{total_actors:,}"
    )

    kpi4.metric(
        "Average rating",
        (
            f"{average_rating:.2f}"
            if pd.notna(average_rating)
            else "N/A"
        )
    )

    st.divider()

    # --------------------------------------------------------
    # Chart 1: Top 10 movies by revenue
    # --------------------------------------------------------

    st.subheader("Top 10 Movies by Revenue")

    if (
        "title" in filtered_movies.columns
        and "revenue" in filtered_movies.columns
    ):

        revenue_data = filtered_movies.copy()

        revenue_data["revenue"] = to_number(
            revenue_data["revenue"]
        )

        revenue_data = revenue_data[
            revenue_data["revenue"] > 0
        ]

        top_revenue = revenue_data.nlargest(
            10,
            "revenue"
        )

        if not top_revenue.empty:

            st.bar_chart(
                top_revenue.set_index("title")["revenue"]
            )

        else:
            st.info(
                "No movies with recorded positive revenue "
                "match the current filters."
            )

    # --------------------------------------------------------
    # Chart 2: Genre distribution
    # --------------------------------------------------------

    st.subheader("Genre Distribution")

    if (
        not filtered_genre_data.empty
        and "genre_name" in filtered_genre_data.columns
    ):

        genre_counts = (
            filtered_genre_data
            .groupby("genre_name")["movie_id"]
            .nunique()
            .sort_values(ascending=False)
            .head(15)
        )

        st.bar_chart(genre_counts)

    else:
        st.info("No genre data matches the current filters.")

    # --------------------------------------------------------
    # Chart 3: Budget versus revenue
    # --------------------------------------------------------

    st.subheader("Budget vs Revenue")

    if all(
        column in filtered_movies.columns
        for column in ["budget", "revenue"]
    ):

        scatter_data = filtered_movies[
            ["budget", "revenue"]
        ].copy()

        scatter_data["budget"] = to_number(
            scatter_data["budget"]
        )

        scatter_data["revenue"] = to_number(
            scatter_data["revenue"]
        )

        scatter_data = scatter_data.dropna(
            subset=["budget", "revenue"]
        )

        # Zero values mean financial data is unknown.
        scatter_data = scatter_data[
            (scatter_data["budget"] > 0)
            & (scatter_data["revenue"] > 0)
        ]

        if not scatter_data.empty:

            st.scatter_chart(
                scatter_data,
                x="budget",
                y="revenue"
            )

            st.caption(
                "Each point represents a movie with positive recorded "
                "budget and revenue. Zero values are excluded because "
                "they represent unknown financial figures."
            )

        else:
            st.info(
                "No movies with positive budget and revenue "
                "match the current filters."
            )

    # --------------------------------------------------------
    # Chart 4: Releases by year
    # --------------------------------------------------------

    st.subheader("Movie Releases by Year")

    if "release_date" in filtered_movies.columns:

        releases = (
            filtered_movies["release_date"]
            .dropna()
            .dt.year
            .value_counts()
            .sort_index()
        )

        if not releases.empty:
            st.line_chart(releases)
    # --------------------------------------------------------
        # --------------------------------------------------------
    # Chart 5: Correlation heatmap
    # --------------------------------------------------------

    st.subheader("Correlation Heatmap")

    correlation_columns = [
        "runtime",
        "budget",
        "revenue",
        "popularity",
        "vote_average",
        "vote_count"
    ]

    available_correlation_columns = [
        column
        for column in correlation_columns
        if column in filtered_movies.columns
    ]

    if len(available_correlation_columns) >= 2:

        correlation_data = filtered_movies[
            available_correlation_columns
        ].copy()

        for column in available_correlation_columns:
            correlation_data[column] = pd.to_numeric(
                correlation_data[column],
                errors="coerce"
            )

        # Zero budget and revenue values represent unknown values.
        if "budget" in correlation_data.columns:
            correlation_data["budget"] = (
                correlation_data["budget"].replace(
                    0,
                    float("nan")
                )
            )

        if "revenue" in correlation_data.columns:
            correlation_data["revenue"] = (
                correlation_data["revenue"].replace(
                    0,
                    float("nan")
                )
            )

        correlation_matrix = correlation_data.corr()

        fig, ax = plt.subplots(figsize=(10, 7))

        sns.heatmap(
            correlation_matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            center=0,
            linewidths=0.5,
            ax=ax
        )

        ax.set_title(
            "Correlation Between Movie Performance Variables"
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info(
            "There is not enough numerical data to create "
            "the correlation heatmap."
        )
    # --------------------------------------------------------
    # Automatic business insight
    # --------------------------------------------------------

    st.subheader("Insight")

    if (
        not filtered_genre_data.empty
        and "revenue" in filtered_genre_data.columns
    ):

        financial_genres = filtered_genre_data.copy()

        financial_genres["revenue"] = to_number(
            financial_genres["revenue"]
        )

        financial_genres = financial_genres[
            financial_genres["revenue"] > 0
        ]

        if not financial_genres.empty:

            revenue_by_genre = (
                financial_genres
                .groupby("genre_name")["revenue"]
                .sum()
                .sort_values(ascending=False)
            )

            if not revenue_by_genre.empty:

                highest_grossing_genre = revenue_by_genre.index[0]
                genre_revenue = revenue_by_genre.iloc[0]

                st.info(
                    f"Within the current filtered selection, "
                    f"**{highest_grossing_genre}** has the highest "
                    f"combined recorded movie revenue "
                    f"({display_money(genre_revenue)}). "
                    f"This is a descriptive finding for this dataset, "
                    f"not proof that genre alone causes higher revenue."
                )

            else:
                st.info(
                    "There is not enough recorded revenue data "
                    "to generate a genre insight."
                )

        else:
            st.info(
                "There is not enough recorded revenue data "
                "to generate a genre insight."
            )

    else:
        st.info(
            "Genre or revenue data is not available "
            "for the current selection."
        )


# ============================================================
# 10. QUERY EXPLORER: SQL QUERIES
# ============================================================

elif page == "Query Explorer":

    st.header("🔎 SQL Query Explorer")

    st.write(
        "Choose one of the ten required SQL questions. "
        "The results use the movies selected by the shared filters."
    )

    QUERY_LABELS = {
        "Question 1 — Action movies released after 2015": "q1",
        "Question 2 — Top 10 highest-grossing movies and genres": "q2",
        "Question 3 — Average budget and revenue by genre": "q3",
        "Question 4 — Top 10 actors by movie appearances": "q4",
        "Question 5 — Directors with more than 3 movies": "q5",
        "Question 6 — Top 10 most frequently used keywords": "q6",
        "Question 7 — Above-average budget and below-average revenue": "q7",
        "Question 8 — Actors in Christopher Nolan movies": "q8",
        "Question 9 — Highest-rated genre with at least 20 movies": "q9",
        "Question 10 — Top 10 movies by keyword count": "q10"
    }

    QUERY_SQL = {

        # QUESTION 1
        "q1": """
            SELECT DISTINCT
                m.title,
                m.release_date
            FROM selected_movie_ids AS selected
            JOIN movies AS m
                ON m.movie_id = selected.movie_id
            JOIN movie_genres AS mg
                ON mg.movie_id = m.movie_id
            JOIN genres AS g
                ON g.genre_id = mg.genre_id
            WHERE LOWER(TRIM(g.genre_name)) = 'action'
              AND CAST(
                    strftime('%Y', m.release_date) AS INTEGER
                  ) > 2015
            ORDER BY m.release_date, m.title;
        """,

        # QUESTION 2
        "q2": """
            SELECT
                m.title,
                GROUP_CONCAT(DISTINCT g.genre_name) AS genres,
                CAST(m.revenue AS REAL) AS revenue
            FROM selected_movie_ids AS selected
            JOIN movies AS m
                ON m.movie_id = selected.movie_id
            JOIN movie_genres AS mg
                ON mg.movie_id = m.movie_id
            JOIN genres AS g
                ON g.genre_id = mg.genre_id
            WHERE CAST(COALESCE(m.revenue, 0) AS REAL) > 0
            GROUP BY m.movie_id, m.title, m.revenue
            ORDER BY CAST(m.revenue AS REAL) DESC
            LIMIT 10;
        """,

        # QUESTION 3
        "q3": """
            SELECT
                g.genre_name AS genre,
                AVG(
                    NULLIF(CAST(m.budget AS REAL), 0)
                ) AS average_budget,
                AVG(
                    NULLIF(CAST(m.revenue AS REAL), 0)
                ) AS average_revenue,
                COUNT(DISTINCT m.movie_id) AS movie_count
            FROM selected_movie_ids AS selected
            JOIN movies AS m
                ON m.movie_id = selected.movie_id
            JOIN movie_genres AS mg
                ON mg.movie_id = m.movie_id
            JOIN genres AS g
                ON g.genre_id = mg.genre_id
            GROUP BY g.genre_name
            ORDER BY average_revenue DESC;
        """,

        # QUESTION 4
        "q4": """
            SELECT
                c.actor_name AS actor,
                COUNT(DISTINCT c.movie_id) AS movie_count
            FROM selected_movie_ids AS selected
            JOIN "cast" AS c
                ON c.movie_id = selected.movie_id
            WHERE c.actor_name IS NOT NULL
              AND TRIM(c.actor_name) <> ''
            GROUP BY c.actor_name
            ORDER BY movie_count DESC, actor
            LIMIT 10;
        """,

        # QUESTION 5
        "q5": """
            SELECT
                cr.person_name AS director,
                COUNT(DISTINCT cr.movie_id) AS movie_count
            FROM selected_movie_ids AS selected
            JOIN crew AS cr
                ON cr.movie_id = selected.movie_id
            WHERE LOWER(TRIM(COALESCE(cr.job, ''))) = 'director'
              AND cr.person_name IS NOT NULL
              AND TRIM(cr.person_name) <> ''
            GROUP BY cr.person_name
            HAVING COUNT(DISTINCT cr.movie_id) > 3
            ORDER BY movie_count DESC, director;
        """,

        # QUESTION 6
        "q6": """
            SELECT
                mk.keyword_name AS keyword,
                COUNT(DISTINCT mk.movie_id) AS movie_count
            FROM selected_movie_ids AS selected
            JOIN movie_keywords AS mk
                ON mk.movie_id = selected.movie_id
            WHERE mk.keyword_name IS NOT NULL
              AND TRIM(mk.keyword_name) <> ''
            GROUP BY mk.keyword_id, mk.keyword_name
            ORDER BY movie_count DESC, keyword
            LIMIT 10;
        """,

                # QUESTION 7
        # Compare against averages across the entire database.
        # Zero budget/revenue values are treated as unknown.
        "q7": """
            WITH overall_averages AS (
                SELECT
                    AVG(NULLIF(CAST(budget AS REAL), 0))
                        AS average_budget,
                    AVG(NULLIF(CAST(revenue AS REAL), 0))
                        AS average_revenue
                FROM movies
            )
            SELECT
                m.title,
                CAST(m.budget AS REAL) AS budget,
                CAST(m.revenue AS REAL) AS revenue
            FROM selected_movie_ids AS selected
            JOIN movies AS m
                ON m.movie_id = selected.movie_id
            CROSS JOIN overall_averages AS averages
            WHERE CAST(COALESCE(m.budget, 0) AS REAL) > 0
              AND CAST(COALESCE(m.revenue, 0) AS REAL) > 0
              AND CAST(m.budget AS REAL) > averages.average_budget
              AND CAST(m.revenue AS REAL) < averages.average_revenue
            ORDER BY budget DESC;
        """,

        # QUESTION 8
        "q8": """
            SELECT DISTINCT
                m.title,
                c.actor_name AS actor
            FROM selected_movie_ids AS selected
            JOIN movies AS m
                ON m.movie_id = selected.movie_id
            JOIN "cast" AS c
                ON c.movie_id = m.movie_id
            WHERE m.movie_id IN (
                SELECT cr.movie_id
                FROM crew AS cr
                JOIN selected_movie_ids AS selected_director_movie
                    ON selected_director_movie.movie_id = cr.movie_id
                WHERE LOWER(TRIM(COALESCE(cr.job, ''))) = 'director'
                  AND cr.person_name LIKE '%Christopher Nolan%'
            )
            AND c.actor_name IS NOT NULL
            ORDER BY m.title, actor;
        """,

        # QUESTION 9
        "q9": """
            SELECT
                g.genre_name AS genre,
                AVG(CAST(m.vote_average AS REAL)) AS average_rating,
                COUNT(DISTINCT m.movie_id) AS movie_count
            FROM selected_movie_ids AS selected
            JOIN movies AS m
                ON m.movie_id = selected.movie_id
            JOIN movie_genres AS mg
                ON mg.movie_id = m.movie_id
            JOIN genres AS g
                ON g.genre_id = mg.genre_id
            WHERE m.vote_average IS NOT NULL
            GROUP BY g.genre_name
            HAVING COUNT(DISTINCT m.movie_id) >= 20
            ORDER BY average_rating DESC
            LIMIT 1;
        """,

        # QUESTION 10
        "q10": """
            SELECT
                m.title,
                COUNT(
                    DISTINCT COALESCE(
                        CAST(mk.keyword_id AS TEXT),
                        mk.keyword_name
                    )
                ) AS keyword_count
            FROM selected_movie_ids AS selected
            JOIN movies AS m
                ON m.movie_id = selected.movie_id
            JOIN movie_keywords AS mk
                ON mk.movie_id = m.movie_id
            GROUP BY m.movie_id, m.title
            ORDER BY keyword_count DESC, m.title
            LIMIT 10;
        """
    }


    # --------------------------------------------------------
    # Choose and execute a query.
    # --------------------------------------------------------

    selected_question = st.selectbox(
        "Choose a SQL question",
        options=list(QUERY_LABELS.keys()),
        key="query_explorer_question"
    )

    question_id = QUERY_LABELS[selected_question]

    try:

        query_result = execute_filtered_sql(
            QUERY_SQL[question_id],
            selected_movie_ids
        )

    except Exception as error:

        st.error(
            "This query could not run. "
            f"Database error: {error}"
        )

        query_result = pd.DataFrame()


    # --------------------------------------------------------
    # Show result table.
    # --------------------------------------------------------

    st.subheader("Query Results")

    show_table(query_result)


    # --------------------------------------------------------
    # Show chart.
    # --------------------------------------------------------

    if not query_result.empty:

        st.subheader("Chart")

        if question_id == "q1":

            chart_dates = pd.to_datetime(
                query_result["release_date"],
                errors="coerce"
            )

            year_counts = (
                chart_dates
                .dropna()
                .dt.year
                .value_counts()
                .sort_index()
            )

            if not year_counts.empty:
                st.bar_chart(year_counts)
            else:
                st.caption(
                    "There are no valid release dates to chart."
                )

        elif question_id == "q7":

            chart_data = query_result[
                ["budget", "revenue"]
            ].dropna()

            if not chart_data.empty:

                st.scatter_chart(
                    chart_data,
                    x="budget",
                    y="revenue"
                )

            else:
                st.caption(
                    "There are no complete budget and revenue values to chart."
                )

        elif question_id == "q8":

            actor_counts = (
                query_result["actor"]
                .value_counts()
                .head(10)
                .sort_values()
            )

            if not actor_counts.empty:
                st.bar_chart(actor_counts)

        else:

            chart_columns = {
                "q2": ("title", "revenue"),
                "q3": ("genre", "average_revenue"),
                "q4": ("actor", "movie_count"),
                "q5": ("director", "movie_count"),
                "q6": ("keyword", "movie_count"),
                "q9": ("genre", "average_rating"),
                "q10": ("title", "keyword_count")
            }

            if question_id in chart_columns:

                x_column, y_column = chart_columns[question_id]

                if (
                    x_column in query_result.columns
                    and y_column in query_result.columns
                ):

                    chart_data = query_result[
                        [x_column, y_column]
                    ].dropna()

                    chart_data = chart_data.head(10)

                    if not chart_data.empty:

                        st.bar_chart(
                            chart_data.set_index(x_column)[y_column]
                        )

    # --------------------------------------------------------
    # Generate an insight for the selected query.
    # --------------------------------------------------------

    st.subheader("Insight")

    if query_result.empty:

        insight_text = (
            "No results were found for this question under the current "
            "filters. Try changing the release year, rating, language, "
            "title search, or genre in the sidebar."
        )

    elif question_id == "q1":

        insight_text = (
            f"The filtered dataset contains {len(query_result)} "
            "Action movies released after 2015."
        )

    elif question_id == "q2":

        first_row = query_result.iloc[0]

        insight_text = (
            f"{first_row['title']} has the highest recorded revenue "
            f"among the returned movies, at "
            f"{display_money(first_row['revenue'])}. "
            f"Its listed genre(s): {first_row['genres']}."
        )

    elif question_id == "q3":

        rows_with_revenue = query_result.dropna(
            subset=["average_revenue"]
        )

        if not rows_with_revenue.empty:

            first_row = rows_with_revenue.iloc[0]

            insight_text = (
                f"{first_row['genre']} has the highest average recorded "
                f"revenue among the returned genres, at "
                f"{display_money(first_row['average_revenue'])}."
            )

        else:
            insight_text = (
                "The selected movies do not contain sufficient "
                "known revenue values for a genre comparison."
            )

    elif question_id == "q4":

        first_row = query_result.iloc[0]

        insight_text = (
            f"{first_row['actor']} has the highest number of distinct "
            f"movie appearances among the returned actors, with "
            f"{int(first_row['movie_count'])} movies."
        )

    elif question_id == "q5":

        first_row = query_result.iloc[0]

        insight_text = (
            f"{first_row['director']} has directed "
            f"{int(first_row['movie_count'])} movies in the filtered "
            "dataset. The table includes directors with more than "
            "three movies."
        )

    elif question_id == "q6":

        first_row = query_result.iloc[0]

        insight_text = (
            f"The keyword '{first_row['keyword']}' appears in "
            f"{int(first_row['movie_count'])} distinct movies "
            "in the filtered dataset."
        )

    elif question_id == "q7":

        insight_text = (
            f"{len(query_result)} movies have a positive recorded "
            "budget above the overall dataset average budget and "
            "positive recorded revenue below the overall dataset "
            "average revenue. This comparison alone does not prove "
            "that every movie made a financial loss."
        )

    elif question_id == "q8":

        unique_actors = query_result["actor"].nunique()

        insight_text = (
            f"The results contain {unique_actors} distinct actors "
            "across the filtered movies directed by Christopher Nolan."
        )

    elif question_id == "q9":

        first_row = query_result.iloc[0]

        insight_text = (
            f"{first_row['genre']} is the highest-rated genre among "
            f"genres with at least 20 distinct movies in the filtered "
            f"dataset, averaging {first_row['average_rating']:.2f} "
            f"across {int(first_row['movie_count'])} movies."
        )

    else:

        first_row = query_result.iloc[0]

        insight_text = (
            f"{first_row['title']} has the highest keyword count "
            "among the returned movies, with "
            f"{int(first_row['keyword_count'])} keywords."
        )

    st.info(insight_text)

    st.caption(
        "Results and insights are descriptive of the selected dataset. "
        "They do not establish causation."
    )


# ============================================================
# END OF REEL INSIGHTS APP
# ============================================================