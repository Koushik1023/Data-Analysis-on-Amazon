import pandas as pd
import re

product = input("Enter product name: ").strip().lower()
input_file = f"sponsored_{product}_raw.csv"
output_file = f"sponsored_{product}_cleaned.csv"

try:
    df = pd.read_csv(input_file)
    original_len = len(df)

    df.columns = df.columns.str.strip().str.lower().str.capitalize()
    df.drop_duplicates(inplace=True)

    def clean_price(val):
        if pd.isna(val):
            return None
        val = re.sub(r"[^\d.]", "", str(val))
        return float(val) if val else None

    def clean_reviews(val):
        if pd.isna(val):
            return 0
        val = re.sub(r"[^\d]", "", str(val).replace(',', ''))
        return int(val) if val else 0

    def clean_rating(val):
        try:
            val = float(str(val).strip())
            return val if 0 <= val <= 5 else None
        except:
            return None

    if 'Price' in df.columns:
        df['Price'] = df['Price'].apply(clean_price)

    if 'Reviews' in df.columns:
        df['Reviews'] = df['Reviews'].apply(clean_reviews)

    if 'Rating' in df.columns:
        df['Rating'] = df['Rating'].apply(clean_rating)

    if 'Price' in df.columns:
        df = df[df['Price'].notna() & (df['Price'] > 0)]
        if df['Price'].notna().any():
            df['Price'] = df['Price'].fillna(df['Price'].median())

    if 'Rating' in df.columns:
        if df['Rating'].notna().any():
            df['Rating'] = df['Rating'].fillna(df['Rating'].median()).infer_objects(copy=False)
        else:
            df['Rating'] = df['Rating'].fillna(0)

    if 'Reviews' in df.columns:
        df['Reviews'] = df['Reviews'].fillna(0).infer_objects(copy=False)

    df.dropna(subset=['Price', 'Rating'], inplace=True)

    cleaned_len = len(df)
    df.to_csv(output_file, index=False)

    print(f"Cleaned data saved to '{output_file}'")
    print(f"{original_len - cleaned_len} rows removed during cleaning")

except FileNotFoundError:
    print(f"File '{input_file}' not found.")
except Exception as e:
    print(f"Error occurred: {e}")
