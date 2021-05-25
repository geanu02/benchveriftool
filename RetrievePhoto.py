from PlotMap import info_graph
import os.path


def display_cphoto(c_num):
    filename = "./assets/images/client/cphoto_{0}.png".format(str(c_num))
    if os.path.exists(filename):
        return filename
    else:
        return "./assets/images/client/c_photo_temp.png"


def retrieve_filename(check, data_type, i):
    if data_type is int:
        filename = info_graph(check, i)
        return filename
    elif check == True:
        return './assets/images/check_box_True.png'
    elif check == False:
        return './assets/images/check_box_False.png'
    else:
        filename = info_graph(check, i)
        return filename
