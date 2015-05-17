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
        id: wifi

        anchors.fill: parent;

        property var wifi_image : "../res/wifi/0.svg"
        property var wifi_text : ""

        function infoUpdate() {
            smoverlay.updateWifi()
            var sig = smoverlay.wifiSignal
            if (sig == -1) {
                wifi_image = "../res/wifi/na.svg"
                wifi_text = "No network"
            } else {
                var img = (Math.floor(sig / 25) * 25)
                wifi_image = "../res/wifi/" + img +".svg"
                wifi_text = smoverlay.wifiEssid
            }
        }

        Image {
            id: wifi_state

            anchors.left: parent.left
            anchors.top: parent.top

            anchors.leftMargin: 20
            anchors.topMargin: 10

            //smooth: true
            width: 3 * parent.height / 4;
            height: 3 * parent.height / 4;

            source: wifi.wifi_image
        }

        Text {
            id: wifi_name

            height: parent.height / 2;

            //anchors.right: parent.left
            //anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.left: wifi_state.right
            //anchors.right: parent.right

            anchors.rightMargin: 20
            anchors.bottomMargin: -15

            font.family: "Lato"
            font.pointSize: 13
            color: "#FFFFFFFF"

            text: wifi.wifi_text
        }

        Timer  {
            interval: 1000; running: true; repeat: true;
            onTriggered: wifi.infoUpdate()
        }

    }
}
