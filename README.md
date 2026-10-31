# Reel Insights: An End-to-End Exploratory Data Analysis of the Global Movie Industry

## 1. Project Overview

**Reel Insights** is an end-to-end exploratory data analysis project using movie data from **The Movie Database (TMDB)**.

The project works with a **multi-file relational dataset containing six linked CSV tables**. It demonstrates data cleaning, relational data validation, SQL analysis, Python-based exploratory data analysis, data visualisation, insight generation, and interactive dashboard development.

The project uses **Python, Pandas, NumPy, SQLite, SQL, Matplotlib, Seaborn, Plotly, Jupyter Notebook, and Streamlit**.

The analysis explores movie ratings, budgets, revenues, profitability, genres, actors, directors, keywords, release trends, popularity, and audience engagement.

---

## 2. Project Objectives

The main objectives of the project are to:

- Clean and prepare six related CSV datasets.
- Validate relationships between the linked datasets.
- Perform data wrangling and feature engineering using Pandas and NumPy.
- Design and use a relational SQLite database.
- Connect Python to SQLite using the `sqlite3` library.
- Answer 10 analytical questions using SQL.
- Perform 10 analyses using Pandas.
- Conduct univariate, bivariate, and multivariate exploratory data analysis.
- Create visualisations using Matplotlib, Seaborn, and Plotly.
- Generate meaningful insights from the analysis.
- Translate analytical findings into business recommendations.
- Build an interactive Streamlit application with Filters, Dashboard, and Query Explorer pages.

---

## 3. Technologies Used

- **Python** — core programming language
- **Pandas** — data cleaning, manipulation, analysis, and feature engineering
- **NumPy** — numerical operations
- **SQLite** — relational database management
- **SQL** — querying and analysing relational data
- **sqlite3** — Python database connectivity
- **Matplotlib** — static data visualisation
- **Seaborn** — statistical data visualisation and correlation analysis
- **Plotly** — interactive data visualisation
- **Jupyter Notebook** — data cleaning, SQL analysis, Pandas analysis, and visualisation workflow
- **Streamlit** — interactive dashboard development

---

## 4. Project Structure

ReelInsights/
└── reel/
    ├── app.py
    ├── check_data.py
    ├── check_database.py
    ├── README.md
    ├── requirements.txt
    ├── run_sql.py
    │
    ├── data/
    │   ├── movies.csv
    │   ├── genres.csv
    │   ├── movie_genres.csv
    │   ├── cast.csv
    │   ├── crew.csv
    │   ├── movie_keywords.csv
    │   ├── movies_cleaned_corrected.csv
    │   ├── genres_cleaned.csv
    │   ├── movie_genres_cleaned.csv
    │   ├── cast_cleaned.csv
    │   ├── crew_cleaned.csv
    │   ├── movie_keywords_cleaned.csv
    │   └── reel_insights.db
    │
    ├── notebook/
    │   ├── 01_data_cleaning.ipynb
    │   ├── 02_sql_analysis.ipynb
    │   ├── 03_pandas_analysis.ipynb
    │   └── 04_visualizations.ipynb
    │
    ├── charts/
    │   ├── chart_01_rating_distribution.png
    │   ├── chart_02_top_revenue.png
    │   ├── chart_03_genre_popularity.png
    │   ├── chart_04_budget_vs_revenue.png
    │   ├── chart_05_releases_per_year.png
    │   ├── chart_06_top_actors.png
    │   ├── chart_07_rating_by_genre.png
    │   ├── chart_08_runtime_distribution.png
    │   ├── chart_09_popularity_vs_votes.png
    │   └── chart_10_top_keywords.png
    │
    └── sql/
        ├── 01_top_revenue.sql
        ├── 02_genre_counts.sql
        ├── 03_genre_ratings.sql
        ├── 04_top_profit.sql
        ├── 05_top_directors.sql
        ├── 06_top_keywords.sql
        ├── 07_movies_per_year.sql
        ├── 08_runtime_by_genre.sql
        ├── 09_budget_revenue.sql
        └── 10_top_rated_movies.sql

