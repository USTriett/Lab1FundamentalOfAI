import os

import cv2

import pygame


class ScreenRecorder:
    """
        This class is used to record a PyGame surface and save it to a video file.
    """

    def __init__(self, width, height, fps, out_file=''):
        """
        Initialize the recorder with parameters of the surface.
        :param width: Width of the surface to capture
        :param height: Height of the surface to capture
        :param fps: Frames per second
        :param out_file: Output file to save the recording
        """
        self.__output = out_file
        self.__fps = fps
        self.__width = width
        self.__height = height

        self.__four_cc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = None
        if out_file != '':
            self.video = cv2.VideoWriter(self.__output, self.__four_cc, float(fps), (width, height))

    def change_output_file(self, filename):
        self.__output = filename

        self.video = cv2.VideoWriter(self.__output, self.__four_cc, float(self.__fps), (self.__width, self.__height))

    def capture_frame(self, surf):
        """
         Call this method every frame, pass in the pygame surface to capture.
        :param surf: pygame surface to capture
        :return: None
        """
        """

            Note: surface must have the dimensions specified in the constructor.
        """
        # transform the pixels to the format used by open-cv
        pixels = cv2.rotate(pygame.surfarray.pixels3d(surf), cv2.ROTATE_90_CLOCKWISE)
        pixels = cv2.flip(pixels, 1)
        pixels = cv2.cvtColor(pixels, cv2.COLOR_RGB2BGR)

        # write the frame
        self.video.write(pixels)

    def end_recording(self):
        """
        Call this method to stop recording.
        :return: None
        """
        # stop recording
        self.video.release()

# References
#   For more tutorials on cv2.VideoWriter, go to:
#   - https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html#display-video
#   - https://medium.com/@enriqueav/how-to-create-video-animations-using-python-and-opencv-881b18e41397