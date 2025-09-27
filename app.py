import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

# ─────────────────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────────────────
st.set_page_config(page_title="🧭 UAV Compass Variance Simulator", layout="wide")
st.title("🧭 UAV Compass Variance Simulator")
st.caption("Live heading visualization, AI response logic, and drift prediction.")

# ─────────────────────────────────────────────────────
# State Initialization
# ─────────────────────────────────────────────────────
if "variance_log" not in st.session_state:
    st.session_state.variance_log = []

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ─────────────────────────────────────────────────────
# Inputs & Variance Modeling
# ─────────────────────────────────────────────────────
true_heading = st.slider("🧭 True Heading (°)", 0, 359, 90)

error_source = st.radio("📡 Simulated Compass Error Source", [
    "None", "EMI", "Nearby Metal", "Poor Calibration"
])

def get_variance(source):
    if source == "None":
        return np.random.normal(0, 1)
    elif source == "EMI":
        return np.random.normal(12, 4)
    elif source == "Nearby Metal":
        return np.random.normal(8, 3)
    elif source == "Poor Calibration":
        return np.random.normal(15, 6)

variance = get_variance(error_source)
mag_heading = (true_heading + variance) % 360
st.metric("📍 Compass Variance", f"{variance:.2f}°")

# ─────────────────────────────────────────────────────
# Drift Estimation + AI Autopilot Response
# ─────────────────────────────────────────────────────
drift_per_km = np.tan(np.radians(abs(variance))) * 1000
st.markdown(f"### 🔀 Predicted Drift: **{drift_per_km:.1f} m per 1 km**")

# AI response
if drift_per_km < 50:
    st.success("🧠 Autopilot: Heading nominal ✅")
elif drift_per_km < 150:
    st.warning("🧠 Autopilot: Drift warning ⚠️ — advise recalibration")
else:
    st.error("🧠 Autopilot: Critical drift 🚨 — initiating Return to Base (RTB)")

# ─────────────────────────────────────────────────────
# Compass UI
# ─────────────────────────────────────────────────────
def draw_compass(true_hdg, mag_hdg):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.add_patch(plt.Circle((0, 0), 1, fill=False, linewidth=2))
    ax.text(0, 1.08, 'N', ha='center', fontsize=12, weight='bold')
    ax.text(0, -1.15, 'S', ha='center', fontsize=12)
    ax.text(1.15, 0, 'E', va='center', fontsize=12)
    ax.text(-1.18, 0, 'W', va='center', fontsize=12)

    angle_true = np.radians(90 - true_hdg)
    angle_mag = np.radians(90 - mag_hdg)

    # Arrows
    ax.arrow(0, 0, 0.8 * np.cos(angle_true), 0.8 * np.sin(angle_true),
             head_width=0.05, head_length=0.1, fc='blue', ec='blue')
    ax.arrow(0, 0, 0.8 * np.cos(angle_mag), 0.8 * np.sin(angle_mag),
             head_width=0.05, head_length=0.1, fc='red', ec='red')

    # Custom legend
    h1, = ax.plot([], [], color='blue', linewidth=5)
    h2, = ax.plot([], [], color='red', linewidth=5)
    ax.legend([h1, h2], ["True (Blue)", "Magnetic (Red)"], loc="lower center")
    st.pyplot(fig)

draw_compass(true_heading, mag_heading)

# ─────────────────────────────────────────────────────
# Drift Map Over Distance
# ─────────────────────────────────────────────────────
def draw_drift_map(variance_deg, max_range_km=5):
    drift_m_per_km = np.tan(np.radians(abs(variance_deg))) * 1000
    distances = np.arange(0, max_range_km + 1, 1)
    ideal_path = np.zeros_like(distances)
    drift_path = distances * drift_m_per_km / 1000  # drift in meters per km

    fig, ax = plt.subplots()
    ax.plot(distances, ideal_path, linestyle='--', label="True Path (Ideal)", color='gray')
    ax.plot(distances, drift_path, label="Drifted Path (Magnetic)", color='red')
    ax.set_title("📍 Simulated UAV Path Deviation")
    ax.set_xlabel("Distance Flown (km)")
    ax.set_ylabel("Lateral Drift (m)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

draw_drift_map(variance)

# ─────────────────────────────────────────────────────
# Recalibrate Button
# ─────────────────────────────────────────────────────
if st.button("🧭 Recalibrate Compass"):
    st.success("Compass reset to 0° variance.")
    st.session_state.variance_log = []

# ─────────────────────────────────────────────────────
# Variance Logging
# ─────────────────────────────────────────────────────
elapsed = time.time() - st.session_state.start_time
st.session_state.variance_log.append({
    "Time (s)": round(elapsed),
    "Variance (°)": round(variance, 2),
    "Source": error_source
})

log_df = pd.DataFrame(st.session_state.variance_log)

# ─────────────────────────────────────────────────────
# Log Viewer & Export
# ─────────────────────────────────────────────────────
with st.expander("📈 View Variance Over Time"):
    st.line_chart(log_df[["Variance (°)"]])

with st.expander("⬇️ Export Logs"):
    csv = log_df.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name="compass_variance_log.csv")

# ─────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("✅ **Low Compass Variance = Reliable UAV Performance**")
