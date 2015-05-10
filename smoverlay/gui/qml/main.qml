import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1

//import remotecast 1.0

Rectangle {
    id: root

    width: cast.overlayWidth;
    height: cast.overlayHeight;

    // comment to show by default
    function freeze() {  console.log("freeze") }
    function unfreeze() { console.log("unfreeze") }
    //function freeze() {  console.log("freeze"); root.setUpdatesEnabled = false }
    //function unfreeze() { console.log("unfreeze"); root.setUpdatesEnabled = true }

    state: "VISIBLE"
    //opacity: 0.
    //Component.onCompleted: { view.x = -root.width + 1; freeze(); }


    color: "#FF2d323d"

    // completely transparent border
    border.color: "#00FFFFFF"
    border.width: 1

    property variant webview;
    property bool autohide: true;

    MouseArea {
        id: mouse_area

        anchors.fill: parent

        hoverEnabled: true
        propagateComposedEvents: true
        cursorShape: Qt.PointingHandCursor

        //focus: true

        Keys.onPressed: {
            console.log("overlay: ", event.key)
        }

        Keys.onEscapePressed: root.state = "HIDE"
        onEntered: root.state = "SHOW"
        onExited: root.state = "HIDE"

        RCHeader {
            id: header

            anchors.right: parent.right
            anchors.left: parent.left
            anchors.top: parent.top

            height: 100
        }

        RCBody {
            id: body

            anchors.right: parent.right
            anchors.left: parent.left
            anchors.top: header.bottom
            anchors.bottom: footer.top
            anchors.topMargin: 10
        }

        RCFooter {
            id: footer

            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.left: parent.left

            height: 90

            anchors.topMargin: 10
        }
    }

    states: [
        State {
            name: "VISIBLE"
            //PropertyChanges { target: root; opacity: 1.0; x: 0 }
        },
        State {
            name: "SHOW"
            //PropertyChanges { target: root; opacity: 1.0; x: 0 }
        },
        State {
            name: "HIDDEN"
            //PropertyChanges { target: root; opacity: 0.0; x: - root.width + 1}
        },
        State {
            name: "HIDE"
            //PropertyChanges { target: root; opacity: 0.0; x: - root.width + 1}
        }
    ]

    transitions: [
        Transition {
            from: "VISIBLE"
            to: "HIDE"
            SequentialAnimation {
                PauseAnimation { duration: 500 }
                ParallelAnimation {
                    NumberAnimation { target: view; property: "x"; to: - root.width + 1; duration: root.width - view.x; easing.type: Easing.InOutQuad  }
                    NumberAnimation { target: view; property: "opacity"; to: 0.0; duration: root.width - view.x }
                }
                //NumberAnimation { properties: "x, opacity"; easing.type: Eeasing.InOutQuad }
                ScriptAction { script: freeze() }
                PropertyAnimation { target: root; property: "state"; to: "HIDDEN" } 
            }
        },
        Transition {
            from: "SHOW"
            to: "HIDE"
            SequentialAnimation {
                ParallelAnimation {
                    NumberAnimation { target: view; property: "x"; to: - root.width + 1; duration: root.width - view.x; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: view; property: "opacity"; to: 0.0; duration: root.width - view.x }
                }
                ScriptAction { script: freeze() }
                PropertyAnimation { target: root; property: "state"; to: "HIDDEN" }
            }
        },
        Transition {
            from: "HIDDEN"
            to: "SHOW"
            SequentialAnimation {
                PauseAnimation { duration: 200 }
                ScriptAction { script: unfreeze() }
                ParallelAnimation {
                    NumberAnimation { target: view; property: "x"; to: 0; duration: - view.x; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: view; property: "opacity"; to: 1.0; duration: - view.x }
                }
                PropertyAnimation { target: root; property: "state"; to: "VISIBLE" } //to: "VISIBLE" }
            }
        },
        Transition{
            from: "HIDE"
            to: "SHOW"
            SequentialAnimation {
                ParallelAnimation {
                    NumberAnimation { target: view; property: "x"; to: 0; duration: x - view.x; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: view; property: "opacity"; to: 1.0; duration: x - view.x }
                }
                PropertyAnimation { target: root; property: "state"; to: "VISIBLE" } //to: "VISIBLE" }
            }
        }
    ]

}
