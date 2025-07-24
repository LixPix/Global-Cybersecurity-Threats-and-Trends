# **Global Cyber Threats 2015-2024 data ML**

# import libraries and packages
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, mean_absolute_error, accuracy_score, r2_score

# load and preprocess data
df = pd.read_csv("data/clean_global_cybersecurity_threats.csv")

# Clean and ensure proper data types
df = df.ffill()  # Updated pandas syntax for forward fill

# Convert numeric columns to proper types
numeric_columns = ['Year', 'Financial Loss (in Million $)', 'Number of Affected Users', 'Incident Resolution Time (in Hours)']
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill any remaining NaN values
df = df.fillna(0)

label_encoders = {}
for col in df.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df[col + '_encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le

# Debug information in collapsible sections
with st.expander("🔍 Data Structure Information (Click to expand)"):
    st.write("**Available columns:**", df.columns.tolist())
    st.write("**Data types:**")
    st.text(str(df.dtypes))
    st.write("**First few rows of encoded data:**")
    encoded_cols = [col for col in df.columns if '_encoded' in col]
    if encoded_cols:
        st.dataframe(df[encoded_cols].head(), use_container_width=True)

# Streamlit Dashboard
st.title("🛡️ Cyber Threat Insight Portal")

st.markdown("""
# 📘 User Story
This dashboard empowers security analysts, decision-makers, and curious observers with insights from global cybersecurity incidents over the last decade.  
Whether you're a **technical user** seeking to model attack outcomes, or a **non-technical audience** looking to understand threat evolution — this app simplifies complex data into actionable intelligence.

- 🔍 Predict the **type of attack**, **targeted industry**, and **financial losses**
- 📈 Explore attack patterns over time
- 🧠 Decode complex trends into clear visuals

---

## 🎓 Academic Purpose & Scalability Framework

**📚 Educational Context:**  
This dashboard is built for **academic purposes** based on a limited data sample (3,001 incidents) to demonstrate data science methodologies, machine learning applications, and interactive visualization techniques in cybersecurity analytics.

**🔄 Replication & Adaptation Potential:**  
The framework and methodologies demonstrated here can be **replicated and adapted** for:

- **🏢 Business Applications:** Corporate threat intelligence, risk assessment, and security investment planning
- **🏭 Industry-Specific Solutions:** Sector-focused threat analysis (healthcare, banking, telecommunications, etc.)
- **🌍 National/Regional Security:** Government cybersecurity planning and policy development
- **🛡️ Enterprise Security:** Internal incident analysis and predictive security modeling
- **📊 Research Institutions:** Academic studies on cybersecurity trends and threat evolution
- **🚨 Security Operations Centers:** Real-time threat monitoring and response optimization

**⚡ Scalability Features:**  
With larger datasets and real-time data feeds, this framework can support enterprise-grade applications including automated threat detection, dynamic risk scoring, and strategic security planning for organizations of any size.
""")

# Interactive filtering tips
with st.expander("💡 Chart Interaction Tips - Click to Learn How to Use Filters"):
    st.markdown("""
    - **Click legend items** to show/hide specific attack types or industries
    - **Double-click** on a legend item to show only that category  
    - **Hover over bars** for detailed values and percentages
    """)

# Decode for plotting
df['Decoded_Attack'] = df['Attack Type']
df['Decoded_Industry'] = df['Target Industry']

# Main Dashboard Visualizations
st.subheader("🎯 Attack Types Over Time")
st.markdown("**💡 Tip:** Click legend items to show/hide specific attack types. Double-click to isolate one type.")

attack_data = df.groupby(['Year', 'Decoded_Attack']).size().unstack(fill_value=0)
fig_attack = px.bar(
    attack_data.reset_index(),
    x='Year',
    y=attack_data.columns.tolist(),
    title="🔴 Cyber Attack Types Distribution by Year",
    labels={"value": "Number of Incidents", "Year": "Year"},
    color_discrete_sequence=px.colors.qualitative.Set3,
    barmode='group'  # This makes bars horizontal/grouped instead of stacked
)
fig_attack.update_xaxes(dtick=1, tickformat='d')
fig_attack.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Incidents",
    legend_title="Attack Types",
    hovermode='x unified'
)
st.plotly_chart(fig_attack, use_container_width=True)

