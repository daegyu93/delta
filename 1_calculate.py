import cv2
import numpy as np
import glob
import sys

def main(argv):
    CHECKERBOARD = (6,8)
    device_num = argv[1]
    cam_dir = 'cam_' + str(device_num) + '/'

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objpoints = []
    imgpoints = [] 
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    prev_img_shape = None

    images = glob.glob(cam_dir + '*.png')
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray,
                                                CHECKERBOARD,
                                                cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
            imgpoints.append(corners2)

    cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    height, width = img.shape[:2]
    fx, fy, cx, cy = mtx[0,0], mtx[1,1], mtx[0,2], mtx[1,2]
    focal_length = (fx + fy)/2
    k0, k1, p0, p1, k2 = dist[0]

    print('focal-length=', focal_length)
    print('src-x0=', cx)
    print('src-y0=', cy)
    print('distortion=',k0,';',k1,';',k2,';',p0,';',p1)

    #save dewarper_config.txt
    f = open('cam_' + str(device_num) + '/dewarper_config.txt', 'w')
    # [property]
    # output-width=1920
    # output-height=1080
    # num-batch-buffers=1
    f.write('[property]\n')
    f.write('output-width=1920\n')
    f.write('output-height=1080\n')
    f.write('num-batch-buffers=1\n')
    f.write('\n')

    # [surface0]
    # projection-type=3
    # width=1920
    # height=1080
    # focal-length=733.1000
    # distortion= -0.2725762476997752;0.06077245841636788;-0.0055581754220842446;-0.0005782749923515222;0.000701124461693587
    # src-x0=936.337
    # src-y0=580.864
    f.write('[surface0]\n')
    f.write('projection-type=3\n')
    f.write('width=1920\n')
    f.write('height=1080\n')
    f.write('focal-length=' + str(focal_length) + '\n')
    f.write('distortion=' + str(k0) + ';' + str(k1) + ';' + str(k2) + ';' + str(p0) + ';' + str(p1) + '\n')
    f.write('src-x0=' + str(cx) + '\n')
    f.write('src-y0=' + str(cy) + '\n')


if __name__ == "__main__":
    main(sys.argv)