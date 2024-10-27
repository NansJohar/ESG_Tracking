import streamlit as st
import pandas as pd

# Initialize session state for data storage
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Year', 'Month', 'Petrol (L)', 'Diesel (L)', 'Gas (L)', 
                                                  'Electricity (kWh)', 'Waste (kg)', 'Transportation (km)', 
                                                  'Scope 1 Emissions', 'Scope 2 Emissions', 'Scope 3 Emissions'])

# Define emission factors (example values)
EMISSION_FACTORS = {
    'Petrol': 2.31,  # kg CO2 per liter of petrol
    'Diesel': 2.68,  # kg CO2 per liter of diesel
    'Gas': 2.75,     # kg CO2 per liter of gas
    'Electricity': 0.5,  # kg CO2 per kWh (this is an example; it varies by region)
    'Waste': 0.5,    # kg CO2 per kg of waste
    'Transportation': 0.2 # kg CO2 per km (this is an example)
}

# Function to calculate total emissions
def calculate_totals(data):
    data['Scope 1 Emissions'] = (data['Petrol (L)'] * EMISSION_FACTORS['Petrol'] +
                                  data['Diesel (L)'] * EMISSION_FACTORS['Diesel'] +
                                  data['Gas (L)'] * EMISSION_FACTORS['Gas'])
    data['Scope 2 Emissions'] = data['Electricity (kWh)'] * EMISSION_FACTORS['Electricity']
    data['Scope 3 Emissions'] = (data['Waste (kg)'] * EMISSION_FACTORS['Waste'] +
                                  data['Transportation (km)'] * EMISSION_FACTORS['Transportation'])
    
    total_scope1 = data['Scope 1 Emissions'].sum()
    total_scope2 = data['Scope 2 Emissions'].sum()
    total_scope3 = data['Scope 3 Emissions'].sum()
    return total_scope1, total_scope2, total_scope3

# Title of the app
st.title("ESG Tracking App")

# User input for year and month
year = st.selectbox("Select Year", range(2020, 2031))
month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", 
                                       "July", "August", "September", "October", "November", "December"])

# User inputs for emissions
petrol = st.number_input("Enter Petrol emissions (L)", min_value=0.0)
diesel = st.number_input("Enter Diesel emissions (L)", min_value=0.0)
gas = st.number_input("Enter Gas emissions (L)", min_value=0.0)
electricity = st.number_input("Enter Electricity emissions (kWh)", min_value=0.0)
waste = st.number_input("Enter Waste emissions (kg)", min_value=0.0)
transportation = st.number_input("Enter Transportation emissions (km)", min_value=0.0)

# Button to submit data
if st.button("Submit Data"):
    new_entry = pd.DataFrame([[year, month, petrol, diesel, gas, electricity, waste, transportation]], 
                              columns=['Year', 'Month', 'Petrol (L)', 'Diesel (L)', 'Gas (L)', 
                                       'Electricity (kWh)', 'Waste (kg)', 'Transportation (km)'])
    st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
    st.success("Data submitted successfully!")

# Displaying current entries
st.subheader("Current Emissions Data")
if not st.session_state.data.empty:
    # Calculate and display total emissions
    total_scope1, total_scope2, total_scope3 = calculate_totals(st.session_state.data)

    # Display data in a table
    st.dataframe(st.session_state.data)

    # Display total emissions
    st.write(f"**Total Scope 1 Emissions:** {total_scope1:.2f} kg CO2")
    st.write(f"**Total Scope 2 Emissions:** {total_scope2:.2f} kg CO2")
    st.write(f"**Total Scope 3 Emissions:** {total_scope3:.2f} kg CO2")

    # Allow users to edit entries
    for index, row in st.session_state.data.iterrows():
        if st.button(f"Edit Entry for {row['Month']} {row['Year']}", key=f"edit_{index}"):
            petrol_input = st.number_input("Edit Petrol emissions (L)", value=row['Petrol (L)'], min_value=0.0, key=f"petrol_{index}")
            diesel_input = st.number_input("Edit Diesel emissions (L)", value=row['Diesel (L)'], min_value=0.0, key=f"diesel_{index}")
            gas_input = st.number_input("Edit Gas emissions (L)", value=row['Gas (L)'], min_value=0.0, key=f"gas_{index}")
            electricity_input = st.number_input("Edit Electricity emissions (kWh)", value=row['Electricity (kWh)'], min_value=0.0, key=f"electricity_{index}")
            waste_input = st.number_input("Edit Waste emissions (kg)", value=row['Waste (kg)'], min_value=0.0, key=f"waste_{index}")
            transportation_input = st.number_input("Edit Transportation emissions (km)", value=row['Transportation (km)'], min_value=0.0, key=f"transportation_{index}")
            
            if st.button("Update", key=f"update_{index}"):
                st.session_state.data.at[index, 'Petrol (L)'] = petrol_input
                st.session_state.data.at[index, 'Diesel (L)'] = diesel_input
                st.session_state.data.at[index, 'Gas (L)'] = gas_input
                st.session_state.data.at[index, 'Electricity (kWh)'] = electricity_input
                st.session_state.data.at[index, 'Waste (kg)'] = waste_input
                st.session_state.data.at[index, 'Transportation (km)'] = transportation_input
                st.success("Entry updated successfully!")
else:
    st.write("No data available.")
