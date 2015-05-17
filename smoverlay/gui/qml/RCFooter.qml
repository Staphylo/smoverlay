import QtQuick 2.4
import QtQuick.Layouts 1.1

Column {
    id: row

    spacing: 10
    property int buttonHeight: 50

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
