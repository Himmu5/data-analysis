import streamlit as st
import os
import importlib.util

DASHBOARD_DIR = 'dashboard'

def get_dashboard_files():
    files = [f for f in os.listdir(DASHBOARD_DIR) if f.endswith('.py')]
    return files

def load_dashboard_module(file_name):
    module_name = file_name[:-3]
    file_path = os.path.join(DASHBOARD_DIR, file_name)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

st.title('Dashboard Viewer')

dashboard_files = get_dashboard_files()
st.sidebar.write(f"Total dashboards: {len(dashboard_files)}")
selected_dashboard = st.sidebar.selectbox('Select a dashboard', dashboard_files)

if selected_dashboard:
    st.write(f"### Showing: {selected_dashboard}")
    try:
        module = load_dashboard_module(selected_dashboard)
        # Try to call main() if it exists, else show a message
        if hasattr(module, 'main'):
            module.main()
        else:
            st.warning(f"No 'main()' function found in {selected_dashboard}.")
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
