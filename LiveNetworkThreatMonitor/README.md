# Live Network Threat Monitor

 **Live Network Threat Monitor** is a Python desktop app that shows your active network connections in real-time and provides geographic and organizational info about remote IPs. It's built with `psutil` for network monitoring, `requests` for IP lookups, and Tkinter for a sleek GUI.

---

## Features

- Monitor live network connections on your machine  
- Lookup IP geolocation and organization info using `ipapi.co`  
- Dark-themed, user-friendly interface built with Tkinter  
- Auto-refreshes every 10 seconds to keep data current  
- Cross-platform (Windows, macOS, Linux) with Python 3.8+

---

## Requirements

- Python 3.8 or higher  
- `psutil` package  
- `requests` package  

Install dependencies with:

```bash
pip install psutil requests
