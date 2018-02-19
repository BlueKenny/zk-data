import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.2

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
    
    property bool isPhone: true

    TextField {
        id: ti
    
        x: parent.width/2 - ti.width/2
        y: parent.height / 50
            
        // for Phone
        height: 500/Screen.pixelDensity
        width: parent.width/2
        font.pixelSize: 300/Screen.pixelDensity
        
        horizontalAlignment: TextInput.AlignHCenter
        font.capitalization: Font.AllUpperCase
        inputMethodHints: Qt.ImhUppercaseOnly, Qt.ImhNoPredictiveText
        placeholderText: "Suche"
        
        text: ""
        focus: true

        onTextChanged: python.call('Stock.main.SearchArt', [text], function() {})
    }
    
    TableView {
        id: liste
        width: parent.width
        x: 0
        y: ti.y + ti.height + 10
        height: parent.height - y
        
        
        TableViewColumn {
            role: "identification"
            title: "ID"
            //width: parent.width/8
            width: parent.width/3
        }
        TableViewColumn {
            role: "artikel"
            title: "Artikel"
            width: parent.width/8
        }
        TableViewColumn {
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
        }
    }
    
    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));
            importModule('Stock', function () {});
            python.call('Stock.main.isPhone', [], function(isPhone) {})
            setHandler("antwortSearchArt", antwortSearchArt);
          
        }
    }
}
