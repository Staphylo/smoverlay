
import QtQuick 2.2
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

Item {
    property variant monitor
    property variant title: monitor.name
    property alias color : content.color

    anchors.fill: parent

    Timer  {
        interval: 1000; running: true; repeat: true;
        onTriggered: monitor.update()
    }

    Rectangle {
        id: content
        //anchors.fill: parent

        height: 40
        anchors.top: parent.top 
        anchors.bottom: scope.top
        anchors.left: parent.left
        anchors.right: parent.right

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

            text: "Battery is " + monitor.status
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

            text: monitor.percent + "%"
            color: "white"
        }

        ProgressBar {
            id: usage_bar

            anchors.top: battery_text.bottom
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 4

            value: monitor.percent / 100

            style: ProgressBarStyle {
                background: Rectangle {
                    radius: 2
                    color: "#222"
                }
                progress: Rectangle {
                    radius: 2
                    color: (usage_bar.value < 0.25) ? "orange" : "green"
                }
            }
        }
    }
}
