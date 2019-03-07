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

        self.__blur_radius = 10.122386537480878

        self.blur_output = None

        self.__hsv_threshold_input = self.blur_output
        self.__hsv_threshold_hue = [45.00060968174613, 102.81248335729883]
        self.__hsv_threshold_saturation = [94.01978417266191, 255.0]
        self.__hsv_threshold_value = [52.824858757062145, 255.0]

        self.hsv_threshold_output = None

        self.__cv_erode_src = self.hsv_threshold_output
        self.__cv_erode_kernel = None
        self.__cv_erode_anchor = (-1, -1)
        self.__cv_erode_iterations = 1.0
        self.__cv_erode_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_bordervalue = (-1)

        self.cv_erode_output = None

        self.__cv_dilate_src = self.cv_erode_output
        self.__cv_dilate_kernel = None
        self.__cv_dilate_anchor = (-1, -1)
        self.__cv_dilate_iterations = 6.0
        self.__cv_dilate_bordertype = cv2.BORDER_CONSTANT
        self.__cv_dilate_bordervalue = (-1)

        self.cv_dilate_output = None

        self.__find_contours_input = self.cv_dilate_output
        self.__find_contours_external_only = True

        self.find_contours_output = None

        self.__filter_contours_contours = self.find_contours_output
        self.__filter_contours_min_area = 500.0
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

        # Draws all contours on original image in red
        #cv2.drawContours(self.outimg, self.filter_contours_output, -1, (0, 0, 255), 1)

        # Gets number of contours
        contourNum = len(self.filter_contours_output)

        # Sorts contours by the smallest area first
        newContours = sortByArea(self.filter_contours_output)

        # Send the contour data over Serial
        substituteMsg = "/0/0/0/0/0/0"

        if (contourNum >= 2):
            contour1 = newContours[(contourNum - 1)]
            contour2 = newContours[(contourNum - 2)]

            if(getXcoord(contour1) < getXcoord(contour2)):
                left_contour = contour1
                right_contour = contour2
            else:
                left_contour = contour2
                right_contour = contour1

            # cv2.boxPoints returns four corners of the rectangle
            # list starts at the lowest point (largest y-value) and goes clockwise

            left_rect = cv2.minAreaRect(left_contour)
            left_box = cv2.boxPoints(left_rect)
            left_box = np.int0(left_box)

            right_rect = cv2.minAreaRect(right_contour)
            right_box = cv2.boxPoints(right_rect)
            right_box = np.int0(right_box)

            left_x_center = float(getXcoord(left_contour))
            left_y_center = float(getYcoord(left_contour))
            right_x_center = float(getXcoord(right_contour))
            right_y_center = float(getYcoord(right_contour))

            if (left_x_center < right_x_center):
                left_x1 = float((left_box[3][0] + left_box[2][0]) / 2)
                left_y1 = float((left_box[3][1] + left_box[2][1]) / 2)
                right_x1 = float((right_box[1][0] + right_box[2][0]) / 2)
                right_y1 = float((right_box[1][1] + right_box[2][1]) / 2)
            else:
                right_x1 = float((left_box[3][0] + left_box[2][0]) / 2)
                right_y1 = float((left_box[3][1] + left_box[2][1]) / 2)
                left_x1 = float((right_box[1][0] + right_box[2][0]) / 2)
                left_y1 = float((right_box[1][1] + right_box[2][1]) / 2)  
        
           ''' 
            if
             
            else:
            '''  
            xLeft,yLeft,wLeft,hLeft = cv2.boundingRect(left_contour) # Get the stats of the contour including width and height
            xRight,yRight,wRight,hRight = cv2.boundingRect(right_contour) # Get the stats of the contour including width and height
            

        

      

            try:
                
                left_angle = int(math.atan((left_y1-left_y_center)/(left_x_center-left_x1))*180/math.pi)
                right_angle = int(math.atan((right_y1-right_y_center)/(right_x_center-right_x1))*180/math.pi)
              
                if(left_angle > 0 and right_angle < 0):
      
                    left_x = getXcoord(left_contour) 
                    right_x = getXcoord(right_contour) 
                    center_x =  (left_x + right_x) /2

                    left_y = getYcoord(left_contour) 
                    right_y = getYcoord(right_contour) 
                    center_y = (left_y + right_y)/2 

                    center = (int(center_x), int(center_y))
                
                    cv2.circle(self.outimg,center, 5, (0,0,255), 2)
                    cv2.drawContours(self.outimg,[right_box],0,(255,0,0),2)
                    cv2.drawContours(self.outimg,[left_box],0,(0,0,255),2)

                    # toSend = ("/0" + 
                    #         "/" + str(left_angle) + 
                    #         "/" + str(getArea(left_contour)) +  # Area of contour
                    #         "/" + str(round(getXcoord(left_contour)-160, 2)) +  # x-coordinate of centroid of contour, -160 to 160 rounded to 2 decimal
                    #         "/" + str(round(120-getYcoord(left_contour), 2)) +  # y-coordinate of contour, -120 to 120 rounded to 2 decimal
                    #         "/" + str(round(hLeft, 2)) +  # Height of contour, 0-320 rounded to 2 decimal
                    #         "/" + str(round(wLeft, 2)) +

                    #         "/1" +
                    #         "/" + str(right_angle) +
                    #         "/" + str(getArea(right_contour)) +  # Area of contour
                    #         "/" + str(round(getXcoord(right_contour)-160, 2)) +  # x-coordinate of centroid of contour, -160 to 160 rounded to 2 decimal
                    #         "/" + str(round(120-getYcoord(right_contour), 2)) +  # y-coordinate of contour, -120 to 120 rounded to 2 decimal
                    #         "/" + str(round(hRight, 2)) +  # Height of contour, 0-320 rounded to 2 decimal
                    #         "/" + str(round(wRight, 2)) + # Width of contour, 0-240 rounded to 2 decimal
                    #         "/" + str(round(center_x)) +
                    #         "/" + str(round(center_y))) 
                    toSend = ("Left angle: " + str(left_angle) + " Right Angle: " + str(right_angle))
                            
                    jevois.sendSerial(toSend)
                else:
                    toSend("@drivers move")
                 

            except:
                toSend = str("ANGLE 1 or ANGLE 2 = 90 OR 180")  
        else:
            jevois.sendSerial(substituteMsg + substituteMsg)


        # Write a title:
        cv2.putText(self.outimg, "Nerdy Jevois", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

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


#BlurType = Enum('BlurType', 'Box_Blur Gaussian_Blur Median_Filter Bilateral_Filter')
