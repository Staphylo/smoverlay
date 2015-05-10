
import QtQuick 2.2
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

Item {
//Rectangle {
//RCGroup {

    property variant monitor
    property variant title: monitor.name
    property alias color : content.color

    property variant mempercent : monitor.memory.used / monitor.memory.total

    anchors.fill: parent

    Timer  {
        interval: 1000; running: true; repeat: true;
        onTriggered: monitor.update()
    }

    Rectangle {
        id: content
        //anchors.fill: parent

        height: 30
        anchors.top: parent.top 
        anchors.bottom: scope.top
        anchors.left: parent.left
        anchors.right: parent.right

        Text {
            id: memory_text

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

            text: "RAM"
        }

        Text {
            id: usage_text

            anchors.top: parent.top
            anchors.left: memory_text.right
            anchors.right: parent.right
            anchors.margins: {
                top: 5
                left: 5
                right: 5
            }
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignRight

            text: monitor.memory.percent + "%"
            color: "white"
        }

        ProgressBar {
            id: usage_bar

            anchors.top: memory_text.bottom
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 4

            value: monitor.memory.percent / 100

            //background: (usage_bar.value >= 75) ? "orange" : "green"
            style: ProgressBarStyle {
                background: Rectangle {
                    radius: 2
                    color: "#222"
                }
                progress: Rectangle {
                    radius: 2
                    color: (usage_bar.value >= 0.75) ? "orange" : "green"
                }
            }
        }
    }
    FocusScope {
        id: scope

        anchors.top: content.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        TextInput {
            id: input
            focus: true
        }
    }
}
