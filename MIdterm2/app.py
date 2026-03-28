import streamlit as st
from vehicles import GroundVehicle, Drone, UGV

st.set_page_config(page_title="Smart Fleet Management", layout="wide")
st.title("🚀 Smart Fleet Management System")

# --- Global Command Center ---
st.subheader("🌐 Global Command Center")
g_col1, g_col2, g_col3 = st.columns(3)

with g_col1:
    if st.button("⚡ Charge All Vehicles", use_container_width=True):
        for v in st.session_state.fleet.values():
            v.charge()
        st.success("All vehicles are charging!")
        st.rerun()

with g_col2:
    if st.button("🛑 Emergency Stop All", use_container_width=True):
        for v in st.session_state.fleet.values():
            v.status = "EMERGENCY STOP"
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
    v_type = st.selectbox("Type", ["Ground Vehicle", "Drone", "UGV"])

    if st.button("Add Vehicle"):
        if v_id and v_id not in st.session_state.fleet:
            if v_type == "Ground Vehicle":
                st.session_state.fleet[v_id] = GroundVehicle(v_id, 20)
            elif v_type == "Drone":
                st.session_state.fleet[v_id] = Drone(v_id, 60)
            else:
                st.session_state.fleet[v_id] = UGV(v_id, 10)
            st.success(f"Added {v_id}")
        else:
            st.error("Invalid or Duplicate ID")

# --- Main Dashboard ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Live Fleet Status")
    if not st.session_state.fleet:
        st.info("No vehicles in fleet. Add one from the sidebar!")
    else:
        for v_id, v in st.session_state.fleet.items():
            # Color battery status
            b_color = "green" if v.battery > 50 else "orange" if v.battery > 20 else "red"
            st.markdown(f"**{v_id}** ({type(v).__name__})")
            st.progress(max(0, min(int(v.battery), 100)))
            st.caption(f"Battery: :{b_color}[{v.battery:.1f}%] | Status: {v.status}")

with col2:
    st.header("🕹️ Control Panel")
    if st.session_state.fleet:
        target_id = st.selectbox("Select Vehicle", list(st.session_state.fleet.keys()))
        target_v = st.session_state.fleet[target_id]

        if st.button("Move / Action"):
            if isinstance(target_v, UGV):
                target_v.deliver(weight=5)
            else:
                target_v.move()
            st.rerun()

        if st.button("Recharge"):
            target_v.charge()
            st.rerun()