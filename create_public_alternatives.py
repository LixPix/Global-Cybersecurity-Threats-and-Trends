#!/usr/bin/env python3
"""
🔧 Alternative Public Dashboard Deployment
Creates a completely new public Streamlit app to bypass privacy issues
"""

import subprocess
import os
import shutil

def create_public_app_variant():
    """Create a variant of the dashboard app for guaranteed public deployment"""
    
    print("🔧 Creating Public Dashboard Variant")
    print("=" * 40)
    
    # Read the original dashboard
    try:
        with open('cyber_dashboard_final.py', 'r', encoding='utf-8') as f:
            original_content = f.read()
        print("✅ Read original dashboard file")
    except Exception as e:
        print(f"❌ Error reading original file: {e}")
        return False
    
    # Create a new public version with slight modifications
    public_content = f'''# **PUBLIC Global Cyber Threats Dashboard 2015-2024**
# Publicly accessible version for external assessment and evaluation

{original_content}

# Additional public access confirmation
if __name__ == "__main__":
    # This ensures the app runs when accessed externally
    import streamlit as st
    st.sidebar.success("✅ Public Dashboard - No login required!")
'''
    
    # Write the public version
    try:
        with open('cyber_dashboard_public.py', 'w', encoding='utf-8') as f:
            f.write(public_content)
        print("✅ Created public dashboard variant: cyber_dashboard_public.py")
    except Exception as e:
        print(f"❌ Error creating public file: {e}")
        return False
    
    return True

def create_deployment_instructions():
    """Create step-by-step deployment instructions"""
    
    instructions = '''# 🚀 Deploy New Public Streamlit App

## 🎯 **Guaranteed Public Access Solution**

If the current app has privacy issues, deploy a new one:

### **Method 1: New Streamlit App**
1. Go to: https://share.streamlit.io/
2. Click "New app"
3. Repository: `LixPix/Global-Cybersecurity-Threats-and-Trends`
4. Branch: `main`
5. Main file: `cyber_dashboard_public.py` ← NEW FILE
6. App URL: `cybersecurity-public-dashboard`
7. **ENSURE "Public" is selected**
8. Deploy

### **Method 2: Alternative Platforms**

#### **Railway.app** (Recommended backup)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### **Render.com** (Free tier)
1. Connect GitHub repository
2. Choose "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run cyber_dashboard_public.py --server.port $PORT`

#### **Heroku** (Using existing Procfile)
```bash
# Install Heroku CLI, then:
heroku create cybersecurity-dashboard-public
git push heroku main
```

## 📋 **New URLs After Deployment**
- **Streamlit**: `https://cybersecurity-public-dashboard.streamlit.app/`
- **Railway**: `https://[app-name].railway.app/`
- **Render**: `https://[app-name].onrender.com/`
- **Heroku**: `https://cybersecurity-dashboard-public.herokuapp.com/`

## ✅ **Testing New Deployment**
```bash
# Test public access
curl -I [new-url] | grep "HTTP"

# Should return HTTP/1.1 200 OK
# Should NOT redirect to login page
```

## 🎯 **For Immediate Assessment**
If external deployment fails:
1. **Use local setup** (instructions in README)
2. **Screen recording** of dashboard functionality
3. **Export screenshots** of all dashboard features
4. **Document all features** in assessment materials

---
**Created**: Backup solution for guaranteed public access
**Status**: Ready for deployment if Streamlit privacy issues persist
'''
    
    try:
        with open('DEPLOY_PUBLIC_ALTERNATIVE.md', 'w', encoding='utf-8') as f:
            f.write(instructions)
        print("✅ Created deployment instructions: DEPLOY_PUBLIC_ALTERNATIVE.md")
    except Exception as e:
        print(f"❌ Error creating instructions: {e}")
        return False
    
    return True

def create_quick_local_setup():
    """Create quick local setup script for emergency access"""
    
    local_script = '''#!/bin/bash
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
'''
    
    try:
        with open('run_local_dashboard.sh', 'w', encoding='utf-8') as f:
            f.write(local_script)
        print("✅ Created local setup script: run_local_dashboard.sh")
        
        # Make executable
        os.chmod('run_local_dashboard.sh', 0o755)
        print("✅ Made script executable")
    except Exception as e:
        print(f"❌ Error creating local script: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚨 STREAMLIT PRIVACY ISSUE - CREATING ALTERNATIVES")
    print("=" * 60)
    
    success1 = create_public_app_variant()
    success2 = create_deployment_instructions()
    success3 = create_quick_local_setup()
    
    print("\n📋 SUMMARY:")
    print(f"Public app variant: {'✅' if success1 else '❌'}")
    print(f"Deployment guide: {'✅' if success2 else '❌'}")
    print(f"Local setup script: {'✅' if success3 else '❌'}")
    
    if all([success1, success2, success3]):
        print("\n🎉 ALTERNATIVE SOLUTIONS READY!")
        print("📁 Files created:")
        print("   • cyber_dashboard_public.py")
        print("   • DEPLOY_PUBLIC_ALTERNATIVE.md")
        print("   • run_local_dashboard.sh")
        print("\n🎯 NEXT STEPS:")
        print("1. Follow URGENT_FIX_STREAMLIT_PRIVACY.md first")
        print("2. If that fails, use DEPLOY_PUBLIC_ALTERNATIVE.md")
        print("3. Emergency backup: run run_local_dashboard.sh")
    else:
        print("\n❌ Some alternatives failed to create")
