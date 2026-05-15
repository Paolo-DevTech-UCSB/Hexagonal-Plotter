import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import os
import pandas as pd
import scipy.linalg

#PARAMETERS DO NOT CHANGE
b = 10/12
g = 1
a = 2.0

def Parse_XLS(selected_file, filepath):
    fileloco = selected_file;
    df = pd.read_excel(filepath + fileloco)
    my_array = df.values
    newlist = [];

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
    return Heightlist

def CycleParse(loco):
    if '100' in loco[-12:]: cycle = 100
    elif '50' in loco[-12:]: cycle = 50
    elif '30' in loco[-12:]: cycle = 30
    elif '10' in loco[-12:]: cycle = 10
    elif '5' in loco[-12:]: cycle = 5
    else: cycle = 0
    return cycle

def Get_Meshgrid(ShapeID):
    if ShapeID == 'LDF' or ShapeID == 'HDF' or ShapeID == 'LD5':
    #if MaskShape == 'LDF' or MaskShape == 'HDF' or MaskShape == 'LD5' or MaskShape == 'LDR':
        
        u = np.linspace(0, 2 * np.pi, 100)   #   0, 2 * np.pi
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin((u) * 3))**g + 2;
        
    elif ShapeID == 'LDR':
        u = np.linspace(-5/6*np.pi, np.pi/6, 100)
        #u = np.linspace(-np.pi/6, (5/6)*np.pi, 100)   #  -np.pi/2, np.pi/2
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin((u + np.pi) * 3))**g + 2;

    elif ShapeID == 'LDL':
        
        #u = np.linspace(np.pi*5/6, 11/6*np.pi, 100)    #  np.pi/2, -np.pi/2
        u = np.linspace(np.pi/6, 7/6*np.pi,  100)
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;
        
    elif ShapeID == 'LDT':
        
        u = np.linspace(-2/6*np.pi, 4/6*np.pi, 100)   # 0, np.pi
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;
        
    elif ShapeID == 'LDB':
        
        u = np.linspace(1/3*np.pi, -2/3*np.pi, 100)    # np.pi, 2*np.pi
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;

    elif ShapeID == 'HDT':     
        
        u = np.linspace(-2/6*np.pi, 4/6*np.pi, 100)
        #u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;
    
    elif ShapeID == 'HDB':    
        
        u = np.linspace(0, 2 * np.pi, 100)   #   0, 2 * np.pi
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin((u) * 3))**g + 2;
        
         
    else:
        print("!!!!! ELSE !!!!!")
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        fn = 15 - 1 * a * np.abs(np.sin(u * 3))**g + 2;
    return u, v, fn

def Get_Z_Fit(DX, DY, Z, DX2, DY2, Z2, points, points2):

    #  FIT VS FIT     or        Individual Points vs Individual Points
    FITvFIT = True; 
    DZ = Z - Z2;
    
    #fit both pointsets to z_fit and z_fit_2, then take the difference of those two fits to get the shape difference.
    # Create the design matrix for a higher-order polynomial
    A = np.c_[np.ones(points.shape[0]), DX, DY, DX**2, DY**2, DX*DY, DX**3, DY**3, DX**2*DY, DX*DY**2]
    B = np.c_[np.ones(points.shape[0]), DX2, DY2, DX2**2, DY2**2, DX2*DY2, DX2**3, DY2**3, DX2**2*DY2, DX2*DY2**2]
    
    #Points are Fit THEN Subtracted
    C, _, _, _ = scipy.linalg.lstsq(A, Z)
    D, _, _, _ = scipy.linalg.lstsq(B, Z2)

    # Calculate the fitted values
    z_fit = A @ C   #not used
    z_fit_2 = B @ D   #not used

    dz_fit = z_fit - z_fit_2   #used
    
    # Solve for the coefficients
    if FITvFIT is True:
        errors = Z - z_fit
    else:  
        errors = DZ - dz_fit

    FitMin  = min(dz_fit)
    FitMax  = max(dz_fit)

    return z_fit, z_fit_2, dz_fit, errors, FitMin, FitMax, C, D

