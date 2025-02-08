import os
import logging
from extractor.extractor import extract_text_from_pdf, extract_text_from_image, convert_mp3_to_wav, transcribe_audio_google
from normalizer.normalizer import process_text_data, save_cleaned_data
from validator.validator import cross_check_with_reference_data, detect_anomalies, save_validated_data
from database.database import create_database, store_extracted_data

# ---------------- Setup Logging ----------------
logging.basicConfig(filename="data/logs/process.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# ---------------- File Paths ----------------
DATA_RAW_PATH = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/raw/"
DATA_PROCESSED_PATH = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/processed/"

FILES = {
    "pdf": "sample-invoice.pdf",
    "image": "Balance-Sheet.jpg",
    "audio": "NPR1180246583.mp3"
}

# ---------------- Run Full Pipeline ----------------
def run_pipeline():
    logging.info("🚀 Starting Financial Data Processing Pipeline")
    
    # Step 1: Extract Data
    try:
        extracted_data = {}
        extracted_data["PDF"] = extract_text_from_pdf(os.path.join(DATA_RAW_PATH, FILES["pdf"]))
        extracted_data["Image"] = extract_text_from_image(os.path.join(DATA_RAW_PATH, FILES["image"]))

        wav_files = convert_mp3_to_wav(os.path.join(DATA_RAW_PATH, FILES["audio"]))
        extracted_data["Audio"] = transcribe_audio_google(wav_files)

        logging.info("✅ Extraction Completed Successfully")
    except Exception as e:
        logging.error(f"❌ Error in Extraction: {e}")
        return
    
    # Save Extracted Data
    extracted_json_path = os.path.join(DATA_PROCESSED_PATH, "extracted_data.json")
    save_cleaned_data(extracted_data, extracted_json_path.replace(".json", ""))
    
    # Step 2: Clean & Normalize
    try:
        cleaned_data = process_text_data(extracted_data)
        cleaned_json_path = os.path.join(DATA_PROCESSED_PATH, "cleaned_data.json")
        save_cleaned_data(cleaned_data, cleaned_json_path.replace(".json", ""))

        logging.info("✅ Data Cleaning & Normalization Completed Successfully")
    except Exception as e:
        logging.error(f"❌ Error in Cleaning & Normalization: {e}")
        return
    
    # Step 3: Validate Data
    try:
        anomalies = detect_anomalies(cleaned_data)
        validated_json_path = os.path.join(DATA_PROCESSED_PATH, "validated_data.json")
        save_validated_data(cleaned_data, anomalies, validated_json_path.replace(".json", ""))

        logging.info("✅ Data Validation Completed Successfully")
    except Exception as e:
        logging.error(f"❌ Error in Validation: {e}")
        return
    
    # Step 4: Store in Database
    try:
        create_database()
        store_extracted_data()
        logging.info("✅ Data Stored in Database Successfully")
    except Exception as e:
        logging.error(f"❌ Error in Database Storage: {e}")
        return
    
    logging.info("🎉 Full Pipeline Completed Successfully!")

# ---------------- Run the Pipeline ----------------
if __name__ == "__main__":
    run_pipeline()
