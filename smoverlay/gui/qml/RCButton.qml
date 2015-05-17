import QtQuick 2.4
import QtQuick.Layouts 1.1

Rectangle {
    id: button

    property string text
    property string image

    signal clicked
    signal entered
    signal exited

    Component.onCompleted: {
        button_area.clicked.connect(button.clicked)
        button_area.entered.connect(button.entered)
        button_area.exited.connect(button.exited)
    }

    color: "#FF383e4b"

    RowLayout {
        anchors.fill: parent
        spacing: height / 2

        //Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        //Layout.alignment: Qt.AlignBottom

        Image {
            id: button_image

            anchors.left: parent.left
            anchors.leftMargin: parent.height / 2
            source: button.image
            height: parent.height / 2
            width: parent.height / 2
        }

        Text {
            id: button_text

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.leftMargin: parent.height / 2

            font.family: "Lato"
            font.pointSize: 20
            font.bold: true
            font.weight: Font.Bold
            font.capitalization: Font.SmallCaps


            color: "#FF36A9E1"
            style: Text.Sunken
            styleColor: "#FF323232"

            text: button.text
        }
    }

    MouseArea {
        id: button_area

        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            button.color = "#FF36A9E1"
            button_text.color = "#FF383e4b"
        }

        onExited: {
            button.color = "#FF383e4b"
            button_text.color = "#FF36A9E1"
        }

    }
}
