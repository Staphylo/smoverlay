
import QtQuick 2.2
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

Rectangle {
//RCGroup {
    //property variant monitor
    //title: monitor.name

    property variant monitor
    property variant title: monitor.name

    anchors.fill: parent

    // height: disks.count * diskview.height

    Timer  {
        interval: monitor.updateInterval; running: true; repeat: true;
        onTriggered: monitor.update()
    }

    ScrollView {
        anchors.fill: parent

        verticalScrollBarPolicy: Qt.ScrollBarAlwaysOff
        ListView {
            Component.onCompleted: {
                console.log("disks: ", monitor.disks)
                //console.log(JSON.stringify(monitor, null, 4))
            }

            anchors.fill: parent
            model: monitor.disks
            delegate: Item {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 30
                Component.onCompleted: {
                    console.log("data: " + modelData)
                }

                Text {
                    id: mountpoint_text

                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: usage_text.left
                    anchors.margins: {
                        top: 5
                        left: 5
                        right: 5
                    }

                    verticalAlignment: Text.AlignVCenter
                    color: "white"

                    text: modelData.mountpoint
                }

                Text {
                    id: usage_text

                    anchors.top: parent.top
                    anchors.left: mountpoint_text.right
                    anchors.right: parent.right
                    anchors.margins: {
                        top: 5
                        left: 5
                        right: 5
                    }
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight

                    text: modelData.usepercent + "%"
                    color: "white"
                }

                ProgressBar {
                    id: usage_bar

                    anchors.top: mountpoint_text.bottom
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 4

                    value: modelData.usepercent / 100
                    //background: (usage_bar.value >= 75) ? "orange" : "green"
                    style: ProgressBarStyle {
                        background: Rectangle {
                            radius: 2
                            color: "#222"
                        }
                        progress: Rectangle {
                            radius: 2
                            color: (usage_bar.value >= 75) ? "orange" : "green"
                        }
                    }
                    //color: (disk.use > 75) ? "orange" : "green"
                }
            }
        }
    }
}
