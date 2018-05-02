import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

Item {
    id: plugin

    anchors.fill: parent
    property variant color

    Timer  {
        interval: monitor.updateInterval
        running: smoverlay.running
        repeat: true;
        onTriggered: monitor.update()
    }

    ListView {
        anchors.fill: parent

        interactive: false

        model: monitor.batteries

        delegate: Rectangle {
            id: content

            anchors.left: parent.left
            anchors.right: parent.right
            height: 40

            color: plugin.color

            Text {
                id: battery_text

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

                text: "Battery " + modelData.label + " is " + modelData.status
            }

            Text {
                id: usage_text

                anchors.top: parent.top
                anchors.left: battery_text.right
                anchors.right: parent.right
                anchors.margins: {
                    top: 5
                    left: 5
                    right: 5
                }
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignRight

                text: modelData.percent + "%"
                color: "white"
            }

            ProgressBar {
                id: usage_bar

                anchors.top: battery_text.bottom
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 4

                value: (modelData.dead / 100) +
                       (modelData.percent / 100) * ((100 - modelData.dead) / 100)

                style: ProgressBarStyle {
                    background: Rectangle {
                        radius: 2
                        color: "#222"
                    }
                    progress: Rectangle {
                        radius: 2
                        color: (modelData.percent < 30) ?
                                  ((modelData.percent < 10) ? "red" : "orange")
                                  : "green"
                    }
                }
            }

            ProgressBar {
                id: death_bar

                anchors.fill: usage_bar

                value: modelData.dead / 100

                style: ProgressBarStyle {
                    background: Rectangle {
                        color: "transparent"
                    }
                    progress: Rectangle {
                        radius: 2
                        color: "grey"
                    }
                }
            }
        }
    }
}
