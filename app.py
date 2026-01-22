import json
import tkinter as tk
from tkinter import simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -----------------------------
# Load routers from JSON
# -----------------------------
with open('routers.json', 'r') as f:
    routers = json.load(f)

# Add default interfaces and BGP info to each router
for r in routers:
    r['interfaces'] = {'Gig0/0': 'down', 'Gig0/1': 'down', 'Gig0/2': 'down'}
    r['bgp'] = {'neighbor_ip': '', 'neighbor_as': ''}

# -----------------------------
# Main window
# -----------------------------
root = tk.Tk()
root.title("Multi-Router Python Demo")

# -----------------------------
# Console for logs
# -----------------------------
console = tk.Text(root, height=10, width=80)
console.pack(pady=10)

def log(msg):
    console.insert(tk.END, msg + '\n')
    console.see(tk.END)

# -----------------------------
# Routers frame
# -----------------------------
routers_frame = tk.Frame(root)
routers_frame.pack(pady=10)

# -----------------------------
# Router actions
# -----------------------------
def connect_router(router):
    log(f"{router['id']}: Simulating connect...")
    router['status'] = 'connected (sim)'
    update_router_display()

def view_router(router):
    log(f"{router['id']}: IP={router['ip']} Port={router['port']} Status={router['status']}")

def restart_router(router):
    log(f"{router['id']}: Restarting...")
    router['status'] = 'restarting (sim)'
    update_router_display()
    root.after(2000, lambda: finish_restart(router))

def finish_restart(router):
    router['status'] = 'connected (sim)'
    update_router_display()
    log(f"{router['id']}: Restart complete")

def toggle_interface(router, intf):
    current = router['interfaces'][intf]
    new_status = 'up' if current == 'down' else 'down'
    router['interfaces'][intf] = new_status
    log(f"{router['id']}: Interface {intf} set to {new_status}")

def configure_bgp(router):
    ip = simpledialog.askstring("BGP Neighbor IP", f"Enter BGP neighbor IP for {router['id']}:")
    asn = simpledialog.askstring("BGP Neighbor AS", f"Enter BGP neighbor AS number for {router['id']}:")
    if ip and asn:
        router['bgp']['neighbor_ip'] = ip
        router['bgp']['neighbor_as'] = asn
        log(f"{router['id']}: BGP neighbor set to {ip} AS{asn}")

def ping_router(router_from, router_to):
    log(f"Pinging from {router_from['id']} to {router_to['id']}...")
    if router_from['status'].startswith('connected') and router_to['status'].startswith('connected'):
        log("Ping successful!")
    else:
        log("Ping failed (simulated)")

def connect_all_routers():
    for r in routers:
        r['status'] = 'connected (sim)'
    log("All routers set to connected (simulated)")
    update_router_display()

def simulate_odl_failure():
    for r in routers:
        r['status'] = 'unauthorized (sim)'
    log("All routers set to unauthorized (simulated ODL failure)")
    update_router_display()

# -----------------------------
# Update router display
# -----------------------------
def update_router_display():
    for widget in routers_frame.winfo_children():
        widget.destroy()
    
    for r in routers:
        frame = tk.Frame(routers_frame, borderwidth=1, relief="solid", padx=5, pady=5)
        frame.pack(pady=5, fill='x')

        # Status dot
        dot_color = "grey"
        if r['status'].startswith('connected'):
            dot_color = "green"
        elif r['status'].startswith('unauthorized') or r['status'].startswith('error'):
            dot_color = "red"
        elif r['status'].startswith('restarting'):
            dot_color = "orange"

        dot = tk.Canvas(frame, width=12, height=12)
        dot.create_oval(2, 2, 12, 12, fill=dot_color)
        dot.pack(side='left', padx=5)

        tk.Label(frame, text=f"{r['id']} ({r['status']})").pack(side='left', padx=5)

        # Router buttons
        tk.Button(frame, text="Connect", command=lambda r=r: connect_router(r)).pack(side='left', padx=3)
        tk.Button(frame, text="View", command=lambda r=r: view_router(r)).pack(side='left', padx=3)
        tk.Button(frame, text="Restart", command=lambda r=r: restart_router(r)).pack(side='left', padx=3)
        tk.Button(frame, text="Interfaces", command=lambda r=r: manage_interfaces(r)).pack(side='left', padx=3)
        tk.Button(frame, text="BGP", command=lambda r=r: configure_bgp(r)).pack(side='left', padx=3)

