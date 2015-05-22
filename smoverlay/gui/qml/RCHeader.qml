import QtQuick 2.4

Rectangle {
    color: "#FF383e4b"

    Item {
        id: clock

        anchors.fill: parent;

        function timeChanged() {
            var date = new Date()
            clock_time.text = Qt.formatTime(date, "hh:mm:ss")
            clock_date.text = Qt.formatDate(date, "ddd d MMMM yyyy")
        }


        Text {
            id: clock_time

            anchors.right: parent.right
            anchors.top: parent.top

            anchors.rightMargin: 20
            anchors.topMargin: 5

            font.family: "Lato"
            font.pointSize: 20
            color: "#FFFFFFFF"

            text: ""

        }

        Text {
            id: clock_date

            anchors.right: parent.right
            anchors.top: clock_time.bottom

            anchors.rightMargin: 20
            anchors.topMargin: 0

            font.family: "Lato"
            font.pointSize: 12
            color: "#FFFFFFFF"

            text: ""
        }

        Timer  {
            interval: 1000; running: true; repeat: true;
            onTriggered: clock.timeChanged()
        }
    }

    Item {
        id: net

        anchors.fill: parent;

        property var net_image : "../res/net/na.svg"
        property var net_text : ""

        function infoUpdate() {
            smoverlay.update()
            // FIXME: use names instead smoverlay.NET_NONE
            if (smoverlay.connectionType == 0 ) {
                net_text = "No network"
                net_image = "../res/net/na.svg"
            } else if (smoverlay.connectionType == 1 ) {
                net_text = "Eth " + smoverlay.ethernetSpeed + " Mbit/s"
                net_image = "../res/net/ethernet.png"
            } else if (smoverlay.connectionType == 2 ) {
                var imgname = Math.floor(smoverlay.wifiSignal / 25) * 25
                net_image = "../res/net/" + imgname + ".svg"
                net_text = smoverlay.wifiEssid
            }
        }

        Image {
            id: net_state

            anchors.left: parent.left
            anchors.top: parent.top

            anchors.leftMargin: 20
            anchors.topMargin: 10

            //smooth: true
            width: 3 * parent.height / 4;
            height: 3 * parent.height / 4;

            source: net.net_image
        }

        Text {
            id: net_name

            height: parent.height / 2;

            //anchors.right: parent.left
            //anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.left: net_state.right
            //anchors.right: parent.right

            anchors.leftMargin: 10
            anchors.rightMargin: 20
            anchors.bottomMargin: -15

            font.family: "Lato"
            font.pointSize: 13
            color: "#FFFFFFFF"

            text: net.net_text
        }

        Timer  {
            interval: 1000; running: true; repeat: true;
            onTriggered: net.infoUpdate()
        }

    }
}
