from flask import Flask, jsonify, render_template
import pandas as pd
from flask_cors import CORS
from scipy.spatial.distance import correlation
from sklearn.decomposition import PCA
from flask import Flask, jsonify, render_template, request
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances
import numpy as np

app = Flask(__name__)
CORS(app)

# Load your data and define categorical columns
data = pd.read_csv('preprocessed_data.csv')
categorical = ['Marital status', 'Application mode', 'Course', 'Daytime/evening attendance', "Mother's occupation", "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor', 'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Target']
numerical = [ 'Application order', 'Age at enrollment', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)', 'Unemployment rate', 'Inflation rate', 'GDP']
desired_columns = numerical + categorical
# Filter DataFrame to keep only the desired columns
#columns_to_keep = [col for col in desired_columns if col in data.columns]
#filtered_data = data
categorical = [ 'Marital status', 'Course', 'Displaced',
       'Debtor', 'Gender',
        'Attendance', 'Special needs',
       'Fees Paid', 'Scholarship', 'Target']
numerical = [ 'Application order', 'Age at enrollment', 'Unemployment rate',
       'Inflation rate', 'GDP', 'Units 1st sem credit', 'Units 1st sem enroll',
       'Units 1st sem approved', 'Units 1st sem grade', 'Units 1st sem eval',
       'Units 1st sem without eval', 'Target']

cat_df_pi = data[categorical]




@app.route('/piechart_data', methods=['GET'])
def get_piechart_data():
    try:
        # Dictionary to store results
        results = {}

        # Iterate over each column (variable) in the categorical DataFrame
        for col in categorical:
            # Group by the column and 'Target', then count occurrences
            counts = cat_df_pi.groupby([col, 'Target']).size().unstack(fill_value=0)

            # Convert counts DataFrame to a nested dictionary with specific keys
            counts_dict = counts.to_dict(orient='index')

            # Store the nested dictionary in results with column name as key
            results[col] = counts_dict

        # Convert results dictionary to JSON format and return
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# For Radar Chart

data_df = pd.read_csv('sampled_data.csv')
from flask import Flask, jsonify
from scipy.spatial.distance import correlation
import pandas as pd

#pp = Flask(__name__)

# Assuming `data` is your dataset
# Create a DataFrame from the dataset
df = pd.DataFrame(data_df)

# Get column names
column_names = df.select_dtypes(include=['number']).columns.tolist()

# Remove non-numeric columns
numeric_df = df[column_names]

# Calculate the correlation distance between each pair of columns
correlation_distances = []
column_names_array = []

for col1 in column_names:
    distances = []
    for col2 in column_names:
        if col1 != col2:
            dist = correlation(numeric_df[col1], numeric_df[col2])
            distances.append({"axis": col2, "value": dist})
    correlation_distances.append(distances)
    column_names_array.append(col1)



# Define route to serve correlation data
@app.route('/correlation_data', methods=['GET'])
def get_correlation_data():
    data = {
        "column_names": column_names_array,
        "correlation_distances": correlation_distances
    }
    #print(data)
    return jsonify(data)


#Barplot Data 


data = pd.read_csv('preprocessed_data.csv')
categorical = ['Marital status', 'Application mode', 'Course', 'Daytime/evening attendance', "Mother's occupation", "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor', 'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Target']
numerical = [ 'Application order', 'Age at enrollment', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)', 'Unemployment rate', 'Inflation rate', 'GDP']
desired_columns = numerical + categorical
# Filter DataFrame to keep only the desired columns
#columns_to_keep = [col for col in desired_columns if col in data.columns]
#filtered_data = data
categorical = [ 'Marital status', 'Course', 'Displaced',
       'Debtor', 'Gender',
        'Attendance', 'Special needs',
       'Fees Paid', 'Scholarship', 'Target']
numerical = [ 'Application order', 'Age at enrollment', 'Unemployment rate',
       'Inflation rate', 'GDP', 'Units 1st sem credit', 'Units 1st sem enroll',
       'Units 1st sem approved', 'Units 1st sem grade', 'Units 1st sem eval',
       'Units 1st sem without eval', 'Target']

cat_data = data[categorical]
num_data = data[numerical]

#data = filtered_data
#cat_data = data[categorical]
#num_data = data[numerical]
#print (cat_data)

@app.route('/get_categorical_data', methods=['GET'])
def get_categorical_data():
    return jsonify(cat_data.to_dict(orient='records'))


@app.route('/getdata_barplot', methods=['GET'])
def get_data():
    # Your DataFrame
    #cat_data = pd.DataFrame()  # Replace this with your actual DataFrame

    column_counts = {}

    # Iterate over each column in the DataFrame
    for col in cat_data.columns:
        # Get value counts of unique classes in the column
        counts = cat_data[col].value_counts().to_dict()
        # Store the counts dictionary with column name as key
        column_counts[col] = counts

    # Return the dictionary containing counts for all columns
    print("column counts",column_counts)
    return jsonify(column_counts)
# Endpoint to render HTML page with D3 visualization

# For MDS Plot

data_df = pd.read_csv('sampled_data.csv')

col_names = data_df.columns.tolist()
"""
# Print the column names
#print(col_names)

# Standardize the data
X_standardized = (X - X.mean()) / X.std()

# Convert data to numpy array
data = X_standardized.values

# Randomly sample 500 points from the data
sampled_indices = np.random.choice(data.shape[0], size=500, replace=False)
sampled_data = data[sampled_indices]

# Create a DataFrame with the sampled data
sampled_df = pd.DataFrame(data_df, columns=col_names)

# Save the DataFrame to a CSV file
sampled_df.to_csv('sampled_data.csv', index=False)
"""
sampled_data = data_df

# Perform K-means clustering
kmeans = KMeans(n_clusters=4)  # Adjust number of clusters as needed
cluster_labels = kmeans.fit_predict(sampled_data)

# Perform MDS for Data
distance_matrix_data = pairwise_distances(sampled_data, metric='euclidean')
mds_data = MDS(n_components=2, dissimilarity='precomputed').fit_transform(distance_matrix_data)

# Perform MDS for Features
correlation_matrix = np.corrcoef(sampled_data.T)
dissimilarity_matrix_features = 1 - np.abs(correlation_matrix)
mds_features = MDS(n_components=2, dissimilarity='precomputed').fit_transform(dissimilarity_matrix_features)

# Prepare results
results = {
    'data_mds': mds_data.tolist(),
    'features_mds': mds_features.tolist(),
    'cluster_labels': cluster_labels.tolist(),
    'correlation_matrix': correlation_matrix.tolist()
}

@app.route('/mds_result')
def mds_results():
    try:
        # Perform K-means clustering
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)})
# for Scatter Plot

