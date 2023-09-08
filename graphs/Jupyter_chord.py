import pandas as pd
import holoviews as hv
from holoviews import opts, dim

# Load the dataset
data_path = "/Users/jerryhughes/Desktop/coding/4chan graphs/Main graphs/pol_top_contextual_thematic_matrix chord.csv"
df = pd.read_csv(data_path)

# Convert the co-occurrence matrix to a long format
links = df.melt(id_vars='Unnamed: 0', var_name='target', value_name='value')

# Rename the columns
links.columns = ['source', 'target', 'value']

# Remove rows with a value of zero (no link)
links = links[links['value'] != 0]

# Drop any rows with NaN values
links = links.dropna(subset=['value'])

# Create a list of all unique names from source and target columns
all_nodes = list(set(df['Unnamed: 0']).union(set(df.columns[1:])))

# Create the nodes dataframe
nodes = pd.DataFrame(all_nodes, columns=['name'])

# Create a mapping from node names to indices
node_indices = pd.Series(range(len(nodes['name'])), index=nodes['name'])

# Replace node names with indices in links dataframe
links['source'] = links['source'].map(node_indices)
links['target'] = links['target'].map(node_indices)

# Initialize HoloViews with the bokeh backend
hv.extension('bokeh')
hv.output(size=900)

# Load the links data into a DataFrame and the nodes data into a Dataset
links_df = hv.Dataset(links, ['source', 'target'])
nodes_df = hv.Dataset(nodes, 'index')

# Create the Chord plot
chord = hv.Chord((links_df, nodes_df)).select(value=(1, None))

# Set options for coloring nodes and edges, and adding labels
chord.opts(
    opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('target').str(), edge_line_width=0.5, edge_alpha=0.8, 
               labels='name', node_color=dim('index').str())
)
