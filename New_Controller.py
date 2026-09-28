

#from plotter_code_clean import Shapes, ProcessTypes, ShapePlotKeys, HeightDiffKeys, LDTopKeys, HDTopKeys, LDBotKeys, LDRightKeys, LDLeftKeys, LDFiveKeys, LDFullKeys, HDFullKeys, HDBottomKeys
from plotter_code_clean import Make_Diff_Plot

def NewMain():

    ShapeID = 'HDF' #'HDF'; #'LDT''HDT''LDB'LDR'LDL''LD5''LDF''HDF'
    ShapePlot = False; #True if we are making a shape plot, false if we are making a height difference plot
    ModuleName = '320-MHF-2TD-SB0125'
    FileName = "320MHF2TDSB0125 Verifier RTvsCOLD cycle10.png"
    #ColdVsRT  C0VsC30

    """ShapeID = 'HDF'; #'LDT''HDT''LDB''LDR''LDL''LD5''LDF''HDF'
    ShapePlot = False; #True if we are making a shape plot, false if we are making a height difference plot
    ModuleName = '320-MHF-2WD-SB0065';
    File_Name_Final = "320MHF1WCSB0006 Barestage Cycle 100.xls"; #insert the file name here. For example, "MLR3TX-SB0002.xls"   Final in Final - Initial
    File_Name_Initial = '320-MHF-2WD-SB0065 Barestage Cycle 0.xls'; #insert the file name here. For example, "MLR3TX-SB0002.xls"  Initial in Final - Initial"""

    a5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0027 InColdbox RT Cycle 100 again.xls"
    a6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0027 InColdbox -20 Cycle 100 again.xls"
    a7 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0027 InColdbox RT Cycle 0.xls"
    a8 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0027 InColdbox -20 Cycle 0.xls"

    b5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0073 InColdbox RT Cycle 100.xls"
    b6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0073 InColdbox -20 Cycle 100.xls"
    b7 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0073 InColdbox RT Cycle 0.xls"
    b8 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0073 InColdbox -20 Cycle 0.xls"

    c5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0012 InColdbox RT Cycle 100.xls"
    c6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0012 InColdbox -20 Cycle 100.xls"
    c7 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0012 InColdbox RT Cycle 0.xls"
    c8 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0012 InColdbox -20 Cycle 0.xls"

    d5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 InColdbox RT Cycle 100.xls"
    d6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 InColdbox -20 Cycle 100.xls"
    d7 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 InColdbox RT Cycle 0.xls"
    d8 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 InColdbox -20 Cycle 0.xls"

    e5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0235 InColdbox RT Cycle 100.xls"
    e6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0235 InColdbox -20 Cycle 100.xls"
    e7 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0235 InColdbox RT Cycle 0.xls"
    e8 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0235 InColdbox -20 Cycle 0.xls"
    e9 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0235 InColdbox RT Cycle 100 After Rebolting.xls"


    f3 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox RT Cycle -70.xls"
    f4 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox -20 Cycle -70.xls"
    f5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox RT Cycle 100.xls"
    f6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox -20 Cycle 100.xls"
    f7 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox RT Cycle 0.xls"
    f8 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox -20 Cycle 0.xls"



    z1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0065 Barestage Cycle 100.xls"
    z2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0065 Barestage Cycle 0.xls"

    y1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0065 Barestage Cycle 100.xls"; #insert the file name here. For example, "MLR3TX-SB0002.xls"   Final in Final - Initial
    y2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0065 Barestage Cycle 0.xls"; #insert the file name here. For example, "MLR3TX-SB0002.xls"  Initial in Final - Initial

    x1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0178 InColdbox -25 After Delamination.xls"
    x2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0178 InColdbox RT After Delamination.xls"


    #320MLR3TXSB0002
    a1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Right\MLR3TX-SB0002 After Irradiation Cycle 100 -35.xls"
    a2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Right\MLR3TX-SB0002 After Irradiation Cycle 100 RT.xls"

    b1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Right\MLR3TX-SB0002 After Irradiation Cycle 1 Coldbox RT.xls"
    b2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Right\MLR3TX-SB0002 After Irradiation Cycle 100 RT.xls"

    #320MLT3W2NT0058
    c1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Top\320MLT3W2NT0058 Coldbox -35 Cycle 30.xls"
    c2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Top\320MLT3W2NT0058 Coldbox RT Cycle 30.xls"
    c3 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Top\320MLT3W2NT0058 Coldbox -25 Cycle 10.xls"
    c4 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Top\320MLT3W2NT0058 Coldbox RT Cycle 10.xls"

    d1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Top\320MLT3W2NT0058 Coldbox RT.xls"
    d2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Top\320MLT3W2NT0058 Coldbox RT Cycle 30.xls"

    #320MLL3W2NT0049
    e1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Left\320MLL3W2NT00049 Coldbox -25 Cycle 30.xls"
    e2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Left\320MLL3W2NT00049 Coldbox RT Cycle 30.xls"

    f1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Left\320MLL3W2NT00049 Coldbox RT Cycle 0.xls"
    f2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Left\320MLL3W2NT00049 Coldbox RT Cycle 30.xls"
    #320MHB1WXNT0054
    g1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD Bottom\320MHB1WXNT00054 Coldbox RT Cycle 30.xls"
    g2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD Bottom\320MHB1WXNT00054 Coldbox -30 Cycle 30.xls"

    h1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD Bottom\320HB1WXNT0054 Coldbox RT Cycle 0.xls"
    h2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD Bottom\320MHB1WXNT00054 Coldbox RT Cycle 30.xls"
    #320MHF1T4SB0016
    I1= r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1T4SB0016 Coldbox -25 Cycle 100.xls"
    I2= r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1T4SB0016 Coldbox RT Cycle 100.xls"

    J1= r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1T4SB0016 In Coldbox RT Cycle 0.xls"
    J2= r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1T4SB0016 Coldbox RT Cycle 100.xls"
    #320MHF1T4SB0018
    k1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1T4SB0018 In Coldbox -25C Cycle 100.xls"
    k2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1T4SB0018 In Coldbox RT Cycle 100.xls"

    L1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1T4SB0018 Coldbox RT Cycle 0.xls"
    L2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1T4SB0018 In Coldbox RT Cycle 100.xls"





    M1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0244 InColdbox -20 Cycle 0.xls"
    M2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0244 InColdbox RT Cycle 0.xls"
    M3 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0244 InColdbox -20 Cycle 100.xls"
    M4 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0244 InColdbox RT Cycle 100.xls"

    N1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0238 InColdbox -20 Cycle 0.xls"
    N2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0238 InColdbox RT Cycle 0.xls"
    N3 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0238 InColdbox RT Cycle 100.xls"
    N4 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0238 InColdbox -20 Cycle 100.xls"
    
    O1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0240 InColdbox -20 Cycle 0.xls"
    O2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0240 InColdbox RT Cycle 0.xls"

    P1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 2025 Error Measure 1.xls"
    P2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 2025 Error Measure 2.xls"
    P3 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 2025 Error Measure 3.xls"
    P4 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 2025 Error Measure 4.xls"
    P5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 2025 Error Measure 5.xls"
    P6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 2025 Error Measure 6.xls"
    P7 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 2025 Error Measure 7.xls"
    P8 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0008 2025 Error Measure 8.xls"

    K1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox RT Cycle +40.xls"
    K2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox RT Cycle +45.xls"
    K3 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0234 InColdbox RT Cycle +30.xls"

    Q1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1WCSB0006 InColdbox RT Cycle 0.xls"
    Q2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0065 InColdbox RT Cycle 0.xls"
    Q3 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0244 InColdbox RT New Cycle 0.xls"
    Q4 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0010 InColdbox RT Cycle 0.xls"
    Q5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0233 InColdbox RT Cycle 0.xls"
    Q6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0236 InColdbox RT Cycle 0.xls"

    R1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF1WCSB0006 InColdbox RT Cycle Warm Again.xls"
    R2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2WDSB0065 InColdbox RT Cycle Warm.xls"
    R3 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0244 InColdbox RT New Cycle Warm.xls"
    R4 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0010 InColdbox RT Cycle Warm.xls"

    R5 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0233 InColdbox RT Cycle Warm.xls"
    R6 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0236 InColdbox RT Cycle Warm.xls"

    S1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0125 InColdbox -20 Cycle 10.xls"
    S2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\HD full\320MHF2TDSB0125 InColdbox RT Cycle 10.xls"



    File_Name_Final = S1
    File_Name_Initial = S2
    
    if ShapePlot is True: DiffPlot = False
    else: DiffPlot = True;
    
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

    Folder_final = folder_path + File_Name_Final    
    
    Folder_Initial = folder_path + File_Name_Initial   

    if DiffPlot is True:
        print(f"Selected file (final): {Folder_final}")
        print(f"Selected file (initial): {Folder_Initial}")
        print(f"Module Name: {ModuleName}")
    else:
        print(f"Selected file (Single): {Folder_final}")
    
    ModuleName2 = ModuleName

    if ShapePlot is True:
        pg_data1 = PGConnect.main(ModuleName)
        pg_data2 = PGConnect.main(ModuleName2)
        Make_Diff_Plot(pg_data1, pg_data2, folder_path, ModuleName, ModuleName2, ShapeID, ShapePlot, FileName)
    elif DiffPlot is True:
        selected_file = Folder_final.replace(folder_path, "")
        selected_file2 = Folder_Initial.replace(folder_path, "")
        Make_Diff_Plot(selected_file, selected_file2, folder_path, ModuleName, ModuleName2, ShapeID, ShapePlot, FileName)


# This code sends (Filename.xls, filename2.xls, path to filename.xls, ModuleName, ModuleName2, ShapeID, Difference or Shape Boolean)

NewMain()