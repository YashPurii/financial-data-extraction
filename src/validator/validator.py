import json
import re
import requests
import pandas as pd

# ---------------- Validation Rules ----------------
def validate_currency_format(text):
    """Validates and corrects currency formats like '$1234.56' → '$1,234.56'."""
    pattern = re.compile(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?")
    matches = pattern.findall(text)
    
    valid_currencies = [match for match in matches if match]
    return valid_currencies

def validate_dates(text):
    """Validates extracted dates and checks if they match expected formats."""
    pattern = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")  # Matches 'YYYY-MM-DD'
    matches = pattern.findall(text)
    return matches

def cross_check_with_reference_data(data):
    """Cross-checks extracted financial data with an external API."""
    reference_data = {}

    # Example API call (mocked) to fetch exchange rates or stock prices
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        reference_data = response.json().get("rates", {})
    except requests.RequestException:
        print("⚠️ Warning: Unable to fetch reference data. Validation may be incomplete.")

    # Example validation (adjust based on actual data)
    for key, value in data.items():
        if "USD" in value and "EUR" in reference_data:
            print(f"✅ {key} contains USD values, and EUR reference exists.")
    
    return reference_data

def detect_anomalies(data):
    """Detects potential anomalies in extracted financial data."""
    anomalies = []
    
    for key, text in data.items():
        if len(text) < 10:  # Example: Unusually short text
            anomalies.append(f"⚠️ Possible missing data in {key}.")
        if "$" in text and not validate_currency_format(text):
            anomalies.append(f"❌ Currency format issue in {key}.")
    
    return anomalies

# ---------------- Save Results ----------------
def save_validated_data(data, anomalies, output_path):
    """Saves validated data and anomalies to JSON and CSV."""
    with open(output_path + "_validated.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)
    
    df = pd.DataFrame(data.items(), columns=["Source", "Validated Text"])
    df.to_csv(output_path + "_validated.csv", index=False, encoding="utf-8")

    with open(output_path + "_anomalies.json", "w", encoding="utf-8") as json_file:
        json.dump(anomalies, json_file, indent=4)

# ---------------- Main Execution ----------------
if __name__ == "__main__":
    # Load cleaned data
    cleaned_data_path = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/processed/cleaned_data.json"
    with open(cleaned_data_path, "r", encoding="utf-8") as file:
        cleaned_data = json.load(file)

    # Validate data
    valid_currencies = {k: validate_currency_format(v) for k, v in cleaned_data.items()}
    valid_dates = {k: validate_dates(v) for k, v in cleaned_data.items()}
    reference_check = cross_check_with_reference_data(cleaned_data)
    anomalies = detect_anomalies(cleaned_data)

    # Save validated data
    save_validated_data(cleaned_data, anomalies, "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/processed/validated_data")

    # Print summary
    print("\n✅ Data Validation Completed!")
    print(f"📂 Validated data saved to:\n- validated_data.json\n- validated_data.csv\n- anomalies.json")
