import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: mainWindow
    height: 800
    width: 1200

    function busy(status) {
        busyindicator.visible = status
    }

    BusyIndicator {
        id: busyindicator
        running: true //image.status === Image.Loadings
        x: mainWindow.width / 2
        y: mainWindow.height / 2
    }

    //SwipeView {
    StackView {
        id: view

        //currentIndex: 0
        initialItem: frameSelect//frameKasse
        anchors.fill: parent

        //Item {
        Component {
            id: frameSelect
            Select {}
        }
        //Item {
        Component {
            id: frameLieferscheinAnzeigen
            LieferscheinAnzeigen {}
        }
        Component {
            id: frameLieferscheinSuchen
            LieferscheinSuchen {}
        }
    }
/*
    PageIndicator {
        id: indicator

        count: view.count
        currentIndex: view.currentIndex

        anchors.bottom: view.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }*/

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));
            importModule('Main', function () {});

            setHandler("busy", busy);
        }
    }
}
