from PIL import ImageEnhance
from pyzbar.pyzbar import decode
from src.config import SIMULATION
from src import utils as u


class QRDecoder(object):
    def __init__(self):
        self.image = None

    def input(self, image):
        """Stores the input image."""
        self.image = image
    
    def get_dist(self, rect):
        return u.fw2d((rect.width + rect.height) / 2)

    def angle_to_qr(self, polygon):
        """Gives heading angle to QR code."""
        return u.get_alpha(polygon)

    def extract_qrs(self, decoded):
        """Extract and return QR code information."""
        qrs = []
        for code in decoded:
            name = code.data.decode('UTF-8')
            rect = code.rect
            distance = self.get_dist(rect)
            polygon = code.polygon
            angle = self.angle_to_qr(polygon)
            qrs.append((name, rect, distance, angle, polygon))
        if not qrs:
            qrs = None
        return qrs

    # TODO: @timed
    def output(self):
        """Returns the decoded QR code."""
        if not SIMULATION:
            contrast = ImageEnhance.Contrast(self.image)
            contrast = contrast.enhance(1.5)
            decoded = decode(contrast)
            qrs = self.extract_qrs(decoded)
        else:
            qrs = None
        return qrs