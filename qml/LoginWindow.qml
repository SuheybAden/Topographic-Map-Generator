import QtQuick 2.0
import QtQuick.Window 2.12
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: loginWindow
    visible: true
    width: 400
    height: 250
    title: "Login Window"

    Material.theme: Material.LightBlue
    Material.accent: Material.Dark
    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.WindowTitleHint

    property QtObject backend
    property var inputValues: {
        "username": usernameField.text,
        "password": passwordField.text
    }

    ColumnLayout {
        anchors.fill: parent

        // // IMAGE IMPORT
        // Image{
        //     id: image
        //     source: "../img/globe.png"
        //     fillMode: Image.PreserveAspectFit
        //     width: 400
        //     height: 400
        //     anchors.left: parent.left
        //     anchors.horizontalCenter: parent.horizontalCenter
        // }

        // TEXT FIELD USERNAME
        TextField{
            id: usernameField
            width: 300
            text: qsTr("")
            selectByMouse: true
            placeholderText: qsTr("Your username or email")
            verticalAlignment: Text.AlignVCenter
            Layout.alignment: Qt.AlignHCenter
        }

        // TEXT FIELD USERNAME
        TextField{
            id: passwordField
            width: 300
            text: qsTr("")
            selectByMouse: true
            placeholderText: qsTr("Your password")
            verticalAlignment: Text.AlignVCenter
            Layout.alignment: Qt.AlignHCenter
            echoMode: TextInput.Password
        }

        Button {
            id: buttonLogin
            width: 300
            text: qsTr("Login")
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                console.log("Button clicked")
                backend.login(inputValues)
            }
        }

        Text {
            id: signUpLink
            text: qsTr('Don\'t have a USGS account? <a href="https://ers.cr.usgs.gov/register">Register here.</a>')
            onLinkActivated: Qt.openUrlExternally(link)
            Layout.alignment: Qt.AlignHCenter
        }
    }
    
    Connections {
        target: backend

        function onSignalLogin(boolValue, apiKey) {
            if (boolValue) {
                loginWindow.close()

                let component = Qt.createComponent("MapWindow.qml")
                let win = component.createObject()
                win.apiKey = apiKey
                backend.createMapBackend(win)
                console.log("Backend in login signal: ")
                console.log(backend.createMapBackend(win))
            } else{
                // CHANGE USER COLOR
                usernameField.Material.foreground = Material.Pink
                usernameField.Material.accent = Material.Pink
                passwordField.Material.foreground = Material.Pink
                passwordField.Material.accent = Material.Pink
            }
        }
    }

    Connections {
        target: backend

        function onSignalBackend(win, backend) {
            console.log("Backend in login signal: ");
            console.log(backend);
            win.backend = backend
            win.show();
        }
    }

}
