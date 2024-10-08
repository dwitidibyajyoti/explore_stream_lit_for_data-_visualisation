import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter
import ast

# App Title
# Adds a title and icon to the browser tab
st.set_page_config(page_title="GitHub Repository Stats", page_icon="📊")
st.title("📊 GitHub Repository Statistics")


# Replace with the path to your CSV file
csv_file = "github_dataset.csv"

# Read the CSV file
df = pd.read_csv(csv_file, skip_blank_lines=True)

# Check the columns in the CSV
st.write("Columns in the dataset:", df.columns)

# Strip any leading or trailing spaces in the column names
df.columns = df.columns.str.strip()

# Display the dataframe
st.subheader("Data from CSV:")
st.dataframe(df)

# Example: Plot any available data (replace 'Date' and 'OtherColumn' with relevant columns)
st.subheader("Graph:")
# Update 'OtherColumn' with actual column name
# Update 'OtherColumn' with actual column name
# fig = px.line(df, x='repositories', y='OtherColumn',
#               title='GitHub Data Over Time')

# # Show the plot
# st.plotly_chart(fig)


if 'language' in df.columns:
    df = df.drop(columns=['language'])


df.columns = df.columns.str.strip()

df_melted_all = pd.melt(
    df, id_vars=['repositories'], var_name='Metric', value_name='Value')

# Display bar chart for all columns with different colors
st.subheader("Bar Chart of GitHub Repository Data with Different Metrics")

# Create the bar chart with different colors for each 'Metric' column
fig = px.bar(df_melted_all, x='repositories', y='Value', color='Metric',
             title='GitHub Repository Statistics', barmode='group')

# Show the plot in the Streamlit app
st.plotly_chart(fig)

# Add a select box for repositories (single select)
all_repos = df['repositories'].unique().tolist()
selected_repo = st.selectbox(
    "Select a repository to display", all_repos, index=0)

# Filter the dataframe based on the selected repository
df_filtered = df[df['repositories'] == selected_repo]

# Display the filtered dataframe
st.subheader(f"Data for {selected_repo}:")
st.dataframe(df_filtered)

# Assuming 'repositories' is the categorical column, and the rest are numeric columns
# We use `pd.melt` to reshape the dataframe
df_melted = pd.melt(df_filtered, id_vars=[
                    'repositories'], var_name='Metric', value_name='Value')

# Display bar chart for the selected repository with different metrics
st.subheader(f"Bar Chart of {selected_repo} GitHub Repository Data")

# Create the bar chart with different colors for each 'Metric' column
fig = px.bar(df_melted, x='repositories', y='Value', color='Metric',
             title=f'{selected_repo} Repository Statistics', barmode='group')

# Show the plot in the Streamlit app
st.plotly_chart(fig)


csv_file_repo = "github_dataset.csv"
df = pd.read_csv(csv_file_repo, skip_blank_lines=True)

# Print the first few rows for inspection
# print(df['languages_used'].head())

# Function to split comma-separated languages


def split_languages(x):
    # Split the string by commas and strip whitespace
    return [lang.strip() for lang in x.split(',')] if isinstance(x, str) else []


# Apply the function to the 'languages_used' column
df['language'] = df['language'].apply(split_languages)

# Flatten the list of languages from all repositories
all_languages = [lang for sublist in df['language'] for lang in sublist]

# Count occurrences of each language using Counter
language_counts = Counter(all_languages)

# Convert the result to a DataFrame for better presentation
language_count_df = pd.DataFrame(
    language_counts.items(), columns=['language', 'count'])

# Plotting the pie chart for languages used in the repository
fig = px.pie(language_count_df, values='count', names='language',
             title='Language Distribution in the Repository')

# Display the plot in Streamlit
st.plotly_chart(fig)
