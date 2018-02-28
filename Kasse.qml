import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1
//import QtQuick.Window 2.2
import QtMultimedia 5.5


Rectangle {
    id: window
    width: 500
    height: 500


    function antwortGetLieferschein(item) {
        //listModel.clear();
        for (var i=0; i<item.length; i++) {
            contactModel.append(item[i]);
        }
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
        y: 50
        focus: true
        highlight: Rectangle { color: "lightsteelblue"; width: window.width }

        width: 180; height: 200
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
                TextField {
                    id: textAnzahl
                    x: labelTitle1.x
                    text: anzahl
                    focus: false

                }
                TextField {
                    id: textBarcode
                    x: labelTitle2.x
                    text: bcode
                    Keys.onPressed: {
                        liste.currentIndex = index
                        console.warn("count: " + contactModel.count);
                       // console.warn(contactModel.get(currentItem).count)
                        console.warn(contactModel.get(1).name)
                    }
                }
                Text {
                    id: textName
                    text: name
                    x: labelTitle3.x
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

            call('Kasse.main.GetLieferschein', ["100200"], function() {});
        }
    }
}
