import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data.csv")
data = data.dropna(subset=['Exercise']).reset_index(drop=True)
data = data.drop([0, 1]).reset_index(drop=True)

data = data.fillna("0x0x0lbs")

df = data


# Function to extract sets, reps, and weight from a string like "3x10x20lbs"
def extract_sets_reps_weight(s):
    try:
        sets, reps, weight = s.replace('lbs', '').split('x')
        return int(sets), int(reps), int(weight)
    except ValueError:
        # Returns 0 for each value if the format is incorrect or if it's "0x0x0lbs"
        return 0, 0, 0

# Apply the function to each cell in the DataFrame (excluding the 'Exercise' column)
for column in df.columns[1:]:  # Skipping the first column which is 'Exercise'
    df[column] = df[column].apply(extract_sets_reps_weight)

# Now, each cell in the DataFrame (except for the 'Exercise' column) contains a tuple of (sets, reps, weight)

# Calculate total weight lifted per exercise per session (sets * reps * weight)
df['Total Weight Lifted'] = df.apply(lambda row: sum(row[column][0] * row[column][1] * row[column][2] for column in df.columns[1:-1]), axis=1)

# Calculate total reps per exercise per session (sets * reps)
df['Total Reps'] = df.apply(lambda row: sum(row[column][0] * row[column][1] for column in df.columns[1:-2]), axis=1)

# Optional: Calculate average weight per rep per exercise session
df['Average Weight Per Rep'] = df.apply(lambda row: row['Total Weight Lifted'] / row['Total Reps'] if row['Total Reps'] > 0 else 0, axis=1)

# At this point, you have three new columns with aggregated metrics per exercise session:
# 'Total Weight Lifted', 'Total Reps', and 'Average Weight Per Rep'

# To analyze trends, you can:
# 1. Group by 'Exercise' and calculate the mean/median of these metrics over all sessions.
# 2. Look at the progression of 'Total Weight Lifted' or 'Average Weight Per Rep' over time for specific exercises.

# Example of grouping by 'Exercise' and calculating mean metrics
summary = df.groupby('Exercise')[['Total Weight Lifted', 'Total Reps', 'Average Weight Per Rep']].mean()

# Example of showing progression for a specific exercise (replace 'Exercise Name' with an actual exercise name)
specific_exercise_progress = df[df['Exercise'] == 'Exercise Name'][['Date', 'Total Weight Lifted', 'Total Reps', 'Average Weight Per Rep']]
specific_exercise_progress.set_index('Date', inplace=True)

print(summary)

# Melting the DataFrame
df_melted = df.melt(id_vars='Exercise', var_name='Date', value_name='Metrics')

# Assuming Metrics are in the format "setsxrepsxweightlbs" and you want to extract these
def extract_metrics(metric_str):
    sets, reps, weight = 0, 0, 0
    try:
        sets, reps, weight = map(int, metric_str.replace('lbs', '').split('x'))
    except ValueError:  # Handles cases like '0x0x0lbs' or any parsing error
        pass
    return sets, reps, weight

# Applying the extraction function to separate sets, reps, and weight
df_melted[['Sets', 'Reps', 'Weight']] = df_melted.apply(lambda row: pd.Series(extract_metrics(row['Metrics'])), axis=1)

# Now, df_melted contains a row for each exercise session with columns for 'Exercise', 'Date', 'Sets', 'Reps', 'Weight'
