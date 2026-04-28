

from Plotter_Config import Shapes, ProcessTypes, ShapePlotKeys, HeightDiffKeys, LDTopKeys, HDTopKeys, LDBotKeys, LDRightKeys, LDLeftKeys, LDFiveKeys, LDFullKeys, HDFullKeys, HDBottomKeys
from Plotter_code_2 import Make_Diff_Plot

def NewMain():

    ShapeID = 'LDR'; #'LDT''HDT''LDB''LDR''LDL''LD5''LDF''HDF'
    ShapePlot = False; #True if we are making a shape plot, false if we are making a height difference plot
    ModuleName = '320-MLR-3TX-SB0002';
    File_Name_Final = "MLR3TX-SB0002 After Irradiation Cycle 100 -35.xls"; #insert the file name here. For example, "MLR3TX-SB0002.xls"   Final in Final - Initial
    File_Name_Initial = 'MLR3TX-SB0002 After Irradiation Cycle 100 RT.xls'; #insert the file name here. For example, "MLR3TX-SB0002.xls"  Initial in Final - Initial

    
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
        Make_Diff_Plot(selected_file, selected_file, folder_path, ModuleName, ModuleName2, ShapeID, ShapePlot)
    elif DiffPlot is True:
        Make_Diff_Plot(selected_file, selected_file2, folder_path, ModuleName, ModuleName2, ShapeID, ShapePlot)


# This code sends (Filename.xls, filename2.xls, path to filename.xls, ModuleName, ModuleName2, ShapeID, Difference or Shape Boolean)

NewMain()