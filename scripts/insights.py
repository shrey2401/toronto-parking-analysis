import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
data_path = os.path.expanduser("~/Desktop/toronto-parking-analysis/data/parking_tickets_cleaned.csv")
df = pd.read_csv(data_path)

# Top 10 violations
top_violations = df['infraction_description'].value_counts().nlargest(10)

# Plot
plt.figure(figsize=(10,6))
sns.barplot(x=top_violations.values, y=top_violations.index, hue=top_violations.index, legend=False, palette="viridis")
plt.title("Top 10 Parking Violations in Toronto (2024)")
plt.xlabel("Number of Tickets")
plt.ylabel("Violation Description")
plt.tight_layout()

# Save figure
os.makedirs(os.path.expanduser("~/Desktop/toronto-parking-analysis/visuals"), exist_ok=True)
plt.savefig(os.path.expanduser("~/Desktop/toronto-parking-analysis/visuals/top_violations.png"))
plt.show()
# --- Most Ticketed Streets ---
print("\n--- Generating Top Streets Chart ---")

# Extract street names from full_location
df['street_name'] = df['full_location'].str.extract(r'([A-Za-z ]+ST|AVE|RD|BLVD|DR|CRES|CT|LN|PL|WAY|TRL)')

# Count top 10 ticketed streets
top_streets = df['street_name'].value_counts().nlargest(10)

# Plot
plt.figure(figsize=(10,6))
sns.barplot(x=top_streets.values, y=top_streets.index, hue=top_streets.index, legend=False, palette="magma")
plt.title("Top 10 Most Ticketed Streets in Toronto (2024)")
plt.xlabel("Number of Tickets")
plt.ylabel("Street Name")
plt.tight_layout()

# Save chart
plt.savefig(os.path.expanduser("~/Desktop/toronto-parking-analysis/visuals/top_streets.png"))
plt.show()

