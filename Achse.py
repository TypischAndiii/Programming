import NemAll_Python_Geometry as Geometry
import NemAll_Python_BasisElements as BasisElements
import NemAll_Python_BaseElements as BaseElements


def check_allplan_version(build_ele, version):
    """Überprüft, ob die Allplan-Version kompatibel ist."""
    return version >= 2025.0


def benutzer_eingabe():
    """
    Ermöglicht dem Benutzer, eine 2D-Polylinie im Modell auszuwählen und anschließend Abstand und Anzahl der Lotlinien festzulegen.

    Rückgabe:
        tuple: Die Liste der ausgewählten 2D-Polylinienobjekte, Abstand und Anzahl der Lotlinien.
    """
    object_input = BaseElements.ObjectInput()
    object_input.SetInputObjectFilter(["Polyline2D"])  # Nur 2D-Polylinien
    result = object_input.GetInput("Bitte wählen Sie eine 2D-Polylinie aus:")

    if not result.Success():
        print("Keine gültige 2D-Polylinie ausgewählt.")
        return None, None, None

    polyline = result.GetResultObjects()[0]  # Wir nehmen die erste Polylinie
    abstand = float(input("Bitte geben Sie den Abstand für die Lotlinien ein: "))
    anzahl_lotlinien = int(input("Bitte geben Sie die Anzahl der Lotlinien ein: "))
    
    return polyline, abstand, anzahl_lotlinien


def erstelle_lotlinie(polyline, abstand, anzahl_lotlinien, länge_lotlinie):
    """
    Erstellt mehrere Lotlinien an verschiedenen Punkten der Polylinie.

    Argumente:
        polyline (Geometry.Polyline2D): Die Eingabe-2D-Polylinie.
        abstand (float): Der Abstand für jede Lotlinie.
        anzahl_lotlinien (int): Anzahl der Lotlinien, die entlang der Polylinie erstellt werden sollen.
        länge_lotlinie (float): Die Länge jeder senkrechten Lotlinie.

    Rückgabe:
        list: Eine Liste der Lotlinien und deren Endpunkte.
    """
    lotlinien = []

    # Die Polylinie in Segmente unterteilen
    for i in range(anzahl_lotlinien):
        t = i / (anzahl_lotlinien - 1)  # Interpolationswert
        punkt = polyline.GetPointAt(t)  # Punkt auf der Polylinie an Position t
        erstes_segment = polyline.GetSegment(int(t * (len(polyline.GetSegments()) - 1)))
        
        richtung = Geometry.Vector2D(
            erstes_segment.X2 - erstes_segment.X1,
            erstes_segment.Y2 - erstes_segment.Y1
        )
        normal = Geometry.Vector2D(-richtung.Y, richtung.X).Normalized()
        
        # Berechnung des Endpunkts basierend auf der Längenangabe
        endpunkt = Geometry.Point2D(
            punkt.X + länge_lotlinie * normal.X,
            punkt.Y + länge_lotlinie * normal.Y
        )
        
        lotlinie = Geometry.Line2D(punkt, endpunkt)
        lotlinien.append((lotlinie, endpunkt))
        
    return lotlinien


def platziere_punkt(doc, punkt):
    """
    Platziert einen Punkt an einem definierten Punkt.

    Argumente:
        doc: Das Allplan-Dokument.
        punkt (Geometry.Point2D): Der Punkt, an dem der Punkt platziert wird.

    Rückgabe:
        BaseElements.ModelElement3D: Das Modell des Punktes.
    """
    punkt_element = Geometry.Point2D(punkt.X, punkt.Y)
    return BaseElements.ModelElement3D(doc, punkt_element)


def erstelle_element(build_ele, doc):
    """
    Verarbeitet eine 2D-Polylinie, erstellt mehrere Lotlinien und platziert Punkte.

    Argumente:
        build_ele: Das Bauelement-Objekt mit benutzerdefinierten Parametern.
        doc: Das Allplan-Dokument.

    Rückgabe:
        list: Eine Liste der erstellten Modellelemente.
    """
    polyline, abstand, anzahl_lotlinien = benutzer_eingabe()
    if not polyline:
        return []

    länge_lotlinie = float(input("Bitte geben Sie die Länge der Lotlinien ein: "))

    lotlinien_daten = erstelle_lotlinie(polyline, abstand, anzahl_lotlinien, länge_lotlinie)
    
    linien_elemente = []
    punkt_elemente = []
    
    for lotlinie, endpunkt in lotlinien_daten:
        linien_elemente.append(BaseElements.ModelElement3D(doc, lotlinie))
        punkt_elemente.append(platziere_punkt(doc, endpunkt))
    
    return linien_elemente + punkt_elemente
