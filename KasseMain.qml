import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 2.0//1.1


Rectangle {
    id: window
    width: parent.width
    height: parent.height

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
        x: window.width / 5 - width / 2
        y: window.height / 10
    }
    Label {
        id: labelTitle2
        text: "Barcode"
        font.pixelSize: window.height / 10 * 0.4
        x: window.width / 5 * 2 - width / 2
        y: window.height / 10
    }
    Label {
        id: labelTitle3
        text: "Name"
        font.pixelSize: window.height / 10 * 0.4
        x: window.width / 5 * 3 - width / 2
        y: window.height / 10
    }
    Label {
        id: labelTitle4
        text: "Preis"
        font.pixelSize: window.height / 10 * 0.4
        x: window.width / 5 * 4 - width / 2
        y: window.height / 10
    }

    ListView {
        id: liste
        y: window.height / 10 * 2
        focus: true
        highlightMoveDuration: 0
        highlight: Rectangle { color: "lightsteelblue"; width: window.width}
/*
        ScrollBar.vertical: ScrollBar {
            active: true;
            policy: ScrollBar.AlwaysOn
        }*/

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
                width: window.width; height: window.height/10
                MouseArea {
                    anchors.fill: parent
                    onClicked: liste.currentIndex = index
                }
                Keys.onReturnPressed: {
                    liste.currentIndex = index + 1
                    if (liste.currentIndex == liste.count) {
                        python.call('KasseMain.main.AddLinie', [], function() {});
                        python.call('KasseMain.main.GetLieferschein', [], function() {});
                    }
                }
                onActiveFocusChanged: {
                    //console.warn("Focus Changed")
                    //console.warn(liste.currentIndex)
                    textBarcode.forceActiveFocus()
                    textBarcode.selectAll()
                }
                Button {
                    id: buttonOption
                    text: "X"
                    y: parent.height / 2 - height / 2
                    onClicked: {
                        liste.currentIndex = itemListe.currentIndex;
                        python.call('KasseMain.main.LinieEntfernen', [liste.currentIndex], function() {});
                    }
                }
                TextField {
                    id: textAnzahl
                    font.pixelSize: parent.height * 0.3
                    width: window.width / 5
                    x: window.width / 5 - width / 2
                    y: parent.height / 2 - height / 2
                    text: anzahl
                    inputMethodHints: Qt.ImhDigitsOnly
                    horizontalAlignment: TextEdit.AlignHCenter

                    focus: false

                    onAccepted: {
                        deselect();
                        python.call('KasseMain.main.SetLieferschein', ["anzahl", liste.currentIndex, text], function() {});
                    }
                    onFocusChanged: {
                        if(focus) {
                            liste.currentIndex = itemListe.currentIndex;
                        }
                    }
                }
                TextField {
                    id: textBarcode
                    font.pixelSize: parent.height * 0.3
                    width: window.width / 5
                    x: window.width / 5 * 2 - width / 2
                    y: parent.height / 2 - height / 2
                    text: bcode
                    inputMethodHints: Qt.ImhDigitsOnly
                    horizontalAlignment: TextEdit.AlignHCenter

                    onAccepted: {
                        deselect();
                        python.call('KasseMain.main.SetLieferschein', ["bcode", liste.currentIndex, text], function() {});
                    }
                    onFocusChanged: {
                        if(focus) {
                            liste.currentIndex = itemListe.currentIndex;
                        }
                    }
                }
                TextField {
                    id: textName
                    font.pixelSize: parent.height * 0.3
                    width: window.width / 5
                    x: window.width / 5 * 3 - width / 2
                    y: parent.height / 2 - height / 2
                    text: name
                    horizontalAlignment: TextEdit.AlignHCenter

                    onAccepted: {
                        deselect();
                        python.call('KasseMain.main.SetLieferschein', ["name", liste.currentIndex, text], function() {});
                    }
                    onFocusChanged: {
                        if(focus) {
                            liste.currentIndex = itemListe.currentIndex;
                        }
                    }
                }
                TextField {
                    id: textPreis
                    font.pixelSize: parent.height * 0.3
                    width: window.width / 5
                    x: window.width / 5 * 4 - width / 2
                    y: parent.height / 2 - height / 2
                    text: preis
                    inputMethodHints: Qt.ImhDigitsOnly
                    horizontalAlignment: TextEdit.AlignHCenter
                    onAccepted: {
                        deselect();
                        python.call('KasseMain.main.SetLieferschein', ["preis", liste.currentIndex, text], function() {});
                    }
                    onFocusChanged: {
                        if(focus) {
                            liste.currentIndex = itemListe.currentIndex;
                        }
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
        x: window.width / 3 - width / 2
        y: window.height * 0.9

        onClicked: {
            python.call('KasseMain.main.Ok', [], function() {});
        }
    }

    CheckBox {
        id: checkBoxFinish
        x: window.width / 3 * 2 - width / 2
        y: window.height * 0.9
        height: window.height * 0.4
        text: "Fertig"
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
            importModule('KasseMain', function () {});

            setHandler("busy", busy);
            setHandler("antwortGetLieferschein", antwortGetLieferschein);

            call('KasseMain.main.GetLieferschein', [], function() {});
        }
    }
}