from flask import Flask, jsonify, send_file


@app.route('/num_data.csv', methods=['GET'])
def get_csv():
    return send_file('num_data.csv', as_attachment=True)


# Load data
data = pd.read_csv('data_chord.csv')
categorical = ['Marital status', 'Application mode', 'Course', 'Daytime/evening attendance', "Mother's occupation", "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor', 'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Target']
numerical = ['Application order', 'Age at enrollment', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)', 'Unemployment rate', 'Inflation rate', 'GDP']
categorical = [ 'Marital status', 'Course', 'Displaced',
       'Debtor', 'Gender',
        'Attendance', 'Special needs',
       'Fees Paid', 'Scholarship', 'Target']
desired_columns = numerical + categorical
# Filter DataFrame to keep only the desired columns
columns_to_keep = [col for col in desired_columns if col in data.columns]
filtered_df = data[columns_to_keep]

df = filtered_df
cat_df = df[categorical]

@app.route('/chord-data', methods=['GET'])
def get_chord_data():
    try:
        # Drop the 'Target' column from the categorical DataFrame
        df_without_target = cat_df.drop(columns=['Target'])

        # Remove rows with NaN values
        df_cleaned = df_without_target.dropna()
        df_transposed = df_cleaned.T

        # Get the values, names, and colors from the cleaned DataFrame
        values = df_transposed.values.tolist()
        names = df_cleaned.columns.tolist()
        colors = ['#c4c4c4', '#69b40f', '#ec1d25', '#c8125c', '#008fc8', '#10218b', '#134b24', '#737373', '#008fc8', '#10218b', '#134b24', '#737373']

        # Construct the data dictionary
        data = {
            'values': values,
            'names': names,
            'colors': colors
        }

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