def manage_interfaces(router):
    top = tk.Toplevel(root)
    top.title(f"{router['id']} Interfaces")
    for intf, status in router['interfaces'].items():
        btn = tk.Button(top, text=f"{intf}: {status}", width=15, 
                        command=lambda r=router, i=intf, b=btn: toggle_intf_gui(r, i, b))
        btn.pack(pady=2)

def toggle_intf_gui(router, intf, btn):
    toggle_interface(router, intf)
    btn.config(text=f"{intf}: {router['interfaces'][intf]}")

# -----------------------------
# Topology window with triangle + ODL
# -----------------------------
def view_topology_graph():
    topo_win = tk.Toplevel(root)
    topo_win.title("Network Topology")

    G = nx.Graph()

    for r in routers:
        G.add_node(r['id'], status=r['status'])

    # Add ODL node
    G.add_node('ODL', status='controller')

    # Triangle links
    G.add_edge('R1', 'R2')
    G.add_edge('R2', 'R3')
    G.add_edge('R3', 'R1')

    # Connect ODL to R1
    G.add_edge('ODL', 'R1')

    # Node colors
    color_map = []
    for node in G.nodes(data=True):
        name, attr = node
        status = attr['status']
        if status.startswith('connected'):
            color_map.append('green')
        elif status.startswith('unauthorized') or status.startswith('error'):
            color_map.append('red')
        elif status.startswith('restarting'):
            color_map.append('orange')
        elif status == 'controller':
            color_map.append('blue')
        else:
            color_map.append('grey')

    # Draw graph
    fig, ax = plt.subplots(figsize=(6, 5))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=1200,
            font_size=12, font_weight='bold', ax=ax)

    canvas = FigureCanvasTkAgg(fig, master=topo_win)
    canvas.draw()
    canvas.get_tk_widget().pack()

    log("Topology window opened (triangle + ODL).")

    # -----------------------------
    # Ping GUI inside topology window
    # -----------------------------
    ping_frame = tk.Frame(topo_win)
    ping_frame.pack(pady=10)

    tk.Label(ping_frame, text="Ping from:").pack(side='left', padx=5)
    from_var = tk.StringVar()
    from_menu = tk.OptionMenu(ping_frame, from_var, *[r['id'] for r in routers])
    from_menu.pack(side='left', padx=5)

    tk.Label(ping_frame, text="to:").pack(side='left', padx=5)
    to_var = tk.StringVar()
    to_menu = tk.OptionMenu(ping_frame, to_var, *[r['id'] for r in routers])
    to_menu.pack(side='left', padx=5)

    def ping_action():
        r_from = next((r for r in routers if r['id'] == from_var.get()), None)
        r_to = next((r for r in routers if r['id'] == to_var.get()), None)
        if not r_from or not r_to:
            messagebox.showwarning("Ping", "Select both routers!")
            return
        log(f"Pinging from {r_from['id']} to {r_to['id']}...")
        if r_from['status'].startswith('connected') and r_to['status'].startswith('connected'):
            log("Ping successful!")
        else:
            log("Ping failed (simulated)")

    tk.Button(ping_frame, text="Ping", command=ping_action).pack(side='left', padx=5)


# -----------------------------
# Top control buttons
# -----------------------------
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Button(control_frame, text="View Topology", command=view_topology_graph).pack(side='left', padx=5)
tk.Button(control_frame, text="Connect All Routers", command=connect_all_routers).pack(side='left', padx=5)
tk.Button(control_frame, text="Simulate ODL Failure", command=simulate_odl_failure).pack(side='left', padx=5)

# -----------------------------
# Initial display
# -----------------------------
update_router_display()

# -----------------------------
# Start Tkinter main loop
# -----------------------------
root.mainloop()
