# Projektdokumentation: Raketen-Simulator

**Autor:** Sasha-Mercedes Fischer  
**Sprache:** Python 3.x  
**GUI Framework:** Tkinter mit ttkbootstrap  

## 1. Projektübersicht

Der Raketen-Simulator ist eine Python-Anwendung zur Berechnung und Simulation von Raketenflügen. Das Programm hat eine grafische Benutzeroberfläche zur Eingabe der Raketenparameter und stellt die Flugeigenschaften durch Diagramme dar.

### Wen spricht dieses Programm an?
Ähnliche Programme werden auch in der Raumfahrt verwendet, um Rakentestarts zu simulieren. Dieser Raketensimulator ist zwar nur sehr einfach, könnte aber für Hobby-Raketenbauer oder Raumfahrt-Interessierte nützlich sein.

### Hauptfunktionen 
- Eingabe der wichtigsten Raketenparameter (verwendeter Treibstoff, Schub, Spezifischer Impuls, Brenndauer, Trockenmasse, Nutzlast)
- Berechnung der restlichen benötigten Raketenparameter (Massefluss, Treibstoffmasse, Gesamtmasse)
- Simulation des Raketenflugs mit einem einfachen physikalischen Modell
- Visualisierung von Flughöhe und Geschwindigkeit
- Unterstützung verschiedener Treibstofftypen
- Benutzerfreundliche grafische Oberfläche

## 2. Technische Spezifikationen

### Systemanforderungen
- **Programmiersprache:** Python
- **Python Version:** 3.6 oder höher

### Benötigte Libraries
Die physikalischen Berechnungen und das grafische Interface wurden mit Hilfe einiger Libraries umgesetzt. Diese müssen vor dem Start des Programms installiert werden.
```python
import tkinter as tk             # Standard GUI-Bibliothek
import ttkbootstrap as ttk       # Erweiterte GUI-Komponenten
import matplotlib.pyplot as plt  # Plotting und Visualisierung
import numpy as np               # Numerische Berechnungen
import math                      # Mathematische Funktionen
```

## Programmaufbau

### Objektorierntierter Aufbau

Ich habe mich bei diesem Programm für eine objektorientierte Herangehensweise entschieden. Das macht den Code übersichtlicher und besser strukturiert. Außerdem ist er so auch einfacher später zu erweitern.

**Objektorientiert:** Arbeiten mit Klassen statt nur mit Funnktionen.

Wichtigster Programmteil ist die Hauptklasse, die alle Funktionen beinhaltet:

```python
class RocketSimulator
```
In der Klasse ```RocketSimulator```gibt es mehrere Funktionen (Die nennt man hier **Methoden**).

Die erste Methode ist immer ```__init__```. Diese Methode nennt man auch den *Constructor*.
```python
def __init__(self, root):
```
Diese Methode wird immer dann ausgeführt, wenn eine neue **Instanz** der Klasse Rocket Simulator erzeugt wird. **Methoden** haben (im Vergleich zu normalen Funktionen) bei den Parametern eine Besonderheit: Als erster Parameter wird immer ```self``` übergeben. Diese Variable enthält die **Instanz** des Objektes. Das funktioniert ganz automatisch.

In der Funktion ```__init__``` wird ein weiterer Parameter übergeben: ```root```. Dabei handelt es sich um das Tkinter Objekt, das in der ersten Zeile der ```__init__```-Funktion mit der Instanz verbunden wird ( ```self.root = root``` ). Dadurch können alle Parameter der Benutzeroberfläche als Variablen der Instanz bearbeitet werden und müssen nicht mühsam von Funktion zu Funktion weitergegeben werden. Als letztes startet ```__init__``` die grafische Benutzeroberfläche mit der Funktion ```setup_gui()```.

### Einrichten der GUI

Die Funktion ```setup_gui()``` definiert nacheinander die GUI-Elemente des Programms. Ich beginne mit einem Hauptrahmen (ttk.Frame), in den ich anschließend einen oberen und einen unteren Rahmen einfüge. Dadurch teile ich die Benutzeroberfläche in einen oberen und unteren Teil auf. Anschließend wird im oberen Rahmen noch eine linke und rechte Spalte (wieder als Frame) eingefügt. Dmait ist das generelle Layout der Oberfläche festgelegt.

