import cv2
import cv2 as cv

img = cv.imread('IMG-20211028-WA0206.jpg', 1)

new_img = cv.line(img, (0, 600), (600, 0), (255, 0, 0), 5)

cv.imshow("image", new_img)
cv.waitKey(0)
cv.destroyAllWindows()
# cap = cv.VideoCapture(0)
# fourcc = cv.VideoWriter_fourcc(*"XVID")
# output = cv.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
# print(cap.isOpened())
#
#
# while cap.isOpened():
#     # check is a boolean that checks if a frame is available
#     # frame is the variable in which the camera frame is saved if present.
#     check, frame = cap.read()
#     if check:
#         # convert a frame to a gray scale
#         output.write(frame)
#         gray = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)
#         cv.imshow("video recorder", gray)
#         key = cv.waitKey(1)
#         if key & 0xFF == ord("q"):
#             break
#     else:
#         break
# cap.release()
# output.release()
# cv.destroyAllWindows()
