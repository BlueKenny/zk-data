import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    anchors.fill: parent
    Button {
        id: buttonLieferschein
        text: "Lieferscheine"
        width: window.width / 5
        height: window.height / 5
        x: window.width / 2 - width / 2
        y: window.height / 2 - height / 2
        onClicked: {
            view.push(frameLieferschein)
        }
    }
}