st.subheader("🏢 Target Industries Over Time")
st.markdown("**💡 Tip:** Use legend filtering to compare vulnerability patterns across different industries.")

industry_data = df.groupby(['Year', 'Decoded_Industry']).size().unstack(fill_value=0)
fig_industry = px.bar(
    industry_data.reset_index(),
    x='Year',
    y=industry_data.columns.tolist(),
    title="🏭 Industry Targeting Patterns by Year",
    labels={"value": "Number of Attacks", "Year": "Year"},
    color_discrete_sequence=px.colors.qualitative.Pastel,
    barmode='group'  # This makes bars horizontal/grouped instead of stacked
)
fig_industry.update_xaxes(dtick=1, tickformat='d')
fig_industry.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Attacks",
    legend_title="Target Industries",
    hovermode='x unified'
)
st.plotly_chart(fig_industry, use_container_width=True)

st.subheader("� Financial Impact Analysis")
st.markdown("**💡 Tip:** Hover over data points for exact financial impact values and trends.")

financial_data = df.groupby('Year')['Financial Loss (in Million $)'].mean().reset_index()
fig_financial = px.line(
    financial_data,
    x='Year',
    y='Financial Loss (in Million $)',
    title='💸 Average Financial Loss per Incident by Year',
    markers=True,
    line_shape='linear'
)
fig_financial.update_xaxes(dtick=1, tickformat='d')
fig_financial.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Financial Loss (Million $)",
    showlegend=False,
    hovermode='x'
)
fig_financial.update_traces(
    mode='lines+markers',
    marker=dict(size=8, color='darkred'),
    line=dict(width=3, color='darkred'),
    hovertemplate='<b>Year:</b> %{x}<br><b>Avg Loss:</b> $%{y:.2f}M<extra></extra>'
)
st.plotly_chart(fig_financial, use_container_width=True)

# Prepare features for ML models
# Only use encoded columns for categorical features
features = pd.concat([
    df[['Country_encoded', 'Attack Source_encoded', 'Security Vulnerability Type_encoded', 'Defense Mechanism Used_encoded']],
    df[['Year', 'Number of Affected Users', 'Incident Resolution Time (in Hours)']]
], axis=1)

# Feature validation in collapsible section
with st.expander("⚙️ Model Features Information (Click to expand)"):
    st.write("**Features data types:**")
    st.text(str(features.dtypes))
    st.write("**Features shape:**", features.shape)
    st.write("**Any non-numeric data:**", 
             features.select_dtypes(include=['object']).columns.tolist())

# Target variables
target_attack = df['Attack Type_encoded']
target_severity = df['Financial Loss (in Million $)']
target_threat = df['Target Industry_encoded']

# Train-test splits
X_train, X_test, y_attack_train, y_attack_test = train_test_split(features, target_attack, test_size=0.2, random_state=42)
_, _, y_sev_train, y_sev_test = train_test_split(features, target_severity, test_size=0.2, random_state=42)
_, _, y_thr_train, y_thr_test = train_test_split(features, target_threat, test_size=0.2, random_state=42)

# Train Models
rf_attack = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_attack_train)
rf_sev = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_sev_train)
rf_thr = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_thr_train)

# Predict and Display Reports
attack_preds = rf_attack.predict(X_test)
sev_preds = rf_sev.predict(X_test)
thr_preds = rf_thr.predict(X_test)

st.subheader("🔍 Model Performance Reports")

# Calculate detailed performance metrics
from sklearn.metrics import precision_recall_fscore_support

# Attack Type Classification Performance
attack_precision, attack_recall, attack_f1, _ = precision_recall_fscore_support(
    y_attack_test, attack_preds, average='weighted'
)
attack_accuracy = accuracy_score(y_attack_test, attack_preds)

# Industry Classification Performance  
industry_precision, industry_recall, industry_f1, _ = precision_recall_fscore_support(
    y_thr_test, thr_preds, average='weighted'
)
industry_accuracy = accuracy_score(y_thr_test, thr_preds)

# Financial Loss Regression Performance
financial_mae = mean_absolute_error(y_sev_test, sev_preds)
financial_r2 = r2_score(y_sev_test, sev_preds)
financial_rmse = np.sqrt(np.mean((y_sev_test - sev_preds) ** 2))

