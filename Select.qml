import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width

    Label {
        id: labelSelectTitle
        text: "Hauptmenu"
        font.pixelSize: mainWindow.width / 50
        x: mainWindow.width / 2 - width / 2
    }

    Button {
        id: buttonLieferschein
        text: "Lieferscheine"
        width: vars.isPhone ? window.width / 2 : window.width / 5
        height: window.height / 5
        x: window.width / 2 - width / 2
        y: window.height / 2 - height / 2
        onClicked: {
            view.push(frameLieferscheinSuchen)
        }
    }
}
