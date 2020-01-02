import colorsys
import numpy as np
import cv2
from PIL import Image
import scipy.misc
import ast

samples = {1: '2.jpg',
           2: '3.jpg',
           3: '4.jpg',
           4: '5.jpg',
           5: '6.jpg',
           6: '7.jpg',
           7: '8.jpg',
           8: '9.jpg',
           9: '10.jpg',
           10: '11.jpg',
           11: '12.jpg',
           12: '13.jpg',
           13: '14.jpg',
           14: '15.jpg',
           15: '16.jpg',
           16: '17.jpg',
           17: '18.jpg',
           18: '19.jpg',
           19: '20.jpg'}

defects = {1: '18.1.jpg', 2: '19.1.jpg', 3: 'error1.jpg', 4: 'error2.jpg'}

def pixel_difference(p1, p2):
    if p1 > p2:
        max = p1
        min = p2
    if p2 > p1:
        max = p2
        min = p1
    if p1 == p2:
        return 0
    difference = max - min
    if max > (255/2):
        base = max
    if max < (255/2):
        base = 255 - min
    if max == (255/2):
        base = (255/2)
    percentage = difference/base
    return percentage

def decimal_to_percentage(piece, Total):
    per = round((piece / Total) * 100, 2)
    return per

def RGB_pixel_amount_processing(image, array_name):
    for y in range(2,718):
        for x in range(2,980):
            coordinate = (x, y)
            RGB = image.getpixel(coordinate)
            array_name[RGB[0]][RGB[1]][RGB[2]] += 1

def GREY_pixel_amount_processing(image, array_name):
    for y in range(2,718):
        for x in range(2,980):
            coordinate = (x, y)
            RGB = image.getpixel(coordinate)
            array_name[RGB[0]][RGB[1]] += 1

def HSV_pixel_amount_processing(image, array_name, picture_array):
    for y in range(2,718):
        for x in range(2,980):
            coordinate = (x, y)
            check = image.getpixel(coordinate)
            if check[0] <= 46 and check[1] <= 46 and check[2] <= 46:  # black detection
                RGB1 = (0, 0, 0)
            elif check[0] >= 230 and check[1] >= 230 and check[2] >= 230:  # white detection
                RGB1 = (255, 255, 255)
            else:
                HSV = colorsys.rgb_to_hsv(check[0], check[1], check[2])
                RGB1 = colorsys.hsv_to_rgb(HSV[0], HSV[1], 255)
            RGB2 = int(RGB1[0]), int(RGB1[1]), int(RGB1[2])
            array_name[RGB2[0]][RGB2[1]][RGB2[2]] += 1
            picture_array[y][x] = RGB2

def whole_pixel_difference_3_by_image(image1, image2):
    wpd = 0
    for y in range(2,718):
        for x in range(2,980):
            coordinate = (x, y)
            RGB = image2.getpixel(coordinate)
            rgb = image1.getpixel(coordinate)
            if RGB[0] != rgb[0] or RGB[1] != rgb[1] or RGB[2] != rgb[2]:
                wpd += 1
    return wpd

def particular_pixel_difference_3_by_image(image1, image2):
    ppd = 0
    for y in range(2,718):
        for x in range(2,980):
            coordinate = (x, y)
            RGB = image2.getpixel(coordinate)
            rgb = image1.getpixel(coordinate)
            if RGB[0] != rgb[0] or RGB[1] != rgb[1] or RGB[2] != rgb[2]:
                sum = pixel_difference(RGB[0], rgb[0])
                sum += pixel_difference(RGB[1], rgb[1])
                sum += pixel_difference(RGB[2], rgb[2])
                ppd += (sum/3)
    return ppd

def whole_pixel_difference_3_by_array(reference_image, array_name1, array_name2):
    whpd = 0
    for y in range(2,718):
        for x in range(2,980):
            RGB = array_name1[y][x]
            rgb = array_name2[y][x]
            if RGB[0] != rgb[0] or RGB[1] != rgb[1] or RGB[2] != rgb[2]:
                whpd += 1
    return whpd

def particular_pixel_difference_3_by_array(array_name1, array_name2):
    ppd = 0
    for y in range(2,718):
        for x in range(2,980):
            RGB = array_name1[y][x]
            rgb = array_name2[y][x]
            #print("RGB: ",RGB,", rgb: ",rgb,", position y: ",y,", position x: ",x)
            if RGB[0] != rgb[0] or RGB[1] != rgb[1] or RGB[2] != rgb[2]:
                sum = pixel_difference(RGB[0], rgb[0])
                sum += pixel_difference(RGB[1], rgb[1])
                sum += pixel_difference(RGB[2], rgb[2])
                ppd += (sum / 3)
    return ppd

