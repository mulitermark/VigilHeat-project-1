import streamlit as st
import csv
import plotly.graph_objects as go

from io import StringIO

def read_data_from_csv(file):
    data = []
    reader = csv.reader(StringIO(file.read().decode('utf-8')))
    next(reader)  # Skip the header row

    for row in reader:
        hour = int(row[0])
        num_people = int(row[1])
        data.append((hour, num_people))

    return data



# Streamlit app
def main():
    st.title("Shop Crowd Visualization")
    st.write("Upload a CSV file to visualize the number of people inside the shop.")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")

    if uploaded_file is not None:
        # Read data from CSV file
        data = read_data_from_csv(uploaded_file)

        # Extract hour and number of people into separate lists for plotting
        hours = [row[0] for row in data]
        num_people = [row[1] for row in data]

        # Create a line plot using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=num_people, mode='lines', name='Number of People'))

        # Customize the layout
        fig.update_layout(
            title='Number of People Inside the Shop',
            xaxis_title='Hour',
            yaxis_title='Number of People'
        )

        # Display the plot using Streamlit
        st.plotly_chart(fig)

# Run the Streamlit app
if __name__ == "__main__":
    main()
