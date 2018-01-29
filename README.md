	ZK-DATA für Linux und Windows
	
	FEATURES

Ein server pro aufgabe:
	- verwaltung des stocks
	- preisvorschläge
Diese arbeiten unabhänging

Clients können:
	- an jedem netwerk drucker ausdrucken (Zebra)
	- mit einem localen drucker arbeiten (Nur linux, Cups)
	- Auf Artikel informationnen zugreifen und ändern
	- Grafiken anzeigen des Verkaufts/Einkaufs
	- Neue Artikel erstellen
	- Preisvorschläge als vorlage nutzen für neue artikel

	- Bis zu 1 000 000 artikel einspeichern, die Suche dauert MAX 0.5s
	- Unendlich viele preisvorschläge nutzen, mit 600 000 getestet (startzeit des servers: ~10 sekunden)
	- Der Server speichert in eine locale MySQl datenbank
	- Möglichkeit einer Externen MySQL datenbank um einem WebServer zugriff auf unsensible daten zu geben
	- Bei jedem Start erstell der Stock Server die Inventur
	- Die Clients bekommen beim öffnen sofort die neuesten änderungen angezeigt

Sie benötigen :
	- Python3 und tkinter für die Clients
	- Python3 auf dem Server

	Für Extras:
		- Git damit die Clients automatisch aktualisieren
		- das python modul "pyperclip" um das Clipboard auf Artikel nummer zu untersuchen
		- das python modul "matplotlib" damit ein Client die grafiken anzeigen kann

![Alt text](DATA/Screenshots/0.png?raw=true "Search")
![Alt text](DATA/Screenshots/1.png?raw=true "Result")
![Alt text](DATA/Screenshots/2.png?raw=true "Change")
![Alt text](DATA/Screenshots/3.png?raw=true "Graph")
