import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.0

Rectangle {
    height: mainWindow.height
    width: mainWindow.width


    function antwortSearchLieferscheine(item) {
        console.warn("antwortSearchLieferscheine")
        //variable.listeIndex = liste.currentIndex
        //console.warn("Current Index: " + variable.listeIndex)
        contactModel.clear();
        for (var i=0; i<item.length; i++) {
            contactModel.append(item[i]);
        }
        //if (variable.listeIndex == -1) { variable.listeIndex = 0 }
        //liste.currentIndex = variable.listeIndex
        //labelTotal.text = summe
        //checkBoxFinish.checked = fertig
    }

    Label {
        id: labelLieferscheinSuchenTitle
        text: "Lieferscheine Suchen"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 2 - width / 2
    }

    Label {
        text: "Lieferscheinnummer"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 3 - width / 2
        y: mainWindow.height / 20
    }
    TextField {
        id: textLieferscheinSuchenIdentification
        text: ""
        width: mainWindow.width / 10
        x: mainWindow.width / 3 * 2 - width / 2
        y: mainWindow.height / 20
        onAccepted: {
            python.call("LieferscheinSuchen.main.GetLieferscheine", [textLieferscheinSuchenIdentification.text, textLieferscheinSuchenName.text, checkLieferscheinSuchenFertige.checked, checkLieferscheinSuchenEigene.checked], function() {});
        }
    }


    Label {
        text: "Kundenname"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 3 - width / 2
        y: mainWindow.height / 20 * 2
    }
    TextField {
        id: textLieferscheinSuchenName
        text: ""
        width: mainWindow.width / 10
        x: mainWindow.width / 3 * 2 - width / 2
        y: mainWindow.height / 20 * 2
        enabled: false
        onAccepted: {
            python.call("LieferscheinSuchen.main.GetLieferscheine", [textLieferscheinSuchenIdentification.text, textLieferscheinSuchenName.text, checkLieferscheinSuchenFertige.checked, checkLieferscheinSuchenEigene.checked], function() {});
        }
    }

    Label {
        text: "Auch fertige lieferscheine anzeigen"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 3 - width / 2
        y: mainWindow.height / 20 * 3
    }
    CheckBox {
        id: checkLieferscheinSuchenFertige
        x: mainWindow.width / 3 * 2 - width / 2
        y: mainWindow.height / 20 * 3
        onCheckedChanged: {
            python.call("LieferscheinSuchen.main.GetLieferscheine", [textLieferscheinSuchenIdentification.text, textLieferscheinSuchenName.text, checkLieferscheinSuchenFertige.checked, checkLieferscheinSuchenEigene.checked], function() {});
        }
    }

    Label {
        text: "Nur die eigenen lieferscheine anzeigen"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 3 - width / 2
        y: mainWindow.height / 20 * 4
    }
    CheckBox {
        id: checkLieferscheinSuchenEigene
        x: mainWindow.width / 3 * 2 - width / 2
        y: mainWindow.height / 20 * 4
        checked: true
        onCheckedChanged: {
            python.call("LieferscheinSuchen.main.GetLieferscheine", [textLieferscheinSuchenIdentification.text, textLieferscheinSuchenName.text, checkLieferscheinSuchenFertige.checked, checkLieferscheinSuchenEigene.checked], function() {});
        }
    }

    Button {
        id: buttonLieferscheinSuchenNeu
        text: "Neuer Lieferschein"
        x: mainWindow.width / 2 - width / 2
        y: mainWindow.height / 20 * 5
        onClicked: {
            python.call("LieferscheinSuchen.main.LastLieferschein", [""], function() {});
            view.push(frameLieferscheinAnzeigen)
        }
    }
    ListView {
        id: listLieferscheinSuchen
        y: mainWindow.height / 20 * 6
        height: (mainWindow.height / 20) * 14
        width: mainWindow.width

        ListModel {
            id: contactModel
        }
        Component {
            id: contactDelegate
            Item {
                id: itemListe
                width: listLieferscheinSuchen.width
                height: listLieferscheinSuchen.height / 12

                Label {
                    id: labelLieferscheinSucheListeEintrag
                    text: identification + ", Kunde: " + kunde_id + ", Preis: " + total + "€"
                    font.pixelSize: listLieferscheinSuchen.width / 30
                    x: listLieferscheinSuchen.width / 2 - width / 2
                    color: fertig ? "green" : "red"

                    MouseArea {
                        anchors.fill: labelLieferscheinSucheListeEintrag
                        onClicked: {
                            python.call("LieferscheinSuchen.main.LastLieferschein", [parent.text], function() {});
                            view.push(frameLieferscheinAnzeigen)
                        }
                    }
                }
            }
        }

        model: contactModel
        delegate: contactDelegate
    }


    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));
            importModule('LieferscheinSuchen', function () {});

            setHandler("antwortSearchLieferscheine", antwortSearchLieferscheine);
            setHandler("busy", busy);

            call("LieferscheinSuchen.main.GetLieferscheine", [textLieferscheinSuchenIdentification.text, textLieferscheinSuchenName.text, checkLieferscheinSuchenFertige.checked, checkLieferscheinSuchenEigene.checked], function() {});
        }
    }
}
