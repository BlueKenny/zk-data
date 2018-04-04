import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2
//Rectangle {
ApplicationWindow {
    id: mainWindow
    height: 2000
    width: 2000
    title: qsTr("ZK-DATA")


    Item {
        id: vars
        property string lieferscheinSuchenTextIdentification: ""
        property string lieferscheinSuchenTextName: ""
        property string kundenSuchenTextIdentification: ""
        property string kundenSuchenTextName: ""
        property string kundenSuchenVorherigeAnsicht: ""
        property bool lieferscheinSuchenCheckFertige: false
        property bool lieferscheinSuchenCheckEigene: true

        property bool isPhone: false
    }

    function busy(status) {
        busyindicator.visible = status
    }

    BusyIndicator {
        id: busyindicator
        running: true //image.status === Image.Loadings
        x: mainWindow.width / 2
        y: mainWindow.height / 2
    }

    StackView {
        id: view

        delegate: StackViewDelegate {

            function transitionFinished(properties)
            {
                properties.exitItem.opacity = 1
            }

            pushTransition: StackViewTransition {
                PropertyAnimation {
                    target: enterItem
                    property: "opacity"
                    from: 0
                    to: 1
                    duration: 300
                }
                PropertyAnimation {
                    target: exitItem
                    property: "opacity"
                    from: 1
                    to: 0
                    duration: 300
                }
            }
        }

        initialItem: frameSelect//frameKasse
        anchors.fill: parent

        Component {
            id: frameSelect
            Select {}
        }
        Component {
            id: frameLieferscheinAnzeigen
            LieferscheinAnzeigen {}
        }
        Component {
            id: frameLieferscheinSuchen
            LieferscheinSuchen {}
        }
        Component {
            id: frameKundenSuchen
            KundenSuchen {}
        }
        Component {
            id: frameStock
            Stock {}
        }
    }

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('./'));
            importModule('Main', function () {});

            call('Main.main.phone', [], function (boolStatus) {vars.isPhone = boolStatus});
            setHandler("busy", busy);
        }
    }
}
