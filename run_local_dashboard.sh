#!/bin/bash
# 🚀 Emergency Local Dashboard Setup
# Use this if external deployment has issues

echo "🛡️ Setting up Local Cybersecurity Dashboard..."
echo "================================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install pip first."
    exit 1
fi

# Install requirements
echo "📦 Installing dependencies..."
pip install streamlit pandas numpy plotly scikit-learn matplotlib seaborn

# Check if data file exists
if [ ! -f "data/clean_global_cybersecurity_threats.csv" ]; then
    echo "❌ Data file not found. Please ensure data/clean_global_cybersecurity_threats.csv exists."
    exit 1
fi

# Run the dashboard
echo "🚀 Starting dashboard on http://localhost:8501"
echo "⚡ Press Ctrl+C to stop"
echo ""
streamlit run cyber_dashboard_final.py --server.port 8501 --server.address localhost

echo ""
echo "✅ Dashboard accessible at: http://localhost:8501"
echo "📱 Share this URL for local network access"
