import streamlit as st
import random
from vehicles import GroundVehicle, Drone, UGV

if 'fleet' not in st.session_state:
    st.session_state.fleet = {}

st.set_page_config(page_title="Smart Fleet Management", layout="wide")
st.title("🚀 Smart Fleet Management System")

# --- Global Command Center (Three Action Version) ---
st.subheader("🌐 Global Command Center")
g_col1, g_col2, g_col3 = st.columns(3)

with g_col1:
    if st.button("⚡ Charge All Vehicles", use_container_width=True):
        for v in st.session_state.fleet.values():
            v.charge()
        st.success("All vehicles charging!")
        st.rerun()

with g_col2:
    # This now replaces the old "Control Panel" in the middle
    if st.button("🛑 Emergency Stop All", use_container_width=True):
        for v in st.session_state.fleet.values():
            v.status = "EMERGENCY STOP"
            # Optional: you could also set speed to 0 here if you like
        st.error("All operations halted!")
        st.rerun()

with g_col3:
    if st.button("🗑️ Clear Entire Fleet", use_container_width=True):
        st.session_state.fleet = {}
        st.warning("Fleet data wiped.")
        st.rerun()

st.divider()

# Initialize the fleet in session state if it doesn't exist
if 'fleet' not in st.session_state:
    st.session_state.fleet = {}

# --- Sidebar: Add New Vehicles ---
with st.sidebar:
    st.header("➕ Add to Fleet")
    v_id = st.text_input("Vehicle ID (Unique)")
    v_speed = st.number_input("Max Speed (km/h)", min_value=1, max_value=200, value=50)
    v_type = st.selectbox("Type", ["Ground Vehicle", "Drone", "UGV"], key="add_vehicle_type")

    if st.button("Add Vehicle"):
        if v_id and v_id not in st.session_state.fleet:
            # Logic for the "Random Column" attribute
            if v_type == "Ground Vehicle":
                # Randomly assign number of wheels
                extra_attr = random.randint(4, 8)
                st.session_state.fleet[v_id] = GroundVehicle(v_id, v_speed)
                st.session_state.fleet[v_id].extra_label = f"{extra_attr} Wheels"

            elif v_type == "Drone":
                # Randomly assign number of rotors
                extra_attr = random.choice([4, 6, 8])
                st.session_state.fleet[v_id] = Drone(v_id, v_speed)
                st.session_state.fleet[v_id].extra_label = f"{extra_attr} Rotors"

            else:
                # Randomly assign a sensor type for UGV
                extra_attr = random.choice(["Lidar", "Radar", "Ultrasonic"])
                st.session_state.fleet[v_id] = UGV(v_id, v_speed)
                st.session_state.fleet[v_id].extra_label = f"{extra_attr} Sensor"

            st.success(f"Added {v_id} with Speed {v_speed}")
        else:
            st.error("Invalid or Duplicate ID")

# --- Main Dashboard ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Live Fleet Status")
    if not st.session_state.fleet:
        st.info("No vehicles in fleet.")
    else:
        for v_id, v in st.session_state.fleet.items():
            b_color = "green" if v.battery > 50 else "orange" if v.battery > 20 else "red"

            # Display ID, Type, Speed, and the Random Attribute
            st.markdown(f"### 🆔 {v_id}")
            # We use columns here to make it look like a organized table/grid
            stat1, stat2, stat3 = st.columns(3)
            stat1.caption(f"**Type:** {type(v).__name__}")
            stat2.caption(f"**Max Speed:** {v.speed} km/h")
            stat3.caption(f"**Spec:** {v.extra_label}")  # This is our random column

            st.progress(max(0, min(int(v.battery), 100)))
            st.caption(f"Battery: :{b_color}[{v.battery:.1f}%] | Status: {v.status}")
            st.divider()

with col2:
    st.header("🕹️ Individual Control")
    if st.session_state.fleet:
        # Select which vehicle to command
        target_id = st.selectbox("Select Vehicle", list(st.session_state.fleet.keys()), key="individual_ctrl")
        target_v = st.session_state.fleet[target_id]

        # --- UGV SPECIFIC CONTROLS ---
        if isinstance(target_v, UGV):
            st.info(f"Setting up delivery for {target_id}")
            # Add a slider so the user can choose the weight
            cargo_weight = st.slider("Cargo Weight (kg)", 1, 50, 10)

            if st.button("📦 Execute UGV Delivery", use_container_width=True):
                target_v.deliver(cargo_weight)
                st.success(f"Delivery dispatched! Weight: {cargo_weight}kg")
                st.rerun()

        # --- GENERAL CONTROLS (For Drone/Ground) ---
        else:
            if st.button("🚀 Move Vehicle", use_container_width=True):
                target_v.move()
                st.rerun()

        # Common button for everyone
        if st.button("⚡ Recharge Selected", use_container_width=True):
            target_v.charge()
            st.rerun()
    else:
        st.write("Add a vehicle to see controls.")
