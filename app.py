import streamlit as st
import pandas as pd

# Initialize session state for data storage
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Year', 'Month', 'Petrol', 'Diesel', 'Gas', 'Electricity', 'Waste', 'Transportation'])

# Function to calculate total emissions
def calculate_totals(data):
    total_scope1 = data[['Petrol', 'Diesel', 'Gas']].sum().sum()
    total_scope2 = data['Electricity'].sum()
    total_scope3 = data[['Waste', 'Transportation']].sum().sum()
    return total_scope1, total_scope2, total_scope3

# Title of the app
st.title("ESG Tracking App")

# User input for year and month
year = st.selectbox("Select Year", range(2020, 2031))
month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", 
                                       "July", "August", "September", "October", "November", "December"])

# User inputs for emissions
petrol = st.number_input("Enter Petrol emissions", min_value=0.0)
diesel = st.number_input("Enter Diesel emissions", min_value=0.0)
gas = st.number_input("Enter Gas emissions", min_value=0.0)
electricity = st.number_input("Enter Electricity emissions", min_value=0.0)
waste = st.number_input("Enter Waste emissions", min_value=0.0)
transportation = st.number_input("Enter Transportation emissions", min_value=0.0)

# Button to submit data
if st.button("Submit Data"):
    new_entry = pd.DataFrame([[year, month, petrol, diesel, gas, electricity, waste, transportation]], 
                              columns=['Year', 'Month', 'Petrol', 'Diesel', 'Gas', 'Electricity', 'Waste', 'Transportation'])
    st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
    st.success("Data submitted successfully!")

# Displaying current entries
st.subheader("Current Emissions Data")
if not st.session_state.data.empty:
    # Display data in a table
    st.dataframe(st.session_state.data)

    # Calculate and display total emissions
    total_scope1, total_scope2, total_scope3 = calculate_totals(st.session_state.data)
    st.write(f"**Total Scope 1 Emissions:** {total_scope1:.2f}")
    st.write(f"**Total Scope 2 Emissions:** {total_scope2:.2f}")
    st.write(f"**Total Scope 3 Emissions:** {total_scope3:.2f}")

    # Allow users to edit entries
    for index, row in st.session_state.data.iterrows():
        if st.button(f"Edit Entry for {row['Month']} {row['Year']}", key=f"edit_{index}"):
            petrol_input = st.number_input("Edit Petrol emissions", value=row['Petrol'], min_value=0.0, key=f"petrol_{index}")
            diesel_input = st.number_input("Edit Diesel emissions", value=row['Diesel'], min_value=0.0, key=f"diesel_{index}")
            gas_input = st.number_input("Edit Gas emissions", value=row['Gas'], min_value=0.0, key=f"gas_{index}")
            electricity_input = st.number_input("Edit Electricity emissions", value=row['Electricity'], min_value=0.0, key=f"electricity_{index}")
            waste_input = st.number_input("Edit Waste emissions", value=row['Waste'], min_value=0.0, key=f"waste_{index}")
            transportation_input = st.number_input("Edit Transportation emissions", value=row['Transportation'], min_value=0.0, key=f"transportation_{index}")
            
            if st.button("Update", key=f"update_{index}"):
                st.session_state.data.at[index, 'Petrol'] = petrol_input
                st.session_state.data.at[index, 'Diesel'] = diesel_input
                st.session_state.data.at[index, 'Gas'] = gas_input
                st.session_state.data.at[index, 'Electricity'] = electricity_input
                st.session_state.data.at[index, 'Waste'] = waste_input
                st.session_state.data.at[index, 'Transportation'] = transportation_input
                st.success("Entry updated successfully!")
else:
    st.write("No data available.")
