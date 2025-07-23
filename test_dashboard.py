# Simple test version to isolate the issue
import pandas as pd
import streamlit as st
import plotly.express as px

# Test 1: Basic setup
st.title("🛡️ Test Dashboard")

try:
    # Test 2: Data loading
    df = pd.read_csv("data/clean_global_cybersecurity_threats.csv")
    st.success(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Test 3: Data processing
    df = df.ffill()
    
    # Convert numeric columns to proper types
    numeric_columns = ['Year', 'Financial Loss (in Million $)', 'Number of Affected Users', 'Incident Resolution Time (in Hours)']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill any remaining NaN values
    df = df.fillna(0)
    st.success("✅ Data processing completed")
    
    # Test 4: Show basic data info
    st.write("**Data Info:**")
    st.write(f"Shape: {df.shape}")
    st.write(f"Columns: {list(df.columns)}")
    
    # Test 5: Simple chart
    st.write("**Simple Chart Test:**")
    yearly_data = df.groupby('Year').size().reset_index(name='Count')
    fig = px.bar(yearly_data, x='Year', y='Count', title='Incidents by Year')
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("✅ All tests passed!")
    
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.write("**Error details:**")
    import traceback
    st.code(traceback.format_exc())