# Create performance summary table
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🎯 Attack Type Prediction")
    attack_metrics = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'Score': [f"{attack_accuracy:.3f}", f"{attack_precision:.3f}", 
                 f"{attack_recall:.3f}", f"{attack_f1:.3f}"],
        'Percentage': [f"{attack_accuracy:.1%}", f"{attack_precision:.1%}", 
                      f"{attack_recall:.1%}", f"{attack_f1:.1%}"]
    })
    st.dataframe(attack_metrics, use_container_width=True, hide_index=True)

with col2:
    st.markdown("#### 🏭 Industry Prediction")
    industry_metrics = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'Score': [f"{industry_accuracy:.3f}", f"{industry_precision:.3f}", 
                 f"{industry_recall:.3f}", f"{industry_f1:.3f}"],
        'Percentage': [f"{industry_accuracy:.1%}", f"{industry_precision:.1%}", 
                      f"{industry_recall:.1%}", f"{industry_f1:.1%}"]
    })
    st.dataframe(industry_metrics, use_container_width=True, hide_index=True)

with col3:
    st.markdown("#### 💸 Financial Loss Prediction")
    financial_metrics = pd.DataFrame({
        'Metric': ['R² Score', 'MAE (Million $)', 'RMSE (Million $)', 'Explained Variance'],
        'Value': [f"{financial_r2:.3f}", f"{financial_mae:.2f}", 
                 f"{financial_rmse:.2f}", f"{financial_r2:.1%}"]
    })
    st.dataframe(financial_metrics, use_container_width=True, hide_index=True)

# Detailed classification reports in expandable sections
with st.expander("📊 Detailed Classification Reports (Click to expand)"):
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Attack Type - Detailed Report**")
        attack_report_df = pd.DataFrame(
            classification_report(
                y_attack_test, attack_preds, 
                target_names=label_encoders['Attack Type'].classes_,
                output_dict=True
            )
        ).transpose()
        # Round numeric columns for better display
        numeric_cols = ['precision', 'recall', 'f1-score']
        for col in numeric_cols:
            if col in attack_report_df.columns:
                attack_report_df[col] = attack_report_df[col].round(3)
        st.dataframe(attack_report_df, use_container_width=True)
    
    with col2:
        st.markdown("**🏭 Target Industry - Detailed Report**")
        industry_report_df = pd.DataFrame(
            classification_report(
                y_thr_test, thr_preds, 
                target_names=label_encoders['Target Industry'].classes_,
                output_dict=True
            )
        ).transpose()
        # Round numeric columns for better display
        for col in numeric_cols:
            if col in industry_report_df.columns:
                industry_report_df[col] = industry_report_df[col].round(3)
        st.dataframe(industry_report_df, use_container_width=True)

# Calculate additional metrics for analysis
# Calculate performance metrics
attack_accuracy = accuracy_score(y_attack_test, attack_preds)
industry_accuracy = accuracy_score(y_thr_test, thr_preds)
financial_r2 = r2_score(y_sev_test, sev_preds)
financial_mae = mean_absolute_error(y_sev_test, sev_preds)

# Feature importance analysis
attack_feature_importance = pd.DataFrame({
    'feature': features.columns,
    'importance': rf_attack.feature_importances_
}).sort_values('importance', ascending=False)

financial_feature_importance = pd.DataFrame({
    'feature': features.columns,
    'importance': rf_sev.feature_importances_
}).sort_values('importance', ascending=False)

industry_feature_importance = pd.DataFrame({
    'feature': features.columns,
    'importance': rf_thr.feature_importances_
}).sort_values('importance', ascending=False)

# Analysis of data trends
yearly_stats = df.groupby('Year').agg({
    'Financial Loss (in Million $)': ['mean', 'median', 'std'],
    'Number of Affected Users': ['mean', 'median'],
    'Incident Resolution Time (in Hours)': 'mean'
}).round(2)

attack_evolution = df.groupby(['Year', 'Attack Type']).size().unstack(fill_value=0)
most_common_attacks_by_year = attack_evolution.idxmax(axis=1)
attack_growth = attack_evolution.pct_change().fillna(0)

# Industry targeting analysis
industry_targeting = df.groupby('Target Industry').agg({
    'Financial Loss (in Million $)': 'mean',
    'Number of Affected Users': 'mean',
    'Incident Resolution Time (in Hours)': 'mean'
}).round(2)

# Create findings text box
st.subheader("📊 Machine Learning Analysis & Key Findings")