Hier eine Darstellung der Hierarchie meiner Frames:
```
main_frame -> top_frame (oben)     -> input_frame (links)
                                   -> results_frame (rechts)
           -> plots_frame (unten)
```               
Die restliche Benutzeroberfläche baue ich aus Labels (für statischen Text), Entries (für Eingabenfelder) und Buttons auf. Dabei verwende ich die ```.grid``` methode von tkinter, um ein einfaches Layout ohne zusätzliche Frames zu erzeugen.

zum Schluss werden noch die Grafiken im unteren tkinter-Frame vorbereitet (wie das funktioniert, habe ich aus einem Tutorial der matplotlib-Dokumnetation https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html ).

### Weitere wichtige Methoden

#### ```calculate_parameters(self)```
Berechnet alle relevanten Raketenparameter basierend auf Benutzereingaben.

#### ```simulate_flight(self, params)```
Führt die numerische Simulation des Raketenflugs durch. Numerisch bedeutet hier, dass ich das schrittweite berechne - also immer für die nächsten 0.1 Sekunden. Das ist nicht ganz so präzise, wie eine direkte Berechnung über eine Funktion, dafür kann man so deutlich kompliziertere Berechnungen näherungsweise berechnen, ohne komplizierte Mathematik verwenden zu müssen.

Anzumerken ist auch, dass alle Raketenparameter gesammelt in einem Dictionary im Parameter ```params``` übergeben werden. Das macht den Code übersichtlicher.

#### ```plot_results(self, time_points, height_points, velocity_points, params)```
Erstellt die Visualisierungen der Simulationsergebnisse. Dafür verwende ich die library matplotlib. Damit die berechneten Werte einfach dargestellt werden können, müssen die Listen mit den berechneten Werten erst in ein numpy-Array umgewandelt werden (passiert ganz am Anfang der Methode).

Die Diagramme werden dann mit ```plot``` erstellt: Hier werden die x-Werte (time_arr) und die y-Werte (hight_arr bzw. velocity_arr) wie in einem Koordinatensystem eingezeichnet. Der Rest der Methode dient nur dafür, dass die Grafiken etwas hübscher aussehen. 

Die letzte Zeile ```self.canvas.draw()``` sorgt dafür, dass die Grafiken dargestellt werden.

## Mathamatische Grundlagen

Zur Berechnung der Raketenflüge verwende ich die sogenannten **Rocket-Equation** bzw. ihre Teilschritte. 

