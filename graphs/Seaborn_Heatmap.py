import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load your data (replace with the correct path)
data = pd.read_csv('/Users/jerryhughes/Desktop/pol heatmap.csv')

# Replace 'Null' strings with NaNs
data = data.replace('Null', np.nan)

# Replace '(Contextual)' with '(C)' and '(Thematic)' with '(T)' in columns and index
data.columns = data.columns.str.replace('(Contextual)', '(C)')
data.columns = data.columns.str.replace('(Thematic)', '(T)')
data[data.columns[0]] = data[data.columns[0]].str.replace('(Contextual)', '(C)')
data[data.columns[0]] = data[data.columns[0]].str.replace('(Thematic)', '(T)')

# Convert all columns to numeric type (except the first one which is the index)
for col in data.columns[1:]:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Define new color map
cmap_cubehelix = sns.cubehelix_palette(start=2, rot=0, dark=0.95, light=0, reverse=True, as_cmap=True)

# Set plot size
plt.figure(figsize=(16,14))

# Set the background color to white
plt.gca().set_facecolor('white')

# Create a mask for the upper triangle
mask = np.triu(np.ones_like(data.set_index(data.columns[0]), dtype=bool))

# Create heatmap with data values displayed and box borders
# Update vmax to the new maximum value, which is 20
heatmap = sns.heatmap(data.set_index(data.columns[0]).clip(upper=20), cmap=cmap_cubehelix, vmin=1, vmax=20, annot=True, fmt=".0f", linewidths=.5, mask=mask)

# Add labels and title
plt.xlabel('Attributes')
plt.ylabel('Rows')
plt.title('Heatmap')

# Show plot
plt.show()


Heat map no numbers 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load your data (replace with the correct path)
data = pd.read_csv('/Users/jerryhughes/Desktop/pol heatmap.csv')

# Replace 'Null' strings with NaNs
data = data.replace('Null', np.nan)

# Replace '(Contextual)' with '(C)' and '(Thematic)' with '(T)' in columns and index
data.columns = data.columns.str.replace('(Contextual)', '(C)')
data.columns = data.columns.str.replace('(Thematic)', '(T)')
data[data.columns[0]] = data[data.columns[0]].str.replace('(Contextual)', '(C)')
data[data.columns[0]] = data[data.columns[0]].str.replace('(Thematic)', '(T)')

# Convert all columns to numeric type (except the first one which is the index)
for col in data.columns[1:]:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Define new color map
cmap_cubehelix = sns.cubehelix_palette(start=2, rot=0, dark=0.95, light=0, reverse=True, as_cmap=True)

# Set plot size
plt.figure(figsize=(16,14))

# Set the background color to white
plt.gca().set_facecolor('white')

# Create a mask for the upper triangle
mask = np.triu(np.ones_like(data.set_index(data.columns[0]), dtype=bool))

# Create heatmap with data values displayed and box borders
# Update vmax to the new maximum value, which is 20
heatmap = sns.heatmap(data.set_index(data.columns[0]).clip(upper=20), cmap=cmap_cubehelix, vmin=1, vmax=20, annot=False, fmt=".0f", linewidths=.5, mask=mask)

# Add labels and title
plt.xlabel('Attributes')
plt.ylabel('Rows')
plt.title('Heatmap')

# Show plot
plt.show()
