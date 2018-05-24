import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.0
import QtQuick.Window 2.2

import QtCharts 2.2


Window {
    id: window
    title: qsTr("ZK-Data Stats")
    x: 0
    y: 0
    width: 500
    height: 500

    Item {
        id: variable
        property string monat: "x"
        //property int listeIndex: 0
        //property bool switchFinishChecked: false
    }

    Slider {
        id: slider
        value: 1
        width: window.width
        maximumValue: 12.0
        minimumValue: 1.0
        stepSize: 1.0
        onValueChanged: {
            variable.monat = value
            python.call('Stats.main.checkStats', [value], function() {});
        }
    }

    function antwortStats(item) {
        chartGewinn.clear()
        for (var i=0; i<item.length; i++) {
            chartGewinn.append(i, item[i])
        }
    }

    function busy(status) {
        busyindicator.visible = status
    }

    ChartView {
        id: chart
        title: ""
        y: slider.height * 2
        width: window.width
        height: window.height - y
        antialiasing: true

        ValueAxis {
            id: valueAxisX
            min: 1
            max: 31
            tickCount: 31
            labelFormat: "%.0f"
        }
        ValueAxis {
            id: valueAxisY
            min: 0
            max: 10000
            tickCount: 11
            labelFormat: "%.0f"
        }

        AreaSeries {
        //LineSeries {
            name: "Gewinn " + variable.monat
            color: "blue"
            axisX: valueAxisX
            axisY: valueAxisY

            upperSeries: LineSeries {
                id: chartGewinn
            }
        }
    }

    BusyIndicator {
        id: busyindicator
        running: true //image.status === Image.Loadings
        x: window.width / 2 - width / 2
        y: window.height / 2 - height / 2
    }

    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));
            importModule('Stats', function () {});

            setHandler("busy", busy);
            setHandler("antwortStats", antwortStats);

            //call('LieferscheinAnzeigen.main.GetLieferschein', [], function() {});
            //call('LieferscheinAnzeigen.main.GetIdentification', [], function(lieferscheinNummer) {labelLieferscheinAnzeigenTitle.text = "Lieferschein: " + lieferscheinNummer});
        }
    }
}
