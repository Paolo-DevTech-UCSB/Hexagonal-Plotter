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

def Make_Diff_Plot(selected_file, selected_file2, folder_path, modulename, modulename2, ShapeID, ShapePlot):

    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from mpl_toolkits.mplot3d import proj3d
    from scipy.interpolate import griddata

    # ------------------------------------------------------------
    # 1. Parse and clean your measurement data
    # ------------------------------------------------------------
    Heightlist  = Parse_XLS(selected_file,  folder_path)
    Heightlist2 = Parse_XLS(selected_file2, folder_path)

    Heightlist  = clean_raw_list(Heightlist)
    Heightlist2 = clean_raw_list(Heightlist2)

    _, OGHeights,  OGX,  OGY,  OGZ  = turn_list_into_four(Heightlist)
    _, OGHeights2, OGX2, OGY2, OGZ2 = turn_list_into_four(Heightlist2)

    points,  Heights,  X,  Y,  Z  = Translate_Center(ShapeID, OGX,  OGY,  OGZ,  OGHeights)
    points2, Heights2, X2, Y2, Z2 = Translate_Center(ShapeID, OGX2, OGY2, OGZ2, OGHeights2)

    # Fit polynomial surface
    Z  = np.asarray(Z,  dtype=float)
    Z2 = np.asarray(Z2, dtype=float)
    X  = np.asarray(X,  dtype=float)
    Y  = np.asarray(Y,  dtype=float)
    X2 = np.asarray(X2, dtype=float)
    Y2 = np.asarray(Y2, dtype=float)

    z_fit, z_fit_2, dz_fit, errors, fit_min, fit_max, C, D = Get_Z_Fit(
        X, Y, Z, X2, Y2, Z2, points, points2
    )

    # ------------------------------------------------------------
    # 2. Build your meshgrid surface model (your existing logic)
    # ------------------------------------------------------------
    u, v, fn = Get_Meshgrid(ShapeID)
    r = np.ones(u.shape) * fn

    if ShapeID == 'HDB':
        x0 = 5 * (r * np.cos(u + np.pi/3)) * np.sin(v)
        y0 = 5 * (r * np.sin(u + np.pi/3)) * np.sin(v)
        x = y0
        y = -x0
    else:
        x = 5 * (r * np.cos(u + np.pi/3)) * np.sin(v)
        y = 5 * (r * np.sin(u + np.pi/3)) * np.sin(v)

    # Polynomial surface Z(x,y)
    Zsurf = (
        C[0] + C[1]*x + C[2]*y +
        C[3]*x**2 + C[4]*y**2 + C[5]*x*y +
        C[6]*x**3 + C[7]*y**3 + C[8]*x**2*y + C[9]*x*y**2
    )

    # ------------------------------------------------------------
    # 3. Generate hex grid (radius 8 → 17 tiles corner-to-corner)
    # ------------------------------------------------------------
    def generate_hex_grid(R, hex_r):
        centers = []
        for q in range(-R, R+1):
            r1 = max(-R, -q - R)
            r2 = min(R, -q + R)
            for r in range(r1, r2+1):
                xh = hex_r * 1.5 * q
                yh = hex_r * np.sqrt(3) * (r + q/2)
                centers.append((xh, yh))
        return centers

    hex_radius = 0.5
    grid_radius = 8
    hex_centers = generate_hex_grid(grid_radius, hex_radius)

    # ------------------------------------------------------------
    # 4. Sample your fitted surface at hex centers
    # ------------------------------------------------------------
    pts = np.column_stack([x.ravel(), y.ravel()])
    vals = Zsurf.ravel()
    hex_xy = np.array(hex_centers)

    heights = griddata(pts, vals, hex_xy, method='linear')
    heights = np.nan_to_num(heights, nan=np.nanmean(heights))

    # ------------------------------------------------------------
    # 5. Basalt column renderer
    # ------------------------------------------------------------
    def hexagon(center, radius=1.0):
        cx, cy = center
        ang = np.linspace(0, 2*np.pi, 7)
        return [(cx + radius*np.cos(a), cy + radius*np.sin(a)) for a in ang]

    def depth(poly, ax):
        xs, ys, zs = zip(*poly)
        _, _, zproj = proj3d.proj_transform(xs, ys, zs, ax.get_proj())
        return np.mean(zproj)

    def set_axes_equal(ax):
        xlim = ax.get_xlim3d()
        ylim = ax.get_ylim3d()
        zlim = ax.get_zlim3d()
        ranges = np.array([xlim[1]-xlim[0], ylim[1]-ylim[0], zlim[1]-zlim[0]])
        centers = np.array([np.mean(xlim), np.mean(ylim), np.mean(zlim)])
        radius = 0.5 * max(ranges)
        ax.set_xlim3d([centers[0]-radius, centers[0]+radius])
        ax.set_ylim3d([centers[1]-radius, centers[1]+radius])
        ax.set_zlim3d([centers[2]-radius, centers[2]+radius])

    # ------------------------------------------------------------
    # 6. Render the basalt columns
    # ------------------------------------------------------------
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    norm = (heights - np.min(heights)) / (np.ptp(heights) + 1e-9)
    colors = plt.cm.Greys(norm)

    all_faces = []

    for (cx, cy), h, col in zip(hex_centers, heights, colors):
        base = hexagon((cx, cy), hex_radius)
        top  = [(x, y, h) for (x, y) in base]
        base3d = [(x, y, 0) for (x, y) in base]

        # walls
        for i in range(6):
            j = (i+1) % 6
            face = [base3d[i], base3d[j], top[j], top[i]]
            all_faces.append((face, col))

        # lid
        all_faces.append((top, col))

    # depth sort
    all_faces.sort(key=lambda fc: depth(fc[0], ax))

    for face, col in all_faces:
        poly = Poly3DCollection([face], facecolor=col, edgecolor='black', linewidth=0.3)
        ax.add_collection3d(poly)

    ax.view_init(elev=60, azim=45)
    set_axes_equal(ax)
    ax.set_axis_off()

    # ------------------------------------------------------------
    # 7. Save output
    # ------------------------------------------------------------
    cycleF1 = CycleParse(selected_file)
    cycleF2 = CycleParse(selected_file2)
    outname = f"{modulename}_BasaltPlot_Cycle{cycleF1}_Vs_{cycleF2}.png"
    outfile = os.path.join(folder_path, outname)

    plt.savefig(outfile, dpi=300)
    plt.close(fig)

    print("Basalt Plot Saved:", outfile)
