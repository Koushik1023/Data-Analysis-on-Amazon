import pandas as pd
import matplotlib.pyplot as plt
import os

def price_vs_rating_analysis(filename):
    if not os.path.isfile(filename):
        print(f"Error: File not found -> {filename}")
        return

    df = pd.read_csv(filename)

    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Price'] = df['Price'].astype(str).str.replace('[^0-9.]', '', regex=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    df = df.dropna(subset=['Price', 'Rating'])

    if df.empty:
        print("No valid data with both price and rating found.")
        return

    bins = [0, 1, 2, 3, 4, 5]
    labels = ['0-1', '1-2', '2-3', '3-4', '4-5']
    df['Rating_Range'] = pd.cut(df['Rating'], bins=bins, labels=labels, include_lowest=True)

    avg_price_by_rating = df.groupby('Rating_Range')['Price'].mean()

    print("\nAverage Price by Rating Range:")
    print(avg_price_by_rating)

    median_price = df['Price'].median()

    affordable_high_rated = df[(df['Price'] < median_price) & (df['Rating'] >= 4)]
    print(f"\nAffordable & High-Rated Products (Price < {median_price:.2f} & Rating >= 4):")
    print(affordable_high_rated[['Title', 'Price', 'Rating']].head(10))

    expensive_low_rated = df[(df['Price'] > median_price) & (df['Rating'] < 3)]
    print(f"\nExpensive & Poorly Rated Products (Price > {median_price:.2f} & Rating < 3):")
    print(expensive_low_rated[['Title', 'Price', 'Rating']].head(10))

    plt.figure(figsize=(10,6))
    plt.scatter(df['Rating'], df['Price'], alpha=0.6, c='dodgerblue', edgecolors='w', s=60)
    plt.title('Price vs Rating Scatter Plot')
    plt.xlabel('Rating')
    plt.ylabel('Price (INR)')
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(8,5))
    avg_price_by_rating.plot(kind='bar', color='coral')
    plt.title('Average Price by Rating Range')
    plt.xlabel('Rating Range')
    plt.ylabel('Average Price (INR)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    file_name = input("Enter the CSV filename (in current folder): ").strip()
    price_vs_rating_analysis(file_name)
