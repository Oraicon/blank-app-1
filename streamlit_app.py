import streamlit as st
from supabase import create_client
import json
from datetime import datetime

# Initialize Supabase client
supabase_url = "https://trrvgpjegudopsgtarne.supabase.co"
supabase_key = "process.env.SUPABASE_KEY"  # Replace with your actual key
supabase = create_client(supabase_url, supabase_key)

# Configure Streamlit to handle CORS
# Disable streamlit UI elements we don't need
st.set_page_config(initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# API endpoints
def handle_get_users():
    try:
        response = supabase.table('users').select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def handle_create_user(data):
    try:
        response = supabase.table('users').insert(data).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

# Main routing logic
def main():
    # Get query parameters and request method
    params = st.experimental_get_query_params()
    
    # Check if it's an API request
    if 'api' in params:
        endpoint = params['api'][0]
        
        # GET /api/users - Get all users
        if endpoint == 'users' and st.request_method == "GET":
            st.json(handle_get_users())
            
        # POST /api/users - Create new user
        elif endpoint == 'users' and st.request_method == "POST":
            try:
                data = json.loads(st.request_body())
                st.json(handle_create_user(data))
            except json.JSONDecodeError:
                st.json({"error": "Invalid JSON data"})
                
        else:
            st.json({"error": "Invalid endpoint"})
    else:
        st.json({"message": "API is running", "endpoints": ["/api/users"]})

if __name__ == "__main__":
    main()
