import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.1

Rectangle {

    color: "#FF383e4b"

    height: 100
    width: 320

    Item {
        id: volume

        anchors.fill: parent
        anchors.margins: 10

        property bool muted: false

        function toggle_mute() {
            muted = !muted
            if (muted)
                image.source = "../res/volume/muted.svg"
            else
                update_volume()
        }

        function update_volume() {
            var val = Math.floor(slider.value / 25) * 25
            if (val == 100)
                val = 75
            var img = "../res/volume/" +  val + ".svg"
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
            value: 50
            stepSize: 1

            onValueChanged: volume.update_volume()
        }
    }
}
