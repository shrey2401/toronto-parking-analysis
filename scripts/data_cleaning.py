import pandas as pd
import os

# Define your file path
data_path = os.path.expanduser("/Users/shrey0107/Desktop/toronto-parking-analysis/data/Parking_Tags_Data_2024_1.csv")

# Load dataset
print("Loading data...")
df = pd.read_csv(data_path)

# steps
# # Show basic info
# print("\n--- Dataset Info ---")
# print(df.info())

# print("\n--- Sample Data ---")
# print(df.head())

# # Save a small cleaned version for testing
# cleaned_path = os.path.expanduser("~/Desktop/toronto-parking-analysis/data/parking_tickets_cleaned.csv")
# df.to_csv(cleaned_path, index=False)

# print(f"\nCleaned file saved to: {cleaned_path}")
# --- Data Cleaning Section ---

# Convert date_of_infraction to datetime
df['date_of_infraction'] = pd.to_datetime(df['date_of_infraction'], format='%Y%m%d', errors='coerce')

# Clean time_of_infraction (convert float like 915.0 -> 09:15)
def format_time(t):
    try:
        t_str = str(int(t)).zfill(4)
        return f"{t_str[:2]}:{t_str[2:]}"
    except:
        return None

df['time_of_infraction'] = df['time_of_infraction'].apply(format_time)

# Merge location columns into a single column
df['full_location'] = df[['location1', 'location2', 'location3', 'location4']].fillna('').agg(' '.join, axis=1).str.strip()

# Drop unnecessary columns
df = df.drop(columns=['tag_number_masked', 'location1', 'location2', 'location3', 'location4', 'province'])

# Preview the cleaned data
print("\n--- Cleaned Data Preview ---")
print(df.head())

# Save cleaned dataset
cleaned_path = os.path.expanduser("~/Desktop/toronto-parking-analysis/data/parking_tickets_cleaned.csv")
df.to_csv(cleaned_path, index=False)

print(f"\n✅ Cleaned file saved to: {cleaned_path}")
