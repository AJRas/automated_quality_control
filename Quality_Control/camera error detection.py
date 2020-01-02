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

#im1 = Image.open('2.jpg') #image object
#im2 = Image.open('error2.jpg') #image object
#gim1 = im1.convert('LA') #keep in mind there's only 2 coordinate pixels
#gim2 = im2.convert('LA')
#gim1.save("gray1.png")
#gim2.save("gray2.png")

pixel_array1 = [[[0 for x in range(256)] for y in range(256)] for Z in range(256)] #3d array creatiion
pixel_array2 = [[[0 for x in range(256)] for y in range(256)] for Z in range(256)] #3d array creatiion
#hsv_pixel_array1 = [[[0 for x in range(256)] for y in range(256)] for Z in range(256)] #3d array creatiion hsv
#hsv_pixel_array2 = [[[0 for x in range(256)] for y in range(256)] for Z in range(256)] #3d array creatiion hsv
#gpixel_array1 = [[0 for x in range(256)] for y in range(256)] #3d array creatiion for greyscale
#gpixel_array2 = [[0 for x in range(256)] for y in range(256)] #3d array creatiion for greyscale
#hsv_picture_array1 = [[0 for x in range(982)] for y in range(719)]
#hsv_picture_array2 = [[0 for x in range(982)] for y in range(719)]
average_picture_array = [[0 for x in range(982)] for y in range(719)]
defect_picture_array = [[0 for x in range(982)] for y in range(719)]
picture_array1 = [[0 for x in range(982)] for y in range(719)]
picture_array2 = [[0 for x in range(982)] for y in range(719)]
picture_array3 = [[0 for x in range(982)] for y in range(719)]
filter_array_L = [[(0,0,0) for x in range(982)] for y in range(719)]
filter_array_H = [[(0,0,0) for x in range(982)] for y in range(719)]

#RGB_pixel_amount_processing(im1, pixel_array1)
#RGB_pixel_amount_processing(im2, pixel_array2)
#GREY_pixel_amount_processing(gim1, gpixel_array1)
#GREY_pixel_amount_processing(gim2, gpixel_array2)
#HSV_pixel_amount_processing(im1, hsv_pixel_array1, hsv_picture_array1)
#HSV_pixel_amount_processing(im2, hsv_pixel_array2, hsv_picture_array2)

#whole_gpixel_difference = whole_pixel_difference_2_by_image(gim1, gim2)
#particular_gpixel_difference = particular_pixel_difference_2_by_image(gim1, gim2)
#whole_pixel_difference = whole_pixel_difference_3_by_image(im1, im2)
##particular_pixel_difference = particular_pixel_difference_3_by_image(im1, im2)
#particular_hpixel_difference = particular_pixel_difference_3_by_array(im1, hsv_picture_array1, hsv_picture_array2)
#whole_hpixel_difference = whole_pixel_difference_3_by_array(im1, hsv_picture_array1, hsv_picture_array2)

#difference = Array_Difference_3D(pixel_array1, pixel_array2)
#gdifference = Array_Difference_2D(gpixel_array1, gpixel_array2)
#hdifference = Array_Difference_3D(hsv_pixel_array1, hsv_pixel_array2)

#Final calculation
##Total = im1.size[0]*im1.size[1]
#gTotal = gim1.size[0]*gim1.size[1]
#Total_Difference = decimal_to_percentage(difference/2, Total)
#gTotal_Difference = decimal_to_percentage(gdifference/2, gTotal)
#hTotal_Difference = decimal_to_percentage(hdifference/2, Total)
#Total_Whole_Pixel_Difference = decimal_to_percentage(whole_pixel_difference, Total)
#Total_Whole_gPixel_Difference = decimal_to_percentage(whole_gpixel_difference, gTotal)
#Total_Whole_hPixel_Difference = decimal_to_percentage(whole_hpixel_difference, Total)
##Total_Particular_Pixel_Difference = decimal_to_percentage(particular_pixel_difference, Total)
#Total_Particular_gPixel_Difference = decimal_to_percentage(particular_gpixel_difference, gTotal)
#Total_Particular_hPixel_Difference = decimal_to_percentage(particular_hpixel_difference, Total)