![image](https://github.com/user-attachments/assets/fea21a9e-bc46-4db6-94af-77fbff286171)


Berechnet werden folgende Parameter über ihre jeweiligen Gleichungen
**Ausstoßgeschwindigkeit (ve):** `ve = Isp × g₀`
- **Massenstromrate:** `ṁ = F / ve`
- **Treibstoffmasse:** `mp = ṁ × tb`

### 5.2 Massenverteilung
- Trockenmasse (Struktur)
- Nutzlastmasse 
- Treibstoffmasse
- Gesamtstartmasse
- Prozentuale Verteilung

### 5.3 Leistungsparameter
- **Delta-V (Tsiolkovsky-Gleichung):** `Δv = ve × ln(m₀/mf)`
- **Schub-zu-Gewicht-Verhältnis:** `TWR = F/(m × g₀)`
- **Tankvolumen:** `V = mp/ρ`

## 6. Physikalische Modelle

### 6.1 Flug-Simulation
Die Simulation berücksichtigt folgende physikalische Effekte:

#### Phase 1: Antriebsphase (0 ≤ t ≤ Brenndauer)
- **Schubkraft:** Konstant basierend auf Eingabeparametern
- **Gewichtskraft:** `Fg = m × g₀`
- **Luftwiderstand:** `Fd = ½ × ρ × cd × A × v²`
- **Luftdichte:** Exponentieller Abfall mit der Höhe

#### Phase 2: Freier Fall (t > Brenndauer)
- Nur Gewichtskraft und Luftwiderstand
- Keine Schubkraft mehr vorhanden

### 6.2 Vereinfachungen
- Konstante Erdbeschleunigung (9,81 m/s²)
- Vereinfachtes Luftwiderstandsmodell
- Konstante Querschnittsfläche
- Eindimensionale Bewegung (nur vertikal)

### 6.3 Numerische Integration
- **Zeitschritt:** dt = 0.1 s
- **Methode:** Euler-Verfahren
- **Abbruchbedingungen:** 
  - Rakete erreicht Boden (h ≤ 0)
  - Maximale Simulationszeit überschritten

## 7. GUI-Komponenten

### 7.1 Eingabebereich
- **Treibstofftyp:** Dropdown-Menü mit automatischer Isp-Aktualisierung
- **Schub:** Eingabe in kN
- **Spezifischer Impuls:** Eingabe in Sekunden
- **Brenndauer:** Eingabe in Sekunden
- **Trockenmasse:** Eingabe in kg
- **Nutzlastmasse:** Eingabe in kg

### 7.2 Ergebnisanzeige
Scrollbares Textfeld mit formatierter Ausgabe:
- Ausstoßgeschwindigkeit
- Detaillierte Massenverteilung
- Leistungsparameter
- Geschätzte Tankgröße

### 7.3 Visualisierung
Zwei nebeneinanderliegende Diagramme:
- **Links:** Flughöhe über Zeit (km vs. s)
- **Rechts:** Geschwindigkeit über Zeit (m/s vs. s)

Beide Diagramme zeigen:
- Markierung des Brennschluss-Zeitpunkts
- Hervorhebung der Maximalwerte
- Gitterlinien für bessere Lesbarkeit

## 8. Beispielrechnung

### 8.1 Standardkonfiguration
- **Treibstoff:** Kerosene/LOX
- **Schub:** 7.500 kN
- **Spezifischer Impuls:** 340 s
- **Brenndauer:** 150 s
- **Trockenmasse:** 22.200 kg
- **Nutzlast:** 22.800 kg

### 8.2 Typische Ergebnisse
- **Treibstoffmasse:** ~345.000 kg
- **Delta-V:** ~8.000-9.000 m/s
- **Maximale Höhe:** 150-200 km
- **Maximale Geschwindigkeit:** 2.500-3.000 m/s

## 9. Mögliche Erweiterungen

### 9.1 Physikalische Verbesserungen
- Mehrstufige Raketen
- Variable Erdbeschleunigung
- Erdrotation berücksichtigen
- Orbitalemechanik für Satellitenbahnen
- Genaueres Atmosphärenmodell

### 9.2 GUI-Erweiterungen
- 3D-Flugbahnvisualisierung
- Animierte Simulation
- Export-Funktionen für Daten
- Vergleich verschiedener Konfigurationen
- Kostenschätzung

### 9.3 Technische Verbesserungen
- Konfigurationsdateien für Treibstoffe
- Datenbankanbindung für Raketendaten
- Web-basierte Version
- Genauere numerische Verfahren

## 10. Bekannte Limitationen

### 10.1 Physikalische Vereinfachungen
- Eindimensionale Bewegung (nur vertikal)
- Konstante Atmosphäreneigenschaften
- Vereinfachter Luftwiderstand
- Keine Berücksichtigung von Windeinflüssen

### 10.2 Technische Limitationen
- Euler-Verfahren ist für große Zeitschritte ungenau
- Keine Validierung gegen reale Flugdaten
- Luftwiderstandskoeffizient ist geschätzt
- Keine Berücksichtigung von Strukturbelastungen

## 11. Validierung und Tests

### 11.1 Plausibilitätsprüfung
- Delta-V-Werte entsprechen typischen Orbital-Raketen
- Flughöhen sind realistisch für die gegebenen Parameter
- Massenverteilung entspricht modernen Raketen

### 11.2 Vergleich mit Referenzdaten
Das Programm sollte gegen bekannte Raketendaten validiert werden:
- Saturn V
- Falcon 9
- Atlas V

## 12. Fazit

Der Raketen-Simulator bietet eine solide Grundlage für die Berechnung und Simulation von Raketenflügen. Trotz der vereinfachten physikalischen Modelle liefert er realistische Ergebnisse für erste Abschätzungen und Bildungszwecke.

Die modulare Struktur ermöglicht einfache Erweiterungen, und die benutzerfreundliche GUI macht das Programm auch für Laien zugänglich. Für professionelle Anwendungen sollten jedoch genauere physikalische Modelle und Validierungen implementiert werden.

### 12.1 Stärken
- Einfache Bedienung durch intuitive GUI
- Solide Grundlagen der Raketenphysik
- Gute Visualisierung der Ergebnisse
- Erweiterbare Architektur

### 12.2 Verbesserungspotential
- Genauere physikalische Modelle
- Mehrstufige Raketen
- Validierung gegen reale Daten
- Performance-Optimierung für große Simulationen

---

**Version:** 1.0  
**Letzte Aktualisierung:** Juni 2025  
**Status:** Funktionsfähig, bereit für Erweiterungen
