import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
import os
import ast

# File path for the master dataset
file_path = "/Users/rickglenn/Desktop/Movie Data Analysis/MovieData/master_movie_data.csv"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: File not found at path: {file_path}")
else:
    # Step 1: Load the dataset
    print("Loading dataset...")
    data: DataFrame = pd.read_csv(file_path)

    # Step 2: Inspect the dataset
    print("\nDataset Overview:")
    print(data.head())

    print("\nDataset Info:")
    print(data.info())

    print("\nSummary Statistics:")
    print(data.describe())

    # Step 3: Clean the data
    print("\nCleaning data...")

    # Drop rows with missing critical values (like 'title', 'genres', 'vote_average', 'revenue', 'release_date')
    data_cleaned = data.dropna(subset=['title', 'genres', 'vote_average', 'revenue', 'release_date'])

    # Convert 'release_date' to datetime
    data_cleaned['release_date'] = pd.to_datetime(data_cleaned['release_date'], errors='coerce')

    # Extract year from 'release_date'
    data_cleaned['release_year'] = data_cleaned['release_date'].dt.year

    # Step 3a: Parse the 'genres' column to convert strings to dictionaries
    data_cleaned['genres'] = data_cleaned['genres'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

    # Step 3b: Extract the genre names
    data_cleaned['genre_names'] = data_cleaned['genres'].apply(lambda genres: [genre['name'] for genre in genres])

    # Step 4: Analyze the data

    # 4.1 Most common genres
    print("\nMost Common Genres:")
    genres_list = data_cleaned['genre_names'].explode()  # Flatten the lists of genres
    most_common_genres = genres_list.value_counts().head(10)
    print(most_common_genres)

    # 4.2 Average rating by release year
    average_ratings_by_year = data_cleaned.groupby('release_year')['vote_average'].mean()
    print("\nAverage Ratings by Year:")
    print(average_ratings_by_year)

    # 4.3 Top 10 highest-grossing movies
    top_grossing = data_cleaned.sort_values(by='revenue', ascending=False).head(10)
    print("\nTop 10 Highest-Grossing Movies:")
    print(top_grossing[['title', 'revenue']])

    # Step 5: Visualize the data

    # 5.1 Genre distribution
    plt.figure(figsize=(10, 6))
    most_common_genres.plot(kind='bar', color='skyblue')
    plt.title('Most Common Genres')
    plt.xlabel('Genre')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # 5.2 Average ratings over time
    plt.figure(figsize=(12, 6))
    average_ratings_by_year.plot(kind='line', color='green')
    plt.title('Average Movie Ratings Over Time')
    plt.xlabel('Release Year')
    plt.ylabel('Average Rating')
    plt.grid()
    plt.tight_layout()
    plt.show()

    # 5.3 Top 10 highest-grossing movies
    plt.figure(figsize=(12, 6))
    plt.bar(top_grossing['title'], top_grossing['revenue'], color='orange')
    plt.title('Top 10 Highest-Grossing Movies')
    plt.xlabel('Movie Title')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    print("\nAnalysis complete!")
