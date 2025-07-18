import pandas as pd
import matplotlib.pyplot as plt
import os

def brand_performance_analysis(filename):
    if not os.path.isfile(filename):
        print(f"Error: File not found -> {filename}")
        return

    df = pd.read_csv(filename)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Brand'] = df['Brand'].astype(str).str.strip().str.lower()
    df = df[(df['Brand'] != 'n/a') & (df['Brand'] != 'nan') & (df['Brand'] != '')]

    if df.empty:
        print("No valid brand data found in the file.")
        return

    brand_freq = df['Brand'].value_counts()
    brand_avg_rating = df.groupby('Brand')['Rating'].mean()
    brand_stats = pd.DataFrame({
        'Frequency': brand_freq,
        'Average_Rating': brand_avg_rating
    }).reset_index().rename(columns={'index': 'Brand'})
    brand_stats = brand_stats.sort_values(by='Frequency', ascending=False)

    top5_brands = brand_stats.head(5)
    median_freq = brand_stats['Frequency'].median()
    high_rated_low_freq = brand_stats[
        (brand_stats['Frequency'] < median_freq) & 
        (brand_stats['Average_Rating'] >= 4)
    ]

    print("\nTop 5 Brands by Frequency:")
    print(top5_brands)

    print("\nHigh-Rated (>=4) but Less Frequent Brands:")
    print(high_rated_low_freq)

    plt.figure(figsize=(10,6))
    plt.bar(top5_brands['Brand'], top5_brands['Frequency'], color='steelblue')
    plt.title('Top 5 Brands by Frequency in Sponsored Products')
    plt.xlabel('Brand')
    plt.ylabel('Number of Sponsored Products')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    top5_sum = top5_brands['Frequency'].sum()
    others_sum = brand_stats['Frequency'].sum() - top5_sum

    sizes = list(top5_brands['Frequency']) + [others_sum]
    labels = list(top5_brands['Brand']) + ['Others']

    plt.figure(figsize=(8,8))
    plt.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=140, 
        colors=plt.cm.Paired.colors[:len(sizes)]
    )
    plt.title('Market Share of Top Brands in Sponsored Products')
    plt.show()

if __name__ == "__main__":
    filename = input("Enter CSV filename: ").strip()
    brand_performance_analysis(filename)