#Final print
#print("Total difference by pixel amount: ", Total_Difference, "%")
#print("Total whole pixel difference by pixel amount and location: ", Total_Whole_Pixel_Difference, "%")
##print("Total particular pixel difference by pixel difference and location: ", Total_Particular_Pixel_Difference, "%")
#print("Greyscale Total difference by pixel amount: ",gTotal_Difference,"%")
#print("Greyscale Total whole pixel difference by pixel amount and location: ", Total_Whole_gPixel_Difference, "%")
#print("Greyscale Total particular pixel difference by pixel difference and location: ", Total_Particular_gPixel_Difference, "%")
#print("HSV Total difference by pixel amount: ",hTotal_Difference,"%")
#print("HSV Total whole pixel difference by pixel amount and location: ", Total_Whole_hPixel_Difference, "%")
#print("HSV Total particular pixel difference by pixel difference and location: ", Total_Particular_hPixel_Difference, "%")

#make a scan of averaging the samples while comparing them to sample 20, error1, error2, 18.1, 19.1

#---particular pixel optimization observation---
im1 = Image.open('20.jpg')  # image object
#file = open("20_array_txt", "w")
#Picture_to_Array(im1, picture_array1)
#file.writelines(["%s\n" % item for item in picture_array1])
#file.close()
#index = 1

#print(picture_array1)
#print(picture_array1.__len__()) #produces 719 for y
#print(picture_array1[0].__len__()) #produces 982 for x


#---Phase 2.1: particular pixel array optimization---Begin
#for select in range(1,19):
#    im2 = Image.open(samples[select])  # image object
#    Total = im1.size[0] * im1.size[1] # Total for calculation
#    Picture_to_Array(im2, picture_array2)
#    if select == 1:
#        particular_pixel_difference = particular_pixel_difference_3_by_array(picture_array1, picture_array2)
#    else:
#        particular_pixel_difference = particular_pixel_difference_3_by_array(average_picture_array, picture_array2)
#    Total_Particular_Pixel_Difference = decimal_to_percentage(particular_pixel_difference, Total)
#    print("PPD between 20.jpg and average array of ",samples[select],": ",Total_Particular_Pixel_Difference)
#    if select == 1:
#        Average_Array_Indexing(picture_array1, picture_array2, index, average_picture_array)
#        print("Added picture to average for first time")
#    else:
#        Average_Array_Indexing(average_picture_array, picture_array2, index, average_picture_array)
#        print("Added picture to average")
#    for defect_select in range(1,5):
#        im2.close()
#        im2 = Image.open(defects[defect_select])
#        Picture_to_Array(im2, defect_picture_array)
#        particular_pixel_difference = particular_pixel_difference_3_by_array(average_picture_array, defect_picture_array)
#        Total_Particular_Pixel_Difference = decimal_to_percentage(particular_pixel_difference, Total)
#        print("PPD between average picture array and ", defects[defect_select], ": ", Total_Particular_Pixel_Difference)
#    index += 1
#    im2.close()
#---Phase 2.1: particular pixel array optimization---End

