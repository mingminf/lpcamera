import numpy as np
import cv2
import sys
import Leap, sys, thread, time
import datetime
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from scipy.spatial import distance

DEBUG = False

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "initialized"

    def on_connect(self, controller):
        print "leap motion connected"
        #controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        #controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

        controller.config.set("Gesture.KeyTap.MinDownVelocity", 5.0)
        controller.config.set("Gesture.KeyTap.HistorySeconds", .3)
        controller.config.set("Gesture.KeyTap.MinDistance", 0.5)
        controller.config.save()

        controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "leap motion disconnected"

    def on_exit(self, controller):
        print "exited"

    def on_frame(self, controller):
        self.frame = controller.frame()

def to_np(v):
    return np.float32([v[0], v[1], v[2]])


def dis(v1, v2):
    return distance.euclidean(v1,v2)

def main():
    controller = Leap.Controller()
    #test the projections

    retval = 13.239646902
    rvec = np.float32([[[ 0.04057411],
           [ 1.93823599],
           [ 2.4833007 ]]])
    tvec = np.float32([[[  8.46050102],
    [-45.35019832],
    [  6.36817543]]])
    cm = np.float32([[ 1558.25767175,     0. ,          962.81545469],
[    0. ,         1715.42003938 ,  860.64197358],
[    0.  ,           0.  ,           1.        ]])
    dist = np.float32([[-0.14262444,  0.88573637,  0.07492765, -0.00911298, -1.1421962 ]])


    #this parameters are for the other LP
    """retval = 12.4304243285
    rvec = np.float32([[[-0.07403326],
           [ 2.15789327],
           [ 2.24751369]]])
    tvec = np.float32([[[ 11.12213436],
    [-44.35437003],
    [ 13.63024487]]])
    cm = np.float32([[ 1518.47267182,     0.,           949.56413171],
[    0.,          1491.83826716,   491.15957871],
[    0.,             0.,             1.        ]])
    dist = np.float32([[-0.18717047,  2.01084122,  0.01116464,  0.0163355,  -4.53963572]])"""

    if DEBUG:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG') #"XVID" was tested and it did not work
        localtime = time.strftime("%H-%M-%S-%d-%m-%Y")
        outputvideo = cv2.VideoWriter('videoinstructions_'+ localtime +'.avi', fourcc, 20, (1920,1080))
        #outputvideo = cv2.VideoWriter('videoinstructions.avi', fourcc, 20, (640,480))

    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    # opencv related content
    cv2.startWindowThread()
    cap = cv2.VideoCapture(2)
    #ret = cap.set(3,640);
    #ret = cap.set(4,480);
    #ret = cap.set(3,1280);
    #ret = cap.set(4,720);
    #ret = cap.set(3,960);
    #ret = cap.set(4,720);
    ret = cap.set(3,1920);
    ret = cap.set(4,1280);

    colors = [(255,255,0),(255,0,0),(0,255,0),(255,0,255)]


    while(True):
        ret, img = cap.read()
        #H, W = img.shape[:2]
        frame = controller.frame()

        tip = None

        for hand1 in frame.hands:
            tip_pos = to_np([0,0,0])
            max_dis = 0
            hand_center = hand1.stabilized_palm_position #__palm_position
            for f in hand1.fingers:
                for bn in range(4):
                    bone = f.bone(bn)
                    if bone.is_valid:
                        if dis(to_np(bone.prev_joint), to_np(hand_center)) > max_dis:
                            max_dis =  dis(to_np(bone.prev_joint), to_np(hand_center))
                            tip_pos = to_np(bone.prev_joint)
                        xy1 = cv2.projectPoints(np.float32([to_np(bone.prev_joint)]), rvec[0], tvec[0], cm, dist)[0][0][0]
                        xy2 = cv2.projectPoints(np.float32([to_np(bone.next_joint)]), rvec[0], tvec[0], cm, dist)[0][0][0]
                        """if bn == 3:
                            tip = (xy1[0],xy1[1])
                            #indicate the index finger
                            cv2.circle(img, tip, 15, (0,0,255), -1)"""
                        try:
                            cv2.line(img, (xy1[0],xy1[1]) , (xy2[0],xy2[1]), (255,255,255) , 3)
                            cv2.circle(img, (xy1[0],xy1[1]), 5, colors[bn], -1)
                            #cv2.circle(img, (xy2[0],xy2[1]), 5, colors[bn], -1)
                        except:
                            pass

            xy = cv2.projectPoints(np.float32([tip_pos]), rvec[0], tvec[0], cm, dist)[0][0][0]
            try:
                cv2.circle(img, (xy[0],xy[1]), 10, (0,0,255), -1)
            except:
                pass
            """for f in hand1.fingers.finger_type(1):
                tip = f.tip_position
                xy = cv2.projectPoints(np.float32([(tip[0], tip[1], tip[2])]), rvec[0], tvec[0], cm, dist)[0][0][0]
                try:
                    cv2.circle(img, (xy[0],xy[1]), 10, (0,0,255), -1)
                except:
                    pass"""


        keycode = cv2.waitKey(1) & 0xff
        if  keycode == ord('q'):
            break
        #img = cv2.flip(img, 0)
        #img = cv2.flip(img, 1)
        if DEBUG:
            outputvideo.write(img)
        cv2.imshow('frame', img)
    cv2.destroyWindow('frame')
    cap.release()
    if DEBUG:
        outputvideo.release()
    cv2.destroyAllWindows()
    controller.clear_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)


if __name__ == "__main__":
    main()
