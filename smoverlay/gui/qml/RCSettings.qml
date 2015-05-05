import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.1
import QtWebKit 3.0

//import remotecast 1.0

Window {
    id: settings

    WebView {
        id: web_admin

        Keys.onPressed: {
            switch (event.key) {
                case Qt.Key_Backspace:
                    goBack();
                    break;
                case Qt.Key_Escape:
                    //settings.close();
                    break;
                default:
                    console.log("key", event.key)
            }
        }


        //url: "http://remotecast.achier.fr/signin"
        url: "http://127.0.0.1:30001/signin"
        anchors.fill: parent

        onNavigationRequested: {
            var schemaRE = /^\w+:/;
            if (schemaRE.test(request.url)) {
                request.action = WebView.AcceptRequest;
            } else {
                request.action = WebView.IgnoreRequest;
            }
        }

        onLoadingChanged: {
            if (loadRequest.status == WebView.LoadStartedStatus)
                loading.visible = true
            else if (loadRequest.status == WebView.LoadSucceededStatus)
                loading.visible = false
            else if (loadRequest.status == WebView.LoadFailedStatus) {
                loading.visible = false
                console.log("failed to connect")
                reload()
            }
        }
    }

    AnimatedImage {
        id: loading
        source: "../res/loading.svg"

        visible: false

        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        NumberAnimation on rotation {
             from: 0
             to: 360
             running: loading.visible == true
             loops: Animation.Infinite
             duration: 1000
         }
    }

}
