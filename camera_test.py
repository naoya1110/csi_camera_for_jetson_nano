import cv2
import time


def gstreamer_pipeline(sensor_id=0, exposure=500000, capture_width=1280, capture_height=720, 
                       display_width=640, display_height=360, framerate=120, flip_method=0):    
	pipeline = f"nvarguscamerasrc sensor-id={sensor_id} exposuretimerange='{int(exposure)} {int(exposure)+1}' !\
				video/x-raw(memory:NVMM), width=(int){capture_width}, height=(int){capture_height}, \
				framerate=(fraction){framerate}/1 ! nvvidconv flip-method={flip_method} ! \
				video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! \
				videoconvert ! video/x-raw, format=(string)BGR ! appsink"
	return(pipeline)


def main():
	pipeline = gstreamer_pipeline(exposure=3.5E+4)
	print(pipeline)

	cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
	old_time = time.time()
	
	if cap.isOpened():
		try:
			while True:
				ret, frame = cap.read()
				new_time = time.time()
				dt = new_time - old_time
				old_time = new_time
				fps = 1/dt
				cv2.putText(frame, f'FPS {fps:.1f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
							fontScale=0.8, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_4) 
				cv2.imshow("camera", frame)

				k = cv2.waitKey(1)
				if k == 27 or k == ord('q'): break
		        
		finally:
			cap.release()
			cv2.destroyAllWindows()
	else:
		print("Error: Unable to open camera")


if __name__ == "__main__":
    main()
