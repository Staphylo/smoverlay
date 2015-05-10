import QtQuick 2.2
import QtQuick.Layouts 1.1

Item {

    ListView {
        id: monitor_list

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: row.top

        height: 500

        interactive: false
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
                        //"height": 50,
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
}
