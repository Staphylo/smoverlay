import QtQuick 2.2
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

Rectangle {
    property variant monitor
    property variant title: monitor.name

    anchors.fill: parent

    Timer  {
        interval: monitor.updateInterval; running: true; repeat: true;
        onTriggered: monitor.update()
    }

    ScrollView {
        anchors.fill: parent

        verticalScrollBarPolicy: Qt.ScrollBarAlwaysOff
        ListView {
            Component.onCompleted: {
                console.log("ifaces: ", monitor.interfaces)
            }

            anchors.fill: parent
            model: monitor.interfaces
            delegate: Item {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 32

                //Behavior on rxspeed { SmoothedAnimation { velocity: 200 } }
                //Behavior on txspeed { SmoothedAnimation { velocity: 200 } }

                function humanSize(bytes) {
                    if ((bytes >> 30) & 0x3FF)
                        bytes = (bytes >>> 30) + '.' + (bytes & (3*0x3FF)) + 'GB' ;
                    else if ((bytes >> 20) & 0x3FF)
                        bytes = (bytes >>> 20) + '.' + (bytes & (2*0x3FF)) + 'MB' ;
                    else if ((bytes >> 10) & 0x3FF)
                        bytes = (bytes >>> 10) + '.' + (bytes & (0x3FF)) + 'KB' ;
                    else if ((bytes >> 1) & 0x3FF)
                        bytes = (bytes >>> 1) + 'B ' ;
                    else
                        bytes = bytes + 'B ' ;
                    return bytes ;
                }


                Text {
                    id: name_text

                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: ip_text.left
                    anchors.bottom: parent.bottom
                    anchors.margins: 5
                    //anchors.margins: {
                    //    top: 5
                    //    left: 5
                    //    right: 5
                    //}

                    verticalAlignment: Text.AlignVCenter
                    color: "white"

                    text: modelData.name
                }

                Text {
                    id: ip_text

                    //anchors.top: parent.top
                    anchors.left: name_text.right
                    anchors.right: speed_text.left
                    //anchors.bottom: parent.bottom
                    anchors.verticalCenter: name_text.verticalCenter

                    anchors.margins: 5
                    //anchors.margins: {
                    //    top: 5
                    //    left: 5
                    //    right: 5
                    //}
                    verticalAlignment: Text.AlignVCenter

                    text: "" //0.0.0.0"
                    color: "white"
                    font.pointSize: 8.
                }

                Column {
                    id: speed_text

                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.right: parent.right

                    width: 75

                    Text {
                        id: rx_text

                        verticalAlignment: Text.AlignVCenter
                        //horizontalAlignment: Text.AlignRight

                        text: "rx: " + humanSize(modelData.rxspeed) + "/s"
                        color: "white"
                        font.pointSize: 8.
                    }

                    Text {
                        id: tx_text

                        verticalAlignment: Text.AlignVCenter
                        //horizontalAlignment: Text.AlignRight

                        text: "tx: " + humanSize(modelData.txspeed) + "/s"
                        color: "white"
                        font.pointSize: 8.
                    }
                }
            }
        }
    }

}
