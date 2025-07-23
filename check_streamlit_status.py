#!/usr/bin/env python3
"""
🔍 Streamlit App URL Checker
Helps identify the correct Streamlit app URL and deployment status
"""

import requests
import time

def check_streamlit_urls():
    """Check various potential Streamlit app URLs"""
    
    potential_urls = [
        "https://global-cybersecurity-dashboard.streamlit.app/",
        "https://lixpix-global-cybersecurity-threats-and-trends-cyber-dashboard-final.streamlit.app/",
        "https://share.streamlit.io/lixpix/global-cybersecurity-threats-and-trends/main/cyber_dashboard_final.py",
        "https://lixpix-global-cybersecurity-dashboard.streamlit.app/",
        "https://global-cybersecurity-threats-and-trends.streamlit.app/",
    ]
    
    print("🔍 Checking Streamlit App URLs...")
    print("=" * 60)
    
    working_urls = []
    
    for i, url in enumerate(potential_urls, 1):
        print(f"\n{i}. Testing: {url}")
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
            
            if status_code == 200:
                print(f"   ✅ SUCCESS! (Status: {status_code})")
                working_urls.append(url)
            elif status_code == 404:
                print(f"   ❌ Not Found (Status: {status_code})")
            elif status_code == 403:
                print(f"   🔒 Access Forbidden (Status: {status_code})")
            elif status_code == 401:
                print(f"   🚫 Unauthorized (Status: {status_code})")
            else:
                print(f"   ⚠️ Other Issue (Status: {status_code})")
                
        except requests.exceptions.Timeout:
            print(f"   ⏳ Timeout - App might be loading")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection Error - URL might not exist")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    
    if working_urls:
        print(f"✅ WORKING URLS FOUND: {len(working_urls)}")
        for url in working_urls:
            print(f"   🔗 {url}")
    else:
        print("❌ NO WORKING URLS FOUND")
        print("\n🛠️ RECOMMENDED ACTIONS:")
        print("1. Check Streamlit Cloud dashboard: https://share.streamlit.io/")
        print("2. Verify app deployment status")
        print("3. Check if repository is connected")
        print("4. Ensure app is set to PUBLIC")
        print("5. Try redeploying the app")
    
    return working_urls

def check_github_repo():
    """Check if GitHub repository is accessible"""
    print("\n🐙 Checking GitHub Repository...")
    print("=" * 40)
    
    repo_url = "https://api.github.com/repos/LixPix/Global-Cybersecurity-Threats-and-Trends"
    
    try:
        response = requests.get(repo_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Repository: {data['full_name']}")
            print(f"📊 Public: {not data['private']}")
            print(f"🌟 Stars: {data['stargazers_count']}")
            print(f"📝 Updated: {data['updated_at']}")
            return True
        else:
            print(f"❌ Repository access failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error checking repository: {str(e)}")
        return False

if __name__ == "__main__":
    print("🛡️ STREAMLIT APP DIAGNOSTICS")
    print("=" * 60)
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check repository first
    repo_ok = check_github_repo()
    
    # Check app URLs
    working_urls = check_streamlit_urls()
    
    print("\n📋 SUMMARY:")
    print("=" * 20)
    print(f"Repository Access: {'✅' if repo_ok else '❌'}")
    print(f"Working App URLs: {len(working_urls)}")
    
    if working_urls:
        print(f"\n🎯 RECOMMENDED URL:")
        print(f"   {working_urls[0]}")
    else:
        print(f"\n🔧 NEXT STEPS:")
        print("1. Go to https://share.streamlit.io/")
        print("2. Sign in and check your apps")
        print("3. Redeploy if necessary")
        print("4. Ensure app is PUBLIC")
