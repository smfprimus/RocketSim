### Rocket Simulator
# Ein einfacher Raketen-Simulator, der die grundlegenden Parameter einer Rakete berechnet und eine Flug-Simulation durchführt.
# Dieses Skript verwendet Tkinter für die GUI, Matplotlib für die Plots und NumPy für mathematische Berechnungen.
# Author: Sasha-Mercedes Fischer
###

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk # Damit wir die GUI schöner machen können
import matplotlib.pyplot as plt # Matplotlib für die Plots (Graphen)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Matplotlib in Tkinter integrieren
import numpy as np # NumPy für alles Rechnerische
import math # Mathematische Funktionen

# Klasse für den Raketen-Simulator
class RocketSimulator:
    def __init__(self, root): # Funktion, die beim Starten der Klasse aufgerufen wird
        self.root = root # klasse wird mit dem Tkinter-Fenster verbunden
        self.root.title("Rocket Calculator & Flight Simulator") # Titel des Fensters
        self.root.geometry("1200x900") # Größe des Fensters
        
        # Konstante
        self.g0 = 9.81  # Standard Erdbeschleunigung (m/s²)
        
        # Eigenschaften der Treibstoffe als JSON
        self.propellants = {
            "LH2/LOX": {"density": 350, "typical_isp": 450},
            "Methane/LOX": {"density": 900, "typical_isp": 370},
            "Kerosene/LOX": {"density": 1000, "typical_isp": 340}
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        # Haupt-Frame für die GUI
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Obererster Frame für Eingabefelder und Ergebnisse
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input Frame (ca. ein Viertel der Breite)
        input_frame = ttk.LabelFrame(top_frame, text="Rocket Parameters", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5)) # Frame wird links angeordnet.
        input_frame.configure(width=400)  # Breite wird fix eingestellt, weil ich nicht weiß wie das dynamisch geht
        
        # Ergebnisse Frame (ca. drei Viertel der Breite)
        results_frame = ttk.LabelFrame(top_frame, text="Calculated Parameters", padding="10")
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0)) # Frame wird rechts angeordnet und nimmt den Rest der Breite ein
        # Textfeld für die Ergebnisse
        self.results_text = tk.Text(results_frame, height=8, width=80)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Textfeld wird links angeordnet und nimmt den Rest der Höhe und Breite ein
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # Scrollbar wird rechts angeordnet und nimmt die volle Höhe ein
        
        # Input Felder
        # Zeilen-Index für die Eingabefelder
        row = 0
        
        # Treibstofftypen
        ttk.Label(input_frame, text="Propellant Type:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.propellant_var = tk.StringVar(value="Kerosene/LOX") # Standardwert
        propellant_combo = ttk.Combobox(input_frame, textvariable=self.propellant_var, # Combobox für Treibstofftypen
                                       values=list(self.propellants.keys()), state="readonly")
        propellant_combo.grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        propellant_combo.bind('<<ComboboxSelected>>', self.update_typical_isp) # Funktion wird aufgerufen, wenn der Treibstofftyp geändert wird
        row += 1 # nächste Zeile
        
        # Schub
        ttk.Label(input_frame, text="Thrust (kN):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.thrust_var = tk.StringVar(value="7500") # Standardwert für Schub
        ttk.Entry(input_frame, textvariable=self.thrust_var).grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        row += 1
        
        # Spezifischen Impuls
        ttk.Label(input_frame, text="Specific Impulse (s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.isp_var = tk.StringVar(value="340") # Standardwert für spezifischen Impuls
        ttk.Entry(input_frame, textvariable=self.isp_var).grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        row += 1
        
        # Brenndauer
        ttk.Label(input_frame, text="Burn Time (s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.burn_time_var = tk.StringVar(value="150") # Standardwert für Brenndauer
        ttk.Entry(input_frame, textvariable=self.burn_time_var).grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        row += 1
        
        # Trockenmasse (Masse der Rakete ohne Treibstoff und Nutzlast)
        ttk.Label(input_frame, text="Dry Mass (kg):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.dry_mass_var = tk.StringVar(value="22200") # Standardwert für Trockenmasse
        ttk.Entry(input_frame, textvariable=self.dry_mass_var).grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        row += 1
        
        # Nutzlastmasse (Masse der Nutzlast, die die Rakete transportieren soll)
        ttk.Label(input_frame, text="Payload Mass (kg):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.payload_var = tk.StringVar(value="22800") # Standardwert für Nutzlastmasse
        ttk.Entry(input_frame, textvariable=self.payload_var).grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        row += 1

        # Button zum Berechnen und Simulieren
        ttk.Button(input_frame, text="Calculate & Simulate",
                  command=self.calculate_and_simulate).grid(row=row, column=0, columnspan=2, pady=10) # Button mit Funktion verbinden
        
        # Frame für die Plots
        plots_frame = ttk.LabelFrame(main_frame, text="Flight Simulation", padding="10")
        plots_frame.pack(fill=tk.BOTH, expand=True)
        
        # Erstellen von Matplotlib-Figuren und Achsen
        # hier habe ich viel Code aus einem Tutorial übernommen, um die Plots in Tkinter einzubauen
        # alles verstehe ich hier noch nicht, aber es funktioniert
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, plots_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_typical_isp(self, event=None):
        """Funktion aktualisiert den spezifischen Impuls je nachdem welcher Treibstoff ausgewählt ist."""
        propellant = self.propellant_var.get()
        typical_isp = self.propellants[propellant]["typical_isp"]
        self.isp_var.set(str(typical_isp))
        
    def calculate_parameters(self):
        """Berechnen der Raketenparameter auf Basis der Eingaben"""
        try:
            # Eingabewerte aus den Eingabefeldern holen
            thrust = float(self.thrust_var.get()) * 1000  # kN zu N umrechnen
            isp = float(self.isp_var.get())
            burn_time = float(self.burn_time_var.get())
            dry_mass = float(self.dry_mass_var.get())
            payload_mass = float(self.payload_var.get())
            propellant_type = self.propellant_var.get()
            
            # Berechnen von Parametern rund um den Antrieb
            ve = isp * self.g0  # Ausstoßgeschwindigkeit (m/s)
            mass_flow_rate = thrust / ve  # Massenstromrate (kg/s)
            propellant_mass = mass_flow_rate * burn_time  # Gesamte Treibstoffmasse (kg)
            
            # Massenberechnungen
            total_initial_mass = dry_mass + payload_mass + propellant_mass # Gesamte Startmasse der Rakete (kg)
            final_mass = dry_mass + payload_mass # Endmasse der Rakete (kg) (nach dem Treibstoffverbrauch)
            
            # Prozentverteilungen der Massen
            dry_mass_percent = (dry_mass / total_initial_mass) * 100
            payload_percent = (payload_mass / total_initial_mass) * 100
            propellant_percent = (propellant_mass / total_initial_mass) * 100
            
            # Delta-v Berechnung mit hilfe der Tsiolkovsky-Raketenformel
            delta_v = ve * math.log(total_initial_mass / final_mass)
            
            # Verhältnis von Schub zu Gewichtskraft (TWR)
            initial_twr = thrust / (total_initial_mass * self.g0)
            final_twr = thrust / (final_mass * self.g0)
            
            # Größe des Treibstofftanks (Volumen, dieser Wert ist nur eine Schätzung)
            propellant_density = self.propellants[propellant_type]["density"]
            tank_volume = propellant_mass / propellant_density
            
            # Ergebnisse in einem Dictionary speichern und zurückgeben
            return {
                'thrust': thrust,
                'isp': isp,
                'burn_time': burn_time,
                'dry_mass': dry_mass,
                'payload_mass': payload_mass,
                'propellant_mass': propellant_mass,
                'total_initial_mass': total_initial_mass,
                'final_mass': final_mass,
                'dry_mass_percent': dry_mass_percent,
                'payload_percent': payload_percent,
                'propellant_percent': propellant_percent,
                'delta_v': delta_v,
                'initial_twr': initial_twr,
                'final_twr': final_twr,
                'mass_flow_rate': mass_flow_rate,
                'exhaust_velocity': ve,
                'tank_volume': tank_volume,
                'propellant_type': propellant_type
            }
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid values.")
            return None
            
    def simulate_flight(self, params):
        """Raketenflug simulieren"""
        dt = 0.1  # Zeitabstand in Sekunden in der die Simulation durchgeführt wird
        # Listen für die Ergebnisse der Simulation
        time_points = []
        height_points = []
        velocity_points = []
        mass_points = []
        
        # Anfangswerte
        t = 0
        h = 0  # Höhe
        v = 0  # Geschwindigkeit
        m = params['total_initial_mass']  # Aktuelle Masse der Rakete
        
        # Phase 1: Flug mit aktivem Raketentriebwerk
        while t <= params['burn_time']:
            time_points.append(t)
            height_points.append(h)
            velocity_points.append(v)
            mass_points.append(m)
            
            # Wirkende Kräfte berechnen
            weight = m * self.g0 # F=m*g (Gewichtskraft)
            
            # Vereinfachter Luftwiderstand (hab ich online nachgeschaut)
            air_density = 1.225 * math.exp(-h / 8400) 
            drag_coeff = 0.3  # Luftwiderstandskoeffizient (angenommen)
            reference_area = 10  # Querschnittsfläche der Rakete (m², angenommener Wert)
            drag = 0.5 * air_density * drag_coeff * reference_area * v * abs(v)
            
            net_force = params['thrust'] - weight - drag  # effektive Kraft = Schub - Gewichtskraft - Luftwiderstand
            acceleration = net_force / m  # Beschleunigung = Kraft / Masse
            
            # Geschwindigkeit und Höhe aktualisieren
            # das ist genaugenommen nicht ganz korrekt, aber für die Simulation reicht es
            v += acceleration * dt
            h += v * dt
            
            # Masse aktualisieren (verbrauchten Treibstoff abziehen)
            m -= params['mass_flow_rate'] * dt
            
            t += dt
            
        # Phase 2: Freier Fall
        # Nach der Brenndauer ist kein Schub mehr vorhanden, nur noch Gewichtskraft und Luftwiderstand
        m = params['final_mass']  # kein Treibstoff mehr, also Endmasse
        
        while v > 0 or h > 0:  # Simuliere bis die Rakete den Boden erreicht oder zum Stillstand kommt
            time_points.append(t)
            height_points.append(max(0, h))  # Don't go below ground
            velocity_points.append(v)
            mass_points.append(m)
            
            if h <= 0:  # Rakete hat den Boden erreicht
                break
                
            # nur mit Schwerkraft und Luftwiderstand arbeiten
            weight = m * self.g0  # Gewichtskraft
            air_density = 1.225 * math.exp(-h / 8400)  # Luftdichte abhängig von der Höhe
            drag = 0.5 * air_density * drag_coeff * reference_area * v * abs(v)  # Luftwiderstand
            
            # Luftwiderstand wirkt entgegen der Bewegung
            if v > 0: # Rakete steigt noch
                # Wenn die Rakete noch steigt, wirkt der Luftwiderstand zusätzlich zur der Schwerkraft
                net_force = -weight - drag
            else:  # Rakete fällt
                # Wenn die Rakete fällt, wirkt der Luftwiderstand gegen die Schwerkraft
                net_force = -weight + drag
                
            acceleration = net_force / m  # Beschleunigung = Kraft / Masse
            
            v += acceleration * dt  # Geschwindigkeit aktualisieren
            h += v * dt  # Höhe aktualisieren
            
            t += dt  # Zeit einen Schritt weiter
            
            # Sicherheitshalber: wenn die Zeit zu lang wird, breche ab
            if t > 1000:
                break
                
        return time_points, height_points, velocity_points, mass_points  # Ergebnisse der Simulation zurückgeben
        
    def calculate_and_simulate(self):
        """Funktion die mit dem Button aufgerufen wird, um die Parameter zu berechnen und die Simulation zu starten"""
        params = self.calculate_parameters()
        if params is None:
            return
            
        # Ergebnisse anzeigen
        self.display_results(params)
        
        # Simulation durchführen
        time_points, height_points, velocity_points, mass_points = self.simulate_flight(params)
        
        # Grafiken aktualisieren / Plots zeichnen
        self.plot_results(time_points, height_points, velocity_points, params)
        
    def display_results(self, params):
        """Berechnete Ergebnisse anzeigen im Textfeld"""
        self.results_text.delete(1.0, tk.END)
        
        # Formatierte Ausgabe der Ergebnisse mit f-Strings
        results = f"""Rocket Parameters Calculation Results:
        
Exhaust Velocity: {params['exhaust_velocity']:.1f} m/s

Mass Distribution of this rocket:
- Dry Mass: {params['dry_mass']:,.0f} kg ({params['dry_mass_percent']:.1f}%)
- Payload Mass: {params['payload_mass']:,.0f} kg ({params['payload_percent']:.1f}%)
- Propellant Mass: {params['propellant_mass']:,.0f} kg ({params['propellant_percent']:.1f}%)
- Total Initial Mass: {params['total_initial_mass']:,.0f} kg
- Final Mass: {params['final_mass']:,.0f} kg

Performance Parameters:
- Delta-V: {params['delta_v']:,.0f} m/s ({params['delta_v']/1000:.2f} km/s)
- Mass Flow Rate: {params['mass_flow_rate']:.1f} kg/s
- Initial Thrust-to-Weight Ratio: {params['initial_twr']:.2f}
- Final Thrust-to-Weight Ratio: {params['final_twr']:.2f}
- Estimated Tank Volume: {params['tank_volume']:.1f} m³
"""
        
        self.results_text.insert(tk.END, results)
        
    def plot_results(self, time_points, height_points, velocity_points, params):
        """Funktion die mit matplotlib die Plots erstellt und anzeigt"""
        """Zeichnet die Ergebnisse der Simulation in zwei Plots: Höhe und Geschwindigkeit über der Zeit."""
        # falls die Plots schon existieren, werden sie gelöscht
        self.ax1.clear()
        self.ax2.clear()
        
        # Werte in ein NumPy-Array umwandeln für die Plots (wird so von matplotlib benötigt)
        time_arr = np.array(time_points)
        height_arr = np.array(height_points) / 1000  # in km umwandeln
        velocity_arr = np.array(velocity_points)
        
        # Plot 1: Höhe
        self.ax1.plot(time_arr, height_arr, 'b-', linewidth=2)
        self.ax1.axvline(x=params['burn_time'], color='r', linestyle='--',  # Vertikale Linie bei Brenndauer
                        label=f'Burn End ({params["burn_time"]:.0f}s)')
        self.ax1.set_xlabel('Time (s)')  # Beschriftung der x-Achse
        self.ax1.set_ylabel('Height (km)')  # Beschriftung der y-Achse
        self.ax1.set_title('Flight Height over Time')  # Titel des Plots
        self.ax1.grid(True, alpha=0.3)  # Gitterlinien im Hintergrund
        self.ax1.legend()  # Legende für den Plot
        
        # Maximalwerte der Höhe finden und markieren
        # Methode direkt aus der Dokumentation von Matplotlib übernommen
        max_height_idx = np.argmax(height_arr)
        max_height = height_arr[max_height_idx]
        max_height_time = time_arr[max_height_idx]
        self.ax1.plot(max_height_time, max_height, 'ro', markersize=8)
        self.ax1.annotate(f'Max Height: {max_height:.1f} km\nat t={max_height_time:.0f}s',
                         xy=(max_height_time, max_height),
                         xytext=(max_height_time + 20, max_height - 5),
                         arrowprops=dict(arrowstyle='->', color='red'))
        
        # Plot 2: Geschwindigkeit
        self.ax2.plot(time_arr, velocity_arr, 'g-', linewidth=2)
        self.ax2.axvline(x=params['burn_time'], color='r', linestyle='--',
                        label=f'Burn End ({params["burn_time"]:.0f}s)')
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Velocity (m/s)')
        self.ax2.set_title('Rocket Velocity over Time')
        self.ax2.grid(True, alpha=0.3)
        self.ax2.legend()
        
        # maximale Geschwindigkeit finden und markieren
        max_velocity_idx = np.argmax(velocity_arr)
        max_velocity = velocity_arr[max_velocity_idx]
        max_velocity_time = time_arr[max_velocity_idx]
        self.ax2.plot(max_velocity_time, max_velocity, 'ro', markersize=8)
        self.ax2.annotate(f'Max Velocity: {max_velocity:.0f} m/s\nat t={max_velocity_time:.0f}s',
                         xy=(max_velocity_time, max_velocity),
                         xytext=(max_velocity_time + 20, max_velocity - 100),
                         arrowprops=dict(arrowstyle='->', color='red'))
        
        # Grafiken aktualisieren
        self.fig.tight_layout()
        self.canvas.draw()

def main():
    """Hauptfunktion zum Starten der Anwendung"""
    root = tk.Tk()  # Tkinter-Hauptfenster erstellen
    app = RocketSimulator(root)  # Instanz der RocketSimulator-Klasse erstellen
    root.mainloop()  # Tkinter-Hauptschleife starten

if __name__ == "__main__":  # Wenn das Skript direkt ausgeführt wird, rufe die main-Funktion auf
    main()