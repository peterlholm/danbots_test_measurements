"light callibration module"
# module for light compensation
# genrating maps:
#   gen_image_diff_map: generate a map with difference for picels compared to meadia picture value
#   gen_image_mult_map: generate a map with multifier for picels compared to meadia picture value
# picture correction:
#   apply_image_diff_map: apply the diff map on the given picture
#   apply_image_mult_map: apply the mult map on the given picture

from pathlib import Path
from PIL import Image, ImageStat, ImageFilter
import numpy as np

_DEBUG = False
COMP_OFFSET = 200
MEDIAN_FILTER_SIZE = 7

### gen maps ###

def gen_image_diff_map(inpicture, outdiffmap):
    outdiffmap = Path(outdiffmap)
    img = Image.open(Path(inpicture))
    imgstat = ImageStat.Stat(img)
    grey = img.convert('L')
    stat = ImageStat.Stat(grey)
    mean = stat.mean[0]
    if _DEBUG:
        print("Image Mean:", imgstat.mean, "extrema:", imgstat.extrema, "Stdv:", imgstat.stddev)
        print("Grey Mean:", mean, "extrema:", stat.extrema, "Stdv:", stat.stddev)
    imean = int(mean)
    korr = Image.new('L', grey.size)
    np_korr = np.empty((grey.width, grey.height), dtype=np.byte)
    if MEDIAN_FILTER_SIZE != 0:
        korr1 = korr.filter(ImageFilter.MedianFilter(size=MEDIAN_FILTER_SIZE))
        korr = korr1
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            cor = imean - grey.getpixel((x,y))
            np_korr[x,y] = cor
            if _DEBUG:
                val = cor + COMP_OFFSET
                korr.putpixel((x,y), val )
    if _DEBUG:
        korr.save(outdiffmap.with_suffix('.png'))
    np.save(outdiffmap, np_korr)

def gen_image_mult_map(inpicture, outmultmap):
    outmultmap = Path(outmultmap)
    img = Image.open(Path(inpicture))
    grey = img.convert('L')
    stat = ImageStat.Stat(grey)
    mean = stat.mean[0]
    if _DEBUG:
        imgstat = ImageStat.Stat(img)
        print("Image Mean:", imgstat.mean, "extrema:", imgstat.extrema, "Stdv:", imgstat.stddev)
        print("Grey Mean:", mean, "extrema:", stat.extrema, "Stdv:", stat.stddev)
        imgout = Image.new('L', grey.size)
    korr = Image.new('L', grey.size)
    np_korr = np.empty((grey.width, grey.height), dtype=np.float32)
    if MEDIAN_FILTER_SIZE != 0:
        korr1 = korr.filter(ImageFilter.MedianFilter(size=MEDIAN_FILTER_SIZE))
        korr = korr1
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            cor = grey.getpixel((x,y))/mean
            np_korr[x,y] = cor
            if _DEBUG:
                val = cor*100 #+ COMP_OFFSET
                imgout.putpixel((x,y), int(val) )
    if _DEBUG:
        imgout.save(outmultmap.with_suffix('.png'))
    np.save(outmultmap, np_korr)

## correct ##

def apply_image_diff_map(image, picmap, outimage):
    outimage = Path(outimage)
    img = Image.open(image)
    np_corr = np.load(picmap)
    for x in range(0, img.width):
        for y in range(0, img.height):
            comp = np_corr[x,y]
            val = img.getpixel((x,y))
            val2 = (val[0]+comp, val[1]+comp, val[2]+comp, val[3])
            img.putpixel((x,y), val2 )
    img.save(outimage)

def apply_image_mult_map(image, multmap, outimage):
    img = Image.open(image)
    kor = np.load(multmap)
    if img.mode != "RGBA":
        raise Exception ('Input error: can only handle coplor pictures')
    for x in range(0, img.width):
        for y in range(0, img.height):
            corr= kor[x,y]
            val = img.getpixel((x,y))
            val2 = (int(val[0]/corr), int(val[1]/corr), int(val[2]/corr), val[3])
            img.putpixel((x,y), val2 )
    img.save(outimage)

if __name__ == '__main__':
    picture = Path(__file__).parent / "testdata" / "dias_light.png"
    outfolder = Path(__file__).parent/ 'out'
    gen_image_diff_map(picture, outfolder / 'diff_map.npy')
    gen_image_mult_map(picture, outfolder / 'mult_map.npy')

    apply_image_diff_map(picture, outfolder / 'diff_map.npy', outfolder / 'new_diff_image.png')
    apply_image_mult_map(picture, outfolder / 'mult_map.npy', outfolder / 'new_mult_image.png')
