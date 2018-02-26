import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1
//import QtQuick.Window 2.2
import QtMultimedia 5.5

// Fedora
//dnf install pyotherside
//dnf install qt5-qtquickcontrols
//dnf install qt5-qtquickcontrols2
//dnf install qt5-qtmultimedia

// Ubuntu Touch
// qml-module-qtquick2
// qml-module-qtmultimedia
// qml-module-qtquick-controls
// pyotherside
// git
// python3-pip
//zbbar-tools


Rectangle {
    id: window
    width: 500
    height: 500

    StackView {
        id: frames
        anchors.fill: parent

        initialItem: frameSuche

        Item {
            id: variable
            property string infoID: ""
        }

        Component {
            id: frameSuche

            Rectangle {
                id: frame

                function open(ID) {
                    variable.infoID = ID
                    frames.push(frameInfo);
                }

                function busy(status) {
                    busyindicator.visible = status
                }

                function ifPhone(bool) {
                    frame.state = "Handy"
                }

                function antwortSearchArt(item) {
                    listModel.clear();
                    for (var i=0; i<item.length; i++) {
                        listModel.append(item[i]);
                    }
                }


                states: [
                    State {
                        name: "Handy"

                        PropertyChanges {target:videoOutput; width: frame.width}
                        PropertyChanges {target:videoOutput; height: frame.height/3}

                        PropertyChanges {target:ti; y:videoOutput.height*1.1}
                        PropertyChanges {target:ti; height:frame.height/15}
                        PropertyChanges {target:ti; width:frame.width*0.7}
                        PropertyChanges {target:ti; font.pixelSize: ti.height*0.4}

                        PropertyChanges {target:busyindicator; height: frame.height*0.2}
                        PropertyChanges {target:busyindicator; width: frame.width*0.2}
                        PropertyChanges {target:busyindicator; x: frame.width/2 - busyindicator.width/2}
                        PropertyChanges {target:busyindicator; y: frame.height/2 - busyindicator.height/2}

                        PropertyChanges {target:columnIdentification; width: frame.width/3}
                        PropertyChanges {target:columnArtikel; width: frame.width/3}
                        PropertyChanges {target:columnLieferant; width: frame.width/3}

                        PropertyChanges {target:row; height: liste.height/5}
                        PropertyChanges {target:row; font.pixelSize: height*0.8}



                    },
                    State {
                        name: "Desktop"
                        //PropertyChanges {target:top1; color:"yellow"}
                    }
                ]

                Camera {
                    id: camera
                    //flash.mode: Camera.FlashOn
                    //captureMode: Camera.CaptureStillImage
                    //imageCapture.resolution: "640x480"
                    focus {
                        focusMode: Camera.FocusContinuous //FocusManual //FocusMacro
                        //focusPointMode: Camera.FocusPointAuto //FocusPointCenter
                    }

                    imageCapture {
                        onImageCaptured: {
                            // Show the preview in an Image
                            photoPreview.source = preview
                        }
                    }
                }

                VideoOutput {
                    id: videoOutput
                    source: camera
                    focus : visible // to receive focus and capture key events when visible
                    //anchors.fill: parent
                    width: 100
                    height: 100

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            camera.searchAndLock()
                            camera.imageCapture.captureToLocation("/home/phablet/Pictures/scan.jpg");
                            python.call('Stock.main.ScanForSearch', [], function() {});
                        }
                    }
                }

                Image {
                    id: photoPreview
                    visible: false
                }

                TextField {
                    id: ti

                    x: frame.width/2 - ti.width/2
                    y: frame.height / 50

                    horizontalAlignment: TextInput.AlignHCenter
                    //font.capitalization: font.AllUpperCase
                    inputMethodHints: Qt.ImhUppercaseOnly, Qt.ImhNoPredictiveText
                    placeholderText: "Suche"

                    text: variable.infoID
                    focus: true

                    onAccepted: {/*
                        console.warn("Start camera")
                        camera.start()
                        console.warn("cameraName: " + camera.displayName)
                        camera.imageCapture.captureToLocation("/home/phablet/zk-data/t")*/
                        python.call('Stock.main.SearchArt', [text], function() {});
                    }
                }


                TableView {
                    id: liste
                    width: parent.width
                    x: 0
                    y: ti.y + ti.height + 10
                    height: parent.height - y


                    rowDelegate: Text {
                        id: row
                        //anchors.left: parent.left
                        //anchors.right: parent.right
                        height: liste.height/10
                        font.pixelSize: height * 0.8

                    }
                    TableViewColumn {
                        id: columnIdentification
                        role: "identification"
                        title: "ID"
                        width: parent.width/8
                    }
                    TableViewColumn {
                        id: columnArtikel
                        role: "artikel"
                        title: "Artikel"
                        width: parent.width/8
                    }
                    TableViewColumn {
                        id: columnLieferant
                        role: "lieferant"
                        title: "Lieferant"
                            width: parent.width/8
                    }
                    TableViewColumn {
                        role: "name_de"
                        title: "Name"
                        width: parent.width/4
                    }
                    TableViewColumn {
                        role: "ort"
                        title: "Ort"
                        width: parent.width/8
                        }
                    TableViewColumn {
                        role: "preisvk"
                        title: "Preis"
                        width: parent.width/8
                    }
                    TableViewColumn {
                        role: "anzahl"
                        title: "Anzahl"
                        width: parent.width/8
                    }
                    model: ListModel {
                        id: listModel
                        //font.pixelSize: parent.height
                    }
                    onClicked: {
                         open(listModel.get(row).identification)
                    }
                }

                BusyIndicator {
                    id: busyindicator
                    running: image.status === Image.Loadings
                    x: frame.width / 2
                    y: frame.height / 2
                }


                Python {
                    id: python
                    Component.onCompleted: {
                        addImportPath(Qt.resolvedUrl('.'));
                        importModule('Stock', function () {});

                        setHandler("ifPhone", ifPhone);
                        setHandler("antwortSearchArt", antwortSearchArt);
                        setHandler("busy", busy);
                        setHandler("antwortScanForSearch", function (ScannedCode) {
                            ti.text = ScannedCode
                        });

                        call("Stock.main.isPhone", [], function () {});
                        call('Stock.main.SearchArt', [ti.text], function() {});
                    }
                }
            }
        }

        Component {
            id: frameInfo

            Rectangle {
                id: frame2
                width: 1000
                height: 1000

                function open2(ID) {
                    variable.infoID = ID
                    frames.push(frameSuche);
                }

                function busy2(status) {
                    busyindicator2.visible = status
                }

                function ifPhone2(bool) {
                    frame2.state = "Handy"
                }

                function antwortGetArt(item) {
                    //listModel.clear();
                    for (var i=0; i<item.length; i++) {
                        listModel2.append(item[i]);
                    }
                }

                states: [
                    State {
                        name: "Handy"
                        PropertyChanges {target:labelIdentification; font.pixelSize:frame2.height*0.05}
                        PropertyChanges {target:labelIdentification; x:frame2.width/2 - width/2}

                        PropertyChanges {target:buttonBack; height:frame2.height/10}
                        PropertyChanges {target:buttonBack; width:frame2.width/5}
                        PropertyChanges {target:buttonBack; x:frame2.width-width}

                        //PropertyChanges {target:liste2; y: labelIdentification.y * 1.5}
                    },
                    State {
                        name: "Desktop"
                        //PropertyChanges {target:top1; color:"yellow"}
                    }
                ]

                Label {
                    id: labelIdentification
                    text: variable.infoID
                    y: frame2.height * 0.03
                    x: frame2.width / 2
                }

                ListView {
                    id: liste2
                    y: labelIdentification.height * 3
                    height: parent.height
                    width: parent.width


                    ListModel {
                        id: listModel2
                    }

                    Component {
                        id: delegateListe2
                        Item {
                            Rectangle {
                                Text {
                                    text: name
                                }


                                Text {
                                    text: name
                                    height: liste2.height / 20
                                    font.pixelSize: height * 0.6
                                }
                            }
                        }

                    }
                    model: listModel2
                    delegate: delegateListe2


                }

                Button {
                    id: buttonBack
                    text: "Zuruck"
                    onClicked: open2(labelIdentification.text)
                    height: frame2.height / 10
                    width: frame2.width / 8
                    x: frame2.width - width
                }

                BusyIndicator {
                    id: busyindicator2
                    running: image.status === Image.Loadings
                    x: frame2.width / 2
                    y: frame2.height / 2
                }


                Python {
                    id: python
                    Component.onCompleted: {
                        addImportPath(Qt.resolvedUrl('.'));
                        importModule('Stock', function () {});

                        setHandler("ifPhone2", ifPhone2);
                        setHandler("busy2", busy2);
                        setHandler("antwortGetArt", antwortGetArt);
                        call("Stock.main.isPhone2", [], function () {})
                        call("Stock.main.GetArt", [variable.infoID], function () {})
                    }
                }
            }
        }
    }
}
