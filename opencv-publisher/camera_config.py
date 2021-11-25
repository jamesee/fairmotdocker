def read_camera_config(filename):
    f = open(filename, "r")
    camera_list = f.readlines()
    f.close()
    
    # cameraName, cameraIP, threshold, lat, longi, _, camera_shift_time = camera_list[0].split(",")
    return camera_list[0].split(",")