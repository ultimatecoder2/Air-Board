from flask import Flask, render_template, Response
import cv2
import numpy as np
import time
import os
import mediapipe as mp
import HandTrackingModule as htm

app=Flask(__name__)
#######################
brushThickness = 25
eraserThickness = 100
########################

cap = cv2.VideoCapture(0)

def gen_frames():
    folderPath = "Header"
    myList = os.listdir(folderPath)
    # print(myList)
    overlayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    # print(len(overlayList))
    header = overlayList[0]
    drawColor = (255, 0, 255)
    cap.set(3, 1280)
    cap.set(4, 720)
    # cap.set(3, 1300)
    # cap.set(4, 800)
    detector = htm.handDetector(detectionCon=0.65,maxHands=1)
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    xp, yp = 0, 0
    # imgCanvas = np.zeros((1300, 800, 3), np.uint8)

    while True:
        

        # 1. Import image
        success, img = cap.read()
        if not success:
            break
        
        img = cv2.flip(img, 1)

        # 2. Find Hand Landmarks
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        print(lmList)

        if len(lmList) != 0:

            # print(lmList)

            # tip of index and middle fingers
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            # print(fingers)

            # 4. If Selection Mode - Two finger are up
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                print("Selection Mode")
                # # Checking for the click
                if y1 < 125:
                    if 250 < x1 < 450:
                        header = overlayList[0]
                        drawColor = (255, 0, 255)
                    elif 550 < x1 < 750:
                        header = overlayList[1]
                        drawColor = (255, 0, 0)
                    elif 800 < x1 < 950:
                        header = overlayList[2]
                        drawColor = (0, 255, 0)
                    elif 1050 < x1 < 1200:
                        header = overlayList[3]
                        drawColor = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

            # 5. If Drawing Mode - Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                # cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1


            # # Clear Canvas when all fingers are up
            if all (x >= 1 for x in fingers):
                xp, yp = 0, 0
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)
                # imgCanvas = np.zeros((1300, 800, 3), np.uint8)

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img,imgInv)
        img = cv2.bitwise_or(img,imgCanvas)


        # Setting the header image
        img[0:125, 0:1280] = header
        # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
        
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        
        
        # cv2.imshow("Image", img)
        # cv2.waitKey(1)

# def gen_frames():  
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             # Resize frame of video to 1/4 size for faster face recognition processing
#             small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#             # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#             rgb_small_frame = small_frame[:, :, ::-1]

#             # Only process every other frame of video to save time
           
#             # Find all the faces and face encodings in the current frame of video
#             face_locations = face_recognition.face_locations(rgb_small_frame)
#             face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#             face_names = []
#             for face_encoding in face_encodings:
#                 # See if the face is a match for the known face(s)
#                 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#                 name = "Unknown"
#                 # Or instead, use the known face with the smallest distance to the new face
#                 face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)
#                 if matches[best_match_index]:
#                     name = known_face_names[best_match_index]

#                 face_names.append(name)
            

#             # Display the results
#             for (top, right, bottom, left), name in zip(face_locations, face_names):
#                 # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#                 top *= 4
#                 right *= 4
#                 bottom *= 4
#                 left *= 4

#                 # Draw a box around the face
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#                 # Draw a label with a name below the face
#                 cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)