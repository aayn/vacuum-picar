from io import BytesIO
from PIL import Image
from src.config import HOST, SIMULATION
from src import picar


class Camera(object):

    def input(self):
        """There is no input to the camera module."""
        ...

    def output(self):
        """Returns an image from the robot."""
        image = None
        if not SIMULATION:
            image_getter = picar.QueryImage(host=HOST)
            image = Image.open(BytesIO(image_getter.queryImage()))
        return image
