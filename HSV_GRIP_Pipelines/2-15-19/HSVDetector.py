import libjevois as jevois
import cv2
import numpy as np
import time
import math

class HSVDetector:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois S to measure our processing framerate:
        # self.timer = jevois.Timer("sandbox", 100, jevois.LOG_INFO)

        self.outimg = None

        # SPECIAL REPLACED BLUR CONSTANT
        self.__blur_type = 0

    # ###################################################################################################
        # ALL CONSTANTS GO UNDER HERE (make sure to remove the self.__blur_type line)

        self.__blur_radius = 0.0

        self.blur_output = None

        self.__desaturate_input = self.blur_output

        self.desaturate_output = None

        self.__cv_threshold_src = self.desaturate_output
        self.__cv_threshold_thresh = 11.0
        self.__cv_threshold_maxval = 50.0
        self.__cv_threshold_type = cv2.THRESH_BINARY

        self.cv_threshold_output = None

        self.__mask_input = self.blur_output
        self.__mask_mask = self.cv_threshold_output

        self.mask_output = None

        self.__hsv_threshold_input = self.mask_output
        self.__hsv_threshold_hue = [36.27118644067796, 94.58612561006309]
        self.__hsv_threshold_saturation = [196.60325001916027, 255.0]
        self.__hsv_threshold_value = [12.295051442726924, 58.89891588922344]

        self.hsv_threshold_output = None

        self.__cv_erode_src = self.hsv_threshold_output
        self.__cv_erode_kernel = None
        self.__cv_erode_anchor = (-1, -1)
        self.__cv_erode_iterations = 2.0
        self.__cv_erode_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_bordervalue = (-1)

        self.cv_erode_output = None

        self.__cv_dilate_src = self.cv_erode_output
        self.__cv_dilate_kernel = None
        self.__cv_dilate_anchor = (-1, -1)
        self.__cv_dilate_iterations = 5.0
        self.__cv_dilate_bordertype = cv2.BORDER_CONSTANT
        self.__cv_dilate_bordervalue = (-1)

        self.cv_dilate_output = None

        self.__find_contours_input = self.cv_dilate_output
        self.__find_contours_external_only = True

        self.find_contours_output = None

        self.__convex_hulls_contours = self.find_contours_output

        self.convex_hulls_output = None

        self.__filter_contours_contours = self.convex_hulls_output
        self.__filter_contours_min_area = 150.0
        self.__filter_contours_min_perimeter = 0.0
        self.__filter_contours_min_width = 0.0
        self.__filter_contours_max_width = 100000.0
        self.__filter_contours_min_height = 0.0
        self.__filter_contours_max_height = 100000.0
        self.__filter_contours_solidity = [0.0, 100.0]
        self.__filter_contours_max_vertices = 10000.0
        self.__filter_contours_min_vertices = 0.0
        self.__filter_contours_min_ratio = 0.0
        self.__filter_contours_max_ratio = 100.0

        self.filter_contours_output = None

        # self.start_time = 0
        # self.end_time = 0

        # END CONSTANTS
    # ###################################################################################################

    ## Process function with USB output

    def processNoUSB(self, inframe):
        source0 = inimg = inframe.getCvBGR()
        self.outimg = inimg = inframe.getCvBGR()

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        # self.timer.start()
        # self.start_time = time.time()

#################################################################################################

        # BEGIN GRIP CODE

