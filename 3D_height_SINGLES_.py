# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 2024
    ---Last edited Oct 25th 2024
This Version of 3D Height Plot Code Adds both the Difference Plots and Shape Plots into One .py
    
    -LD Right and HD Full seem to be working
        -features that needed to be added:
            -Center offset, - becuase this code centers at x&y averages, a manual offset is needed for partial shapes. 
            -added more code to improve confidence in xls parsing:
                Z value needs to come immediately after X and Y to register as a data point
            -Added labeling and error features that differentiate difference from shape plot. 
                -Fixed Shape Plots Using error Correction. (V7)
                V10 - added hdb using a white cover layer

@author: Paolo Jordano
"""
#For Difference plots
import numpy as np

import numpy.ma as ma

import scipy.linalg
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
from matplotlib.colors import Normalize


#For other Operations
import os
import datetime

workDir = os.getcwd()

LDTopKeys = ['ld top','5'];
HDTopKeys = ['hd top','HD Top', '7'];
LDBotKeys = ['ld bot', "ld bottom"];
LDRightKeys = ['ld right','right','2'];
LDLeftKeys = ['ld left', '4'];
LDFiveKeys = ['ld five'];
LDFullKeys = ['ld full'];
HDFullKeys = ['hd full','1'];
HDBottomKeys = ['hd bottom','6']

ShapePlotKeys = ['Shape','shape','curvature','1'];
HeightDiffKeys = ['Heights','heights','difference','Difference','2'];

Shapes = LDTopKeys + HDTopKeys + LDBotKeys+ LDRightKeys + LDLeftKeys + LDFiveKeys +LDFullKeys + HDFullKeys + HDBottomKeys;
ProcessTypes = ShapePlotKeys + HeightDiffKeys;
#print(Shapes)

def Make_Diff_Plot(selected_file, selected_file2, folder_path, modulename, modulename2, ShapeID, ShapePlot):
    #print(selected_file, selected_file2, folder_path, modulename, ShapeID)
    ###################### PROGRAM DOES 1 - 2 so : Final goes in the first slot. (most of the time)
    MaskShape = ShapeID;
    #print("this is shape ID:", ShapeID)
    
    ##- 1 -##
    fileloco = selected_file;
    #modulename = fileloco.replace("C:\\Users\\Admin\\Documents\\OGPQualityControl-master\\data\\HD full\\","").replace(".xls","")
    df = pd.read_excel(fileloco)
    my_array = df.values
    newlist = [];
    
    ##- 1 -##
    for line in my_array:
        newline = [];
        elcount = 0;
        for entry in line:
            
            if type(entry) == float:
                newline.append('')
                elcount = elcount + 1; 
            else:
                newline.append(entry)
        if elcount < 8:
            newlist.append(newline);
            
    ##- 1 -##
    previousline = ['','','']; 
    beforeline = ['','','']; 
    rawheightslist = []
    for line in newlist:
        if 'ModuleThickness1' == line[2]:
            rawheightslist.append(line)
        if 'J' not in str(line[2]):
            if 'flat' or 'Thick' in line[2]:
                #print(line)
                rawheightslist.append(line)
            elif 'flat' or 'Thick' in beforeline[2]: 
                #print(line);
                rawheightslist.append(line)
            elif 'flat' or 'Thick' in previousline[2]: 
                #print(line);
                rawheightslist.append(line)

        beforeline = previousline;    
        previousline = line;   
    
    #print("#1#")
    #print(rawheightslist)


        
    ##- 1 -##
    lastname = '';
    Heightlist = []; LineNames = []; skiplines = 0; 
    for line in rawheightslist:
        if type(line[2]) is str:
            if 'FD' in line[2]:
                skiplines  = 3;
        if skiplines == 0:
            if 'flat' or 'Thick' in line[2]:
                lastname = line[2];
            #if line[3] == 'X':
            #    print("X is recognized")
            if line[3] == 'X':
                #print(lastname, 'X:', line[5])
                Heightlist.append([lastname, 'X', line[5], line[2]])
                LineNames.append(line[2])
                #print(line[2])

            if line[3] == 'Y':
                #print(lastname, 'Y:', line[5])
                Heightlist.append([lastname, 'Y', line[5], line[2]])
            if line[3] == 'Z':
                #print(lastname, 'Z:', line[5])
                Heightlist.append([lastname, 'Z', line[5], line[2]])
        else: skiplines = skiplines - 1;
    
    #print("#1#")
    #print(LineNames)
    #LineNames = [];
    
    #print("List 1:")
    #print(Heightlist)

    ##- 2 -##   
    if ShapePlot == True:
        fileloco2 = selected_file;
        print("Making a Shape Plot..")
    else:
        fileloco2 = selected_file2;
        
    #modulename2 = fileloco2.replace("C:\\Users\\Admin\\Documents\\OGPQualityControl-master\\data\\HD full\\","").replace(".xls","")
    #modulename2 = selected_file.replace(folder_path,"").replace(".xls","")
    df2 = pd.read_excel(fileloco2)
    my_array2 = df2.values
    newlist2 = []; 

    ##- 2 -##        
    for line in my_array2:
        newline = [];
        elcount = 0;
        for entry in line:
            
            if type(entry) == float:
                newline.append('')
                elcount = elcount + 1; 
            else:
                newline.append(entry)
        if elcount < 8:
            newlist2.append(newline);        

    ##- 2 -##
    rawheightslist2 = []
    for line in newlist2:
        if 'ModuleThickness1' == line[2]:
            rawheightslist2.append(line)
        if 'J' not in str(line[2]):
            if 'flat' or 'Thick' in line[2]:
                #print(line)
                rawheightslist2.append(line)
            elif 'flat' or 'Thick' in beforeline[2]: 
                #print(line);
                rawheightslist2.append(line)
            elif 'flat' or 'Thick' in previousline[2]: 
                #print(line);
                rawheightslist2.append(line)
                
        beforeline = previousline;    
        previousline = line;    
    
    #print("#2#")
    #print(rawheightslist2)



    ##- 2 -##        
    lastname2 = '';
    Heightlist2 = []; LineNames2 = []; past = False; skiplines = 0
    for line in rawheightslist2:
        if type(line[2]) is str:
            if 'FD' in line[2]:
                skiplines  = 3;
        if skiplines == 0:
            if type(line[2]) is str:
                if 'BacksideSurface' in line[2]:
                    past = False;
                elif 'Backside' in line[2]:
                    print('going past')
                    past = True;
            if past != True:
            
                #print(line[2], line[5], line[3])
                #if type(line[2]) is str:
                #    if 'BacksideSurface' in line[2]:
                #        print('present')
                if 'ModuleThickness' == line[2]:
                    print("FOUND MODTHICK1", line[2])
                if 'flat' or 'Thick' in line[2]:
                    lastname2 = line[2];
                if line[3] == 'X':
                    #print(lastname2, 'X:', line[5])
                    Heightlist2.append([lastname2, 'X', line[5], line[2]])
                    LineNames2.append(line[2])
                    #print(line[2])
                if line[3] == 'Y':
                    #print(lastname2, 'Y:', line[5])
                    Heightlist2.append([lastname2, 'Y', line[5], line[2]])
                if line[3] == 'Z':
                    #print(lastname2, 'Z:', line[5])
                    Heightlist2.append([lastname2, 'Z', line[5], line[2]])
        else: skiplines = skiplines - 1
    
    #print("#2#")        
    #print(LineNames)
            
    print("List 1:")
    print(len(Heightlist))
    for height in Heightlist:
        print(height)
    print("List 2:")
    print(len(Heightlist2))
    for height in Heightlist2:
        print(height)       
            
    ##############################################
            
    exclude_strings = {'#','Glass', 'HB', 'J', 'Top', 'Left', "Bot", "bottom", 'bot', 'Bottom', 'Right', 'FD1', 'FD2', 'FD3', 'FD4', 'FD4rough', 'FD2rough'}
    Heightlist = [array for array in Heightlist if not any(exclude in array[0] for exclude in exclude_strings)]
    Heightlist2 = [array for array in Heightlist2 if not any(exclude in array[0] for exclude in exclude_strings)]
    
    
    #print(LineNames, LineNames2)
    

    """
    ###1###    
    #Heightlist = [array for array in Heightlist if not any(exclude in array[0] for exclude in exclude_strings)]
    filtered_list = []; skip_count = 0;
    for i, array in enumerate(Heightlist):
        if skip_count > 0:
            skip_count -= 1
            continue
    
        if any(exclude in array[0] for exclude in exclude_strings):
            skip_count = 2
            continue
    
        if i + 1 < len(Heightlist) and any(exclude in Heightlist[i + 1][1] for exclude in ['Y', 'Z']):
            skip_count = 1
            continue
    
        if i + 2 < len(Heightlist) and any(exclude in Heightlist[i + 2][1] for exclude in ['Y', 'Z']):
            skip_count = 0
            continue
        filtered_list.append(array)
    
    ###2###
    #Heightlist2 = [array for array in Heightlist2 if not any(exclude in array[0] for exclude in exclude_strings)]
    filtered_list2 = []; skip_count2 = 0;
    for i, array in enumerate(Heightlist):
        if skip_count2 > 0:
            skip_count2 -= 1
            continue
    
        if any(exclude in array[0] for exclude in exclude_strings):
            skip_count = 2
            continue
    
        if i + 1 < len(Heightlist2) and any(exclude in Heightlist2[i + 1][1] for exclude in ['Y', 'Z']):
            skip_count = 1
            continue
    
        if i + 2 < len(Heightlist2) and any(exclude in Heightlist2[i + 2][1] for exclude in ['Y', 'Z']):
            skip_count = 0
            continue
        filtered_list2.append(array)
        
    #### TURN OFF THESE LINES TO STOP THE FILTERING
    print(filtered_list)
    print(filtered_list2)
    Heightlist = filtered_list;
    Heightlist2 = filtered_list2;
    
    """
    
    #LineNames = [array for array in LineNames if not any(exclude in array[0] for exclude in exclude_strings)]
    #LineNames2 = [array for array in LineNames2 if not any(exclude in array[0] for exclude in exclude_strings)]
    #print(Heightlist)
    #print(Heightlist2)
    #print(LineNames);
    #print(LineNames2);
        
                        ### BOTH ###
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    b = 10/12;

    #HEXAGON PARAMETERS
    g = 1;

    #a = 2.5;
    a = 2.0;


    # Initialize points as an empty 2D array with shape (0, 3)
    OGpoints = np.empty((0, 3))
    points = np.empty((0, 3))

    # Initialize points as an empty 2D array with shape (0, 3)
    OGpoints2 = np.empty((0, 3))
    points2 = np.empty((0, 3))


    # Initialize variables
    Heights = []; HeightsX = [];
    HeightsY = []; HeightsZ = [];

    OGHeights = []; OGHeightsX = [];
    OGHeightsY = []; OGHeightsZ = [];

    # Initialize variables
    Heights2 = []; HeightsX2 = [];
    HeightsY2 = []; HeightsZ2 = [];

    OGHeights2 = []; OGHeightsX2 = [];
    OGHeightsY2 = []; OGHeightsZ2 = [];

    xchk = ychk = zchk = False
    b = 0

    # Manual inputs (21-number list)
    #manual_inputs = [3.154031,2.742428,3.1284282,3.1598353,3.153044,3.1124034,3.0663586,3.0198457,3.0234919,3.035145,3.0669577,3.1332173,3.2058258,3.0808156,3.084127,3.1072996,3.0949214,3.0403807,3.0896013,3.0865164,3.0832746]
    #manual_inputs = [3.440, 3.420, 3.420, 3.408, 3.412, 3.420, 3.426, 3.440, 3.463, 3.463, 3.485, 3.413, 3.415, 3.390, 3.485, 3.383, 3.407, 3.402]
    #summed_inputs = [0.866, 0.960, 0.706, 0.710, 0.766, 0.692, 0.608, 0.926, 1.028, 0.820, 1.102, 1.006, 1.018, 1.104, 0.958, 0.838, 1.142, 1.166, 1.162, 1.122, 1.116]

    def fill_third_section(arr, inputs):
        input_index = 0
        for sub_arr in arr:
            if sub_arr[1] == 'Z':
                if input_index < len(inputs):
                    sub_arr[2] = inputs[input_index]
                    input_index += 1
                else:
                    print("Not enough manual inputs to fill all 'Z' positions.")
                    break

    ## Display ARRAY before filling
    #print("Before filling:")
    #print(Heightlist[2])
    
    # Fill the 3rd section with manual inputs
    #fill_third_section(Heightlist, manual_inputs)
    
    # Display ARRAY after filling
    #print("After filling:")
    #print(Heightlist[2]) 

    #comment out here

        ##- 1 -##
    #print("#1#")
    timer = 0; nameyet = False;
    for line in Heightlist:
        ptype = line[1]
        pvalue = line[2] 
        
        if ptype == 'X':
            xchk = True
            tempsX = pvalue
            timer = 0;
            #xlinename = line[0];
            if line[0] != '':
                nameyet = True;
        if ptype == 'Y':
            ychk = True
            tempsY = pvalue
        if ptype == 'Z':
            zchk = True
            tempsZ = pvalue
        
        #print(strX,strY,strZ)
            
        #while nameyet == False:
        #    tempsX, tempsY, tempsZ = 100, 100, 100;
            
        timer = timer + 1;
        if timer > 3:
            #print(line);
            timer = 0;
            xchk = ychk = zchk = False;
                
        
        if xchk and ychk and zchk and nameyet:
            if tempsX == '':
                print("empty X")
            if tempsY == '':
                print("empty Y")
            if tempsZ == '':
                print("empty Z")
            #print(tempsX,tempsY,tempsZ, b+1)
            strX = float(tempsX); strY = float(tempsY); strZ = float(tempsZ);
            
            
            
            
            OGHeights.append([float(tempsX) - 140, float(tempsY) - 300, float(tempsZ), b + 1])
            OGHeightsX.append(float(tempsX) - 140)
            OGHeightsY.append(float(tempsY) - 300)
            OGHeightsZ.append(float(tempsZ))
            #print(line);
            #print(xlinename);
            OGpoint = np.array([[float(tempsX) - 140, float(tempsY) - 300, float(tempsZ)]])
            
            OGpoints = np.vstack([OGpoints, OGpoint])
            
            #print(point)
            
            xchk = ychk = zchk = False;
            zchk = False;
            timer = 0;
            b += 1;
    #print()
    #print(OGHeights)        
    #print()
                 
         ##- 2 -##       
    #print(); 
    nameyet = False;
    if not ShapePlot: print("#2#")
    b = 0; timer = 0; nameyet = False;
    for line in Heightlist2:
        ptype = line[1]
        pvalue = line[2]

        if ptype == 'X':
            xchk = True
            tempsX = pvalue
            timer = 0;
            if line[0] != '':
                nameyet = True;
        if ptype == 'Y':
            ychk = True
            tempsY = pvalue
        if ptype == 'Z':
            zchk = True
            tempsZ = pvalue
            
        #print(strX,strY,strZ)
        
            
        #while nameyet == False:
        #    tempsX, tempsY, tempsZ = 100, 100, 100;
            
        
        
        timer = timer + 1;
        #print(line, timer);
        if timer > 3:
            timer = 0;
            xchk = ychk = zchk = False;
        
        if xchk and ychk and zchk and nameyet:
            
            #print(tempsX,tempsY,tempsZ, b+1)
            OGHeights2.append([float(tempsX) - 140, float(tempsY) - 300, float(tempsZ), b + 1])
            OGHeightsX2.append(float(tempsX) - 140)
            OGHeightsY2.append(float(tempsY) - 300)
            OGHeightsZ2.append(float(tempsZ))
            
            OGpoint2 = np.array([[float(tempsX) - 140, float(tempsY) - 300, float(tempsZ)]])
            
            OGpoints2 = np.vstack([OGpoints2, OGpoint2])
            
            #print(point)
            
            xchk = ychk = zchk = False;
            zchk = False;
            timer = 0;
            b += 1


    #print()
    #print(OGHeights2)        
    #print()

    
    #print(OGpoints , OGpoints2)
    #### THIS CENTERS THE MEASUREMENTS ###  
    ##- 1 -##       
    if MaskShape == 'LDR':
        ShapeAdjustmentX = -30;
        ShapeAdjustmentY = 0;
    if MaskShape == 'LDT':
        ShapeAdjustmentX = 0;
        ShapeAdjustmentY = -50;
    if MaskShape == 'HDB':
        ShapeAdjustmentX = -15;
        ShapeAdjustmentY = 0;
    else: 
        ShapeAdjustmentX = 0;
        ShapeAdjustmentY = 0;
        
    scale = 100/100;    
    
    
    print("#1#",len(OGHeightsZ), "#2#",len(OGHeightsZ2))
    print(OGHeightsX)
    print(OGHeightsY)
    
    #AvgX = sum(OGHeightsX)/len(OGHeightsX) + ShapeAdjustmentX;      
    #AvgY = sum(OGHeightsY)/len(OGHeightsY) + ShapeAdjustmentY;
    
    AvgX = np.mean(OGHeightsX) + ShapeAdjustmentX;      
    AvgY = np.mean(OGHeightsY) + ShapeAdjustmentY;
    
    AvgZ = np.sum(OGHeightsZ)/len(OGHeightsZ);      
    AvgZ2 = np.mean(OGHeightsZ2);
    
    #if ShapePlot: print( )
        #print(" File 1: Coordinate Averages:", AvgX, AvgY);
    #else: 
        #print("File 1: Coordinate Averages:", AvgX, AvgY); 
        #print("File 2: Coordinate Averages:", AvgX, AvgY);
    
    #ShapeAdjustments
    if MaskShape == 'LDF' or MaskShape == 'HDF' or MaskShape == 'LD5':
        shadjX = 0; shadjy = 0;
    elif MaskShape == 'LDR':
        shadjX = 0; shadjy = 0;
    elif MaskShape == 'LDL':
        shadjX = -40; shadjy = 0;
    elif MaskShape == 'LDT':
        shadjX = 0; shadjy = 0;
    elif MaskShape == 'LDB':
        shadjX = 0; shadjy = 0;
    elif MaskShape == 'HDT':     
        shadjX = 0; shadjy = 40;
    elif MaskShape == 'HDB':     
        shadjX = 0; shadjy = 0;
    else:
        shadjX = 0; shadjy = 0;

    
    
    
    for line in OGHeights:
        Heights.append([(line[0]- AvgX + shadjX)*scale, (line[1] - AvgY + shadjy)* scale, line[2], line[3]])
        HeightsX.append(line[0]- AvgX + shadjX)
        HeightsY.append(line[1] - AvgY + shadjy)
        HeightsZ.append(line[2])

        point = np.array([(line[0]- AvgX + shadjX)*scale, (line[1] - AvgY + shadjy)*scale, line[2]])

        points = np.vstack([points, point])
    
    print("this was ogheights", OGHeights)
        
        ##- 2 -## 
    AvgX2 = np.mean(OGHeightsX2) + ShapeAdjustmentX;     
    AvgY2 = np.mean(OGHeightsY2) + ShapeAdjustmentY; 

    for line in OGHeights2:
        Heights2.append([(line[0]- AvgX2)*scale, (line[1] - AvgY2)*scale, line[2], line[3]])
        HeightsX2.append(line[0]- AvgX2)
        HeightsY2.append(line[1] - AvgY2)
        HeightsZ2.append(line[2])

        point2 = np.array([(line[0]- AvgX2)*scale, (line[1] - AvgY2)*scale, line[2]])

        points2 = np.vstack([points2, point2])
        
    print("this was ogheights2", OGHeights2)
        

    #HeightsAverage = sum(HeightsZ) / len(HeightsZ)
    #HeightsMin  = min(HeightsZ)
    #HeightsMax  = max(HeightsZ)

    #HeightsAverage2 = sum(HeightsZ2) / len(HeightsZ2)
    #HeightsMin2  = min(HeightsZ2)
    #HeightsMax2  = max(HeightsZ2)
    #print(OGHeights)
    #print(OGHeights2)
    
    

            
    
    tolerance = 1.2;
    corrections = True;
    if corrections is True:
        print('This is Z average:', AvgZ)
        for point in points:
            #print(point)
            if np.abs(point[2] - AvgZ) > tolerance:
                print("!!! ALERT !!!!")
                print("Value of Point:", point, "is higher than the tolerance, Setting to Avg")
                point[2] = AvgZ ;
                print("now:", point);
                
            #if point[2] > 4:
            #    print("Value of Point:", point, "is greater than 4, setting to 3")
            #    point[2] = AvgZ2;
            #    print("now", point);
        
        if ShapePlot == False:
            for point in points2:
                #print(point)
                if np.abs(point[2] - AvgZ2) > tolerance:
                    print("Value of Point:", point, "is higher than the tolerance, Setting to Avg")
                    point[2] = AvgZ2;
                    print("now:", point);
        
                    
        print('This is Z average:', AvgZ)
        if AvgZ > 20:
            print("Moving down from Average adding 3.1");
            print("After Height Value Adjustment: ")
            for point in points:
                if ShapePlot: point[2] = point[2] - AvgZ;
                else: point[2] = point[2] - AvgZ + 3.1;
                print(point)
            
               
                
            #if point[2] > 4:
            #    print("Value of Point:", point, "is greater than 4, setting to 3")
            #    point[2] = AvgZ2;
            #    print("now", point);
        if AvgZ2 > 20:
            if not ShapePlot: print("Moving down from Average adding 3.1");
            for point in points2:
                point[2] = point[2] - AvgZ + 3.1;
                
    # Extract x, y, z coordinates
    
    print("THIS IS POINTS_2:", points2)
    
    X = points[:, 0]
    Y = points[:, 1]
    Z = points[:, 2]
    #print("Max value:", max(Z))
    #print("Min value:", min(Z))
    
    #print("---")
    #print(OGHeights)
    
    #print("---")
    #print(Heights)
    
    #TEST ARRAY
    #X.fill(4)
    #Y.fill(4)
    
    #Z = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0] #25 points center bowl
    #Z = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0] #21 points center bowl
    #print(X,Y,Z)
    
    #X2 = points2[:, 0]
    #Y2 = points2[:, 1]
    Z2 = points2[:, 2]
    #print("Max value:", max(Z2))
    #print("Min value:", min(Z2))
    
    print(Z2, Z)
    
    #print(Z);
    #print(Z2);

    DX = X;
    DY = Y;
    if ShapePlot == True:
        DZ = Z;
    else:
        print(len(Z))
        print('------')
        print(len(Z2))
        DZ = Z - Z2;
        
        
    #DZ = Z - Z2;
    
    #test points
    #DZ[0] = 10;
    #DX[0] = 0; DY[0] = 0;
    #DX[8] = 60; DY[8] = 0;
    #DZ[8] = 10;
    #print(DX[0], DY[0], DZ[0])
    #print(DX[0], DY[0], DZ[0])


    # Create the design matrix for a higher-order polynomial
    A = np.c_[np.ones(points.shape[0]), DX, DY, DX**2, DY**2, DX*DY, DX**3, DY**3, DX**2*DY, DX*DY**2]
    # Solve for the coefficients
    C, _, _, _ = scipy.linalg.lstsq(A, DZ)
    # Calculate the fitted values
    z_fit = A @ C
    # Calculate the errors
    errors = DZ - z_fit
    
    
    FitMin  = min(z_fit)
    FitMax  = max(z_fit)
    
    #print(FitMin, FitMax)
    
    errorsMax = round(max(errors),2);
    total_error = np.sum(np.abs(errors))
    print()
    print(f" (1) Total error: {total_error}")
    print()

    #newFitMax = FitMax - FitMax; 


    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    u, v = np.meshgrid(u, v)  # Create a meshgrid for u and v
    #fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2

    #'LDT''HDT''LDB''LDR''LDL''LD5''LDF''HDF'
    
    #HEXAGON Formula
    if MaskShape == 'LDF' or MaskShape == 'HDF' or MaskShape == 'LD5':
    #if MaskShape == 'LDF' or MaskShape == 'HDF' or MaskShape == 'LD5' or MaskShape == 'LDR':
        
        u = np.linspace(0, 2 * np.pi, 100)   #   0, 2 * np.pi
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin((u) * 3))**g + 2;
        
    elif MaskShape == 'LDR':
        u = np.linspace(-5/6*np.pi, np.pi/6, 100)
        #u = np.linspace(-np.pi/6, (5/6)*np.pi, 100)   #  -np.pi/2, np.pi/2
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin((u + np.pi) * 3))**g + 2;

    elif MaskShape == 'LDL':
        
        #u = np.linspace(np.pi*5/6, 11/6*np.pi, 100)    #  np.pi/2, -np.pi/2
        u = np.linspace(np.pi/6, 7/6*np.pi,  100)
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;
        
    elif MaskShape == 'LDT':
        
        u = np.linspace(-2/6*np.pi, 4/6*np.pi, 100)   # 0, np.pi
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;
        
    elif MaskShape == 'LDB':
        
        u = np.linspace(1/3*np.pi, -2/3*np.pi, 100)    # np.pi, 2*np.pi
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;

    elif MaskShape == 'HDT':     
        
        u = np.linspace(-2/6*np.pi, 4/6*np.pi, 100)
        #u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;
    
    elif MaskShape == 'HDB':    
        
        u = np.linspace(0, 2 * np.pi, 100)   #   0, 2 * np.pi
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin((u) * 3))**g + 2;
        
        #fn[fn > threshold] = threshold
        
        #UCOMMENT IF BUNDARY DOESNT WORK
        
        
        """
        u = np.linspace(0, 2 * np.pi, 100)   # theta from 0 to 2π
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        
        # Rotate 60 degrees to the left (counterclockwise)
        u_rot = u + np.pi / 3
        
        # Define components using rotated angle
        Y = 17 - 2 * np.abs(np.sin(u_rot * 3))**1
        T = -np.abs(np.cos(u_rot / 2 + (9 * np.pi / 12)))**25 + 1
        J = np.abs(np.cos(u_rot / 2 + (9 * np.pi / 12)))**70
        U = 20 - 10 * (np.sin(u_rot))**2
        E = 0.5 - np.sin(9 * u_rot)
        K = np.abs(np.cos(u_rot / 2 + (9 * np.pi / 12)))**20


        
        # Final function
        fn = Y * T + J * U + E * K
        """
         
    else:
        print("!!!!! ELSE !!!!!")
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;

    
    #important Do not move from here!!!!
    r = np.ones(u.shape) * fn

     #Calculate x, y, and z using the meshgrid
    if MaskShape == 'HDB': 
        x0 = 5 * (r * np.cos(u + np.pi / 3)) * np.sin(v)
        y0 = 5 * (r * np.sin(u + np.pi / 3)) * np.sin(v)
        x = y0
        y = -1*x0
    else:
        x = 5 * (r * np.cos(u + np.pi / 3)) * np.sin(v)
        y = 5 * (r * np.sin(u + np.pi / 3)) * np.sin(v)
    

        
    # Define y threshold for masking
    #y_threshold = 100  # Example threshold
    
    
    #x_masked = np.ma.masked_where(y < y_threshold, x)
    #y_masked = np.ma.masked_where(y < y_threshold, y)


    if MaskShape == 'HD Top':                            ##CHECK THAT THIS WORKS / MAKE IT WORK 
        x_min, x_max = -1000, -30;

        # Apply limits using a for loop
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                if x[i, j] < x_min or x[i, j] > x_max:
                    x[i, j] = np.nan  # Set to NaN or any other value to indicate out of bounds
                    
                    

    ############### THE FUNCTION ###########################

    min_value = np.nanmin(Z)
    max_value = np.nanmax(Z)

    if np.abs(max_value-min_value) >= 0.3:
        print("Spread is too large, ","DELTA:", (max_value-min_value))
        woc = input("Would You Like To Continue With Linear Coeficcients = 0 (t/f)?: ")
        if woc == 't':
            print(C)
            C[2] = 0     
            C[1] = 0
            C[0] = 0
            print(C)
    print();
        
  
    Z = (C[0] + C[1] * x + C[2] * y + C[3] * x**2 + C[4] *y**2 + C[5] * x * y +
         C[6] * x**3 + C[7] * y**3 + C[8] * x**2 * y + C[9] * x * y**2)

    
    Coeficient_Value = np.abs(C[1]) + np.abs(C[2])

    #spike locators
          
    spike_locations = []
    for i in range(len(HeightsX)):
        spike_locations.append((HeightsX[i], HeightsY[i]))
    #print("spike locations", spike_locations)

        
    #Locations of spikes
    #spike_heights = [0.1, 0.2, 0.3, 0.5, 0.8, 1.2, 1.6, 2.1, 2.7, 3.4, 4.2, 5.1, 6.1, 7.2, 8.4, 9.7, 11.1, 12.6, 14.2, 15.9, 17.7, 19.6, 21.6, 23.7, 25.9]  # Heights of spikes
    #spike_widths = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]  # Widths of spikes
    #
    
    #for (x_spike, y_spike), height, width in zip(spike_locations, spike_heights, spike_widths):
    #    spike = height * np.exp(-((x - x_spike)**2 + (y - y_spike)**2) / (2 * width**2))
    #    Z += spike
    
    #print(spike_locations)
    
    #TURN OFF!!!!!!!!!!!!!!!!!!!!!!!!
    #This removes a slant IF NEEDED!!!
    #Z = (C[0] + C[3] * x**2 + C[4] * y**2 + C[5] * x * y + C[6] * x**3 + C[7] * y**3 + C[8] * x**2 * y + C[9] * x * y**2)
    
    #print("look for points that arent near 4:", Z)
    #for value in Z:
    #    for data in value: 
    #       if data > 6:
                 #print(data)
    
    ############ TEST POINTS #############
    #X[0] = 0; Y[0] = 0;
    #X[8] = 100; Y[8] = 0;
    #Z[8] = 3.6;
    #########################


    #print("Min and Max: ",min_value, max_value)
    #print()
    #print("DELTA:", (max_value-min_value))
    #print()
    

    dZdX = (C[1]);       dZdY = (C[2]);      dZdX2 = (2*C[3]);      dZdY2 =(2*C[4]);      dZdXdY = (C[5]);

    Curvature = np.abs((dZdY**2)*(dZdX2) - 2*(dZdX)*(dZdY)*(dZdXdY) + (dZdX**2)*(dZdY2))  /  ((dZdX**2 + dZdY**2)**(3/2))


    print("Curvature @ (x=0 , y=0): " , Curvature)

    k1 = (dZdX2 + dZdY2 + np.sqrt((dZdX2 - dZdY2)**2 + 4*(dZdXdY)**2))/2

    k2 = (dZdX2 + dZdY2 - np.sqrt((dZdX2 - dZdY2)**2 + 4*(dZdXdY)**2))/2

    S = (2/np.pi)*np.arctan((k1 + k2)/(k1 - k2))

    print("Shape Index: " , S)



    C_1 = ["{:.2e}".format(x) for x in C]

    #print(C_1)

    print(f' Z = {C_1[0]} + {C_1[1]}x + {C_1[2]}y + {C_1[3]}x^2 + {C_1[4]}y^2 + {C_1[5]}xy + {C_1[6]}x^3 + {C_1[7]}y^3 + {C_1[8]}yx^2 + {C_1[9]}xy^2')


    z_0 = Z * 0 +  FitMin*0.99# - HeightsMin;
    z_E = Z * 0 +  FitMax*1.01
    
    #print("-",np.sum(Z), "/" , len(Z)*len(Z[0]), '=', np.sum(Z)/(len(Z)*len(Z[0])));
    
    if ShapePlot: 
        NewAvg = np.sum(Z)/(len(Z)*len(Z[0]))
        #print(Z)
        Z = Z - NewAvg;
        z_0 = Z * 0 + np.min(Z)
        FitMin = np.min(Z) - 0.1;
        #print(Z)
    else: 
        NewAvg = 0;
        
    
    #print(z_0)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.axis('off')
    
    # Define the min and max values for the color scale
    #vmin = -0.5
    #vmax = 0.6

    # Plot the surface with a fixed color scale
    #NORMAILZING IS VERY IMPORTANT 
    norm = Normalize(vmin=-0.4, vmax=0.4)
    surf = ax.plot_surface(x, y, Z, cmap=cm.rainbow, norm=norm)
    
    ##### cmap=cm.rainbow
    
    
    if ShapeID  == 'HDB':
        ax.view_init(elev=0, azim=0)
        ax.set_xlim([-75, 75])
        ax.set_ylim([-75, 0])
        ax.set_zlim([-1, 1])
    else:
        ax.view_init(elev=0, azim=0)
        ax.set_xlim([-75, 75])
        ax.set_ylim([-75, 75])
        ax.set_zlim([-1, 1])
    
    # Adding a colorbar (legend) for the heightmap with consistent scale
    cbar = fig.colorbar(surf, ax=ax, orientation='vertical')
    cbar.set_label('Height (mm)')
    
    
    # Add error text below the plot
    if ShapePlot == False:
        error_message = f"Maximum Error Between Measured Difference and Fit +/-{errorsMax}mm "
    else:
        error_message = f"Maximum Error Between Measurement and Fit +/-{errorsMax}mm "
    fig.text(0.5, 0.06, error_message, ha='center', fontsize=8, color='black')
    
    
    dirs = fileloco.replace(".xls","").replace(modulename,"")

    
    filename_1 = selected_file;
    edit1 = filename_1.replace(r"C:\Users\Admin\Documents\OGPQualityControl-master\data\\", "")
    edit2 = edit1.replace(r"Full", '').replace("\\","").replace("TOP","")
    main_name = edit2.split()[0]
    
    #print("This is main name", main_name)
    
    
    #shortmodulename = modulename[14:]
    shortmodulenameedit = selected_file.replace(r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD ", "").replace(r"Full", '').replace("\\","");
    shortmodulename = shortmodulenameedit.replace('.xls','').replace(main_name, '')
    
    """
    if ShapePlot == False:
        title = main_name + " Height Movement Plot" ;
        title2 =  modulename[:16] + " Difference Plot";
    else: 
        title = main_name + " Shape Plot " ;
        title2 = modulename[:16] + " Shape Plot";
    """
    
    titles = input("Enter Custom Title: ")
    title = titles
    title2 = titles
    
    
    #print("DEBUGGING:",title, title2)
    
    l1 = -0.90;
    l2 = 0.90;
    
    #ax.set_zlim([FitMin - 0.3, FitMax + 2.5])
    ax.set_zlim([l1, l2])

    #ax.text(-100, -40, 0, 'CH1', color='black', fontsize=12, zorder=10)  # Bottom-left corner
    #ax.text(-100, 40, 0, 'CH8', color='black', fontsize=12, zorder=10) 
    ax.text(40, 100, FitMin, 'CH8', color='black', fontsize=12, zorder=10)  # Bottom-left corner
    ax.text(-50, 100, FitMin, 'CH1', color='black', fontsize=12, zorder=10) 

    ax.set_title(title2, fontsize=14)

    #surf = ax.plot_surface(x, y, Z, cmap=cm.rainbow, norm=norm)
    shadow = ax.plot_surface(x, y, z_0, color='k', zorder=0)
            
    
    print(FitMax, np.nanmean(z_E))
    print(FitMin, np.nanmean(z_0))
    
    if np.nanmean(z_E) > np.nanmean(z_0):
        print('the mask is on top')
    else:
        print('the mask is below')
            
    
    if ShapeID == 'HDB':
        if ShapePlot is False:
            print(' DIFFERENCE PLOT ???')   
            print(FitMax, np.nanmean(z_0))
            print(FitMin, np.nanmean(z_E))
            cutout = ax.plot_surface(u*12-20, v*80 - 80, z_E+1,
                                 color='white', shade=False, alpha=1.0, zorder=0)
            
        else:    
            cutout = ax.plot_surface(u*-40, v*60 - 60, z_E,
                                 color='white', shade=False, alpha=1.0, zorder=0)
            
            
            
            
    # Axis limits and view settings
    if ShapeID == 'LD5':
        ax.set_xlim([-75, 0])
        ax.set_ylim([-50, 50])
    else:
        ax.set_xlim([-75, 75])
        ax.set_ylim([-75, 75])
    
    l1 = FitMin - 0.3
    l2 = FitMax + 0.3
    ax.set_zlim([l1, l2])
    
    if ShapeID == 'HDB':
        ax.view_init(elev=65, azim=0)
    else:
        ax.view_init(elev=65, azim=-90)

    # Define hand-placed points
    #x_points = np.array([0, 2, -3])
    #y_points = np.array([0, 2, -3])
    #z_points = np.ones_like(x_points) * 0.3 * 4  # Points at the same height
    #ax.scatter(x_points, y_points, z_points, color='black')
    #for i in range(len(x_points)):
    #    ax.text(x_points[i], y_points[i], z_points[i], f'({x_points[i]}, {y_points[i]}, {z_points[i]})', color='black')
        

    print("Current working directory:", os.getcwd())
         
    if ShapePlot is False:
        print("saving into:", dirs , modulename + '-Minus-' + modulename2  , '.png' )
        filename = os.path.join(dirs, modulename + '-Minus-' + modulename2 + '.png')
        plt.savefig(filename)

    else:
        
        filename = os.path.join(dirs, modulename.replace(' ','') + '.png')
        print("saving into:", filename )
        plt.savefig(filename)
    #filenames.append(dirs + '\\GIFS\\tempphotos\\' + str(i) + '.png')

    #print("frame", i)
    plt.show();
    plt.close(fig)  # Clear the current figure
    
    

##########################################################
######PLOTS ABOVE THIS LINE###############################



def get_recent_files(directory, num_files=300):
    # Get all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f)) and not (f.endswith('.png') or f.endswith('.pdf'))]
    # Sort files by modification time in descending order
    files.sort(key=os.path.getmtime, reverse=True)
    # Return the most recent files
    return files[:num_files]

def OldMain():
    
    ###### GET INSTRUCTIONS ########
    gotshape = False; gottype = False;
    while gotshape == False:
        Shape = input("Enter The Shape of the Module: ");
        if Shape in Shapes:
            gotshape = True;
    while gottype == False:
        Process = input("Are we making a Shape Plot or Height (Difference) Plot?:")
        if Process in ProcessTypes:
            gottype = True;
    #################################
    
    ######INTERPRET INSTRUCTIONS#####
    ShapePlot = False; DiffPlot = False;
    if Process in ShapePlotKeys:
        ShapePlot = True;
    elif Process in HeightDiffKeys: 
        DiffPlot = True;
        
    ShapeID = '';
    
    #print("This is the transacation happening: ", Shape, LDRightKeys)

    if Shape in LDTopKeys: ShapeID = 'LDT';
    elif Shape in HDTopKeys: ShapeID = 'HDT';
    elif Shape in LDBotKeys: ShapeID = 'LDB';
    elif Shape in LDRightKeys: ShapeID = 'LDR';
    elif Shape in LDLeftKeys: ShapeID = 'LDL';
    elif Shape in LDFiveKeys: ShapeID = 'LD5';
    elif Shape in LDFullKeys: ShapeID = 'LDF';
    elif Shape in HDFullKeys: ShapeID = 'HDF';
    elif Shape in HDBottomKeys: ShapeID = 'HDB';
    else:  print("no shape detected ")
    
    #print("this is Shape ID:", ShapeID)
    #################################'LDT''HDT''LDB''LDR''LDL''LD5''LDF''HDF'
    
    #############LOOK IN DATA FOLDER FOR APPROPRIATE FOLDER#############
    # Specify the folder path
    folder_path = "C:\\Users\\Admin\\Documents\\OGPQualityControl-master\\data\\"
    if ShapeID == 'LDT':
        folder_path = folder_path + "LD TOP\\"
    if ShapeID == 'HDT':
        folder_path = folder_path + "HD TOP\\"
    if ShapeID == 'LDB':
        folder_path = folder_path + "LD Bottom\\"
    if ShapeID == 'LDR':
        folder_path = folder_path + "LD Right\\"
    if ShapeID == 'LDL':
        folder_path = folder_path + "LD Left\\"
    if ShapeID == 'LD5':
        folder_path = folder_path + "LD Five\\"
    if ShapeID == 'LDF':
        folder_path = folder_path + "LD Full\\"
    if ShapeID == 'HDF':
        folder_path = folder_path + "HD Full\\"
    if ShapeID == 'HDB':
        folder_path = folder_path + "HD Bottom\\"
        
    
    # List all files in the folder
    #files = os.listdir(folder_path)
    #print(f"Files in folder: {files}")  # Debugging print
    
    # Iterate over each file and get the last access time
    #for file in files:
        #file_path = os.path.join(folder_path, file)
        #print(f"Checking file: {file_path}")  # Debugging print
        #if os.path.isfile(file_path):
        #    last_access_time = os.path.getatime(file_path)
        #    last_access_date = datetime.datetime.fromtimestamp(last_access_time)
        #    print(f"File: {file} - Last Accessed: {last_access_date}")
        #else:
        #    print(f"{file_path} is not a file.")  # Debugging print
    
    recent_files = get_recent_files(folder_path);
    
    file_dict = {};
    # Print the list of recent files with corresponding numbers
    #print("Most recent files:")
    for i, file in enumerate(recent_files):
        #print(f"{i + 1}: {file}")
        filename = os.path.basename(file)
        # Extract the main name part, e.g., "MLR3TX-SB0002"
        main_name = filename.split()[0]
        if main_name not in file_dict:
            file_dict[main_name] = []
        file_dict[main_name].append((i + 1, filename))

    # Print the organized files with the original enumerated numbers
    print("\nOrganized files by name:")
    for main_name, files in file_dict.items():
        print(f"Name: {main_name}")
        for file_info in files:
            # Print original enumerated number and file name without the main name part
            enumerated_number, filename = file_info
            description = filename.replace(main_name, '').strip()
            print(f"  {enumerated_number}: {description}")
    

    # Print the list of recent files with corresponding numbers
    #rint("Most recent files:")
    #for i, file in enumerate(recent_files):
    #    print(f"{i + 1}: {file}")

    # Ask the user to select a file
    if DiffPlot is True:
        file_number = int(input("Enter the number of the file you would like to use in the plot (final in f-i): ")) - 1
    else:
        file_number = int(input("Enter the number of the file you would like to use in the plot: ")) - 1
    #);
    # Define and print the selected file
    selected_file = recent_files[file_number]
    
    
    if DiffPlot is True:
        file_number2 = int(input("Enter the number of the file you would like to use in the plot(initial in f-i): ")) - 1
        print();
        # Define and print the selected file
        selected_file2 = recent_files[file_number2]
    
    
    print(f"Selected file: {selected_file}")
    print(f"Selected path: {folder_path}")
    modulename = selected_file.replace(folder_path,"").replace(".xls","")
    print(f"Module Name: {modulename}")
    print();
    
    if DiffPlot is True:
        print(f"Selected file (2): {selected_file2}")
        print(f"Selected path (2): {folder_path}")
        modulename2 = selected_file2.replace(folder_path,"").replace(".xls","")
        print(f"Module Name (2): {modulename2}")
        print();
    else: modulename2 = modulename;
    
    #print(selected_file, folder_path, modulename, ShapeID)
    
    if ShapePlot is True:
        Make_Diff_Plot(selected_file, selected_file, folder_path, modulename, modulename2, ShapeID, ShapePlot)
    elif DiffPlot is True:
        Make_Diff_Plot(selected_file, selected_file2, folder_path, modulename, modulename2, ShapeID, ShapePlot)
        
   
    
def NewMain():
    
    #Ask Weather There's going to be more than one output desired
    Qbatch = False;
    while Qbatch == False:
        BatchStr = input("Single Plot Or Batch?: ")
        if 'Single' in BatchStr or 'single' in BatchStr or 's' in BatchStr:
            BatchBool = False; Qbatch = True;
        elif 'Batch' in BatchStr or 'batch' in BatchStr or 'b' in BatchStr:
            BatchBool = True; Qbatch = True;
        else: 
            print("Not Accepted")
    
            
        
    campaign = False;
    if campaign: 
        print("The Important Plots are:")
        print("All PreRad: Cycle 0 [-35] vs [RT]")
        print("All PreRad: Cycle 0 [RT] vs Cycle 10 [RT]")
        #print("PreRad: Cycle 0 [RT] vs PostRad: Cycle 0 [RT]")
        print("PreRad: Cycle 10 [RT] vs PostRad: Cycle 0 [RT] (Rad Change)")
        #print("PreRad: Cycle 0 [RT] vs PostRad: Cycle 30 [RT]")
        print("All PostRad: Cycle 0 [RT] vs Cycle 30 [RT] (Thermal Change)")
        print("PreRad: Cycle 0 [RT] vs PostRad: Cycle 1 [RT]")
        print("PreRad: Cycle 0 [RT] vs PostRad: Cycle 50 [RT]")
        print("PreRad: Cycle 0 [RT] vs PostRad: Cycle 50 [Bare]")
    
    
    
    
    
    
OldMain();
    