# Add scroll disclaimer
st.info("📜 **Navigation Tip:** This is a comprehensive analysis report. Please **scroll down within the text box below** to read the complete findings, trends analysis, strategic recommendations, and model limitations.")

findings_text = f"""
## 🔍 **Model Performance Analysis**

**Attack Type Prediction:**
- Model Accuracy: {attack_accuracy:.2%}
- Most Important Features: {', '.join(attack_feature_importance.head(3)['feature'].tolist())}

**Financial Loss Prediction:**
- R² Score: {financial_r2:.3f} (explains {financial_r2:.1%} of variance)
- Mean Absolute Error: ${financial_mae:.2f} Million
- Most Important Features: {', '.join(financial_feature_importance.head(3)['feature'].tolist())}

**Target Industry Prediction:**
- Model Accuracy: {industry_accuracy:.2%}
- Most Important Features: {', '.join(industry_feature_importance.head(3)['feature'].tolist())}

## 📈 **Cybersecurity Trends (2015-2024)**

**Financial Impact Evolution:**
- Average Financial Loss: ${yearly_stats['Financial Loss (in Million $)']['mean'].mean():.2f} Million per incident
- Highest Loss Year: {yearly_stats['Financial Loss (in Million $)']['mean'].idxmax()} (${yearly_stats['Financial Loss (in Million $)']['mean'].max():.2f}M avg)
- Most Volatile Year: {yearly_stats['Financial Loss (in Million $)']['std'].idxmax()} (σ=${yearly_stats['Financial Loss (in Million $)']['std'].max():.2f}M)

**Attack Pattern Insights:**
- Most Targeted Industry: {industry_targeting['Financial Loss (in Million $)'].idxmax()} (${industry_targeting['Financial Loss (in Million $)'].max():.2f}M avg loss)
- Fastest Recovery Industry: {industry_targeting['Incident Resolution Time (in Hours)'].idxmin()} ({industry_targeting['Incident Resolution Time (in Hours)'].min():.1f}h avg)
- Slowest Recovery Industry: {industry_targeting['Incident Resolution Time (in Hours)'].idxmax()} ({industry_targeting['Incident Resolution Time (in Hours)'].max():.1f}h avg)

**User Impact Analysis:**
- Average Users Affected: {df['Number of Affected Users'].mean():,.0f} per incident
- Peak Impact Year: {yearly_stats['Number of Affected Users']['mean'].idxmax()} ({yearly_stats['Number of Affected Users']['mean'].max():,.0f} avg users)
- Average Resolution Time: {df['Incident Resolution Time (in Hours)'].mean():.1f} hours

## 🎯 **Strategic Recommendations**

1. **Predictive Modeling:** The models show moderate to good performance, suggesting that cyber attack patterns are partially predictable based on country, timing, and security infrastructure factors.

2. **Industry Focus:** {industry_targeting['Financial Loss (in Million $)'].idxmax()} sector requires enhanced security investments given highest average financial losses.

3. **Temporal Patterns:** Year-over-year analysis reveals evolving attack strategies, with {most_common_attacks_by_year.value_counts().index[0]} being the most persistent threat type.

4. **Response Optimization:** Industries with longer resolution times should adopt faster incident response protocols similar to {industry_targeting['Incident Resolution Time (in Hours)'].idxmin()} sector.

## ⚠️ **Model Limitations**

- Models are based on historical data and may not capture emerging threat vectors
- Feature importance reflects correlation, not necessarily causation
- Prediction accuracy varies by attack complexity and data quality
- External factors (geopolitical events, new technologies) not fully captured
"""

st.text_area("📋 Detailed Analysis Report", findings_text, height=600)

# Interactive Prediction Form
st.subheader("🎛️ Simulate an Attack Scenario")