#################################################################################################
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step Blur0:
        self.__blur_input = source0
        (self.blur_output) = self.__blur(self.__blur_input, self.__blur_type, self.__blur_radius)

        # Step HSV_Threshold0:
        self.__hsv_threshold_input = self.blur_output
        (self.hsv_threshold_output) = self.__hsv_threshold(self.__hsv_threshold_input, self.__hsv_threshold_hue, self.__hsv_threshold_saturation, self.__hsv_threshold_value)

        # Step CV_erode0:
        self.__cv_erode_src = self.hsv_threshold_output
        (self.cv_erode_output) = self.__cv_erode(self.__cv_erode_src, self.__cv_erode_kernel, self.__cv_erode_anchor, self.__cv_erode_iterations, self.__cv_erode_bordertype, self.__cv_erode_bordervalue)

        # Step CV_dilate0:
        self.__cv_dilate_src = self.cv_erode_output
        (self.cv_dilate_output) = self.__cv_dilate(self.__cv_dilate_src, self.__cv_dilate_kernel, self.__cv_dilate_anchor, self.__cv_dilate_iterations, self.__cv_dilate_bordertype, self.__cv_dilate_bordervalue)

        # Step Find_Contours0:
        self.__find_contours_input = self.cv_dilate_output
        (self.find_contours_output) = self.__find_contours(self.__find_contours_input, self.__find_contours_external_only)

        # Step Filter_Contours0:
        self.__filter_contours_contours = self.find_contours_output
        (self.filter_contours_output) = self.__filter_contours(self.__filter_contours_contours, self.__filter_contours_min_area, self.__filter_contours_min_perimeter, self.__filter_contours_min_width, self.__filter_contours_max_width, self.__filter_contours_min_height, self.__filter_contours_max_height, self.__filter_contours_solidity, self.__filter_contours_max_vertices, self.__filter_contours_min_vertices, self.__filter_contours_min_ratio, self.__filter_contours_max_ratio)

#################################################################################################

        # END GRIP CODE

##################################################################################################

        # DEFAULT CUSTOM CODE

        def getArea(con): # Gets the area of the contour
            return cv2.contourArea(con)

        def getYcoord(con): # Gets the Y coordinate of the contour center
            M = cv2.moments(con)
            cy = int(M['m01']/M['m00'])
            return cy

        def getXcoord(con): # Gets the X coordinate of the contour center
            M = cv2.moments(con)
            cy = int(M['m10']/M['m00'])
            return cy

        def sortByArea(conts) : # Returns an array sorted by area from smallest to largest
            contourNum = len(conts) # Gets number of contours
            sortedBy = sorted(conts, key=getArea) # sortedBy now has all the contours sorted by area
            return sortedBy

##################################################################################################

        # PUT YOUR CUSTOM CODE HERE

