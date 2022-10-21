import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui
import math


def distance(point1, point2):

    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt(abs((x2-x1)**2-(y2-y1)**2))


def blinkRatio(landmarks, eye):
    # horizontal points of right eye
    rh_right = landmarks[eye[0]]
    rh_left = landmarks[eye[8]]

    # vertical points of right eye

    rv_top = landmarks[eye[12]]
    rv_bottom = landmarks[eye[4]]
    rh_distance = distance(rh_right, rh_left)
    rv_distance = distance(rv_top, rv_bottom)+0.001

    return rh_distance/rv_distance
FACE_OVAL=[ 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]


# creating the facemesh
LIPS=[ 61, 146, 91, 181, 84, 17, 314, 405, 321, 375,291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78 ]

mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390,
            249, 263, 466, 388, 387, 386, 385, 384, 398]
LEFT_EYEBROW = [336, 296, 334, 293, 300, 276, 283, 282, 295, 285]
RIGHT_IRIS = [469, 470, 471, 472]
LEFT_IRIS = [474, 475, 476, 477]
# right eyes indices
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154,
             155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYEBROW = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]

cap = cv.VideoCapture(0)
pos_mousex = pyautogui.position()[0]
pos_mousey = pyautogui.position()[1]
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as face_mesh:

    while True:
        # pyautogui.moveTo(pos_mousex,pos_mousey)
        ret, frame = cap.read()
        if not ret:
            break
        # flipping the image in order to see it properly
        fram = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]  # Skipping some

        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            # print(results.multi_face_landmarks[0].landmark)
            mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(
                int) for p in results.multi_face_landmarks[0].landmark])
            # print(mesh_points[LEFT_IRIS])
            # if(mesh_points[LEFT_IRIS][0][0]>380 and mesh_points[LEFT_IRIS][0][0]<405):
            #     pos_mousex+=10
            # elif(mesh_points[LEFT_IRIS][0][0]<380 and mesh_points[LEFT_IRIS][0][0]>360):
            #     pos_mousex-=10
            # pyautogui.moveTo(
            #     int(mesh_points[LEFT_EYE][0][0])*3, int(mesh_points[LEFT_EYE][0][1])*3)
            eyebrows=distance((mesh_points[RIGHT_EYE][12][0],mesh_points[RIGHT_EYE][12][1]),(mesh_points[RIGHT_EYEBROW][2][0],mesh_points[RIGHT_EYEBROW][2][1]))
            print(eyebrows)
            if(blinkRatio(mesh_points, RIGHT_EYE) > 11 and blinkRatio(mesh_points, LEFT_EYE)<6):
                pyautogui.press("d")
            if(blinkRatio(mesh_points, LEFT_EYE) > 11 and blinkRatio(mesh_points, RIGHT_EYE)<6):
                pyautogui.press("a")
            if(blinkRatio(mesh_points, RIGHT_EYE) > 6 and blinkRatio(mesh_points, LEFT_EYE)>6):
                pyautogui.press("s")
            if(eyebrows>35 and blinkRatio(mesh_points, RIGHT_EYE) <6 and blinkRatio(mesh_points, LEFT_EYE)<6):
                pyautogui.press("w")
            # print(distance((int((mesh_points[LEFT_EYEBROW][4][1]+mesh_points[RIGHT_EYEBROW][0][0])/2),mesh_points[FACE_OVAL][0][0]),(int((mesh_points[LEFT_EYEBROW][4][1]+aa[RIGHT_EYEBROW][0][1])/2),mesh_points[FACE_OVAL][0][1])))

            # cv.polylines(frame, [mesh_points[LEFT_IRIS]],
            #              True, (0, 255, 0), 1, cv.LINE_AA)
            # cv.polylines(frame, [mesh_points[RIGHT_IRIS]],
            #              True, (0, 255, 0), 1, cv.LINE_AA)
            cv.circle(frame, (mesh_points[RIGHT_EYE][12][0],mesh_points[RIGHT_EYE][12][1]), radius=3, color=(0, 0, 255), thickness=-1)
            # cv.circle(frame, (int((mesh_points[LEFT_EYEBROW][4][0]+mesh_points[RIGHT_EYEBROW][0][0])/2),int((mesh_points[LEFT_EYEBROW][4][1]+mesh_points[RIGHT_EYEBROW][0][1])/2)), radius=3, color=(0, 0, 255), thickness=-1)
            cv.circle(frame, (mesh_points[RIGHT_EYEBROW][2][0],mesh_points[RIGHT_EYEBROW][2][1]), radius=3, color=(0, 0, 255), thickness=-1)
            

            
        cv.imshow("fame", frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
cap.release()
cv.destroyAllWindows()
