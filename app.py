import streamlit as st
import pandas as pd

# Initialize session state for data storage
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Year', 'Month', 'Scope 1', 'Scope 2', 'Scope 3'])

# Function to calculate total emissions
def calculate_totals(data):
    total_scope1 = data['Scope 1'].sum()
    total_scope2 = data['Scope 2'].sum()
    total_scope3 = data['Scope 3'].sum()
    return total_scope1, total_scope2, total_scope3

# Title of the app
st.title("ESG Tracking App")

# User input for year and month
year = st.selectbox("Select Year", range(2020, 2031))
month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", 
                                       "July", "August", "September", "October", "November", "December"])

# User inputs for emissions
scope1 = st.number_input("Enter Scope 1 emissions (Diesel, Petrol, Gas)", min_value=0.0)
scope2 = st.number_input("Enter Scope 2 emissions (Purchased Electricity)", min_value=0.0)
scope3 = st.number_input("Enter Scope 3 emissions (Waste, Transportation)", min_value=0.0)

# Button to submit data
if st.button("Submit Data"):
    new_entry = pd.DataFrame([[year, month, scope1, scope2, scope3]], columns=['Year', 'Month', 'Scope 1', 'Scope 2', 'Scope 3'])
    st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
    st.success("Data submitted successfully!")

# Displaying current entries
st.subheader("Current Emissions Data")
if not st.session_state.data.empty:
    # Display data in a table
    st.dataframe(st.session_state.data)

    # Calculate and display total emissions
    total_scope1, total_scope2, total_scope3 = calculate_totals(st.session_state.data)
    st.write(f"Total Scope 1 Emissions: {total_scope1}")
    st.write(f"Total Scope 2 Emissions: {total_scope2}")
    st.write(f"Total Scope 3 Emissions: {total_scope3}")

    # Allow users to edit entries
    for index, row in st.session_state.data.iterrows():
        if st.button(f"Edit Entry for {row['Month']} {row['Year']}", key=f"edit_{index}"):
            new_scope1 = st.number_input("Edit Scope 1 emissions", value=row['Scope 1'], min_value=0.0, key=f"scope1_{index}")
            new_scope2 = st.number_input("Edit Scope 2 emissions", value=row['Scope 2'], min_value=0.0, key=f"scope2_{index}")
            new_scope3 = st.number_input("Edit Scope 3 emissions", value=row['Scope 3'], min_value=0.0, key=f"scope3_{index}")
            
            if st.button("Update", key=f"update_{index}"):
                st.session_state.data.at[index, 'Scope 1'] = new_scope1
                st.session_state.data.at[index, 'Scope 2'] = new_scope2
                st.session_state.data.at[index, 'Scope 3'] = new_scope3
                st.success("Entry updated successfully!")
else:
    st.write("No data available.")
