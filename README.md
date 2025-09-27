# 🧭 UAV Compass Variance Simulator

**Understand how compass variance impacts UAV navigation with this live, interactive Streamlit app.** Simulate interference, view drift in real-time, and export variance logs — ideal for drone engineers, UAV students, and field testers.

---
## ✈️ What Is Compass Variance?

Compass variance is the difference between:
- **True Heading**: Based on geographic north
- **Magnetic Heading**: What the UAV's compass thinks is north

> Even small errors can lead to **major waypoint drift** during long-range missions.

---

## ⚙️ Features

✅ Live compass UI (True North vs Magnetic)  
✅ Real-time compass variance simulation  
✅ Toggle simulated interference (EMI, metal, miscalibration)  
✅ Drift estimation: meters off-course per 1 km  
✅ Recalibration button (zero variance)  
✅ CSV export of variance logs  
✅ Line chart of variance over time  

---

## 🚀 Quickstart

1. Clone or download the repo  
2. Install dependencies:
   ```bash
   pip install streamlit matplotlib pandas
