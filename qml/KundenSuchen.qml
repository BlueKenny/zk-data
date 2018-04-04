import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.0

Rectangle {
    height: mainWindow.height
    width: mainWindow.width


    function antwortSearchKunden(item) {
        contactModel.clear();
        for (var i=0; i<item.length; i++) {
            contactModel.append(item[i]);
        }
    }


    Button {
        text: "Hauptmenu"
        height: mainWindow.height / 15
        width: mainWindow.width / 5
        onClicked: {
            view.push(frameSelect)
        }
    }

    Label {
        id: labelKundenSuchenTitle
        text: "Kunden Suchen"
        font.pixelSize: vars.isPhone ? mainWindow.width / 20 : mainWindow.width / 50
        x: mainWindow.width / 2 - width / 2
    }

    Label {
        text: "Identification"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 3 - width / 2
        y: mainWindow.height / 20
    }
    TextField {
        id: textKundenSuchenIdentification
        text: vars.kundenSuchenTextIdentification
        width: mainWindow.width / 10
        x: mainWindow.width / 3 * 2 - width / 2
        y: mainWindow.height / 20
        onAccepted: {
            vars.kundenSuchenTextIdentification = text
            python.call("KundenSuchen.main.SearchKunden", [textKundenSuchenIdentification.text, textKundenSuchenName.text], function() {});
        }
    }

    Label {
        text: "Name"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 3 - width / 2
        y: mainWindow.height / 20 * 2
    }
    TextField {
        id: textKundenSuchenName
        text: vars.kundenSuchenTextName
        width: mainWindow.width / 10
        x: mainWindow.width / 3 * 2 - width / 2
        y: mainWindow.height / 20 * 2
        onAccepted: {
            vars.kundenSuchenTextName = text
            python.call("KundenSuchen.main.SearchKunden", [textKundenSuchenIdentification.text, textKundenSuchenName.text], function() {});
        }
    }

    Button {
        id: buttonKundenSuchenNeu
        text: "Neuer Kunde"
        x: mainWindow.width / 2 - width / 2
        y: mainWindow.height / 20 * 5
        height: mainWindow.height / 15
        width: mainWindow.width / 5

        onClicked: {
            //python.call("LieferscheinSuchen.main.LastLieferschein", [""], function() {});
            //view.push(frameLieferscheinAnzeigen)
        }
    }
    ListView {
        id: listKundenSuchen
        y: mainWindow.height / 20 * 7
        height: (mainWindow.height / 20) * 14
        width: mainWindow.width

        ListModel {
            id: contactModel
        }
        Component {
            id: contactDelegate
            Item {
                id: itemListe
                width: listKundenSuchen.width
                height: vars.isPhone ? listKundenSuchen.height / 8 : listKundenSuchen.height / 12

                Label {
                    id: labelKundenSucheListeEintrag
                    text: identification + ", Name: " + name
                    font.pixelSize: vars.isPhone ? listKundenSuchen.width / 15 : listKundenSuchen.width / 40
                    x: listKundenSuchen.width / 2 - width / 2
                    //color: fertig ? "blue" : "red"

                    MouseArea {
                        anchors.fill: labelKundenSucheListeEintrag
                        onClicked: {
                            if (vars.kundenSuchenVorherigeAnsicht == "frameLieferscheinSuchen") {
                                vars.kundenSuchenVorherigeAnsicht = ""
                                vars.lieferscheinSuchenTextName = identification
                                view.push(frameLieferscheinSuchen)
                            }
                            if (vars.kundenSuchenVorherigeAnsicht == "frameLieferscheinAnzeigen") {
                                vars.kundenSuchenVorherigeAnsicht = ""
                                vars.lieferscheinAnzeigenKundeID = identification
                                view.push(frameLieferscheinAnzeigen)
                            }

                            //python.call("LieferscheinSuchen.main.LastLieferschein", [parent.text], function() {});
                            //view.push(frameLieferscheinAnzeigen)
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
            addImportPath(Qt.resolvedUrl('./'));
            importModule('KundenSuchen', function () {});

            setHandler("antwortSearchKunden", antwortSearchKunden);
            setHandler("busy", busy);

            call("KundenSuchen.main.SearchKunden", [textKundenSuchenIdentification.text, textKundenSuchenName.text], function() {});
        }
    }
}
