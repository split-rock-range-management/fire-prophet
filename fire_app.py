import streamlit as st

# --- Constants ---
DEFAULT_HEAT_CONTENT = 18600  # kJ/kg, typical for forest fuels

# --- Fireline Intensity Calculation ---
def calculate_fireline_intensity(H, w, r):
    return round((H * w * r) / 1000, 2)  # kW/m

# --- Flame Length Estimation (simplified) ---
def estimate_flame_length(intensity):
    # Empirical formula: L = 0.45 * (I)^0.46
    return round(0.45 * (intensity ** 0.46), 2)

# --- Plant Survival Estimation (mock logic) ---
def estimate_survival(flame_length, vegetation_type):
    thresholds = {
        "Oak Woodland": 3.0,
        "Grassland": 1.5,
        "Chaparral": 2.5,
        "Riparian": 2.0
    }
    threshold = thresholds.get(vegetation_type, 2.5)
    survival = max(0, 100 - ((flame_length - threshold) * 25))
    return round(min(survival, 100), 1)

# --- Streamlit UI ---
st.title("🔥 Fire Intensity & Plant Survival Estimator")

st.sidebar.header("🌡️ Input Parameters")
temperature = st.sidebar.slider("Temperature (°F)", 60, 120, 95)
humidity = st.sidebar.slider("Humidity (%)", 5, 80, 20)
wind_speed = st.sidebar.slider("Wind Speed (mph)", 0, 40, 15)
fuel_load = st.sidebar.slider("Fuel Load (kg/m²)", 0.5, 5.0, 1.5)
slope = st.sidebar.slider("Slope (°)", 0, 45, 20)
vegetation = st.sidebar.selectbox("Vegetation Type", ["Oak Woodland", "Grassland", "Chaparral", "Riparian"])

# --- Derived Rate of Spread (simplified proxy) ---
rate_of_spread = round((wind_speed / 100) + (slope / 100), 3)  # m/s

# --- Calculations ---
intensity = calculate_fireline_intensity(DEFAULT_HEAT_CONTENT, fuel_load, rate_of_spread)
flame_length = estimate_flame_length(intensity)
survival = estimate_survival(flame_length, vegetation)

# --- Output ---
st.subheader("📊 Results")
st.metric("Fireline Intensity", f"{intensity} kW/m")
st.metric("Estimated Flame Length", f"{flame_length} m")
st.metric("Estimated Plant Survival", f"{survival}%")

st.caption("Note: Survival estimates are illustrative and based on simplified thresholds.")

# --- Footer ---
st.markdown("---")
st.markdown("Created for community advocacy and ecological planning.")