#---Phase 2.2: whole pixel array optimization---Begin
#for select in range(1,19):
#    im2 = Image.open(samples[select])  # image object
#    Total = im1.size[0] * im1.size[1] # Total for calculation
#    Picture_to_Array(im2, picture_array2)
#    if select == 1:
#        whole_pixel_difference = whole_pixel_difference_3_by_array(0, picture_array1, picture_array2)
#    else:
#        whole_pixel_difference = whole_pixel_difference_3_by_array(0, average_picture_array, picture_array2)
#    Total_Whole_Pixel_Difference = decimal_to_percentage(whole_pixel_difference, Total)
#    print("PPD between 20.jpg and average array of ",samples[select],": ",Total_Whole_Pixel_Difference)
#    if select == 1:
#        Average_Array_Indexing(picture_array1, picture_array2, index, average_picture_array)
#        print("Added picture to average for first time")
#    else:
#        Average_Array_Indexing(average_picture_array, picture_array2, index, average_picture_array)
#        print("Added picture to average")
#    for defect_select in range(1,5):
#        im2.close()
#        im2 = Image.open(defects[defect_select])
#        Picture_to_Array(im2, defect_picture_array)
#        whole_pixel_difference = whole_pixel_difference_3_by_array(0, average_picture_array, defect_picture_array)
#        Total_Whole_Pixel_Difference = decimal_to_percentage(whole_pixel_difference, Total)
#        print("PPD between average picture array and ", defects[defect_select], ": ", Total_Whole_Pixel_Difference)
#    index += 1
#    im2.close()
#---Phase 2.2: whole pixel array optimization---End

#---Phase 2.3: filter algorithm optimization---Begin
# Use 2 and 3 to create filter, Check 4, add 4 to filter range, and so on.
#im2 = Image.open('2.jpg')
#im3 = Image.open('3.jpg')
#Picture_to_Array(im2, picture_array2)
#file = open("2_array_txt", "w")
#file.writelines(["%s\n" % item for item in picture_array2])
#file.close()
#Picture_to_Array(im3, picture_array3)
#file = open("3_array_txt", "w")
#file.writelines(["%s\n" % item for item in picture_array3])
#file.close()
#Create_Filter_Basis(picture_array2, picture_array3, filter_array_H, filter_array_L) #filter creation
#print("basis filter has been created from pictures 2.jpg and 3.jpg")
#Total = im1.size[0] * im1.size[1]
#for select in range(3, 19):
#    #print("Opening picture", samples[select])
#    im4 = Image.open(samples[select])
#    Picture_to_Array(im4, picture_array3)
#    new_picture_check_results = Filter_pass_and_results(filter_array_H, filter_array_L, picture_array1)
#    print("filter pass shows that 20.jpg has a difference of ", new_picture_check_results)
#    for defect_select in range(1, 5):
#        def_im = Image.open(defects[defect_select])
#        Picture_to_Array(def_im, defect_picture_array)
#        defect_filter_pass = Filter_pass_and_results(filter_array_H, filter_array_L, defect_picture_array)
#        print("filter pass difference for ", defects[defect_select], ": ", defect_filter_pass)
#    Filter_adjustment(filter_array_H, picture_array3, 'H')
#    Filter_adjustment(filter_array_L, picture_array3, 'L')
#    print("Factored ", samples[select]," into filter pass")
#    im4.close()
#im2.close()
#im3.close()
#---Phase 2.3: filter algorithm optimization---End

#Write_2D_Array_to_Text(average_picture_array,"array")

#---Phase 3: difference comparison---Begin

#difference_array1 = [[(0, 0, 0) for x in range(982)] for y in range(719)]
#Combined_picture_array = [[(0, 0, 0) for x in range(1964)] for y in range(719)]