def Translate_Center(ShapeID, X_list, Y_list, Z_list, OGHeights):
    Adjusted_Heights = []; Adjusted_HeightsX = []; Adjusted_HeightsY = []; Adjusted_HeightsZ = []
    Adjusted_Points = np.empty((0, 3)); 
    if ShapeID == 'LDR':
        ShapeAdjustmentX = -30;
        ShapeAdjustmentY = 0;
    if ShapeID == 'LDT':
        ShapeAdjustmentX = 0;
        ShapeAdjustmentY = -50;
    if ShapeID == 'HDB':
        ShapeAdjustmentX = -15;
        ShapeAdjustmentY = 0;
    else: 
        ShapeAdjustmentX = 0;
        ShapeAdjustmentY = 0;
    
    if ShapeID == 'LDF' or ShapeID == 'HDF' or ShapeID == 'LD5':
        shadjX = 0; shadjy = 0;
    elif ShapeID == 'LDR':
        shadjX = 0; shadjy = 0;
    elif ShapeID == 'LDL':
        shadjX = -40; shadjy = 0;
    elif ShapeID == 'LDT':
        shadjX = 0; shadjy = 0;
    elif ShapeID == 'LDB':
        shadjX = 0; shadjy = 0;
    elif ShapeID == 'HDT':     
        shadjX = 0; shadjy = 40;
    elif ShapeID == 'HDB':     
        shadjX = 0; shadjy = 0;
    else:
        shadjX = 0; shadjy = 0;
        
    scale = 100/100;    
    
    
    #print("#1#",len(OGHeightsZ), "#2#",len(OGHeightsZ2))
    
    AvgX = sum( X_list)/len( X_list) + ShapeAdjustmentX;      
    AvgY = sum( Y_list)/len( Y_list) + ShapeAdjustmentY;
    
    AvgZ = sum( Z_list)/len( Z_list);      

    
    
    for line in OGHeights:
        Adjusted_Heights.append([(line[0]- AvgX + shadjX)*scale, (line[1] - AvgY + shadjy)* scale, line[2], line[3]])
        Adjusted_HeightsX.append(line[0]- AvgX + shadjX)
        Adjusted_HeightsY.append(line[1] - AvgY + shadjy)
        Adjusted_HeightsZ.append(line[2])

        point = np.array([(line[0]- AvgX + shadjX)*scale, (line[1] - AvgY + shadjy)*scale, line[2]])

        Adjusted_Points = np.vstack([Adjusted_Points, point])
    
    return Adjusted_Points, Adjusted_Heights, Adjusted_HeightsX, Adjusted_HeightsY, Adjusted_HeightsZ, 
        
def turn_list_into_four(HeightList):

    #Takes Array, The Returns, New_HeightList, HeightList_X, HeightList_Y, HeightList_Z
    # New Lists that are in Order 
    b = 10/12
    xchk = False
    ychk = False
    zchk = False
    nameyet = False
    timer = 0
    OGpoints = np.empty((0, 3))
    timer = 0; nameyet = False;
    HeightList_Z = []; HeightList_X = []; HeightList_Y = [];
    New_HeightList = [];
    for line in HeightList:
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
            
            
            
            
            New_HeightList.append([float(tempsX) - 140, float(tempsY) - 300, float(tempsZ), b + 1])
            HeightList_X.append(float(tempsX) - 140)
            HeightList_Y.append(float(tempsY) - 300)
            HeightList_Z.append(float(tempsZ))
            #print(line);
            #print(xlinename);
            OGpoint = np.array([[float(tempsX) - 140, float(tempsY) - 300, float(tempsZ)]])
            Cleaned_HeightList = np.vstack([OGpoints, OGpoint])
            
            #print(point)
            
            xchk = ychk = zchk = False;
            zchk = False;
            timer = 0;
            b += 1;
    return Cleaned_HeightList, New_HeightList, HeightList_X, HeightList_Y, HeightList_Z

def clean_raw_list(Heightlist):
    exclude_strings = {'#','Glass', 'HB', 'J', 'Top', 'Left', "Bot", "bottom", 'bot', 'Bottom', 'Right', 'FD1', 'FD2', 'FD3', 'FD4', 'FD4rough', 'FD2rough'}
    cleaned_list = [array for array in Heightlist if not any(exclude in array[0] for exclude in exclude_strings)]
    return cleaned_list