---

## 5. Dataset and Relational Structure

The project uses six linked datasets:

1. **Movies** — contains the main movie-level information.
2. **Genres** — contains genre IDs and genre names.
3. **Movie Genres** — links movies with their associated genres.
4. **Cast** — contains movie cast information.
5. **Crew** — contains movie crew information.
6. **Movie Keywords** — contains keywords associated with movies.

The datasets are connected using movie and genre identifiers, allowing information from multiple tables to be combined for relational analysis.

### Cleaned Dataset Record Counts

| Dataset | Records |
|---|---:|
| Movies | 2,503 |
| Genres | 19 |
| Movie–genre relationships | 6,878 |
| Cast | 24,902 |
| Crew | 7,289 |
| Movie keywords | 41,681 |

---

## 6. Data Cleaning and Preparation

The data-cleaning stage prepares the six related datasets for analysis.

The cleaning process includes:

- Inspecting dataset dimensions and data types.
- Identifying and removing exact duplicate records.
- Converting release dates into an appropriate date format.
- Handling missing and invalid values.
- Treating zero budget and revenue values as unknown where appropriate.
- Checking movie IDs across related tables.
- Checking genre IDs between genre and movie–genre tables.
- Maintaining relational consistency between datasets.
- Saving cleaned datasets separately from the original raw files.

The cleaned datasets are then used for SQL, Pandas, and visualisation analysis.

---

## 7. Relational Database and SQL Analysis

The cleaned datasets are stored in a **SQLite relational database** named:

`reel_insights.db`

Python connects to the database using the built-in **sqlite3** library.

The database contains six main tables:

- `movies`
- `genres`
- `movie_genres`
- `cast`
- `crew`
- `movie_keywords`

SQL queries are used to investigate movie performance, financial information, genres, actors, directors, keywords, and other industry patterns.

The project contains **10 SQL analytical questions**, with SQL query files stored in the `sql` folder.

---

## 8. Pandas Analysis

Pandas is used alongside SQL to explore and analyse the cleaned movie datasets.

The Pandas analysis examines areas such as:

- Movie ratings
- Popularity
- Budgets
- Revenue
- Profitability
- Return on investment
- Genres
- Actors and directors
- Keywords
- Movie release patterns

This demonstrates how similar business and analytical questions can be investigated using Python-based data analysis.

---

## 9. Exploratory Data Analysis

The project includes **univariate, bivariate, and multivariate exploratory data analysis**.

### Univariate Analysis

Univariate analysis examines individual variables independently.

For example, the distribution of movie ratings is analysed using a **Seaborn histogram and density curve** to understand how ratings are distributed across the dataset.

### Bivariate Analysis

Bivariate analysis examines the relationship between two variables.

A **Plotly scatter plot** is used to explore the relationship between movie **budget and revenue**. The interactive chart allows individual movie observations to be explored.

### Multivariate Analysis

Multivariate analysis examines relationships among several variables simultaneously.

A **Seaborn correlation heatmap** is used to examine relationships among:

- Runtime
- Budget
- Revenue
- Popularity
- Vote average
- Vote count

This helps identify how financial, audience, and movie characteristics relate to one another.

---

## 10. Data Visualisation

The project uses multiple visualisation libraries:

### Matplotlib

Matplotlib is used to create static visualisations for the exploratory analysis.

### Seaborn

Seaborn is used for statistical visualisations, including:

- Movie rating distribution
- Correlation heatmap

### Plotly

Plotly is used to create interactive visualisations, including the relationship between movie budget and revenue.

Together, these visualisations make the analytical findings easier to interpret and communicate.

---

## 11. Key Findings

### 1. Movie Ratings

The average movie rating is approximately **6.94 out of 10**.

**The Shawshank Redemption** has the highest average rating in the cleaned dataset.

### 2. Box-Office Revenue

**Avatar** leads the recorded revenue results, generating approximately **$2.924 billion** in revenue.

### 3. Genre Performance

Adventure has the highest average revenue among the genres analysed, at approximately **$400.31 million**.

