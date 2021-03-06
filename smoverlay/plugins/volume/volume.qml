import QtQuick 2.4
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.3

Rectangle {

    color: "#FF383e4b"

    property variant monitor
    height: volume.height

    Item {
        id: volume

        anchors.fill: parent
        anchors.margins: 10
        height: 100

        function toggle_mute() {
            monitor.muted = !monitor.muted
            if (monitor.muted)
                image.source = "res/muted.svg"
            else
                update_volume()
        }

        function update_volume() {
            monitor.volume = slider.value
            var val = Math.floor(slider.value / 25) * 25
            if (val == 100)
                val = 75
            var img = "res/" +  val + ".svg"
            image.source = img
        }

        Image {
            id: image

            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left

            fillMode: Image.PreserveAspectFit
            height: 2 * parent.height / 3
            width: 2 * parent.height / 3

            MouseArea {
                anchors.fill: parent
                onClicked: volume.toggle_mute()
            }
        }

        Text {
            id: text

            anchors.top: parent.top
            anchors.right: parent.right
            anchors.left: image.right
            anchors.bottom: slider.top

            //anchors.horizontalCenter: parent.horizontalCenter
            //anchors.leftMargin: parent.height / 2
            horizontalAlignment: Text.AlignHCenter

            font.family: "Lato"
            font.pointSize: 16

            color: "#FFFFFFFF"

            style: Text.Sunken
            styleColor: "#FF323232"

            text: qsTr("Volume") + ": " + slider.value + "%"

        }

        Slider {
            id: slider

            anchors.top: text.top
            anchors.right: parent.right
            anchors.left: image.right
            anchors.bottom: parent.bottom

            maximumValue: 100
            minimumValue: 0
            //value: monitor.volume
            value: 0
            stepSize: 1

            onValueChanged: volume.update_volume()
        }

        Component.onCompleted: update_volume()
    }
}
