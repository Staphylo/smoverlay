import QtQuick 2.4
import QtQuick.Layouts 1.1

Item {

    ListView {
        id: monitor_list

        anchors.fill: parent

        //interactive: false
        spacing: 10

        headerPositioning: ListView.OverlayHeader
        header: RCHeader {
            height: 100
            z: 10
            anchors.left: parent.left
            anchors.right: parent.right
        }

        footerPositioning: ListView.OverlayFooter
        footer: RCFooter {
            //anchors.topMargin: 10
            height: 50
            z: 10
            anchors.left: parent.left
            anchors.right: parent.right
        }

        //section.property: "monitorName"
        //section.delegate: Rectangle {
        //    anchors.left: parent.left
        //    anchors.right: parent.right

        //    height: 18
        //    color: "lightsteelblue"

        //    Text {
        //        text: section
        //        font.bold: true
        //        font.pixelSize: 13
        //    }
        //}

        model: monitors
        delegate: Rectangle {
            id: monitor

            z: 0
            anchors.left: parent.left
            anchors.right: parent.right
            color: "purple"
            height: modelData.monitorHeight

            Loader {
                id: loader
                anchors.fill: parent
                source: modelData.monitorView

                property var title: modelData.monitorName
                property var monitor: modelData

                Component.onCompleted: {
                    item.color = "#FF383e4b"
                    console.log(JSON.stringify(modelData, null, 4))
                }
            }
        }
    }
}
