import streamlit as st

# Define emission factors
EMISSION_FACTORS_SCOPE1 = {'diesel': 2.68, 'petrol': 2.31, 'gas': 2.05}
EMISSION_FACTORS_SCOPE2 = {'electricity': 0.92}
EMISSION_FACTORS_SCOPE3 = {'waste': 0.10, 'transportation': 0.50}

# Target emissions
target_emissions = {'scope1': 800, 'scope2': 900, 'scope3': 300}

# Streamlit UI
st.title("ESG Tracking Platform")
st.write("Enter monthly data for Scope 1, 2, and 3 components:")

# Input fields for monthly data
diesel = st.number_input("Diesel (liters)", min_value=0.0, step=1.0)
petrol = st.number_input("Petrol (liters)", min_value=0.0, step=1.0)
gas = st.number_input("Gas (cubic meters)", min_value=0.0, step=1.0)
electricity = st.number_input("Electricity (kWh)", min_value=0.0, step=1.0)
waste = st.number_input("Waste (tons)", min_value=0.0, step=1.0)
transportation = st.number_input("Transportation (km)", min_value=0.0, step=1.0)

# Calculate emissions
if st.button("Calculate Emissions"):
    scope1_emissions = diesel * EMISSION_FACTORS_SCOPE1['diesel'] + petrol * EMISSION_FACTORS_SCOPE1['petrol'] + gas * EMISSION_FACTORS_SCOPE1['gas']
    scope2_emissions = electricity * EMISSION_FACTORS_SCOPE2['electricity']
    scope3_emissions = waste * EMISSION_FACTORS_SCOPE3['waste'] + transportation * EMISSION_FACTORS_SCOPE3['transportation']

    # Calculate gaps
    scope1_lacking = target_emissions['scope1'] - scope1_emissions
    scope2_lacking = target_emissions['scope2'] - scope2_emissions
    scope3_lacking = target_emissions['scope3'] - scope3_emissions

    # Display results
    st.write(f"**Scope 1 Emissions:** {scope1_emissions:.2f} kg CO2, lacking by {scope1_lacking:.2f}")
    st.write(f"**Scope 2 Emissions:** {scope2_emissions:.2f} kg CO2, lacking by {scope2_lacking:.2f}")
    st.write(f"**Scope 3 Emissions:** {scope3_emissions:.2f} kg CO2, lacking by {scope3_lacking:.2f}")
