import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1


Rectangle {
    id: frame
    width: 800
    height: 800
    
    function antwortSearchArt(item) {
        listModel.clear();
        for (var i=0; i<item.length; i++) {
            listModel.append(item[i]);
        }
    }

    TextField {
        id: ti
    
        x: parent.width/2 - ti.width/2
        y: parent.height/10
        
        text: ""
        focus: true

        onTextChanged: {
            python.call('Stock.main.SearchArt', [text], function() {});
            
        }
    }
    
    ListView {
        id: liste
        x: parent.width/2
        y: parent.height/2
        anchors.fill: parent
        
        model: ListModel {
            id: listModel
        }
        delegate: Text {
            text: name_de
            color: farbe
        }
    }
    
    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));
            importModule('Stock', function () {});
            
            setHandler("antwortSearchArt", antwortSearchArt);
        }
    }
}