with st.form("prediction_form"):
    st.markdown("_Enter hypothetical feature values to simulate an attack incident_")
    
    user_input = {}
    
    # Create input fields for each feature
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Categorical Features**")
        
        # Country selection
        country_options = df['Country'].unique()
        selected_country = st.selectbox("Country", country_options)
        user_input['Country_encoded'] = label_encoders['Country'].transform([selected_country])[0]
        
        # Attack Source selection
        attack_source_options = df['Attack Source'].unique()
        selected_attack_source = st.selectbox("Attack Source", attack_source_options)
        user_input['Attack Source_encoded'] = label_encoders['Attack Source'].transform([selected_attack_source])[0]
        
        # Security Vulnerability Type selection
        vuln_options = df['Security Vulnerability Type'].unique()
        selected_vuln = st.selectbox("Security Vulnerability Type", vuln_options)
        user_input['Security Vulnerability Type_encoded'] = label_encoders['Security Vulnerability Type'].transform([selected_vuln])[0]
        
        # Defense Mechanism selection
        defense_options = df['Defense Mechanism Used'].unique()
        selected_defense = st.selectbox("Defense Mechanism Used", defense_options)
        user_input['Defense Mechanism Used_encoded'] = label_encoders['Defense Mechanism Used'].transform([selected_defense])[0]
    
    with col2:
        st.markdown("**Numerical Features**")
        user_input['Year'] = st.slider(
            "Year", 
            int(df['Year'].min()), 
            int(df['Year'].max()), 
            int(df['Year'].mean())
        )
        user_input['Number of Affected Users'] = st.number_input(
            "Number of Affected Users", 
            value=int(df['Number of Affected Users'].mean()),
            min_value=0,
            max_value=int(df['Number of Affected Users'].max())
        )
        user_input['Incident Resolution Time (in Hours)'] = st.slider(
            "Incident Resolution Time (Hours)", 
            float(df['Incident Resolution Time (in Hours)'].min()), 
            float(df['Incident Resolution Time (in Hours)'].max()), 
            float(df['Incident Resolution Time (in Hours)'].mean())
        )

    submitted = st.form_submit_button("🔮 Predict Outcome")
    
    # Store form values for display outside form
    if submitted:
        st.session_state.form_data = {
            'country': selected_country,
            'attack_source': selected_attack_source,
            'vuln_type': selected_vuln,
            'defense': selected_defense,
            'user_input': user_input
        }
        st.session_state.submitted = True

# Check if form was submitted
if hasattr(st.session_state, 'submitted') and st.session_state.submitted:
    user_input = st.session_state.form_data['user_input']
    
    # Create input dataframe with correct column order
    input_df = pd.DataFrame([user_input])
    input_df = input_df[features.columns]  # Ensure correct column order
    
    # Make predictions
    attack_pred = rf_attack.predict(input_df)[0]
    industry_pred = rf_thr.predict(input_df)[0]
    loss_pred = rf_sev.predict(input_df)[0]

    # Decode predictions
    decoded_attack = label_encoders['Attack Type'].inverse_transform([attack_pred])[0]
    decoded_industry = label_encoders['Target Industry'].inverse_transform([industry_pred])[0]

    # Display results
    st.success("🚨 Prediction Results:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Predicted Attack Type", decoded_attack)
    with col2:
        st.metric("Predicted Target Industry", decoded_industry)
    with col3:
        st.metric("Estimated Financial Loss", f"${loss_pred:,.2f}M")
    
    # Display input summary
    if 'form_data' in st.session_state:
        st.markdown("**📋 Input Summary:**")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"• **Country:** {st.session_state.form_data['country']}")
            st.write(f"• **Attack Source:** {st.session_state.form_data['attack_source']}")
            st.write(f"• **Year:** {st.session_state.form_data['user_input']['Year']}")
            st.write(f"• **Affected Users:** {st.session_state.form_data['user_input']['Number of Affected Users']:,}")
        with col2:
            st.write(f"• **Security Vulnerability:** {st.session_state.form_data['vuln_type']}")
            st.write(f"• **Defense Mechanism:** {st.session_state.form_data['defense']}")
            st.write(f"• **Resolution Time:** {st.session_state.form_data['user_input']['Incident Resolution Time (in Hours)']} hours")
        
        st.divider()
    
    # Additional insights
    st.info(f"""
    **Scenario Analysis:**
    - This prediction suggests a **{decoded_attack}** attack targeting the **{decoded_industry}** sector
    - Expected financial impact: **${loss_pred:,.2f} Million**
    - Based on the input parameters, this scenario has a moderate to high risk profile
    """)
    
    # Show feature importance for this prediction
    st.markdown("**Top 3 Most Important Features for this Prediction:**")
    st.write(f"1. {attack_feature_importance.iloc[0]['feature']}")
    st.write(f"2. {attack_feature_importance.iloc[1]['feature']}")
    st.write(f"3. {attack_feature_importance.iloc[2]['feature']}")
