import subprocess
import requests
from datetime import datetime
import pytz

# URLs to fetch
urls = [
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/doh-vpn-proxy-bypass.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/hoster.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/ultimate.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/popupads.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/spam-tlds.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/dyndns.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adguard/dns-rebind-protection.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/social.txt",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/analyticsparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/doubleclickparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/dnsparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/proxiesparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/shortlinksparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/productsparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/androidparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/fiberparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/firebaseparsed",
    "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/generalparsed",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/native.oppo-realme.txt",
    "https://raw.githubusercontent.com/jmdugan/blocklists/master/corporations/microsoft/all",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/native.xiaomi.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/native.winoffice.txt",
]

# Manual domains
manual_domains = [
    "storeimg.heytapimg.com", "time-push-in.heytapmobile.com",
    "httpdns-push.heytapmobile.com", "client-uc.heytapmobi.com",
    "app-measurement.com", "alt1-mtalk.google.com", "alt2-mtalk.google.com",
    "alt3-mtalk.google.com", "alt4-mtalk.google.com", "alt5-mtalk.google.com",
    "alt6-mtalk.google.com", "alt7-mtalk.google.com", "alt8-mtalk.google.com",
    "mtalk.google.com"
]

# Build blocklist
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S IST')

blocklist = [
    "127.0.0.1 localhost",
    "127.0.1.1 home-desktop",
    "::1 ip6-localhost ip6-loopback",
    "",
    "# DNS Blocklist - Auto-generated",
    f"# Last Updated: {now}",
    "# ==============================================",
    ""
]

# Fetch and process domains
domains = set()
for url in urls:
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            for line in response.text.splitlines():
                line = line.strip()
                if line and not line.startswith(('#', '!', '0.0.0.0', '127.0.0.1')):
                    domains.add(line.split()[0] if ' ' in line else line)
    except:
        continue

# Filter out unwanted domains
domains = {d for d in domains if not any(x in d for x in ['facebook.com', '.fb.com', 'blogspot.com'])}

# Add manual domains
domains.update(manual_domains)

# Write to file
with open('blocklist.txt', 'w') as f:
    f.write('\n'.join(blocklist))
    f.write('\n'.join(sorted(domains)))
    
    # Add wildcard comments
    f.write('\n\n# === WILDCARD DOMAINS (Not natively supported by /etc/hosts) ===\n')
    for wc in ['*.heytapimg.com', '*.heytapmobile.com', '*.heytapmobi.com', 
               '*.heytap.com', '*.heytapdl.com', '*.heytapdownload.com',
               '*.app-measurement.com', '*.mtalk.google.com']:
        f.write(f'# {wc}\n')

print(f"Blocklist updated: {now}")
