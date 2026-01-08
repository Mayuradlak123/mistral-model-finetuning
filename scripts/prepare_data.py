import csv
import json
import random
import os
import sys

# Add project root to path to import app modules if needed, or just stand-alone logger setup
# Since this is a script, we can do a quick local setup or append path.
# Let's try to append path to use our nice logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logger import logger

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, 'property_data.csv')
OUTPUT_TRAIN = os.path.join(BASE_DIR, 'scripts', 'training_data.jsonl')
OUTPUT_VAL = os.path.join(BASE_DIR, 'scripts', 'validation_data.jsonl')

def create_message(system_content, user_content, assistant_content):
    """Creates a message list in Mistral chat format."""
    messages = []
    messages.append({"role": "user", "content": user_content})
    messages.append({"role": "assistant", "content": assistant_content})
    return {"messages": messages}

def prepare_data():
    logger.info(f"Reading data from {CSV_FILE}...")
    
    data_entries = []
    
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Variant 1: General details
                user_q1 = f"Can you give me the details for property {row['Property_ID']}?"
                ans_1 = (f"Certainly. {row['Property_Name']} is a {row['Property_Type']} located in {row['Location']}. "
                         f"It has {row['Bedrooms']} bedrooms, {row['Bathrooms']} bathrooms, and is {row['Size_sqft']} sqft. "
                         f"The price is ${row['Price_USD']}. It was built in {row['Year_Built']} and is currently {row['Status']}.")
                data_entries.append(create_message(None, user_q1, ans_1))
                
                # Variant 2: Specific attribute (Price)
                user_q2 = f"How much does the {row['Property_Type']} at {row['Location']} (ID: {row['Property_ID']}) cost?"
                ans_2 = f"The price for property {row['Property_ID']} is ${row['Price_USD']}."
                data_entries.append(create_message(None, user_q2, ans_2))
                
                # Variant 3: Status check
                user_q3 = f"Is property {row['Property_ID']} available for purchase?"
                ans_3 = f"The current status of property {row['Property_ID']} is {row['Status']}."
                data_entries.append(create_message(None, user_q3, ans_3))
                
                # Variant 4: Natural language query about specs
                user_q4 = f"Tell me about the size and rooms of {row['Property_Name']}."
                ans_4 = f"It is {row['Size_sqft']} square feet with {row['Bedrooms']} bedrooms and {row['Bathrooms']} bathrooms."
                data_entries.append(create_message(None, user_q4, ans_4))
    except FileNotFoundError:
        logger.error(f"File not found: {CSV_FILE}")
        return

    # Shuffle and split
    random.shuffle(data_entries)
    split_index = int(len(data_entries) * 0.9) # 90% train, 10% val
    train_data = data_entries[:split_index]
    val_data = data_entries[split_index:]
    
    logger.info(f"Generated {len(data_entries)} total examples.")
    logger.info(f"Writing {len(train_data)} to {OUTPUT_TRAIN}")
    logger.info(f"Writing {len(val_data)} to {OUTPUT_VAL}")
    
    with open(OUTPUT_TRAIN, 'w', encoding='utf-8') as f:
        for entry in train_data:
            f.write(json.dumps(entry) + '\n')
            
    with open(OUTPUT_VAL, 'w', encoding='utf-8') as f:
        for entry in val_data:
            f.write(json.dumps(entry) + '\n')

if __name__ == "__main__":
    prepare_data()
