import cv2
from picamera2 import Picamera2

ARUCO_DICT = {
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
}

aruco_type = "DICT_6X6_250"

arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (1280, 720)}))
picam2.start()

def multitargetCenter(cordinates):
	X, Y = zip(*cordinates)
	center = (sum(X)/len(X), sum(Y)/len(Y))
	return center

def aruco_display(corners, ids, rejected, image):
	relX, relY = None, None

	if len(corners) > 0:
		ids = ids.flatten()
		if len(corners) == 4:
			for (markerCorner, markerID) in zip(corners, ids):
				markerCorners = markerCorner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = markerCorners

				topRight = (int(topRight[0]), int(topRight[1]))
				bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
				bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
				topLeft = (int(topLeft[0]), int(topLeft[1]))

				cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
				cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
				cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
				cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

				cX = int((topLeft[0] + bottomRight[0]) / 2.0)
				cY = int((topLeft[1] + bottomRight[1]) / 2.0)
				

				relX = cX - 640
				relY = -(cY - 360)

				cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

				cv2.putText(image, str(markerID), (topLeft[0], topLeft[1] - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
				cv2.putText(image, f"({cX}, {cY})", (cX + 10, cY - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

				#print(f"Marker ID {markerID} | Center: ({cX}, {cY})")
	

		else:
			cordinates = []
			for (markerCorner, markerID) in zip(corners, ids):
				markerCorners = markerCorner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = markerCorners

				topRight = (int(topRight[0]), int(topRight[1]))
				bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
				bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
				topLeft = (int(topLeft[0]), int(topLeft[1]))

				cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
				cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
				cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
				cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

				cX = int((topLeft[0] + bottomRight[0]) / 2.0)
				cY = int((topLeft[1] + bottomRight[1]) / 2.0)
				
				relCord = [cX, cY]
				cordinates.append(relCord)

				relX = cX - 640
				relY = -(cY - 360)

				cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

				cv2.putText(image, str(markerID), (topLeft[0], topLeft[1] - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
				cv2.putText(image, f"({cX}, {cY})", (cX + 10, cY - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

				#print(f"Marker ID {markerID} | Center: ({cX}, {cY})")

			center = multitargetCenter(cordinates)
			cv2.circle(image, (int(center[0]), int(center[1])), 4, (255, 255, 0), -1)

			relX = int(center[0]) - 640
			relY = -(int(center[1]) - 360)

	return image,relX,relY

def get_frame(tracking):
	if tracking:
		img = picam2.capture_array()
		corners, ids, rejected = detector.detectMarkers(img)
		output,x,y = aruco_display(corners, ids, rejected, img)
		if output is None:
			output = img
		output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
		return output,x,y
	else:
		noWork = picam2.capture_array()
		noWork = cv2.cvtColor(noWork, cv2.COLOR_RGB2BGR)
		return noWork,0,0

def stop():
    picam2.stop()
