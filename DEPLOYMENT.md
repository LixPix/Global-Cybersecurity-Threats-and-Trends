# 🚀 Streamlit Community Cloud Deployment Guide

## 📋 **Quick Deployment Steps**

### **1. Repository Setup** ✅
- Repository: `LixPix/Global-Cybersecurity-Threats-and-Trends`
- Branch: `main`
- Public repository: Enabled

### **2. Deploy to Streamlit Cloud**

1. **Visit Streamlit Community Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app"
   - Repository: `LixPix/Global-Cybersecurity-Threats-and-Trends`
   - Branch: `main`
   - Main file path: `cyber_dashboard_final.py`
   - App URL: Choose custom name like `global-cybersecurity-dashboard`

3. **Deploy:**
   - Click "Deploy!"
   - Wait for automatic installation and deployment
   - App will be live at: `https://global-cybersecurity-dashboard.streamlit.app/`

### **3. Configuration Files** ✅

**requirements.txt** (Updated for Python 3.11 compatibility):
```txt
streamlit>=1.31.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
scikit-learn>=1.3.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

**runtime.txt** (Python version specification):
```txt
python-3.11
```

**.python-version** (Local development):
```txt
3.11
```

**.streamlit/config.toml** (Already configured):
```toml
[server]
headless = true
port = $PORT
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

**Procfile** (For backup deployment):
```
web: sh setup.sh && streamlit run cyber_dashboard_final.py --server.port=$PORT --server.address=0.0.0.0
```

### **4. Verification Steps**

✅ **Check Deployment:**
1. App builds successfully without errors
2. All dependencies install correctly
3. Dashboard loads with data visualizations
4. Interactive features work (filtering, ML predictions)
5. External access confirmed from different networks

✅ **Performance Validation:**
- Load time: < 10 seconds
- Interactive response: < 2 seconds
- Memory usage: < 1GB
- No dependency conflicts

### **5. Troubleshooting**

**Common Issues & Solutions:**

1. **Build Failures:**
   - Check requirements.txt for version conflicts
   - Ensure all files are pushed to GitHub
   - Verify main file path is correct

2. **Memory Issues:**
   - Optimize data loading with caching
   - Use `@st.cache_data` decorators
   - Limit dataset size if needed

3. **Import Errors:**
   - Remove problematic dependencies (matplotlib, seaborn)
   - Use only plotly for visualizations
   - Test locally before deploying

### **6. Troubleshooting Deployment Issues**

**Common Issues and Solutions:**

1. **Python Version Compatibility:**
   ```
   Error: numpy==1.26.1 not compatible with Python 3.13
   Solution: Use Python 3.11 (specified in runtime.txt)
   ```

2. **Package Conflicts:**
   ```
   Error: scikit-learn version conflicts
   Solution: Use flexible version ranges (>=) instead of exact versions
   ```

3. **Missing Dependencies:**
   ```
   Error: No module named 'cgi' (htmlmin/ydata-profiling)
   Solution: Removed problematic packages, using core libraries only
   ```

4. **Build Failures:**
   - Check logs in Streamlit Cloud dashboard
   - Verify all files are committed and pushed to GitHub
   - Ensure data files are in correct paths (data/ directory)

5. **Performance Issues:**
   - Use st.cache_data for data loading
   - Optimize large file operations
   - Monitor memory usage

**Deployment Status Check:**
- Visit: `https://share.streamlit.io/` → Your Apps
- Check build logs for detailed error messages
- Restart app if needed from dashboard

### **7. Monitoring & Maintenance**

**Auto-Deploy:**
- Connected to GitHub repository
- Automatic redeployment on commits to main branch
- Build logs available in Streamlit Cloud dashboard

**Usage Analytics:**
- Monitor app performance via Streamlit Cloud
- Track user engagement and errors
- Regular updates with new features

## 🌐 **External Access URL**

**Live Dashboard:** `https://global-cybersecurity-dashboard.streamlit.app/`

**Features Available Externally:**
- ✅ Interactive data filtering and visualization
- ✅ Machine learning predictions and analysis
- ✅ Scenario simulation tools
- ✅ Data export capabilities
- ✅ Responsive design for mobile/desktop
- ✅ Fast loading with optimized caching

**Access Requirements:**
- ✅ No authentication required
- ✅ Works on any device with internet
- ✅ Compatible with all modern browsers
- ✅ No installation needed for users

---

## 📞 **Support Information**

**For Assessors:**
If you experience any issues accessing the dashboard:

1. **Primary URL:** https://global-cybersecurity-dashboard.streamlit.app/
2. **Backup:** Run locally using installation instructions in README.md
3. **Repository:** https://github.com/LixPix/Global-Cybersecurity-Threats-and-Trends

**Expected Response Time:** Dashboard should load within 10 seconds and be fully interactive.
