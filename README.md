Road markings identification using OpenCV and Python and testing in a video

Explanation of the code:

In the first two lines, we have cv2: it is the OpenCV library, used for manipulating and processing images and videos; and numpy: a library for manipulating arrays and matrices.
The function |\verb region_of_interest(image)|, defines a region of interest in the image, and uses a polygon to mask the image, focusing only on the lower part (road) and a little above the horizon. Ja |\verb cv2.fillPoly| creates a polygon-shaped mask, and \verb|cv2.bitwise_and| applies the mask to the image, isolating the area of ​​interest.
The function |\verb process_lines(lines, frame_shape)| filters detected lines based on slope and length to ensure only road lines are considered, and uses slope between points and line length as filtering criteria.
The function |\verb vid_inf(vid_path)| opens the video for processing, and the hurricane |\verbcv2.VideoCapture| loads the video and |\verb cv2.VideoWriter| prepares to record the processed video.
Inside |\verb while|, it reads each frame, applies color filters to highlight yellow and white lines, detects edges with \verb|Canny|, applies the Hough Transform to detect lines, and draws these lines over the original frame . The |\verbcv2.imshow| displays the processed video in a window.
The final video its processed, displayed in real time, and saved in the folder |\textit{opencv} |along with the original video and the code.
