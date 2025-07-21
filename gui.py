import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# ─────────────────────────── Example data ──────────────────────────────
time = np.linspace(0, 10, 100)

telemetry_data      = np.random.rand(100) * 100
position_data       = np.sin(time) * 100
mission_data        = np.cos(time) * 50
payload_data        = np.random.rand(100) * 50
communication_data  = np.random.rand(100) * 50
system_data         = np.random.rand(100) * 50
environmental_data  = np.random.rand(100) * 50

gnss_x = np.cumsum(np.random.randn(100))
gnss_y = np.cumsum(np.random.randn(100)) * 0.8
gnss_z = np.cumsum(np.random.randn(100)) * 0.6
altitude_data = np.linspace(0, 400, 100) + 10 * np.sin(0.5 * time)

# ─────────────────────────── GUI setup ─────────────────────────────────
root = tk.Tk()
root.title("CubeSat Data Viewer")
root.geometry("1200x800")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="CubeSat Data")
tab_control.pack(expand=1, fill="both")

frame = ttk.Frame(tab1)
frame.pack(fill="both", expand=True)

canvas = tk.Canvas(frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# ─────────────────────────── Grid frames ───────────────────────────────
frame1 = ttk.Frame(inner_frame); frame1.grid(row=0, column=0, padx=10, pady=10)
frame2 = ttk.Frame(inner_frame); frame2.grid(row=0, column=1, padx=10, pady=10)
frame3 = ttk.Frame(inner_frame); frame3.grid(row=0, column=2, padx=10, pady=10)
frame4 = ttk.Frame(inner_frame); frame4.grid(row=1, column=0, padx=10, pady=10)  # GNSS now
frame5 = ttk.Frame(inner_frame); frame5.grid(row=1, column=1, padx=10, pady=10)
frame6 = ttk.Frame(inner_frame); frame6.grid(row=1, column=2, padx=10, pady=10)  # Altitude now
frame7 = ttk.Frame(inner_frame); frame7.grid(row=2, column=1, padx=10, pady=10)
frame8 = ttk.Frame(inner_frame); frame8.grid(row=2, column=0, padx=10, pady=10)  # Payload moved
frame9 = ttk.Frame(inner_frame); frame9.grid(row=2, column=2, padx=10, pady=10)  # System moved

# ─────────────────────────── Plot helper ───────────────────────────────
def add_plot(frame, x, y, xlabel, ylabel, title, **plot_kwargs):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, **plot_kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    canvas_fig = FigureCanvasTkAgg(fig, master=frame)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack()

# Main plots with colors
add_plot(frame1, time, telemetry_data,      'Time', 'Telemetry',  'Telemetry Data',        color='royalblue')
add_plot(frame2, time, position_data,       'Time', 'Position',   'Position & Orbit',      color='forestgreen')
add_plot(frame3, time, mission_data,        'Time', 'Events',     'Mission Events',        color='crimson')
add_plot(frame5, time, communication_data,  'Time', 'Comm',       'Communication Data',    color='mediumorchid')
add_plot(frame7, time, environmental_data,  'Time', 'Env',        'Environmental Data',    color='saddlebrown')

# GNSS now in frame4
fig_gnss, ax_gnss = plt.subplots(figsize=(6, 4))
ax_gnss.plot(time, gnss_x, label='X', color='dodgerblue')
ax_gnss.plot(time, gnss_y, label='Y', color='limegreen')
ax_gnss.plot(time, gnss_z, label='Z', color='tomato')
ax_gnss.set_xlabel('Time')
ax_gnss.set_ylabel('Meters')
ax_gnss.set_title('GNSS Position (X/Y/Z)')
ax_gnss.legend()
canvas_gnss = FigureCanvasTkAgg(fig_gnss, master=frame4)
canvas_gnss.draw()
canvas_gnss.get_tk_widget().pack()

# Altitude now in frame6
add_plot(frame6, time, altitude_data, 'Time', 'Altitude (m)', 'Altitude Profile', color='skyblue')

# Payload now in frame8
add_plot(frame8, time, payload_data, 'Time', 'Payload', 'Payload Data', color='darkorange')

# System now in frame9
add_plot(frame9, time, system_data, 'Time', 'System', 'System Performance', color='teal')

# ─────────────────────────── Scroll region ─────────────────────────────
inner_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

root.mainloop()
