

from Plotter_Config import Shapes, ProcessTypes, ShapePlotKeys, HeightDiffKeys, LDTopKeys, HDTopKeys, LDBotKeys, LDRightKeys, LDLeftKeys, LDFiveKeys, LDFullKeys, HDFullKeys, HDBottomKeys
from Plotter_code import Make_Diff_Plot

def NewMain():

    ShapeID = 'LDR' #'HDF'; #'LDT''HDT''LDB'LDR'LDL''LD5''LDF''HDF'
    ShapePlot = False; #True if we are making a shape plot, false if we are making a height difference plot
    ModuleName = 'MLR3TXSB0002 MAY15'
    FileName = "MLR3TXSB0002 Plot1 50MRad Difference"


    #320MLR3TXSB0002
    a1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Right\MLR3TX-SB0002 After Irradiation Cycle 100 -35.xls"
    a2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Right\MLR3TX-SB0002 After Irradiation Cycle 100 RT.xls"

    b1 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Right\MLR3TX-SB0002 After Irradiation Cycle 1 Coldbox RT.xls"
    b2 = r"C:\Users\Admin\Documents\OGPQualityControl-master\data\LD Right\MLR3TX-SB0002 After Irradiation Cycle 100 RT.xls"

    #320MLT3W2NT0058

    #320MLL3W2NT0049

    #320MHB1WXNT0054

    #320MHF1T4SB0016

    #320MHF1T4SB0018




    File_Name_Final = a1
    File_Name_Initial = a2
    
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
    else: print(f"Selected file (Single): {Folder_final}")
    
    selected_file = Folder_final.replace(folder_path, "")
    selected_file2 = Folder_Initial.replace(folder_path, "")

    ModuleName2 = ModuleName
    
    if ShapePlot is True:
        Make_Diff_Plot(selected_file, selected_file, folder_path, ModuleName, ModuleName2, ShapeID, ShapePlot, FileName)
    elif DiffPlot is True:
        Make_Diff_Plot(selected_file, selected_file2, folder_path, ModuleName, ModuleName2, ShapeID, ShapePlot, FileName)


# This code sends (Filename.xls, filename2.xls, path to filename.xls, ModuleName, ModuleName2, ShapeID, Difference or Shape Boolean)

NewMain()