def particular_pixel_difference_2_by_image(image1, image2):
    pgpd = 0
    for y in range(2,718):
        for x in range(2,980):
            coordinate = (x, y)
            RGB = image2.getpixel(coordinate)
            rgb = image1.getpixel(coordinate)
            if RGB[0] != rgb[0] or RGB[1] != rgb[1]:
                pgpd += ((pixel_difference(RGB[0], rgb[0]) + pixel_difference(RGB[1], rgb[1])) / 2)
    return pgpd

def whole_pixel_difference_2_by_image(image1, image2):
    wgpd = 0
    for y in range(2,718):
        for x in range(2,980):
            coordinate = (x, y)
            RGB = image2.getpixel(coordinate)
            rgb = image1.getpixel(coordinate)
            if RGB[0] != rgb[0] or RGB[1] != rgb[1]:
                wgpd += 1
    return wgpd

def Array_Difference_3D(array_name1, array_name2):
    difference = 0
    for z in range(256):
        for y in range(256):
            for x in range(256):
                difference += abs(array_name1[z][y][x] - array_name2[z][y][x])
    return difference

def Array_Difference_2D(array_name1, array_name2):
    difference = 0
    for y in range(256):
        for x in range(256):
            difference += abs(array_name1[y][x] - array_name2[y][x])
    return difference

def Picture_to_Array(Image, array_name):
    for y in range(2,718):
        for x in range(2,980):
            coordinate = (x, y)
            array_name[y][x] = Image.getpixel(coordinate)

def Average_Array_Indexing(array_name1, array_name2, index, average_array1):
    for y in range(2,718):
        for x in range(2,980):
            AVG = array_name1[y][x]
            avg = array_name2[y][x]
            T0 = ((AVG[0] * index) + avg[0]) / (index + 1)
            T1 = ((AVG[1] * index) + avg[1]) / (index + 1)
            T2 = ((AVG[2] * index) + avg[2]) / (index + 1)
            average_array1[y][x] = (T0, T1, T2)

def Write_2D_Array_to_Text(array_name1, txt_name):
    txt = open(str(txt_name), "w")
    for y in range(2,718):
        for x in range(2,980):
            txt.write(str(array_name1[y][x]))
    txt.close()

def Create_Filter_Basis(array_name1, array_name2, basis_filter_H, basis_filter_L):
    for y in range(2,718):
        for x in range(2,980):
            FIL = array_name1[y][x]
            fil = array_name2[y][x]
            #print("FIL: ", array_name1[y][x], ", coordinate y: ", y, " coordinate x:", x)
            #print("fil: ", array_name2[y][x], ", coordinate y: ", y, " coordinate x:", x)
            H0 = HL_Comparison_adjustment(int(FIL[0]), int(fil[0]), 'H')
            H1 = HL_Comparison_adjustment(int(FIL[1]), int(fil[1]), 'H')
            H2 = HL_Comparison_adjustment(int(FIL[2]), int(fil[2]), 'H')
            basis_filter_H[y][x] = (H0, H1, H2)
            L0 = HL_Comparison_adjustment(int(FIL[0]), int(fil[0]), 'L')
            L1 = HL_Comparison_adjustment(int(FIL[1]), int(fil[1]), 'L')
            L2 = HL_Comparison_adjustment(int(FIL[2]), int(fil[2]), 'L')
            basis_filter_L[y][x] = (L0, L1, L2)

def HL_Comparison_adjustment(val1, val2, selection):
    if selection == 'H': #returns higher value
        if val1 > val2:
            return val1
        elif val1 < val2:
            return val2
        elif val1 == val2:
            return val1
    if selection == 'L': #returns lower value
        if val1 > val2:
            return val2
        elif val1 < val2:
            return val1
        elif val1 == val2:
            return val1

def Filter_adjustment(filter_array, new_value_array, setting):
    for y in range(2,718):
        for x in range(2,980):
            ADJ = filter_array[y][x]
            adj = new_value_array[y][x]
            T0 = HL_Comparison_adjustment(ADJ[0], adj[0], setting)
            T1 = HL_Comparison_adjustment(ADJ[1], adj[1], setting)
            T2 = HL_Comparison_adjustment(ADJ[2], adj[2], setting)
            filter_array[y][x] = (T0, T1, T2)