##################################################################################################

        CAMERA_MATRIX = np.array([[332.75, 0, 160],
                                 [0, 332.77, 120],
                                 [0,0,1]])

        OBJ_POINTS = [(149, 67), (123, 59), (139, 5), (166 , 13)]

        def solvePnP(imgPoints):
            rvec, tvec = cv2.solvePnP(OBJ_POINTS, imgPoints, CAMERA_MATRIX, None)
            return(rvec, tvec)

        def draw(img, corners, rvec, tvec):
            axis = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0], 
            [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])

            imgpts, jac = cv2.projectPoints(axis, rvec, tvec, CAMERA_MATRIX, None)

            imgpts = np.int32(imgpts).reshape(-1,2)
            # draw ground floor in green
            img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
            # draw pillars in blue color
            for i,j in zip(range(4),range(4,8)):
                img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
            # draw top layer in red color
            img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

            return img

        def getContourCorners(cnt):
            contour_rect = cv2.minAreaRect(cnt)
            contour_corners = cv2.boxPoints(contour_rect)
            contour_corners = np.int0(contour_corners)
            return contour_corners
        
        def sortByPosition(conts):
            sortedBy = sorted(conts, key=getXcoord)
            return sortedBy

        # checks if the contour is tilted to the right based on y-differences
        def get_orientation(cnt): 
            contour_rect = cv2.minAreaRect(cnt)
            contour_corners = cv2.boxPoints(contour_rect)
            contour_corners = np.int0(contour_corners)

            contour_ab = contour_corners[0][1] - contour_corners[1][1]
            contour_ad = contour_corners[0][1] - contour_corners[3][1]
            
            # 1 is oriented left, 2 is right, 3 is vertical
            if(contour_ab < contour_ad):
                return 1
            elif(contour_ab > contour_ad):
                return 2
            elif(contour_corners[2][0] == contour_corners[1][0] or contour_corners[2][1] == contour_corners[2][1]):
                return 3
    
        def getTwoContourCenter(left_contour, right_contour):
            center_x = (getXcoord(left_contour) + getXcoord(right_contour)) / 2
            center_y = (getYcoord(left_contour) + getYcoord(right_contour)) / 2
            return(center_x, center_y)

        def getXCenter(left_contour, right_contour):
            return getTwoContourCenter(left_contour, right_contour)[0]

        def getYCenter(left_contour, right_contour):
            return getTwoContourCenter(left_contour, right_contour)[1]

        def drawRectContours(left_contour, right_contour):
            center_x, center_y = getTwoContourCenter(left_contour, right_contour)
            center = (int(center_x), int(center_y))

            left_rect = cv2.minAreaRect(left_contour)
            left_box = cv2.boxPoints(left_rect)
            left_box = np.int0(left_box)

            right_rect = cv2.minAreaRect(right_contour)
            right_box = cv2.boxPoints(right_rect)
            right_box = np.int0(right_box)

            cv2.circle(self.outimg,center, 5, (0,0,255), 2)
            cv2.drawContours(self.outimg,[left_box],0,(255,0,0),2)
            cv2.drawContours(self.outimg,[right_box],0,(0,0,255),2)

        def getTargetYDegrees():
            m_focalLength = (320 / 2) / math.tan(math.radians(55 / 2))
            pixel_y = 120 - getYCenter(left_contour, right_contour)            
            angle = math.copysign(1.0, pixel_y) * math.atan(abs(pixel_y / m_focalLength))

            return math.degrees(angle)
 
        def getTargetXDegrees():
            m_focalLength = (320 / 2) / math.tan(math.radians(55 / 2))
            pixel_x = getXCenter(left_contour, right_contour) - 160            
            angle = math.copysign(1.0, pixel_x) * math.atan(abs(pixel_x / m_focalLength))

            return math.degrees(angle)

        def getDistance():
            mount_height = 39
            target_height = 28.75
            angle = getTargetYDegrees()
            radian = math.radians(angle)

            distance = abs((mount_height - target_height) / math.tan(radian))
            return distance

        def getRobotAngleToTurn():
            angleOffset = 6
            radians = math.radians(getTargetXDegrees() + angleOffset) 
            # - 10 if camera is on the right, + 10 if camera is on the left

            horizontalAngle = math.pi / 2 - radians
            distance = getDistance()
            cameraHorizontalOffset = 5.5

            f = math.sqrt(distance * distance + math.pow(cameraHorizontalOffset, 2) - 2 * distance * cameraHorizontalOffset * math.cos(horizontalAngle))
            c= math.asin(cameraHorizontalOffset * math.sin(horizontalAngle) / f)
            b = math.pi - horizontalAngle - c
            calculatedAngle = math.degrees((math.pi / 2 - b))
            return calculatedAngle

        contourNum = len(self.filter_contours_output)

        # Sorts contours by the smallest area first
        newContours = sortByArea(self.filter_contours_output)

        if(contourNum == 2):
            newContours = sortByPosition(self.filter_contours_output)
            if(get_orientation(newContours[0]) == 1 or get_orientation(newContours[1]) == 2):
                if(getXcoord(newContours[0]) < getXcoord(newContours[1])):
                    left_contour = newContours[0]
                    right_contour = newContours[1]
                    drawRectContours(left_contour, right_contour)
                    toSend = ("/" + str(contourNum) +
                        "/" + str(getArea(left_contour) + getArea(right_contour)) +  # Total area 
                        "/" + str(round(getTwoContourCenter(left_contour, right_contour)[0] - 160, 2)) + # center x point; -160 to 160 scale to be used in robot code
                        "/" + str(round(120 - getTwoContourCenter(left_contour, right_contour)[1], 2))) # center y point
                    # rvec, tvec = solvePnP(getContourCorners(left_contour))
                    # draw(self.outimg, corners, rvec, tvec)
                    # toSend = ("Degrees: " + str(getTargetYDegrees(120 - getYCenter(left_contour, right_contour))) + 
                    #     "Distance: " + str(getDistance(28.5, 40, 120 - getYCenter(left_contour, right_contour))) + 
                    #     "Horizontal Angle: " + str(getRobotAngleToTurn()))
                    jevois.sendSerial(toSend)
            elif(get_orientation(newContours[0]) == 3 or get_orientation(newContours[1]) == 3):
                toSend = "rip"
                jevois.sendSerial(toSend)

        elif (contourNum == 3):
            sortedByPosition = sortByPosition(self.filter_contours_output) # left to right
            mid_contour = sortedByPosition[1]
            if(get_orientation(mid_contour) == 1):
                left_contour = mid_contour 
                right_contour = sortedByPosition[2]
            elif(get_orientation(mid_contour) == 2):
                right_contour = mid_contour
                left_contour = sortedByPosition[0]
            drawRectContours(left_contour, right_contour)
            toSend = ("/" + str(contourNum) +
                        "/" + str(getArea(left_contour) + getArea(right_contour)) +  # Total area 
                        "/" + str(round(getTwoContourCenter(left_contour, right_contour)[0] - 160, 2)) + # center x point; -160 to 160 scale to be used in robot code
                        "/" + str(round(120 - getTwoContourCenter(left_contour, right_contour)[1], 2))) # center y point
            # toSend = "Distance: " + str(getDistance(29, 35, 120 - getTwoContourCenter(left_contour, right_contour)[1]))
            # toSend = ("Degrees: " + str(getTargetYDegrees(120 - getYCenter(left_contour, right_contour))) + 
            #     "Distance: " + str(getDistance(28.5, 40, 120 - getYCenter(left_contour, right_contour))) + 
            #     "Horizontal Angle: " + str(getRobotAngleToTurn()))
            jevois.sendSerial(toSend)

        else:
            toSend = "/0/0/0/0/0/0"
            jevois.sendSerial(toSend)

        # Write a title:
      #  cv2.putText(self.outimg, "687 Nerdy JeVois", (3, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        # fps = self.timer.stop()
        #height, width, channels = outimg.shape # if outimg is grayscale, change to: height, width = outimg.shape
        # self.end_time = time.time()
        # delta_time = self.end_time - self.start_time

        #height, width, channels = self.outimg.shape
        # cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

    def process(self, inframe, outframe):
        self.processNoUSB(inframe)

        # Write a title:
        # cv2.putText(self.outimg, "NerdyJevois USB", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        # fps = self.timer.stop()
        #height, width, channels = outimg.shape # if outimg is grayscale, change to: height, width = outimg.shape
        # height, width, channels = outimg.shape
        # cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

        # Convert our BGR output image to video output format and send to host over USB. If your output image is not
        # BGR, you can use sendCvGRAY(), sendCvRGB(), or sendCvRGBA() as appropriate:
        outframe.sendCvBGR(self.outimg)
        # outframe.sendCvGRAY(outimg)

