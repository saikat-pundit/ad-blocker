#!/usr/bin/env python3
import requests
import os
from datetime import datetime
import pytz
import sys

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

def format_size(bytes):
    for unit in ['B', 'KB', 'MB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} GB"

def fetch_url(url):
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            size = len(response.content)
            print(f"✓ {url.split('/')[-1][:30]:30} | {format_size(size):>8}")
            return response.text
        else:
            print(f"✗ {url.split('/')[-1][:30]:30} | ERROR: HTTP {response.status_code}")
            return None
    except requests.Timeout:
        print(f"✗ {url.split('/')[-1][:30]:30} | ERROR: Timeout")
        return None
    except requests.ConnectionError:
        print(f"✗ {url.split('/')[-1][:30]:30} | ERROR: Connection failed")
        return None
    except Exception as e:
        print(f"✗ {url.split('/')[-1][:30]:30} | ERROR: {str(e)[:30]}")
        return None

print(f"\n{'File':32} | Size")
print("-" * 55)

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
failed = 0

for url in urls:
    content = fetch_url(url)
    if content:
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith(('#', '!', '0.0.0.0', '127.0.0.1')):
                domains.add(line.split()[0] if ' ' in line else line)
    else:
        failed += 1

print("-" * 55)
print(f"Total: {len(urls)} files, Failed: {failed}, Success: {len(urls)-failed}")

# Filter out unwanted domains
domains = {d for d in domains if not any(x in d for x in ['facebook.com', '.fb.com', 'blogspot.com'])}

# Add manual domains
domains.update(manual_domains)

# Write to file
with open('blocklist.txt', 'w') as f:
    f.write('\n'.join(blocklist))
    f.write('\n' + '\n'.join(sorted(domains)))
    
    # Add wildcard comments
    f.write('\n\n# === WILDCARD DOMAINS (Not natively supported by /etc/hosts) ===\n')
    for wc in ['*.heytapimg.com', '*.heytapmobile.com', '*.heytapmobi.com', 
               '*.heytap.com', '*.heytapdl.com', '*.heytapdownload.com',
               '*.app-measurement.com', '*.mtalk.google.com']:
        f.write(f'# {wc}\n')

file_size = format_size(os.path.getsize('blocklist.txt'))
print(f"\n✅ Blocklist generated: blocklist.txt ({file_size})")
print(f"📊 Total domains: {len(domains)}")
