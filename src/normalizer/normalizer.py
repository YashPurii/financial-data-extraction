import re
import json
import pandas as pd

# ---------------- Data Cleaning ----------------
def clean_text(text):
    """Cleans extracted text by removing extra spaces, special characters, and fixing encodings."""
    if not text:
        return ""

    text = text.replace("\n", " ")  # Remove newlines
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^a-zA-Z0-9$.,%/-]", " ", text)  # Keep financial characters
    text = text.strip()
    
    return text

# ---------------- Normalization ----------------
def normalize_numbers(text):
    """Converts financial abbreviations like '$1M' to full format '$1,000,000'."""
    text = re.sub(r"\$([\d.]+)M", lambda x: f"${float(x.group(1)) * 1_000_000:,.2f}", text)
    text = re.sub(r"\$([\d.]+)K", lambda x: f"${float(x.group(1)) * 1_000:,.2f}", text)
    return text

def normalize_dates(text):
    """Standardizes date formats (e.g., 'Jan 1, 2024' → '2024-01-01')."""
    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
              "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    pattern = re.compile(r"(\b[A-Za-z]{3}) (\d{1,2}), (\d{4})")
    text = pattern.sub(lambda x: f"{x.group(3)}-{months[x.group(1)]}-{int(x.group(2)):02d}", text)
    
    return text

# ---------------- Apply Cleaning & Normalization ----------------
def process_text_data(data):
    """Applies cleaning and normalization to extracted data."""
    cleaned_data = {}
    for source, text in data.items():
        text = clean_text(text)
        text = normalize_numbers(text)
        text = normalize_dates(text)
        cleaned_data[source] = text
    return cleaned_data

# ---------------- Save to JSON & CSV ----------------
def save_cleaned_data(data, output_path):
    """Saves cleaned and normalized data to JSON and CSV."""
    with open(output_path + ".json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

    df = pd.DataFrame(data.items(), columns=["Source", "Cleaned Text"])
    df.to_csv(output_path + ".csv", index=False, encoding="utf-8")

# ---------------- Main Execution ----------------
if __name__ == "__main__":
    # Load extracted data
    extracted_data_path = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/processed/extracted_data.json"
    with open(extracted_data_path, "r", encoding="utf-8") as file:
        extracted_data = json.load(file)

    # Process data
    cleaned_data = process_text_data(extracted_data)

    # Save cleaned data
    save_cleaned_data(cleaned_data, "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/processed/cleaned_data")

    print("\n✅ Data Cleaning & Normalization Completed!")
    print("📂 Cleaned data saved to: \n- cleaned_data.json\n- cleaned_data.csv")
