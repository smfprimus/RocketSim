# Projektdokumentation: Raketen-Simulator

**Autor:** Sasha-Mercedes Fischer  
**Sprache:** Python 3.x  
**GUI Framework:** Tkinter mit ttkbootstrap  

## Projektübersicht

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

## Technische Spezifikationen

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

Zur Berechnung der Raketenflüge verwende ich die sogenannten **Rocket-Equation** bzw. ihre Teilschritte. Die Mathematischen Grundlagen wurden großteils vom **Beginners Guide to Aeronautics** übernommen (https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/) 

![image](https://github.com/user-attachments/assets/fea21a9e-bc46-4db6-94af-77fbff286171)

Δv ist die Geschwindigkeitsänderung der Rakete, ve ist die Geschwindigkeit der ausgestoßenen Gase (also die Geschwindigkeit, mit der die verbrannte Treibstoffmasse hinten an der Raketendüse hinausgeschossen wird), m0 ist die Anfangsmasse der Rakete, mf ist die Masse des Treibstoffs.

Berechnet werden folgende Parameter über ihre jeweiligen Gleichungen
- **Ausstoßgeschwindigkeit (ve):** `ve = Isp × g₀`
- **Massenstromrate:** `ṁ = F / ve` (Massenstromrate oder Massefluss: Wieviel kg fließen pro Sekunde durch das Triebwerk der Rakete)
- **Treibstoffmasse:** `mp = ṁ × tb` 

Berechnete Leistungsparameter (die geben einen guten Überblick über die allgemeine Leistungsfähigkeit einer Rakete)
- **Delta-V (Tsiolkovsky-Gleichung):** `Δv = ve × ln(m₀/mf)`
- **Schub-zu-Gewicht-Verhältnis:** `TWR = F/(m × g₀)`
- **Tankvolumen:** `V = mp/ρ`

## Physikalisches Modell

Das Raketenflug wird über eine sehr einfaches Modell berechnet, das die Schwerkraft und eine grobe Schätzung des Luftwiderstandes beinhaltet. Die Simulation erfolgt in zwei Phasen:

#### Phase 1: Antriebsphase (0 ≤ t ≤ Brenndauer)
- **Schubkraft:** Konstant basierend auf Eingabeparametern
- **Gewichtskraft:** `Fg = m × g₀`
- **Luftwiderstand:** `Fd = ½ × ρ × cd × A × v²`
- **Luftdichte:** Exponentieller Abfall mit der Höhe

#### Phase 2: Freier Fall (t > Brenndauer)
- Nur Gewichtskraft und Luftwiderstand
- Keine Schubkraft mehr vorhanden

### Vereinfachungen
- Die Erdbeschleunigung wird als konstant angenommen (9,81 m/s²). In Wirklichkeit würde sie mit zunehmender Höhe der Rakete geringer werden. 
- Vereinfachtes Luftwiderstandsmodell
- Der Flug wird nur als vertikaler Flug berechnet, nicht als Kurve oder Orbitalmaneuver. (Streng genommen wird die erste nicht einmal als Kugel simuliert, sondern als flache Ebene)

### Numerische Berechnung
Die Simulation wird in kleinen Zeitabschnitten von 0.1s berechnet. Dazu verwende ich das sogenannte Euler-Verfahren. Ich berechne die aktuelle Beschleunigung, indem ich die aktuelle Kraft aus Gewicht und Luftwiderstand durch die aktuelle Masse der Rakete teile. Anschließend addiere ich die Beschleunigung (multipliziert mit der kleinen Zeiteinheit von 0.1s) zur aktuellen Geschwindigkeit. Die Höhe berechne ich auf dieselbe Art, indem ich die Geschwindigkeit (multipliziert mit der kleinen Zeiteinheit von 0.1s) zur Höhe addiere.

Hier findet eine Näherung statt: Ich tue so, als ob in den 0.1s die Bewegung geradlinig verlaufen würde und sich die Geschwindigkeit nicht ändern würde. Das ist in Wirklichkeit natürlich anders. 

**Abbruchbedingungen:** 
  - Rakete erreicht Boden (h ≤ 0)
  - Maximale Simulationszeit überschritten

## Mögliche Erweiterungen

### Physikalische Verbesserungen
- Mehrstufige Raketen
- Realistische Erdbeschleunigung und Raketenstart von anderen Planeten aus
- Erdrotation berücksichtigen
- Orbitalemechanik für Satellitenbahnen
- Genaueres Atmosphärenmodell

### GUI-Erweiterungen
- Flugbahnvisualisierung
- Animierte Simulation

---

**Version:** 1.0  
**Letzte Aktualisierung:** Juni 2025  
**Status:** Funktionsfähig, bereit für Erweiterungen
