import cv2 as cv
import time
from backend import send_email

# Constants
VIDEO_CAPTURE_INDEX = 0
THRESHOLD_VALUE = 60
MIN_CONTOUR_AREA = 5000

# Variable to track object presence
object_in_frame = False

def main():
    global object_in_frame  # Use the global variable

    video = cv.VideoCapture(VIDEO_CAPTURE_INDEX)

    # Check if the video capture was successful
    if not video.isOpened():
        print("Error: Could not open video capture.")
        return

    time.sleep(1)
    first_frame = None

    while True:
        check, frame = video.read()
        if not check:
            break

        grey_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        grey_frame_gau = cv.GaussianBlur(grey_frame, (21, 21), 0)

        if first_frame is None:
            first_frame = grey_frame_gau

        delta_frame = cv.absdiff(first_frame, grey_frame_gau)

        # Apply thresholding to create a binary frame
        threshold_frame = cv.threshold(delta_frame, THRESHOLD_VALUE, 255, cv.THRESH_BINARY)[1]

        # Remove noise with dilation
        dil_frame = cv.dilate(threshold_frame, None, iterations=2)

        # Find contours
        contours, _ = cv.findContours(dil_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Check if any object is present in the frame
        object_in_current_frame = False

        for contour in contours:
            if cv.contourArea(contour) < MIN_CONTOUR_AREA:
                continue
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            object_in_current_frame = True

        # If an object was previously in the frame but not anymore, send an email
        if object_in_frame and not object_in_current_frame:
            send_email(email_message="An object has left your screen")

        object_in_frame = object_in_current_frame  # Update the object_in_frame variable

        cv.imshow("Object Detector", frame)
        key = cv.waitKey(1)
        if key == ord("q"):
            break

    video.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
