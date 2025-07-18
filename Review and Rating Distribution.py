import pandas as pd
import matplotlib.pyplot as plt
import os

def review_rating_distribution(filename):
    if not os.path.isfile(filename):
        print(f"Error: File not found -> {filename}")
        return

    df = pd.read_csv(filename)

    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0).astype(int)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    df = df.dropna(subset=['Title', 'Rating'])

    if df.empty:
        print("No valid data found for analysis.")
        return

    top_by_reviews = df.sort_values(by='Reviews', ascending=False).head(5)
    top_by_rating = df.sort_values(by=['Rating', 'Reviews'], ascending=[False, False]).head(5)

    print("\nTop 5 Products by Number of Reviews:")
    print(top_by_reviews[['Title', 'Reviews', 'Rating']])

    print("\nTop 5 Products by Rating:")
    print(top_by_rating[['Title', 'Rating', 'Reviews']])

    plt.figure(figsize=(10,6))
    plt.barh(top_by_rating['Title'], top_by_rating['Rating'], color='seagreen')
    plt.xlabel('Rating')
    plt.title('Top 5 Highest Rated Products')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10,6))
    plt.barh(top_by_reviews['Title'], top_by_reviews['Reviews'], color='royalblue')
    plt.xlabel('Number of Reviews')
    plt.title('Top 5 Most Reviewed Products')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    filename = input("Enter CSV filename (in current folder): ").strip()
    review_rating_distribution(filename)