#im2 = Image.open('2.jpg')
#im3 = Image.open('3.jpg')
#Picture_to_Array(im2, picture_array2)
#Picture_to_Array(im3, picture_array3)
#Create_Filter_Basis(picture_array2, picture_array3, filter_array_H, filter_array_L) #filter creation
#print("basis filter has been created from pictures 2.jpg and 3.jpg")
#Total = im1.size[0] * im1.size[1]
#for select in range(3, 19):
#    #print("Opening picture", samples[select])
#    im4 = Image.open(samples[select])
#    Picture_to_Array(im4, picture_array3)
#    Filter_adjustment(filter_array_H, picture_array3, 'H')
#    Filter_adjustment(filter_array_L, picture_array3, 'L')
#    print("Factored ", samples[select], " into filter pass")
#    im4.close()
#
#im4 = Image.open(defects[2])
#Picture_to_Array(im4, picture_array3)
#im4.close()
#def_im = Image.open(defects[2])
#Picture_to_Array(def_im, defect_picture_array)
#defect_filter_pass = Filter_pass_and_results(filter_array_H, filter_array_L, defect_picture_array)
#print("filter pass difference for ", defects[1], ": ", defect_filter_pass)
#filter_pass_difference_array(filter_array_H, filter_array_L, picture_array3, difference_array1)
#
#for y in range(2, 718): #Combines picture 18.1 with its defect correlation showing
#    for x in range(2, 980):
#        Combined_picture_array[y-1][x] = picture_array3[y][x]
#    for x in range(981,1959):
#        Combined_picture_array[y-1][x] = difference_array1[y][x-979]
#
##Need to convert 2D to 1D
#
#img = Image.new('RGB', (1959, 719), color='red')
#
#Combined_array_lineup = [(0, 0, 0) for x in range(719*1959)]
#print(Combined_array_lineup[0])
#for y in range(2,718):
#    for x in range(2,1959):
#        index = x + (y * 1959)
#        Combined_array_lineup[index] = Combined_picture_array[y][x]
#
#for index in range(719*1964):
#    #img.putdata(Combined_array_lineup[index])
#    #img.putdata(Combined_array_lineup[index], 1.0, 0.0)
#
#img.putdata(Combined_array_lineup)
#
#print(img)
#img.save('test19.2.png')
#
#img = Image.new('RGB', im.size, color='red')
#pixel_array1 = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for x in range((im.size[0])*(im.size[0]))] #Long 1D array
#img.putdata(pixel_array1)
#img.save('generated.jpg')
#
#im2.close()
#im3.close()
#---Phase 3: difference comparison---End

#---Phase 4: Saving min and max array---Begin
test_array_L = [[(0, 0, 0) for x in range(982)] for y in range(719)]
test_array_H = [[(0, 0, 0) for x in range(982)] for y in range(719)]

im2 = Image.open('2.jpg')
im3 = Image.open('3.jpg')
Picture_to_Array(im2, picture_array2)
Picture_to_Array(im3, picture_array3)
Create_Filter_Basis(picture_array2, picture_array3, filter_array_H, filter_array_L) #filter creation
print("basis filter has been created from pictures 2.jpg and 3.jpg")
Total = im1.size[0] * im1.size[1]
for select in range(3, 4): #Normal is 3,19
    #print("Opening picture", samples[select])
    im4 = Image.open(samples[select])
    Picture_to_Array(im4, picture_array3)
    Filter_adjustment(filter_array_H, picture_array3, 'H')
    Filter_adjustment(filter_array_L, picture_array3, 'L')
    print("Factored ", samples[select], " into filter pass")
    im4.close()

#Write L and H array to txt file

save_array_to_text_file(0, 719, 0, 982, filter_array_L, "Adorable_Kitten_L")
save_array_to_text_file(0, 719, 0, 982, filter_array_H, "Adorable_Kitten_H")

#Chunk to save array to file
#for y in range(0, 719):
#    for x in range(0, 982):
#        str_L = str(filter_array_L[y][x])
#        str_L += "\n"
#        str_H = str(filter_array_H[y][x])
#        str_H += "\n"
#        file_output_L.write(str_L)
#        file_output_H.write(str_H)
#file_output_L.close()
#file_output_H.close()
#saving array to file complete

txt_file_to_array(0, 719, 0, 982, "Adorable_Kitten_L", test_array_L)
txt_file_to_array(0, 719, 0, 982, "Adorable_Kitten_H", test_array_H)

#Test to show that the generated array and file array are the same, it proves it's lossless
for y in range(0, 719):
    for x in range(0, 982):
        if test_array_L[y][x] != filter_array_L[y][x]:
            item = test_array_L[y][x]
            print("At X-index: ",x,", Y-index: ",y,", test_array: ",item,", filter_array_L: ",filter_array_L[y][x])

#---test_array is the area to put the file into---

im2.close()
im3.close()
#---Phase 4: Saving min and max array---End