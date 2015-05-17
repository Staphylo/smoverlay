import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

Rectangle {
    id: root

    width: ui.overlayWidth;
    height: ui.overlayHeight;

    // comment to show by default
    function freeze() {
        console.log("freeze")
    }
    function unfreeze() {
        console.log("unfreeze")
    }
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

        RCBody {
            id: body
            height: parent.height
            anchors.fill: parent
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
                PauseAnimation { duration: ui.hideDelay }
                ParallelAnimation {
                    NumberAnimation { target: view; property: "x"; to: ui.overlayHideX; easing.type: Easing.InOutQuad  }
                    NumberAnimation { target: view; property: "opacity"; to: ui.opacityHide }
                }
                ScriptAction { script: freeze() }
                PropertyAnimation { target: root; property: "state"; to: "HIDDEN" } 
            }
        },
        Transition {
            from: "SHOW"
            to: "HIDE"
            SequentialAnimation {
                ParallelAnimation {
                    NumberAnimation { target: view; property: "x"; to: ui.overlayHideX; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: view; property: "opacity"; to: ui.opacityHide }
                }
                ScriptAction { script: freeze() }
                PropertyAnimation { target: root; property: "state"; to: "HIDDEN" }
            }
        },
        Transition {
            from: "HIDDEN"
            to: "SHOW"
            SequentialAnimation {
                PauseAnimation { duration: ui.showDelay }
                ScriptAction { script: unfreeze() }
                ParallelAnimation {
                    NumberAnimation { target: view; property: "x"; to: ui.overlayShowX; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: view; property: "opacity"; to: ui.opacityShow; }
                }
                PropertyAnimation { target: root; property: "state"; to: "VISIBLE" } //to: "VISIBLE" }
            }
        },
        Transition{
            from: "HIDE"
            to: "SHOW"
            SequentialAnimation {
                ParallelAnimation {
                    NumberAnimation { target: view; property: "x"; to: ui.overlayShowX; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: view; property: "opacity"; to: ui.opacityShow }
                }
                PropertyAnimation { target: root; property: "state"; to: "VISIBLE" } //to: "VISIBLE" }
            }
        }
    ]

    Component.onCompleted: console.log(JSON.stringify(ui, null, 4))

}