def Make_Diff_Plot(selected_file, selected_file2, folder_path, modulename, modulename2, ShapeID, ShapePlot, FileName):

    Comments = ''
    mtype = 'ALL'; #barestage, coldbox, unconstrained, ALL
    
    #  1. Retreive Raw Height Data from Excel Files
    
    Heightlist = Parse_XLS(selected_file, folder_path)
    Heightlist2 = Parse_XLS(selected_file2, folder_path)
    #    fileloco2 = selected_file2;
        
    # 2. clean up the lists. (remove lines that are not height measurements)

    exclude_strings = {'#','Glass', 'HB', 'J', 'Top', 'Left', "Bot", "bottom", 'bot', 'Bottom', 'Right', 'FD1', 'FD2', 'FD3', 'FD4', 'FD4rough', 'FD2rough'}
    Heightlist = clean_raw_list(Heightlist)
    Heightlist2 = clean_raw_list(Heightlist2)

    # 3. Extract X, Y, and Z vlaues from the cleaned lists and store in new lists.)

    #Masterlist, Pointslist, Xlist, ylist, zlist = turn_list_into_four(Heightlist)

    Cleaned_HeightList, OGHeights, OGHeightsX, OGHeightsY, OGHeightsZ = turn_list_into_four(Heightlist)
    Cleaned_HeightList2, OGHeights2, OGHeightsX2, OGHeightsY2, OGHeightsZ2 = turn_list_into_four(Heightlist2)

    


    points, Heights, HeightsX, HeightsY, HeightsZ = Translate_Center(ShapeID, OGHeightsX, OGHeightsY, OGHeightsZ, OGHeights)
    points2, Heights2, HeightsX2, HeightsY2, HeightsZ2 = Translate_Center(ShapeID, OGHeightsX2, OGHeightsY2, OGHeightsZ2, OGHeights2)

    X = points[:, 0]
    Y = points[:, 1]
    Z = points[:, 2]

    Z2 = points2[:, 2]
    DX = X; DX2 = X;
    DY = Y; DY2 = Y;
    
    z_fit, z_fit_2, dz_fit, errors, fit_min, fit_max, C, D = Get_Z_Fit(DX, DY, Z, DX2, DY2, Z2, points, points2)
    
    errorsMax = round(max(errors),2);
    total_error = np.sum(np.abs(errors))


    #MOVES THESE VARIABLE DEFIITIONS WITH THE REWRITE
        
                        ### BOTH ###
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    # Initialize points as an empty 2D array with shape (0, 3)
    points = np.empty((0, 3))

    # Initialize points as an empty 2D array with shape (0, 3)
    points2 = np.empty((0, 3))

    xchk = ychk = zchk = False
    b = 0



    u, v, fn = Get_Meshgrid(ShapeID)
    r = np.ones(u.shape) * fn

     #Calculate x, y, and z using the meshgrid
    if ShapeID == 'HDB': 
        x0 = 5 * (r * np.cos(u + np.pi / 3)) * np.sin(v)
        y0 = 5 * (r * np.sin(u + np.pi / 3)) * np.sin(v)
        x = y0
        y = -1*x0
    else:
        x = 5 * (r * np.cos(u + np.pi / 3)) * np.sin(v)
        y = 5 * (r * np.sin(u + np.pi / 3)) * np.sin(v)
    

    if ShapeID == 'HDT':                            ##CHECK THAT THIS WORKS / MAKE IT WORK 
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
        if Comments: 
            print(); print("Spread is large, ","DELTA:", (max_value-min_value)); print()
        
    
    if ShapePlot == False:
        E = C - D
        Z = (E[0] + E[1] * x + E[2] * y + E[3] * x**2 + E[4] *y**2 + E[5] * x * y + E[6] * x**3 + E[7] * y**3 + E[8] * x**2 * y + E[9] * x * y**2)
    else:
        Z = (C[0] + C[1] * x + C[2] * y + C[3] * x**2 + C[4] *y**2 + C[5] * x * y + C[6] * x**3 + C[7] * y**3 + C[8] * x**2 * y + C[9] * x * y**2)
    

    Coeficient_Value = np.abs(C[1]) + np.abs(C[2])

    dZdX = (C[1]);       dZdY = (C[2]);      dZdX2 = (2*C[3]);      dZdY2 =(2*C[4]);      dZdXdY = (C[5]);

    Curvature = np.abs((dZdY**2)*(dZdX2) - 2*(dZdX)*(dZdY)*(dZdXdY) + (dZdX**2)*(dZdY2))  /  ((dZdX**2 + dZdY**2)**(3/2))


    k1 = (dZdX2 + dZdY2 + np.sqrt((dZdX2 - dZdY2)**2 + 4*(dZdXdY)**2))/2

    k2 = (dZdX2 + dZdY2 - np.sqrt((dZdX2 - dZdY2)**2 + 4*(dZdXdY)**2))/2

    S = (2/np.pi)*np.arctan((k1 + k2)/(k1 - k2))

    C_1 = ["{:.3f}".format(x) for x in C]


    z_0 = Z * 0 +  fit_min*0.99# - HeightsMin;
    z_E = Z * 0 +  fit_max*1.01
    
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
    



    
    # Add error text below the plot
    if ShapePlot == False:
        if mtype == 'barestage':
            error_message = f"Maximum Error of the (two) Polynomial Fits  +/-{errorsMax}mm "
        else:
            error_message = f"Maximum Error Between Measured Difference and Fit +/-{errorsMax}mm "
    else:
        error_message = f"Maximum Error Between Measurement and Fit +/-{errorsMax}mm "
    #fig.text(0.5, 0.06, error_message, ha='center', fontsize=8, color='black')
    
    
    dirs = selected_file.replace(".xls","").replace(modulename,"")

    
    filename_1 = selected_file;
    edit1 = filename_1.replace(r"C:\Users\Admin\Documents\OGPQualityControl-master\data\\", "")
    edit2 = edit1.replace(r"Full", '').replace("\\","").replace("TOP","")
    main_name = edit2.split()[0]
    
    #print("This is main name", main_name)
    
    
    #shortmodulename = modulename[14:]
    shortmodulenameedit = selected_file.replace(r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD ", "").replace(r"Full", '').replace("\\","");
    shortmodulename = shortmodulenameedit.replace('.xls','').replace(main_name, '')
    
    if ShapePlot == False:
        title = main_name + " Height Movement Plot" ;
        title2 =  modulename[:16] + " Difference Plot";
    else: 
        title = main_name + " Shape Plot " ;
        title2 = modulename[:16] + " Shape Plot";
    
    #print("DEBUGGING:",title, title2)
    
    l1 = -0.90;
    l2 = 0.90;
    
    #ax.set_zlim([FitMin - 0.3, FitMax + 2.5])
    ax.set_zlim([l1, l2])

    ax.text(40, 100, fit_min, 'CH8', color='black', fontsize=12, zorder=10)  # Bottom-left corner
    if ShapeID != 'LD5':
        ax.text(-50, 100, fit_min, 'CH1', color='black', fontsize=12, zorder=10) 

    #ax.set_title(title2, fontsize=14)
    ax.set_title("")   # Remove title
    


    #surf = ax.plot_surface(x, y, Z, cmap=cm.rainbow, norm=norm)
    shadow = ax.plot_surface(x, y, z_0, color='k', zorder=0)
            

    if ShapeID == 'HDB':
        if ShapePlot is False:   
            print(fit_max, np.nanmean(z_0))
            print(fit_min, np.nanmean(z_E))
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
    
    l1 = fit_min - 0.3
    l2 = fit_max + 0.3
    ax.set_zlim([l1, l2])
    
    if ShapeID == 'HDB':
        ax.view_init(elev=90, azim=0)
    else:
        ax.view_init(elev=90, azim=-90)

    # --- Projected axes overlay (show module dimensions) ---
    # Compute plot bounds
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    # Raise axis level above surface so axis and labels appear in front
    z_axis_level = l2 + 0.08

    # Place axes at the plot bottom and left (L-shaped layout)
    # X axis runs left->right at the bottom (y = y_min)
    x_axis_y = y_min
    x_line_x = np.array([x_min, x_max])
    x_line_y = np.array([x_axis_y, x_axis_y])
    x_line_z = np.array([z_axis_level, z_axis_level])
    ax.plot(x_line_x, x_line_y, x_line_z, color='k', linewidth=2)

    # Y axis runs bottom->top at the left (x = x_min)
    y_axis_x = x_min
    y_line_x = np.array([y_axis_x, y_axis_x])
    y_line_y = np.array([y_min, y_max])
    y_line_z = np.array([z_axis_level, z_axis_level])
    ax.plot(y_line_x, y_line_y, y_line_z, color='k', linewidth=2)

    # Map plot units to physical length: X span -> 18.75 cm, Y span -> 16.75 cm
    plot_span_x = x_max - x_min if (x_max - x_min) != 0 else 1.0
    plot_span_y = y_max - y_min if (y_max - y_min) != 0 else 1.0
    cm_per_unit_x = 18.75 / plot_span_x
    cm_per_unit_y = 16.75 / plot_span_y

    # Add end labels for X axis at bottom-left and bottom-right, placed outside (in Y)
    outside_y = y_min - 0.08 * plot_span_y
    # (removed duplicate end labels; ticks will carry numeric labels)

    # Add end labels for Y axis at left-bottom and left-top, placed outside (in X)
    outside_x = x_min - 0.03 * plot_span_x
    # (removed duplicate end labels; ticks will carry numeric labels)

    # Add tick marks on X axis (0, 5, 10, 15, 18.75 cm)
    tick_cms_x = [0.0, 5.0, 10.0, 15.0, 18.75]
    tick_height = 0.02 * (l2 - l1)
    label_offset = 0.01 * (l2 - l1)
    for t in tick_cms_x:
        # convert cm to plot x coordinate
        tx = x_min + (t / 18.75) * plot_span_x
        # draw tick as short vertical line in z
        tz0 = z_axis_level - tick_height
        tz1 = z_axis_level
        ax.plot([tx, tx], [x_axis_y, x_axis_y], [tz0, tz1], color='k', linewidth=1.5)
        # place numeric label just outside in Y (no unit)
        ax.text(tx, outside_y, z_axis_level + label_offset, '{:g}'.format(t), color='k', fontsize=9, ha='center', va='top', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

    # Add tick marks on Y axis (0, 4, 8, 12, 16.75 cm)
    tick_cms_y = [0.0, 4.0, 8.0, 12.0, 16.75]
    for t in tick_cms_y:
        ty = y_min + (t / 16.75) * plot_span_y
        tz0 = z_axis_level - tick_height
        tz1 = z_axis_level
        ax.plot([y_axis_x, y_axis_x], [ty, ty], [tz0, tz1], color='k', linewidth=1.5)
        # place numeric label just outside in X (no unit)
        ax.text(outside_x, ty, z_axis_level + label_offset, '{:g}'.format(t), color='k', fontsize=9, ha='right', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

    # Add a single unit label centered along the X axis outside the ticks
    # Move the unit label further down so it doesn't overlap tick labels
    # Move the unit label further down (larger offset) so it doesn't overlap any ticks
    ax.text((x_min + x_max) / 2, outside_y - 0.12 * plot_span_y, z_axis_level + label_offset * 2, '(cm)', color='k', fontsize=10, ha='center', va='top', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))


    # --- Add colorbar FIRST ---
    # moved slightly left so it doesn't get cropped by the figure edge
    cax = fig.add_axes([0.84, 0.15, 0.03, 0.70])
    cbar = fig.colorbar(surf, cax=cax)
    cbar.set_label('Height (mm)')

    # --- NOW move subplot (this is the ONLY place it works) ---
    ax.set_position([0.08, 0.12, 0.75, 0.78])

    # --- Annotation inside subplot ---
    # Place the small annotation in the figure's top-left corner (figure coordinates)
    fig.text(
        0.02, 0.98, "CMS Preliminary\n" + "320-ML-R3TX-SB-0002",
        transform=fig.transFigure,
        ha="left", va="top",
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black", alpha=0.8)
    )

    # --- UCSB in top-right of entire figure ---
    fig.text(
        0.98, 0.98, "Phase 2",
        ha="right", va="top",
        fontsize=16, fontweight="bold"
    )

    # Define hand-placed points
    #x_points = np.array([0, 2, -3])
    #y_points = np.array([0, 2, -3])
    #z_points = np.ones_like(x_points) * 0.3 * 4  # Points at the same height
    #ax.scatter(x_points, y_points, z_points, color='black')
    #for i in range(len(x_points)):
    #    ax.text(x_points[i], y_points[i], z_points[i], f'({x_points[i]}, {y_points[i]}, {z_points[i]})', color='black')
        
    """print()
    print("Current working directory:", os.getcwd())
    
    print()
    print("Folder_Path Check: ", Folder_Path(ShapeID))
    
    print()
    print("Dirs: ", dirs)
    
    
    print("This is suffix:", suffix)"""
    suffix = dirs.replace(folder_path,'')
    directory = folder_path
    cycleF1 = CycleParse(selected_file)
    cycleF2 = CycleParse(selected_file2)
    # Determine save path using FileName passed from controller
    def _make_save_path(file_name):
        # If file_name is an absolute path or contains a directory, use it as-is
        if os.path.isabs(file_name) or os.path.dirname(file_name):
            base = file_name
        else:
            base = os.path.join(folder_path, file_name)
        # Add .png if missing
        if not os.path.splitext(base)[1]:
            base = base + '.png'
        return base

    save_path = _make_save_path(FileName)

    if ShapePlot is False:
        if Comments:
            print(); print("saving into:", directory , modulename , '_Difference_Plot_Cycle', cycleF1, "Vs", cycleF2, '.png' )
        print ("Difference Plot: ", modulename.replace(' ',''), "::", cycleF1, "-" , cycleF2, mtype )
        plt.savefig(save_path)
    else:
        if Comments:
            print(); print("saving into:", save_path )
        else:
            print ("Shape Plot: ", modulename.replace(' ',''), cycleF1, mtype)
        plt.savefig(save_path)
    #filenames.append(dirs + '\\GIFS\\tempphotos\\' + str(i) + '.png')

    #print("frame", i)
    #plt.show();
    plt.close(fig)  # Clear the current figure
    if Comments:
        print(); 
        print('-----------------    Done   -----------------------');
        print(); 
    
    


