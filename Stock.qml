import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1
//import QtQuick.Window 2.2

// Fedora
//dnf install pyotherside
//dnf install qt5-qtquickcontrols
//dnf install qt5-qtquickcontrols2

Rectangle {
    id: frame
    width: 1000
    height: 1000
    
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
            PropertyChanges {target:ti; height:frame.height/10}
            PropertyChanges {target:ti; width:frame.width*0.7}
            PropertyChanges {target:ti; font.pixelSize: ti.height*0.5}
            
            //PropertyChanges {target:liste; font.pixelSize: 100}
            PropertyChanges {target:busyi; visible: true}
            
            
        },
        State {
            name: "Desktop"
            //PropertyChanges {target:top1; color:"yellow"}
        }
    ]
    
    TextField {
        id: ti
        
        x: frame.width/2 - ti.width/2
        y: frame.height / 50      
        
            
        horizontalAlignment: TextInput.AlignHCenter
        //font.capitalization: font.AllUpperCase
        inputMethodHints: Qt.ImhUppercaseOnly, Qt.ImhNoPredictiveText
        placeholderText: "Suche"
            
        text: ""
        focus: true

        onAccepted: {
            python.call('Stock.main.SearchArt', [text], function() {})
        }
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
            width: parent.width/8
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
        }/*
        rowDelegate: Rectangle{
            height: 100
            //font.pixelSize: 100
        }*/
        model: ListModel {
            id: listModel
        }      
    }
       
    BusyIndicator {
        id: busyindicator
        running: image.status === Image.Loadings
        visible: true
        x: parent.width / 2
        y: parent.height / 2
    }
    
    
    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));
            importModule('Stock', function () {});
            
            call("Stock.main.isPhone", [], function () {})
            setHandler("ifPhone", ifPhone);
            setHandler("antwortSearchArt", antwortSearchArt);
            setHandler("busy", busy);
            
            
          
        }
    }
}