def Filter_pass_and_results(High_Filter_Array, Low_Filter_Array, Test_Array):
    fail = 0
    Total = 0
    for y in range(2,718):
        for x in range(2,980):
            H = High_Filter_Array[y][x]
            L = Low_Filter_Array[y][x]
            T = Test_Array[y][x]
            if H[0] >= T[0] and T[0] >= L[0] and H[1] >= T[1] and T[1] >= L[1] and H[2] >= T[2] and T[2] >= L[2]:
                Total += 1
            else:
                fail += 1
                Total +=1
    #print("Fail is ",fail)
    return round((fail/Total) * 100, 2)

def filter_pass_difference_array(High_Filter_Array, Low_Filter_Array, Test_Array, image_array):
    for y in range(2,718):
        for x in range(2,980):
            H = High_Filter_Array[y][x]
            L = Low_Filter_Array[y][x]
            T = Test_Array[y][x]
            if H[0] >= T[0] and T[0] >= L[0] and H[1] >= T[1] and T[1] >= L[1] and H[2] >= T[2] and T[2] >= L[2]:
                image_array[y][x] = (0, 0, 0)
                #print("likeness detected")
            else:
                #print("defect detected")
                image_array[y][x] = (255, 255, 255)

def txt_file_to_array(r1, r2, r3, r4, file_name, array_name):
    read_file = open(file_name, "r")
    for y in range(r1, r2):
        for x in range(r3, r4):
            item = read_file.readline()  # read from text file
            item_1 = item.rstrip()  # takes away newline character
            array_name[y][x] = ast.literal_eval(item_1)  # Turns trapped string tuple into a tuple
    read_file.close()

def save_array_to_text_file(r1, r2, r3, r4, array_name, file_name):
    file_output = open(file_name, "w")
    for y in range(r1, r2):
        for x in range(r3, r4):
            stri = str(array_name[y][x])
            stri += "\n"
            file_output.write(stri)
    file_output.close()

defect_picture_array = [[0 for x in range(982)] for y in range(719)]
picture_array1 = [[0 for x in range(982)] for y in range(719)]
picture_array2 = [[0 for x in range(982)] for y in range(719)]
picture_array3 = [[0 for x in range(982)] for y in range(719)]
filter_array_L = [[(0,0,0) for x in range(982)] for y in range(719)]
filter_array_H = [[(0,0,0) for x in range(982)] for y in range(719)]

im1 = Image.open('20.jpg')  # image object
Picture_to_Array(im1, picture_array1)

#---Phase 2.3: filter algorithm optimization---Begin
# Use 2 and 3 to create filter, Check 4, add 4 to filter range, and so on.
im2 = Image.open('2.jpg')
im3 = Image.open('3.jpg')
Picture_to_Array(im2, picture_array2)
file = open("2_array_txt", "w")
file.writelines(["%s\n" % item for item in picture_array2])
file.close()
Picture_to_Array(im3, picture_array3)
file = open("3_array_txt", "w")
file.writelines(["%s\n" % item for item in picture_array3])
file.close()
Create_Filter_Basis(picture_array2, picture_array3, filter_array_H, filter_array_L) #filter creation
print("basis filter has been created from pictures 2.jpg and 3.jpg")
Total = im1.size[0] * im1.size[1]
for select in range(3, 19):
    #print("Opening picture", samples[select])
    im4 = Image.open(samples[select])
    Picture_to_Array(im4, picture_array3)
    new_picture_check_results = Filter_pass_and_results(filter_array_H, filter_array_L, picture_array1)
    print("filter pass shows that 20.jpg has a difference of ", new_picture_check_results)
    for defect_select in range(1, 5):
        def_im = Image.open(defects[defect_select])
        Picture_to_Array(def_im, defect_picture_array)
        defect_filter_pass = Filter_pass_and_results(filter_array_H, filter_array_L, defect_picture_array)
        print("filter pass difference for ", defects[defect_select], ": ", defect_filter_pass)
    Filter_adjustment(filter_array_H, picture_array3, 'H')
    Filter_adjustment(filter_array_L, picture_array3, 'L')
    print("Factored ", samples[select]," into filter pass")
    im4.close()
im2.close()
im3.close()
#---Phase 2.3: filter algorithm optimization---End