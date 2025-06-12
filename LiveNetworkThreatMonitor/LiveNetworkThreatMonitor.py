import psutil
import tkinter as tk
from tkinter import ttk
import requests
import threading
import ipaddress

class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Network Threat Monitor")
        self.root.geometry("1000x600")
        self.root.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.configure("Treeview", background="#2d2d2d", foreground="white", fieldbackground="#2d2d2d")
        style.map("Treeview", background=[("selected", "#007acc")])
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#1e1e1e", foreground="white")

        self.tree = ttk.Treeview(root, columns=("IP", "Port", "Status", "Details"), show='headings')
        self.tree.heading("IP", text="Remote IP")
        self.tree.heading("Port", text="Port")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Details", text="Threat Info")
        self.tree.column("IP", width=200)
        self.tree.column("Port", width=100)
        self.tree.column("Status", width=150)
        self.tree.column("Details", width=400)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.ip_cache = {}
        self.refresh_data()

    def refresh_data(self):
        threading.Thread(target=self.update_network_data, daemon=True).start()
        self.root.after(15000, self.refresh_data)

    def update_network_data(self):
        try:
            connections = psutil.net_connections(kind='inet')
            self.tree.delete(*self.tree.get_children())

            for conn in connections:
                if conn.raddr:
                    ip, port = conn.raddr
                    status = conn.status

                    try:
                        if ipaddress.ip_address(ip).is_private:
                            continue
                    except:
                        continue

                    if ip in self.ip_cache:
                        threat_info = self.ip_cache[ip]
                    else:
                        threat_info = self.check_ip_threat(ip)
                        self.ip_cache[ip] = threat_info

                    self.tree.insert("", "end", values=(ip, port, status, threat_info))
        except Exception as e:
            print("Error updating network data:", e)

    def check_ip_threat(self, ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                country = data.get("country", "Unknown")
                org = data.get("org", "Unknown")
                return f"{country} - {org}"
            else:
                return "Lookup Failed"
        except:
            return "Lookup Error"

# --- Main ---
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = NetworkMonitorApp(root)
        root.mainloop()
    except Exception as e:
        print("ERROR:", e)
        input("Press Enter to exit...")
