import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1
//import QtQuick.Window 2.2
import QtMultimedia 5.5


Rectangle {
    id: window
    width: 500
    height: 500

    Item {
        id: variable
        property int listeIndex: 0
    }

    function antwortGetLieferschein(item) {
        variable.listeIndex = liste.currentIndex
        contactModel.clear();
        for (var i=0; i<item.length; i++) {
            contactModel.append(item[i]);
        }
        liste.currentIndex = variable.listeIndex
    }

    Label {
        id: labelTitle1
        x: parent.width / 10
        text: "Anzahl"
    }
    Label {
        id: labelTitle2
        x: parent.width / 10 * 4
        text: "Barcode / Identification"
    }
    Label {
        id: labelTitle3
        x: parent.width / 10 * 8
        text: "Name"
    }

    ListView {
        id: liste
        y: 80
        focus: true
        highlight: Rectangle { color: "lightsteelblue"; width: window.width }

        width: window.width; height: window.height * 0.8

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
                    python.call('Kasse.main.AddLinie', [], function() {});
                    python.call('Kasse.main.GetLieferschein', [], function() {});

                }
                onActiveFocusChanged: {
                    console.warn(liste.currentIndex)
                    textBarcode.forceActiveFocus()
                    textBarcode.selectAll()
                }

                TextField {
                    id: textAnzahl
                    x: labelTitle1.x
                    text: anzahl
                    focus: false

                    onAccepted: {
                        deselect()
                    }
                }
                TextField {
                    id: textBarcode
                    x: labelTitle2.x
                    text: bcode

                    onAccepted: {
                        deselect()
                    }
                }
                TextField {
                    id: textName
                    text: name
                    x: labelTitle3.x

                    onAccepted: {
                        deselect()
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
        width: parent.width / 5
        x: parent.width * 0.4 - width
        y: parent.height * 0.9
    }

    Button {
        id: buttonAdd
        text: "Neue linie"
        width: parent.width / 5
        x: parent.width * 0.8 - width
        y: parent.height * 0.9
    }


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
