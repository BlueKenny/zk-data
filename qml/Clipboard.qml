import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.0
import QtQuick.Window 2.2


Window {
    id: window
    title: qsTr("ZK-Data Clipboard")
    x: 0
    y: 0
    width: 500
    height: 500

    Item {
        id: variable
        property int listeIndex: 0
        property bool switchFinishChecked: false
    }

    function antwortClipboard(item) {
        contactModel.clear();
        for (var i=0; i<item.length; i++) {
            contactModel.append(item[i]);
            if (checkboxAutoForeground.checked == true) {
                flags = Qt.WindowStaysOnTopHint
            }
        }
    }

    function busy(status) {
        busyindicator.visible = status
    }

    Timer {
        id: timerClipboard
        interval: 1000; running: true; repeat: true
        onTriggered: {
            console.warn("timerClipboard")
            python.call('Clipboard.main.checkClipboard', [], function () {});
        }
    }

    CheckBox {
        id: checkboxAutoForeground
        text: "Automatisch in den vordergrund"
        onCheckedChanged: {
            //if (checked == true) {flags = Qt.WindowStaysOnTopHint}
            if (checked == false) {flags = Qt.Window}
        }
    }

    ListView {
        id: liste
        y: window.height / 10 * 2
        focus: true
        highlightMoveDuration: 0
        highlight: Rectangle { color: "lightsteelblue"; width: window.width}

        width: window.width
        height: window.height * 0.5

        ListModel {
            id: contactModel
        }

        Component {
            id: contactDelegate
            Item {
                id: itemListe
                property int currentIndex: index // store item index
                width: window.width
                height: window.height/10
                Label {
                    id: labelAnzahl
                    text: anzahl + "x"
                    x: window.width / 6 * 1 - width / 2
                    width: window.width / 6
                    y: parent.height / 2 - height / 2
                }
                Label {
                    id: labelName
                    text: name_de
                    x: window.width / 6 * 2 - width / 2
                    width: window.width / 6
                    y: parent.height / 2 - height / 2
                }
                Label {
                    id: labelLieferant
                    text: lieferant
                    x: window.width / 6 * 3 - width / 2
                    width: window.width / 6
                    y: parent.height / 2 - height / 2
                }
                Label {
                    id: labelOrt
                    text: ort
                    x: window.width / 6 * 4 - width / 2
                    width: window.width / 6
                    y: parent.height / 2 - height / 2
                }
                Label {
                    id: labelPreis
                    text: preisvk + "€"
                    x: window.width / 6 * 5 - width / 2
                    width: window.width / 6
                    y: parent.height / 2 - height / 2
                }
            }
        }

        model: contactModel
        delegate: contactDelegate
    }

    BusyIndicator {
        id: busyindicator
        running: true //image.status === Image.Loadings
        x: window.width / 2 - width / 2
        y: window.height / 2 - height / 2
    }

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));
            importModule('Clipboard', function () {});

            setHandler("busy", busy);
            setHandler("antwortClipboard", antwortClipboard);

            //call('LieferscheinAnzeigen.main.GetLieferschein', [], function() {});
            //call('LieferscheinAnzeigen.main.GetIdentification', [], function(lieferscheinNummer) {labelLieferscheinAnzeigenTitle.text = "Lieferschein: " + lieferscheinNummer});
        }
    }
}
