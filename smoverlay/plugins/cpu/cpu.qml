import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3
import QtQuick.Layouts 1.1
import QtGraphicalEffects 1.0

Item {
    anchors.fill: parent
    property variant color

    height: cpu_average.height + cpu_list.height

    Timer  {
        interval: monitor.updateInterval; running: true; repeat: true;
        onTriggered: monitor.update()
    }

    Rectangle {
        anchors.fill: parent
        color: "#FF383e4b"
    Column {
        anchors.fill: parent

        Item {
        //Rectangle {
            id: cpu_average

            height: 30
            anchors.left: parent.left
            anchors.right: parent.right

            // FIXME
            //color: "#FF383e4b"

            Text {
                id: cpu_label

                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: cpu_usage.left
                anchors.margins: {
                    top: 5
                    left: 5
                    right: 5
                }

                verticalAlignment: Text.AlignVCenter
                color: "white"

                text: "CPU"
            }

            Text {
                id: cpu_usage

                anchors.top: parent.top
                anchors.left: cpu_label.right
                anchors.right: parent.right
                anchors.margins: {
                    top: 5
                    left: 5
                    right: 5
                }
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignRight

                text: Math.round(monitor.percent, 2) + "%"
                color: "white"
            }

            ProgressBar {
                id: cpu_bar

                anchors.top: cpu_label.bottom
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 4

                value: monitor.percent / 100

                //background: (usage_bar.value >= 75) ? "orange" : "green"
                style: ProgressBarStyle {
                    background: Rectangle {
                        radius: 2
                        color: "#222"
                    }
                    progress: Rectangle {
                        radius: 2
                        color: {
                            if ( cpu_bar.value >= 0.90 )
                                return "red";
                            if ( cpu_bar.value >= 0.75 )
                                return "orange";
                            return "green"
                        }
                    }
                }
            }
        }

        ListView {
            id: cpu_list

            anchors.left: parent.left
            anchors.right: parent.right

            orientation: ListView.Horizontal
            height: 35

            model: monitor.cpus
            delegate: ProgressBar {
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                height: 35
                width: 35
                //minimumValue: 0
                //maximumValue: 100
                value: modelData.percent / 100
                style: ProgressBarStyle {
                    panel : Rectangle {
                        color: "transparent"
                        implicitWidth: 80
                        implicitHeight: implicitWidth

                        Rectangle {
                            id: outerRing
                            z: 0
                            anchors.fill: parent
                            radius: Math.max(width, height) / 2
                            color: "transparent"
                            //border.color: "gray"
                            border.color: "#FF383e4b"
                            border.width: 8
                        }

                        Rectangle {
                            id: innerRing
                            z: 1
                            anchors.fill: parent
                            anchors.margins: (outerRing.border.width - border.width) / 2
                            radius: outerRing.radius
                            color: "transparent"
                            //border.color: "darkgray"
                            border.color: "#222"
                            border.width: 2

                            ConicalGradient
                            {
                                source: innerRing
                                anchors.fill: parent
                                gradient: Gradient
                                {
                                    GradientStop { position: 0.00; color: "green" }
                                    GradientStop { position: control.value; color: "green" }
                                    GradientStop { position: control.value + 0.01; color: "transparent" }
                                    GradientStop { position: 1.00; color: "transparent" }
                                }
                            }
                        }

                        Text {
                            id: progressLabel
                            anchors.centerIn: parent
                            color: "white"
                            text: (control.value * 100).toFixed()
                        }
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        console.log(JSON.stringify(monitor, null, 4))
    }
    }
}
