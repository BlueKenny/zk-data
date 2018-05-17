import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.0

Rectangle {
    height: mainWindow.height
    width: mainWindow.width

    Button {
        height: mainWindow.height / 15
        width: mainWindow.width / 5
        text: "Hauptmenu"/*
        contentItem: Label {
            text: parent.text
            font.pixelSize: parent.width / 25
            verticalAlignment: Text.AlignVCenter
            //x: parent.width / 2 - width / 2
            anchors.fill: parent
        }*/
        onClicked: {
            view.push(frameSelect)
        }
    }

    Label {
        id: labelEinstellungenTitle
        text: "Einstellungen"
        font.pixelSize: vars.isPhone ? mainWindow.width / 20 : mainWindow.width / 50
        x: mainWindow.width / 2 - width / 2
    }

    Label {
        text: "Server"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 3 - width / 2
        y: mainWindow.height / 20
    }
    TextField {
        id: textEinstellungenServer
        text: vars.serverIP
        width: mainWindow.width / 10
        x: mainWindow.width / 3 * 2 - width / 2
        y: mainWindow.height / 20
        onAccepted: {
            python.call("Einstellungen.main.SetServer", [text], function() {});
        }
    }

    Label {
        text: "Drucker"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 3 - width / 2
        y: mainWindow.height / 20 * 2
    }
    TextField {
        id: textDruckerName
        text: vars.druckerIP
        width: mainWindow.width / 10
        x: mainWindow.width / 3 * 2 - width / 2
        y: mainWindow.height / 20 * 2
        onAccepted: {
            python.call("Einstellungen.main.SetDrucker", [text], function() {});
        }
    }

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('./'));
            importModule('Einstellungen', function () {});


            call("Einstellungen.main.GetServer", [], function(ipAdr) {vars.serverIP = ipAdr});
            call("Einstellungen.main.GetDrucker", [], function(ipAdr) {vars.druckerIP = ipAdr});

            //setHandler("antwortSearchKunden", antwortSearchKunden);
            //setHandler("busy", busy);

            //call("KundenSuchen.main.SearchKunden", [textKundenSuchenIdentification.text, textKundenSuchenName.text], function() {});
        }
    }
}
