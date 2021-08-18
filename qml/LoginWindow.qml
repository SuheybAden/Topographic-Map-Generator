import QtQuick 2.0
import QtQuick.Window 2.12
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: loginWindow
    visible: true
    width: 800
    height: 600
    title: "Login Window"

    Material.theme: Material.Dark
    Material.accent: Material.LightBlue

    property QtObject backend
    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.Dialog | Qt.WindowTitleHint
}