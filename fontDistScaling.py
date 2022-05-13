import cv2


###############################################################################################################
###############################################################################################################
###############################################################################################################


# to make name scalable (its size increases if person face increases and decreases if width of person face decreases)
def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        #print(new_width)
        if (new_width <= width):
            return scale/10
    return 1


###############################################################################################################
###############################################################################################################
###############################################################################################################


# print separators between outputs
def spaceRegion():
    return print("\n\n", "#"*100, end="\n\n")
