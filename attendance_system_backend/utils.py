# ---------------------------------------------------
# utils
# @author: Shi Junjie A178915
# Thur 13 June 2024
# ---------------------------------------------------

import io
import numpy as np
from PIL import Image

class Utils:
    def _binary_to_np_image(binary_data) -> Image:
        return np.array(Image.open(io.BytesIO(binary_data)))
