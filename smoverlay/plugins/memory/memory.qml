import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

Item {
    id: plugin

    anchors.fill: parent
    property variant color

    Timer  {
        interval: monitor.updateInterval; running: smoverlay.running; repeat: true;
        onTriggered: monitor.update()
    }

    ListView {
        anchors.fill: parent

        interactive: false

        model: ListModel {
            Component.onCompleted: {
                append(monitor.memory)
                if (monitor.hasSwap) {
                    var swap = monitor.swap
                    append(monitor.swap)
                }
            }
        }

        delegate: Rectangle {

            height: 30
            anchors.left: parent.left
            anchors.right: parent.right

            color: plugin.color

            Text {
                id: memory_label

                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: memory_usage.left
                anchors.margins: {
                    top: 5
                    left: 5
                    right: 5
                }

                verticalAlignment: Text.AlignVCenter
                color: "white"

                text: model.label
            }

            Text {
                id: memory_usage

                anchors.top: parent.top
                anchors.left: memory_label.right
                anchors.right: parent.right
                anchors.margins: {
                    top: 5
                    left: 5
                    right: 5
                }
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignRight

                text: model.percent + "%"
                color: "white"
            }

            ProgressBar {
                id: memory_bar

                anchors.top: memory_label.bottom
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 4

                value: model.percent / 100

                //background: (usage_bar.value >= 75) ? "orange" : "green"
                style: ProgressBarStyle {
                    background: Rectangle {
                        radius: 2
                        color: "#222"
                    }
                    progress: Rectangle {
                        radius: 2
                        color: {
                            if ( memory_bar.value >= 0.90 )
                                return "red";
                            if ( memory_bar.value >= 0.75 )
                                return "orange";
                            return "green"
                        }
                    }
                }
            }
        }
    }
}
