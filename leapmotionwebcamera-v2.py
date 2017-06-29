import numpy as np
import cv2
import sys
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture



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

def main():
    controller = Leap.Controller()
    """controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Initial Intrinsic Camaera Parameters
    # the resolution is 1280x720,
    cm0 = np.float32([[  1.25542912e+03,   0.00000000e+00,   6.39500000e+02],
           [  0.00000000e+00,   1.23283056e+03,   3.59500000e+02],
           [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
    dist0 = np.float32([[ 0.54520465, -1.47166739,  0.02451086, -0.02110954,  1.96975927]])


    cm=None
    #test points are 5 * 3
    #test_pos=[(0.1+(1.0*i/4)*0.8,0.1+(1.0*j/2)*0.8) for i in range(5) for j in range(3)]

    #test points are 5 * 5
    test_pos=[(0.1+(1.0*i/4)*0.8,0.1+(1.0*j/4)*0.8) for i in range(5) for j in range(5)]

    result = []
    screen_pos = []

    # opencv related content
    cv2.startWindowThread()
    cap = cv2.VideoCapture(3)
    #ret = cap.set(3,1280);
    #ret = cap.set(4,720);
    ret = cap.set(3,960);
    ret = cap.set(4,720);

    idx = 0

    while(True):
        ret, img = cap.read()
        H, W = img.shape[:2]
        keycode = cv2.waitKey(1) & 0xff
        frame = controller.frame()
        tip = None

        if len(frame.hands) > 0:
            hand1 = frame.hands[0]
            fingers = hand1.fingers.finger_type(1)
            if len(fingers):
                #use first fingertip's position for calibration, so make sure only show one fingertip during calibration
                tip = fingers[0].tip_position
        else:
            pass

        if keycode == ord('q'):
            break;
        elif keycode == ord(' '):
            if tip:
                screen_pos.append((int(test_pos[idx][0]*W), int(test_pos[idx][1]*H)))

                result.append((tip[0], tip[1], tip[2]))
                idx += 1
                if idx >= len(test_pos):
                    idx = 0
        cv2.circle(img, (int(test_pos[idx][0]*W), int(test_pos[idx][1]*H)), 10, (0,0,255) if tip else (255,0,0), -1)
        img = cv2.flip(img, 1)
        cv2.imshow('frame', img)

    cv2.destroyWindow('frame')
    cap.release()
    controller.clear_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)


    screen_pos2 = [(W-1-x, y) for (x,y) in screen_pos]

    retval, cm, dist, rvec, tvec = cv2.calibrateCamera(np.float32([result]), \
                                                   np.float32([screen_pos]), (W, H), cm0.copy(), dist0.copy(),\
                                                   flags=cv2.CALIB_USE_INTRINSIC_GUESS)

    np.set_printoptions(threshold='nan')
    np.set_printoptions(suppress = True)

    print retval, rvec, tvec, cm, dist"""


    #test the projections
    retval = 16.826
    rvec = np.float32([[[0.09729],[-1.89334],[-2.54269]]])
    tvec = np.float32([[[8.28679],[-41.54688],[-5.01759]]])
    cm = np.float32([[778.88388, 0, 469.63578],[0, 801.50064, 553.11922],[0,0,1]])
    dist = np.float32([[0.73277, -1.95912, 0.08203, 0.00496, 1.30627]])

    """retval = 8.02756
    rvec = np.float32([[[0.010405],[-2.291228],[-2.152310]]])
    tvec = np.float32([[[4.852279],[-39.95777],[23.757688]]])
    cm = np.float32([[914.648037, 0, 467.4740700],[0, 915.239926, 207.621896],[0,0,1]])
    dist = np.float32([[-0.573064, 1.2334596, -0.0372897, -0.03753238, -0.947574]])"""

    """retval = 50.1596
    rvec = np.float32([[[1.50373942],[0.14284951],[-0.12614873]]])
    tvec = np.float32([[[-62.30916795],[-19.56128693],[-4817.38957097]]])
    cm = np.float32([[10610.2934361,0.,344.41161879],[ 0.,10053.06582873,168.95419919],[0,0,1]])
    dist = np.float32([[1048.68418025,-643322.9091576,3.91323224,3.45493043,8159.42009355]])"""


    """retval = 35.0234082148
    rvec = np.float32([[[1.43909934],[0.10473613],[-0.09349311]]])
    tvec = np.float32([[[219.75664907],[-267.88726673],[-2967.68486709]]])
    cm = np.float32([[9031.4738709,0.,1411.13392706],[0.,4292.10987202,-402.58906935],[0.,0.,1.]])
    dist = np.float32([[28.22682829,-2199.33684929,1.99013351,0.55428915,38236.54786816]])"""


    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    # opencv related content
    cv2.startWindowThread()
    cap = cv2.VideoCapture(2)
    #ret = cap.set(3,1280);
    #ret = cap.set(4,720);
    #ret = cap.set(3,960);
    #ret = cap.set(4,720);
    ret = cap.set(3,1920);
    ret = cap.set(4,1280);

    while(True):
        ret, img = cap.read()
        H, W = img.shape[:2]
        keycode = cv2.waitKey(1) & 0xff
        frame = controller.frame()

        tip = None
        for hand1 in frame.hands:
            for f in hand1.fingers:
                for bn in range(3):
                    bone = f.bone(bn)
                    if bone.is_valid:
                        xy1 = cv2.projectPoints(np.float32([to_np(bone.prev_joint)]), rvec[0], tvec[0], cm, dist)[0][0][0]
                        xy2 = cv2.projectPoints(np.float32([to_np(bone.next_joint)]), rvec[0], tvec[0], cm, dist)[0][0][0]
                        #print xy1
                        try:
                            cv2.line(img, (xy1[0],xy1[1]) , (xy2[0],xy2[1]), (255,255,255) , 3)
                            cv2.circle(img, (xy1[0],xy1[1]), 5, (255,255,128), -1)
                            cv2.circle(img, (xy2[0],xy2[1]), 5, (255,255,128), -1)
                        except:
                            pass
            #indicate the index finger
            for f in hand1.fingers.finger_type(1):
                tip = f.tip_position
                xy = cv2.projectPoints(np.float32([(tip[0], tip[1], tip[2])]), rvec[0], tvec[0], cm, dist)[0][0][0]
                try:
                    cv2.circle(img, (xy[0],xy[1]), 10, (0,0,255), -1)
                except:
                    pass

        if  keycode == ord('q'):
            break
        #img = cv2.flip(img, 1)
        cv2.imshow('frame', img)
    cv2.destroyWindow('frame')
    cap.release()
    controller.clear_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        #controller.remove_listener(listener)
        pass

if __name__ == "__main__":
    main()