##################################################################################################

        # END CUSTOM CODE

###################################################################################################

    # FUNCTIONS GO HERE (Anything that starts with "@staticmethod")

    @staticmethod
    def __blur(src, type, radius):
        """Softens an image using one of several filters.
        Args:
            src: The source mat (numpy.ndarray).
            type: The blurType to perform represented as an int.
            radius: The radius for the blur as a float.
        Returns:
            A numpy.ndarray that has been blurred.
        """
        ksize = int(2 * round(radius) + 1)
        return cv2.blur(src, (ksize, ksize))
        #return cv2.medianBlur(src, (ksize, ksize)) # Perform a Median Blur
        #return cv2.GaussianBlur(src,(ksize, ksize),0) # Perform a Gaussian Blur

    @staticmethod
    def __cv_extractchannel(src, channel):
        """Extracts given channel from an image.
        Args:
            src: A numpy.ndarray.
            channel: Zero indexed channel number to extract.
        Returns:
             The result as a numpy.ndarray.
        """
        return cv2.extractChannel(src, (int) (channel + 0.5))

    @staticmethod
    def __cv_threshold(src, thresh, max_val, type):
        """Apply a fixed-level threshold to each array element in an image
        Args:
            src: A numpy.ndarray.
            thresh: Threshold value.
            max_val: Maximum value for THRES_BINARY and THRES_BINARY_INV.
            type: Opencv enum.
        Returns:
            A black and white numpy.ndarray.
        """
        return cv2.threshold(src, thresh, max_val, type)[1]

    @staticmethod
    def __mask(input, mask):
        """Filter out an area of an image using a binary mask.
        Args:
            input: A three channel numpy.ndarray.
            mask: A black and white numpy.ndarray.
        Returns:
            A three channel numpy.ndarray.
        """
        return cv2.bitwise_and(input, input, mask=mask)

    @staticmethod
    def __normalize(input, type, a, b):
        """Normalizes or remaps the values of pixels in an image.
        Args:
            input: A numpy.ndarray.
            type: Opencv enum.
            a: The minimum value.
            b: The maximum value.
        Returns:
            A numpy.ndarray of the same type as the input.
        """
        return cv2.normalize(input, None, a, b, type)

    @staticmethod
    def __hsv_threshold(input, hue, sat, val):
        """Segment an image based on hue, saturation, and value ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max value.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        return cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))

    @staticmethod
    def __cv_erode(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of lower value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for erosion. A numpy.ndarray.
           iterations: the number of times to erode.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after erosion.
        """
        return cv2.erode(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    @staticmethod
    def __cv_dilate(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of higher value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for dilation. A numpy.ndarray.
           iterations: the number of times to dilate.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after dilation.
        """
        return cv2.dilate(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    @staticmethod
    def __find_contours(input, external_only):
        """Sets the values of pixels in a binary image to their distance to the nearest black pixel.
        Args:
            input: A numpy.ndarray.
            external_only: A boolean. If true only external contours are found.
        Return:
            A list of numpy.ndarray where each one represents a contour.
        """
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        im2, contours, hierarchy =cv2.findContours(input, mode=mode, method=method)
        return contours

    @staticmethod
    def __filter_contours(input_contours, min_area, min_perimeter, min_width, max_width,
                        min_height, max_height, solidity, max_vertex_count, min_vertex_count,
                        min_ratio, max_ratio):
        """Filters out contours that do not meet certain criteria.
        Args:
            input_contours: Contours as a list of numpy.ndarray.
            min_area: The minimum area of a contour that will be kept.
            min_perimeter: The minimum perimeter of a contour that will be kept.
            min_width: Minimum width of a contour.
            max_width: MaxWidth maximum width.
            min_height: Minimum height.
            max_height: Maximimum height.
            solidity: The minimum and maximum solidity of a contour.
            min_vertex_count: Minimum vertex Count of the contours.
            max_vertex_count: Maximum vertex Count.
            min_ratio: Minimum ratio of width to height.
            max_ratio: Maximum ratio of width to height.
        Returns:
            Contours as a list of numpy.ndarray.
        """
        output = []
        for contour in input_contours:
            x,y,w,h = cv2.boundingRect(contour)
            if (w < min_width or w > max_width):
                continue
            if (h < min_height or h > max_height):
                continue
            area = cv2.contourArea(contour)
            if (area < min_area):
                continue
            if (cv2.arcLength(contour, True) < min_perimeter):
                continue
            hull = cv2.convexHull(contour)
            solid = 100 * area / cv2.contourArea(hull)
            if (solid < solidity[0] or solid > solidity[1]):
                continue
            if (len(contour) < min_vertex_count or len(contour) > max_vertex_count):
                continue
            ratio = (float)(w) / h
            if (ratio < min_ratio or ratio > max_ratio):
                continue
            output.append(contour)
        return output
