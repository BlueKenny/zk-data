import QtQuick 2.4
import QtQuick.Layouts 1.1
import Ubuntu.Components 1.3
import io.thp.pyotherside 1.2

MainView {
    id: root
    objectName: 'mainView'
    applicationName: 'zk-data.kasse'
    automaticOrientation: true

    width: units.gu(45)
    height: units.gu(75)

    Page {
        anchors.fill: parent

        header: PageHeader {
            id: header
            title: i18n.tr('Kasse')
        }

        Label {
            anchors.centerIn: parent
            text: i18n.tr('Hello World!')
        }
    }

    Python {
        id: python

        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('./'));

            importModule('python3-pyqt5', function() {
                console.log('python3-pyqt5 module imported');
                python.call('python3-pyqt5.speak', ['Hello World!'], function(returnValue) {
                    console.log('python3-pyqt5.speak returned ' + returnValue);
                })
            });
        }

        onError: {
            console.log('python error: ' + traceback);
        }
    }
}
