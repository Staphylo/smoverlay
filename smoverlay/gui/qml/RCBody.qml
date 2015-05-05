import QtQuick 2.2
import QtQuick.Layouts 1.1

Item {

    Keys.forwardTo: [ button_settings ]

    ListView {
        id: monitor_list

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: row.top

        height: 500

        spacing: 10

        model: monitors
        delegate: Rectangle {
            id: monitor

            anchors.left: parent.left
            anchors.right: parent.right
            height: 100
            color: "purple"

            property var component;
            property variant sprite;

            function loadMonitors() {
                console.log("monitor: ", modelData)
                console.log(JSON.stringify(modelData, null, 4))

                //console.log(disklist)

                component = Qt.createComponent(modelData.monitor_view);
                //component = Qt.createQmlObject(model.viewsrc);
                if (component.status == Component.Ready)
                    finishLoadMonitors();
                else if (component.status == Component.Error)
                    console.log("Error loading component:", component.errorString());
                else
                    component.statusChanged.connect(finishLoadMonitor);
            }

            function finishLoadMonitors() {
                if (component.status == Component.Ready) {
                    sprite = component.createObject(monitor, {
                        "anchors.left": monitor.left,
                        "anchors.right": monitor.right,
                        "height": 30,
                        "title": modelData.monitor_name,
                        "monitor": modelData,
                        "color": "#FF383e4b"
                    });
                    if (sprite == null) {
                        console.log("Error creating object");
                        return
                    }
                } else if (component.status == Component.Error) {
                    console.log("Error loading component:", component.errorString());
                    return
                }
            }

            Component.onCompleted: loadMonitors();
        }
    }


    Column {
        id: row

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.top: monitor_list.bottom

        spacing: 10
        property int buttonHeight: 50

        //RCGroup {
        //    anchors.left: parent.left
        //    anchors.right: parent.right

        //    title: "Disk usage"
        //    //updateEvery: 5
        //}

        RCVolume {
            id: volume

            height: 100

            anchors.left: parent.left
            anchors.right: parent.right
        }

        RCButton {
            id: button_settings

            anchors.left: parent.left
            anchors.right: parent.right

            //anchors.bottom: button_exit.top


            height: row.buttonHeight
            //width: row.width

            image: "../res/settings.svg"
            text: qsTr("Settings")

            Keys.onEscapePressed: sprite_hide.start()


            property var component;
            property variant sprite;

            function createWebView() {
                component = Qt.createComponent("RCSettings.qml");
                if (component.status == Component.Ready)
                    finishWebViewCreation();
                else if (component.status == Component.Error)
                    console.log("Error loading component:", component.errorString());
                else
                    component.statusChanged.connect(finishWebViewCreation);
            }

            function finishWebViewCreation() {
                if (component.status == Component.Ready) {
                    sprite = component.createObject(root);
                    if (sprite == null) {
                        console.log("Error creating object");
                        return
                    }
                } else if (component.status == Component.Error) {
                    console.log("Error loading component:", component.errorString());
                    return
                }

                sprite.width = cast.screenWidth - cast.overlayWidth;
                sprite.height = cast.screenHeight
                sprite.x = -cast.screenWidth
                sprite.y =  0
                sprite.flags = Qt.ToolTip | Qt.FramelessWindowHint
            }

            onClicked: {
                if (sprite.visibility) {
                    sprite_show.stop()
                    sprite_hide.start()
                } else {
                    sprite_hide.stop()
                    sprite_show.start()
                }
            }

            Component.onCompleted: createWebView();

            SequentialAnimation {
                id: sprite_show;
                ScriptAction { script: { button_settings.sprite.show(); view.raise(); root.autohide = false; } }
                NumberAnimation { target: button_settings.sprite; property: "x"; to: cast.overlayWidth; duration: 500 }
            }

            SequentialAnimation {
                id: sprite_hide;
                NumberAnimation { target: button_settings.sprite; property: "x"; to: cast.overlayWidth - button_settings.sprite.width; duration: 500 }
                ScriptAction { script: {  button_settings.sprite.hide(); view.raise(); root.autohide = true } }
            }
        }

        RCButton {
            id: button_exit

            anchors.left: parent.left
            anchors.right: parent.right
            //anchors.bottom: parent.bottom

            height: parent.buttonHeight

            text: qsTr("exit")

            onClicked: Qt.quit()
        }
    }
}
