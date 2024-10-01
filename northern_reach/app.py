from flask import Flask, render_template
import pandas as pd  # Assuming you're using pandas for your DataFrame
import json
from datetime import datetime

app = Flask(__name__)

# Custom JSON encoder to handle Timestamp objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)

# Load your data
# Replace this with your actual data loading method
df = pd.read_csv('/app/uk_interactions.csv')

@app.route("/")
def map_view():
    # Prepare marker data
    marker_data = []
    for index, row in df.iterrows():
        popup_text = f"""
        <b>Date:</b> {row['Date']}<br>
        <b>Postcode:</b> {row['Postcode']}<br>
        <b>Email:</b> {row['Email']}<br>
        <b>First Name:</b> {row['First Name']}<br>
        <b>Last Name:</b> {row['Last Name']}<br>
        <b>Interaction:</b> {row['Interaction']}<br>
        <b>Sector:</b> {row['Sector']}
        """
        marker_data.append({
            'lat': row['Latitude'],
            'lon': row['Longitude'],
            'popup': popup_text,
            'date': row['Date'],
            'sector': row['Sector'],
            'interaction': row['Interaction']  # Add this line
        })

    # Convert DataFrame to list of dictionaries, sorted by date in descending order
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure 'Date' is in datetime format
    df_sorted = df.sort_values('Date', ascending=False)
    interactions = df_sorted.to_dict('records')

    # Use the custom JSON encoder to serialize the data
    marker_data_json = json.dumps(marker_data, cls=CustomJSONEncoder)

    # Render the map in the HTML template
    return render_template('app.html', interactions=interactions, marker_data=marker_data_json)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
