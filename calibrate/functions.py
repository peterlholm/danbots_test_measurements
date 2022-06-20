""" calibrations functions """
from calibrate.calibrate import get_img_slope, get_img_freq
from calibrate.mask import create_mask_in_config
from api.device_config import read_device_config, save_device_config

_DEBUG=True

def cal_camera(deviceid, folder):
    if _DEBUG:
        print("Calibrating", deviceid)
    cal_picture = folder / 'color.png'
    #slope = get_img_slope(cal_picture)
    slope = 0
    freq = get_img_freq(cal_picture)
    if _DEBUG:
        print("Slope:", slope, "deg Freq:", freq, " f/100 bit" )
    print ("folder",folder)
    config = read_device_config(deviceid)
    config['calibrate'] = {'calibrate': True, "slope": slope, "frequency": freq }
    file = folder / 'flash.jpg'
    create_mask_in_config(file, config)
    file = folder / 'dias.jpg'
    create_mask_in_config(file, config, label="dias_mask", blur=True)
    save_device_config(config, deviceid)

    return True
