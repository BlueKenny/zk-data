import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1
//import QtQuick.Window 2.2
import QtMultimedia 5.5


Rectangle {
    id: window
    width: 800
    height: 800

    Item {
        id: variable
        property int listeIndex: 0
    }

    function antwortGetLieferschein(item) {
        console.warn("antwortGetLieferschein")
        variable.listeIndex = liste.currentIndex
        console.warn("Current Index: " + variable.listeIndex)
        contactModel.clear();
        for (var i=0; i<item.length; i++) {
            contactModel.append(item[i]);
        }
        if (variable.listeIndex == -1) { variable.listeIndex = 0 }
        liste.currentIndex = variable.listeIndex
    }

    Label {
        id: labelTitle1
        text: "Anzahl"
        font.pixelSize: window.height / 10 * 0.4
        x: window.width / 4 - width / 2
        y: window.height / 10
    }
    Label {
        id: labelTitle2
        text: "Barcode"
        font.pixelSize: window.height / 10 * 0.4
        x: window.width / 2 - width / 2
        y: window.height / 10
    }
    Label {
        id: labelTitle3
        text: "Name"
        font.pixelSize: window.height / 10 * 0.4
        x: window.width * 0.75 - width / 2
        y: window.height / 10
    }

    ListView {
        id: liste
        y: window.height / 10 * 2
        focus: true
        highlight: Rectangle { color: "lightsteelblue"; width: window.width }

        width: window.width
        height: window.height * 0.5

        ListModel {
            id: contactModel
        }

        Component {
            id: contactDelegate
            Item {
                width: window.width; height: window.height/10
                MouseArea {
                    anchors.fill: parent
                    onClicked: liste.currentIndex = index
                }
                Keys.onReturnPressed: {
                    liste.currentIndex = index + 1
                    console.warn("Enter")
                    if (liste.currentIndex == liste.count) {
                        python.call('Kasse.main.AddLinie', [], function() {});
                        python.call('Kasse.main.GetLieferschein', [], function() {});
                    }
                }
                onActiveFocusChanged: {
                    console.warn("Focus Changed")
                    console.warn(liste.currentIndex)
                    textBarcode.forceActiveFocus()
                    textBarcode.selectAll()
                }

                TextField {
                    id: textAnzahl
                    width: window.width / 5
                    x: window.width / 4 - width / 2
                    y: parent.height / 2 - height / 2
                    text: anzahl
                    focus: false

                    onAccepted: {
                        deselect();
                        python.call('Kasse.main.SetLieferschein', ["anzahl", liste.currentIndex, text], function() {});
                    }
                }
                TextField {
                    id: textBarcode
                    width: window.width / 5
                    x: window.width / 2 - width / 2
                    y: parent.height / 2 - height / 2
                    text: bcode

                    onAccepted: {
                        deselect();
                        python.call('Kasse.main.SetLieferschein', ["bcode", liste.currentIndex, text], function(neuerName) {textName.text = neuerName});
                    }
                }
                TextField {
                    id: textName
                    width: window.width / 5
                    x: window.width * 0.75 - width / 2
                    y: parent.height / 2 - height / 2
                    text: name

                    onAccepted: {
                        deselect();
                        python.call('Kasse.main.SetLieferschein', ["bcode", liste.currentIndex, text], function() {});
                    }
                }
            }
        }

        model: contactModel
        delegate: contactDelegate
    }

    Button {
        id: buttonOK
        text: "OK"
        width: window.width / 5
        x: window.width / 2 - width / 2
        y: window.height * 0.9
    }
/*
    Button {
        id: buttonAdd
        text: "Neue linie"
        width: parent.width / 5
        x: parent.width * 0.8 - width
        y: parent.height * 0.9
    }*/


    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));
            importModule('Kasse', function () {});

            setHandler("antwortGetLieferschein", antwortGetLieferschein);

            call('Kasse.main.GetLieferschein', [], function() {});
        }
    }
}
