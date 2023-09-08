import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import matplotlib.patches as mpatches

# Load the data
data = pd.read_csv("/Users/jerryhughes/Desktop/pol image analysis - Code System.csv")

# Get the names of the codes and their types
data['category'] = data['Codes'].apply(lambda x: x.replace(" (Contextual)", "").replace(" (Thematic)", ""))
data['type'] = data['Codes'].apply(lambda x: 'contextual' if 'Contextual' in x else 'thematic')

# Split the data into two subsets based on the type
contextual_data = data[data['type'] == 'contextual']
thematic_data = data[data['type'] == 'thematic']

# Select the top 15 codes from each subset
top_contextual = contextual_data.nlargest(15, 'Frequency')
top_thematic = thematic_data.nlargest(15, 'Frequency')

# Combine the top codes into a single DataFrame
top_data = pd.concat([top_contextual, top_thematic])

# Order the DataFrame by 'Frequency'
top_data = top_data.sort_values('Frequency', ascending=False)

# Apply a linear normalization to the 'Frequency' column
top_data['Frequency_normalized'] = (top_data['Frequency'] - top_data['Frequency'].min()) / (top_data['Frequency'].max() - top_data['Frequency'].min())

# Adjust the normalization so the minimum is 0.5 instead of 0
top_data['Frequency_normalized'] = 0.5 + 0.5 * top_data['Frequency_normalized']

# Create a color palette with the 'Blues' cmap for contextual codes and the 'Reds' cmap for thematic codes
top_data['color'] = top_data.apply(lambda row: cm.Blues(row['Frequency_normalized']) if row['type'] == 'contextual' else cm.Reds(row['Frequency_normalized']), axis=1)

# Set the figure size and style
plt.figure(figsize=(15, 10))
sns.set_style("whitegrid")

# Create a bar plot with a black border around the bars
sns.barplot(x='Frequency', y='category', data=top_data, orient='h', palette=top_data['color'], edgecolor="black", linewidth=1)

# Set the labels and title with larger font sizes
plt.xlabel('Total Uses', fontsize=15)
plt.ylabel('Codes', fontsize=15)
plt.title('Usage of Top Contextual and Thematic Codes', fontsize=20)

# Increase the font size of the tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Create a legend with matplotlib patches
contextual_patch = mpatches.Patch(color=cm.Blues(0.5), label='Contextual Codes')
thematic_patch = mpatches.Patch(color=cm.Reds(0.5), label='Thematic Codes')
plt.legend(handles=[contextual_patch, thematic_patch], loc='lower right')

# Adjust the layout
plt.tight_layout()

# Display the plot
plt.show()
