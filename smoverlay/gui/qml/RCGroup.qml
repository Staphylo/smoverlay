import QtQuick.Controls 1.3
import QtQuick 2.2

Rectangle {
    id: box

//r   property variant monitor;

    property var min_height : title_box.height
    property var max_height : 100
    property var title : ""

    state: "COLLAPSED"
    height: 30

    states: [
        State {
            name: "EXPANDED"
            //PropertyChanges { target: bodybox; height: box.max_height }
        },
        State {
            name: "COLLAPSED"
            //PropertyChanges { target: bodybox; height: 0 }
        }
    ]

    transitions: [
        Transition {
            from: "EXPANDED"
            to: "COLLAPSED"
            NumberAnimation { target: box; property: "height"; to: title_box.height; duration: 100 }
        },
        Transition {
            from: "COLLAPSED"
            to: "EXPANDED"
            NumberAnimation { target: box; property: "height"; to: box.max_height; duration: 100 } //bodybox.height + title_box.height; duration: 100 }
        }
    ]

    Rectangle {
        id: title_box
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 30
        color: "#FF383e4b"

        function state_toggle() {
            box.state = (box.state == "EXPANDED") ? "COLLAPSED" : "EXPANDED"
            icon.source = "../res/" + box.state + ".png"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: title_box.state_toggle()
        }

        Image {
            id: icon
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            width: height

            source: "../res/" + box.state + ".png"
        }

        Text {
            id: title
            anchors.left: icon.right
            anchors.leftMargin: 5
            anchors.verticalCenter: icon.verticalCenter

            color: "white"
            //font.weight: Font.DemitBold
            font.pointSize: 10.
            text: box.title
        }
    }
}
