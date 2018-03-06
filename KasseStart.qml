import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 2.2//1.1

Rectangle {
    height: 800
    width: 1200

    function busy(status) {
        busyindicator.visible = status
    }

    BusyIndicator {
        id: busyindicator
        running: true //image.status === Image.Loadings
        x: parent.width / 2
        y: parent.height / 2
    }

    SwipeView {
        id: view

        currentIndex: 0
        anchors.fill: parent

        Item {
            id: firstPage
            KasseSelect {}
        }
        Item {
            id: secondPage
            KasseMain {}
        }
    }

    PageIndicator {
        id: indicator

        count: view.count
        currentIndex: view.currentIndex

        anchors.bottom: view.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
