"calculate sharpness of folder"
from pathlib import Path
import sharpness
import cv2 as cv


folder=Path(__file__).parent / "TestImages/zoom080"

pictures = Path(folder).glob('*.jpg')
sort_pic = sorted(pictures)
print(folder)

for pic in sort_pic:
    #print(pic)
    im1 = cv.imread(str(pic))
    val = sharpness.calc_sharpnes(im1)
    print(pic.name, val)