import pandas as pd
import plotly.express as px

# Test the year formatting fix
df = pd.read_csv("clean_global_cybersecurity_threats.csv")

# Create the same financial trend data as in the dashboard
financial_trend = df.groupby('Year')['Financial Loss (in Million $)'].mean().reset_index()
financial_trend['Year'] = financial_trend['Year'].astype(int)

print("Financial trend data:")
print(financial_trend)
print(f"\nYear column type: {financial_trend['Year'].dtype}")

# Create Plotly line chart with proper integer year formatting
fig_financial = px.line(
    financial_trend,
    x='Year',
    y='Financial Loss (in Million $)',
    title='Average Financial Loss by Year',
    markers=True
)
fig_financial.update_xaxes(
    dtick=1,  # Show every year
    tickmode='linear',
    tickformat='d'  # Display as integers (no decimals)
)
fig_financial.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Financial Loss (Million $)",
    showlegend=False
)

print("\n✅ Chart created successfully with integer year formatting!")
print("Years will now display as: 2015, 2016, 2017, ... instead of 2015.0, 2016.0, etc.")