This represents an average across movies with recorded information and does not guarantee the performance of an individual film.

### 4. Movie Release Trends

The year **2016** has the highest number of movie releases represented in the dataset, with **121 movies**.

Recent years may contain incomplete data, so comparisons should be interpreted carefully.

### 5. Popularity and Audience Votes

Movie popularity and vote count have a positive correlation of approximately **0.36**.

This suggests that movies with greater popularity tend to receive more audience votes. However, correlation does not establish causation.

---

## 12. Business Insights and Recommendations

The exploratory analysis provides several insights that may support decision-making in the movie industry.

### Key Business Insights

- Movie budget and revenue show a positive relationship, suggesting that larger investments can be associated with greater revenue potential. However, a high production budget does not guarantee commercial success.
- Popularity and audience engagement provide useful indicators of movie performance but should be interpreted together with financial and rating information.
- Genre-level analysis shows differences in historical commercial performance across movie genres.
- High audience ratings do not necessarily correspond to the highest box-office revenue.
- Historical movie data can provide useful evidence for identifying patterns in movie performance.

### Recommendations

1. **Evaluate investment risk using multiple factors.**  
   Production companies should consider budget, expected revenue, genre, popularity, and audience demand together rather than assuming that a larger budget will automatically result in greater financial success.

2. **Use multiple performance indicators.**  
   Financial performance, popularity, ratings, and audience engagement should be considered together when evaluating movie performance.

3. **Consider historical genre performance.**  
   Studios and investors can use historical genre-level performance as one factor when assessing future movie projects.

4. **Monitor audience engagement.**  
   Popularity and voting activity can provide useful signals of audience interest and may support marketing and distribution decisions.

5. **Support decisions with data.**  
   Historical movie data can support production, marketing, and investment planning. However, past performance should not be treated as a guarantee of future success.

---

## 13. Streamlit Application

An interactive Streamlit application was developed to make the analysis easier to explore.

The application contains three main pages:

### Filters

Allows users to filter and explore movie records using available criteria such as ratings, release year, genre, language, and movie title.

### Dashboard

Displays summary statistics and visualisations related to movie performance, including revenue, genres, budgets, ratings, and release trends.

### Query Explorer

Allows users to explore the results of the project's **10 analytical SQL questions** and view the associated insights and visualisations.

---

## 14. How to Run the Project

### Prerequisites

Python must be installed on the computer.

Open a terminal inside the `reel` folder of the main `ReelInsights` project.

### Install Required Libraries

Run:

```bash
python -m pip install -r requirements.txt
```

### Launch the Streamlit Application

Run:

```bash
python -m streamlit run app.py
```

Streamlit will start the application and provide a local address that can be opened in a web browser.

---

## 15. Project Workflow

The overall project workflow is:

**Raw CSV Data → Data Cleaning → Cleaned Relational Data → SQLite Database → SQL Analysis → Pandas EDA → Data Visualisation → Streamlit Dashboard → Business Insights and Recommendations**

This workflow demonstrates an end-to-end data analytics process using a multi-table relational movie dataset.

---

## 16. Limitations

The analysis has several limitations:

- Budget and revenue values are unavailable or recorded as zero for some movies.
- The dataset represents a selected collection of movies and should not be assumed to represent the entire global film industry.
- Recent release years may contain incomplete movie records.
- TMDB popularity is a platform-specific measure and should not be interpreted as a direct measure of financial success.
- Correlations identify relationships between variables but do not establish causation.
- Historical performance does not guarantee the future performance of a movie.

---

## 17. Conclusion

Reel Insights demonstrates an end-to-end data analytics workflow using a multi-file relational movie dataset.

The project combines **data cleaning, relational schema validation, Python data wrangling, feature engineering, SQLite and SQL analysis, Pandas-based exploratory analysis, univariate/bivariate/multivariate EDA, Matplotlib, Seaborn, Plotly, Streamlit dashboarding, insight generation, and business recommendation writing**.

The analysis shows how data from multiple related sources can be transformed into meaningful insights and presented through both analytical notebooks and an interactive application to support data-driven decision-making.