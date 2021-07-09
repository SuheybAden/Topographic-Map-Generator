import QtQuick 2.0
import QtLocation 5.12
import QtPositioning 5.12
import QtQuick.Window 2.12
import QtQuick.Layouts 1.2
import QtQuick.Controls 1.2
import QtQuick.Controls.Material 2.15

ApplicationWindow {
	id: window
	visible: true
	width: 800
	height: 600
	title: "Topographic Map Generator"

	Material.theme: Material.Dark
	Material.accent: Material.LightBlue

	property QtObject backend
	property bool isShiftPressed: false
	property string selectionMode: "Rect"
	property var inputValues: { "selectionMode": selectionMode,
	 "circleLat": circle.center.latitude,
	 "circleLong": circle.center.longitude,
	 "topLeftRectLat": rectSelection.topLeft.latitude,
	 "topLeftRectLong": rectSelection.topLeft.longitude,
	 "bottomRightRectLat": rectSelection.bottomRight.latitude,
	 "bottomRightRectLong": rectSelection.bottomRight.longitude}

	// Sets the selection mode for the map
	function setSelectionMode(mode: string): string{
		if(mode === "Rect") {
			circle.center = QtPositioning.coordinate(0, 0)
			circle.radius = 0
			}
		else if(mode === "Circle"){
			rectSelection.topLeft = QtPositioning.coordinate(0, 0)
			rectSelection.bottomRight = QtPositioning.coordinate(0, 0)
			}
		selectionMode = mode
		mouseArea.focus = true
		}

	RowLayout {
		anchors.fill: parent

		// Main Layout containing the map
		ColumnLayout {
			id: mapLayout
			anchors.right: inputsLayout.left
			anchors.left: parent.left
			anchors.top: parent.top
			anchors.bottom: parent.bottom

			// Sets up the OpenStreetMaps plugin
			Plugin {
				id: osmPlugin
				name: "osm"
			}

			// The map widget
			Map {
				id: map
				anchors.fill: parent
				plugin: osmPlugin
				zoomLevel: 3
				
				// The circle that marks which country to generate the STL for
				MapCircle {
					id: circle
					center {
						latitude: 0
						longitude: 0
					}
					radius: 0
					color: 'green'
					border.width: 3
				}

				// The rectangle that marks what region to generate the STL for
				MapRectangle {
					id: rectSelection
					opacity: .5
					color: 'green'
					border.width: 2
					topLeft {
						latitude: 0
						longitude: 0
						}
					bottomRight {
						latitude: 0
						longitude: 0
						}
					}
			}

			// Handles mouse events in the area of the map
			MouseArea {
				id: mouseArea
				anchors.fill: parent
				focus: true

				Keys.onPressed: {
					if(event.key === Qt.Key_Shift) {
						isShiftPressed = true
						}
					}
				Keys.onReleased:{
					if(event.key === Qt.Key_Shift) {
						isShiftPressed = false
						}
					}

				onPressed: {
					if (isShiftPressed){
						if (selectionMode === "Rect") {
							mouse.accepted = true

							var topLeftCoord = map.toCoordinate(Qt.point(mouse.x, mouse.y))
							rectSelection.topLeft = topLeftCoord
							rectSelection.bottomRight = topLeftCoord
							}
						else if(selectionMode === "Circle"){
							mouse.accepted = true

							circle.center = map.toCoordinate(Qt.point(mouse.x,mouse.y))
							circle.radius = 100000
							}
						}
					}
				onPositionChanged: {
					if (isShiftPressed && selectionMode === "Rect"){
						mouse.accepted = true

						var bottomRightCoord = map.toCoordinate(Qt.point(mouse.x, mouse.y))
						rectSelection.bottomRight = bottomRightCoord
						}
					}
				}
		}

		// Side Layout for Controls
		ColumnLayout{
			id: inputsLayout
			RowLayout{
				ComboBox {
					width: 200
					currentIndex: 1

				}
				Text {
					text: "Some Text"

				}
			}
			GroupBox {
				title: "Selection Mode"

				RowLayout {       
					ExclusiveGroup {
						id: radioGroup
					}     
					RadioButton{
						text: "Within Rectangle"
						checked: true
						exclusiveGroup: radioGroup
						onClicked: setSelectionMode("Rect")
					}
					RadioButton{
						text: "By Country"
						exclusiveGroup: radioGroup
						onClicked: setSelectionMode("Circle")
					}
				}
			}
			RowLayout {
				Button {
					text: "Generate STL"
					onClicked: {
						backend.generate_mesh(inputValues)
					}
				}
			}
		}
	}
}

