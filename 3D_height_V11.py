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
                
    Version 11: Fundamental Rewrite With Batch Procesing in mind. 

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
from plotter_code_clean import Make_Diff_Plot as CleanMakeDiffPlot


#For other Operations
import os
import datetime
import re

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

Shapes = LDTopKeys + HDTopKeys + LDBotKeys + LDRightKeys + LDLeftKeys + LDFiveKeys +LDFullKeys + HDFullKeys + HDBottomKeys;
ProcessTypes = ShapePlotKeys + HeightDiffKeys;
#print(Shapes)

def Parse_XLS(selected_file):
    fileloco = selected_file;
    df = pd.read_excel(fileloco)
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

def Folder_Path(ShapeID):
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
    return folder_path

def CycleParse(loco):
    lower_loco = str(loco).lower()
    cycle_match = re.search(r'\bcycle\s*([+-]?\d+)\b', lower_loco)
    if cycle_match:
        cycle = int(cycle_match.group(1))
        if cycle == 100 and 'again' in lower_loco:
            return 101
        if cycle == 70 and 'again' in lower_loco:
            return -71
        if cycle == -70 and 'again' in lower_loco:
            return -71
        return cycle

    if '+30' in lower_loco or 'plus30' in lower_loco or '30+' in lower_loco:
        return 30
    if '+40' in lower_loco or 'plus40' in lower_loco or '40+' in lower_loco:
        return 40
    if '+45' in lower_loco or 'plus45' in lower_loco or '45+' in lower_loco:
        return 45
    if '-71' in lower_loco or 'negative71' in lower_loco:
        return -71
    if '-70 again' in lower_loco or 'negative70 again' in lower_loco or '70 again' in lower_loco or '70again' in lower_loco:
        return -71
    if '-70' in lower_loco or 'negative70' in lower_loco:
        return -70
    if '100 again' in lower_loco or '100again' in lower_loco or 'again' in lower_loco and '100' in lower_loco:
        return 101
    if '100' in lower_loco:
        return 100
    if '50' in lower_loco:
        return 50
    if '30' in lower_loco:
        return 30
    if '10' in lower_loco:
        return 10
    if '5' in lower_loco:
        return 5
    return 0


def ConditionLabel(loco):
    lower = str(loco).lower()
    if 'rt' in lower:
        return 'RT'
    if 'cold' in lower:
        return 'Cold'
    if 'bare' in lower or 'stage' in lower:
        return 'Barestage'
    if 'uncon' in lower:
        return 'Unconstrained'
    return 'Unknown'


def ClassifyMeasurementType(suffix):
    lower = str(suffix).lower()
    if 'uncon' in lower:
        return 'unconstrained'
    if 'bare' in lower or 'stage' in lower:
        return 'barestage'
    if 'rt' in lower or 'room temperature' in lower or 'room temp' in lower:
        return 'coldbox_rt'
    if 'cold' in lower or 'coldbox' in lower:
        return 'coldbox_cold'
    return None


def OrderThermalPair(first_loco, second_loco):
    first_type = ClassifyMeasurementType(first_loco)
    second_type = ClassifyMeasurementType(second_loco)
    if first_type == 'coldbox_rt' and second_type == 'coldbox_cold':
        return second_loco, first_loco
    return first_loco, second_loco


def BuildPlotFileName(selected_file, selected_file2, modulename, ShapePlot):
    base_name = modulename.replace(' ', '')
    cycleF1 = CycleParse(selected_file)
    cycleF2 = CycleParse(selected_file2)
    tag1 = ConditionLabel(selected_file)
    tag2 = ConditionLabel(selected_file2)

    if ShapePlot:
        return f"{base_name}_Shape_{tag1}_Cycle_{cycleF1}.png"

    if tag1 == tag2:
        return f"{base_name}_{tag1}_{cycleF1}_vs_{tag2}_{cycleF2}.png"

    return f"{base_name}_{tag1}_{cycleF1}_vs_{tag2}_{cycleF2}.png"


def Make_Diff_Plot(selected_file, selected_file2, folder_path, modulename, modulename2, ShapeID, ShapePlot, Comments, mtype):
    file_name = BuildPlotFileName(selected_file, selected_file2, modulename, ShapePlot)

    return CleanMakeDiffPlot(
        selected_file,
        selected_file2,
        folder_path,
        modulename,
        modulename2,
        ShapeID,
        ShapePlot,
        file_name,
    )
def get_recent_files(directory, num_files=200):
    # Get all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f)) and not (f.endswith('.png') or f.endswith('.pdf'))]
    # Sort files by modification time in descending order
    files.sort(key=os.path.getmtime, reverse=True)
    # Return the most recent files
    return files[:num_files]

def OldMain(full_location, modulename, ShapeID, DiffPlot, ShapePlot, Labels, MType, Comments, selected_file2, modulename2):
    folder_path = Folder_Path(ShapeID)

    recent_files = get_recent_files(folder_path)

    #Making A Library called file_dict
    file_dict = {}
    for i, file in enumerate(recent_files):
        filename = os.path.basename(file)
        main_name = filename.split()[0]
        if main_name not in file_dict:
            file_dict[main_name] = []
        file_dict[main_name].append((i + 1, filename))
    
    
    #########################      IF SHAPE, USE 1st, IF DIFF, USe TARGET     #################
    condition_mapping = {
        "unconstrained": "Unconstrained",
        "barestage": "Barestage",
        "coldbox_cold": "In Cold Box, at Cold",
        "coldbox_rt": "In Cold Box, at Room Temperature"
    }
    mtype = condition_mapping.get(MType)
    
    if ShapePlot:
        if Comments: print(); print(f"-------------   Plotting {mtype} : ({Labels[0]}/{Labels[1]}) Batch Shape Plots ---------------"); print();
        selected_file = full_location
        selected_f = full_location.replace(Folder_Path(ShapeID),"")
        if ShapePlot: 
            if Comments:print(f"Shape Plot of: {selected_f}")
        if DiffPlot: 
            if Comments:print("NOT WORKING YET")
    else: 
        if Comments: print(); print(f"-------------   Plotting {mtype} : ({Labels[0]}/{Labels[1]})  ---------------"); print();



    """if DiffPlot is True:
        file_number2 = int(input("Enter the number of the file you would like to use in the plot(initial in f-i): ")) - 1
        print();
        # Define and print the selected file
        selected_file2 = recent_files[file_number2]
    
    if DiffPlot is True:
        if Comments:
            print(f"Selected file (2): {selected_file2}")
            print(f"Selected path (2): {folder_path}")
        modulename2 = selected_file2.replace(folder_path,"").replace(".xls","")
        if Comments:
            print(f"Module Name (2): {modulename2}")
            print();
    else: modulename2 = modulename;"""
    
    #print(selected_file, folder_path, modulename, ShapeID)
    selected_file = full_location
    if ShapePlot is True:
        Make_Diff_Plot(selected_file, selected_file, folder_path, modulename, modulename2, ShapeID, ShapePlot, Comments, MType)
    elif DiffPlot is True:
        Make_Diff_Plot(selected_file, selected_file2, folder_path, modulename, modulename2, ShapeID, ShapePlot, Comments, MType)
        
   
def RetreiveList(folder_path, ShapeID):
    recent_files = get_recent_files(folder_path);
    file_dict = {};
    
    # Print the list of recent files with corresponding numbers
    print(f"All {ShapeID} Files:")
    for i, file in enumerate(recent_files):
        #print(f"{i + 1}: {file}")
        filename = os.path.basename(file)
        # Extract the main name part, e.g., "MLR3TX-SB0002"
        main_name = filename.split()[0]
        
        if main_name not in file_dict:
            file_dict[main_name] = []
        file_dict[main_name].append((i + 1, filename))


    # Sort modules by number of items (descending)
    sorted_modules = sorted(file_dict.items(), key=lambda x: len(x[1]), reverse=True)

    #THIS IS THE SEARCH RESULTS
    for key, files in sorted_modules:
        count = len(files)
        print(f"Module: {key} ({count} items)")
            
            
    file_name = input("Enter part of the Module's Name:")
    results_dict = {}; MatchList = []; Matches = 0; 
    modulename = ''; key = ''; suffix = ''; full_location = '';
    query = file_name;
    
    for file in recent_files:
        if str(file_name) in str(file):
            selected_file = os.path.basename(file).split()[0]
            #print('Selected: ', selected_file)
            full_location = file
            modulename = selected_file.replace(folder_path, "").replace(".xls", "")
            #Info = Make_Data_Get(full_location, folder_path, modulename, ShapeID)
    
            # Key = module name (first token before space)
            key = os.path.basename(file).split()[0]
            # Value = remainder of filename (after the key)
            suffix = os.path.basename(file).replace(key, "").strip()
            if modulename not in MatchList:
                Matches += 1; MatchList.append(modulename);
            # Initialize nested dict if not present
            if key not in results_dict:
                results_dict[key] = {}
    

    return modulename, key, suffix, full_location, Matches, query;

def Make_Data_Get(selected_file, folder_path, modulename, ShapeID):
    
    ###########################PARSER FROM DATACOLLECTOR, GETS FLATNESS AND OTHER INFO FROM XLSs
    
    fileloco = selected_file;
    df = pd.read_excel(fileloco)
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
    SurfnFlat = "N/A"
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
                
            #ADDING OTHER STATS
        if isinstance(line[2], str):
            if 'Surface' in line[2] or "Extract" in line[2] or line[2] == 'ExtractedSurface':
                SurfnFlat = line[5]

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
    OGHeights = []; OGHeightsX = [];
    OGHeightsY = []; OGHeightsZ = [];
    b = 10/12
    OGpoints = np.empty((0, 3))
    xchk = ychk = zchk = False
    exclude_strings = {'#','Glass', 'HB', 'J', 'Top', 'Left', "Bot", "bottom", 'bot', 'Bottom', 'Right', 'FD1', 'FD2', 'FD3', 'FD4', 'FD4rough', 'FD2rough'}
    Heightlist = [array for array in Heightlist if not any(exclude in array[0] for exclude in exclude_strings)]
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
            OGHeights.append([float(tempsX), float(tempsY), float(tempsZ), b + 1])
            OGHeightsX.append(float(tempsX))
            OGHeightsY.append(float(tempsY))
            OGHeightsZ.append(float(tempsZ))
            OGpoint = np.array([[float(tempsX) - 140, float(tempsY) - 300, float(tempsZ)]])
            OGpoints = np.vstack([OGpoints, OGpoint])
            xchk = ychk = zchk = False;
            zchk = False;
            timer = 0;
            b += 1;
       
    Info = [SurfnFlat, np.average(OGHeightsZ), np.max(OGHeightsZ), np.max(OGHeightsZ)-np.min(OGHeightsZ)]
    return Info

def Locator(modulename, folder_path, ShapeID):
    recent_files = get_recent_files(folder_path)
    return [file for file in recent_files if str(modulename) in str(file)]

def GetDataBreakDown(modulename, folder_path, ShapeID):
    recent_files = get_recent_files(folder_path);
    file_dict = {};
    for i, file in enumerate(recent_files):
        filename = os.path.basename(file)
        # Extract the main name part, e.g., "MLR3TX-SB0002"
        main_name = filename.split()[0]
        
        if main_name not in file_dict:
            file_dict[main_name] = []
        file_dict[main_name].append((i + 1, filename))
   
    results_dict = {};
    for file in recent_files:
        if str(modulename) in str(file):
            selected_file = os.path.basename(file).split()[0]
            full_location = file
            modulename = selected_file.replace(folder_path, "").replace(".xls", "")
            Info = Make_Data_Get(full_location, folder_path, modulename, ShapeID)
    
            # Key = module name (first token before space)
            key = os.path.basename(file).split()[0]
            # Value = remainder of filename (after the key)
            suffix = os.path.basename(file).replace(key, "").strip()
    
            # Initialize nested dict if not present
            if key not in results_dict:
                results_dict[key] = {}
    
            # Store Info under the suffix
            results_dict[key][suffix] = Info
            
    # Now you can inspect the dictionary
    # Create buckets for each measurement type
    measurements = {
        "unconstrained": [],
        "barestage": [],
        "coldbox_cold": [],
        "coldbox_rt": []
    }
    labels = ["flatness", "z_average", "z_max", "range"]

    Survey_Count = 0;
    for key, files in results_dict.items():
        #print(f"Module: {key}")
        for suffix, info in files.items():
            labeled_info = dict(zip(labels, info))
            measurement_type = ClassifyMeasurementType(suffix)
            if measurement_type is None:
                continue

            measurements[measurement_type].append((suffix, labeled_info))
            Survey_Count += 1;
                
    return measurements;

def measurement_matrix(measurements):
    table = []
    for mtype, entries in measurements.items():
        for suffix, info in entries:
            # Try to extract cycle number from filename
            cycle = None
            for word in suffix.replace(".xls", "").split():
                if word.isdigit():
                    cycle = word
            if cycle is None:
                cycle = suffix  # fallback if no cycle number

            table.append([
                cycle,
                info["flatness"],
                info["z_average"],
                info["z_max"],
                info["range"], 
                mtype
            ])

        # Print nicely formatted table
    #print(table)
    return table

def NewMain():
    Comments = False;
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
            
    #GET Shape Instructions  
    gotshape = False; gottype = False;
    while gotshape == False:
        Shape = input("Enter The Shape of the Module: ");
        if Shape in Shapes:
            gotshape = True;
    
    #Batches Should Include Both Shape and Difference Plots
    
    #Get Shape/Difference Plot Instructions'
    if BatchBool == False: 
        while gottype == False:
            Process = input("(Single) -> Are we making a Shape Plot or Height Difference Plot?:")
            if Process in ProcessTypes:
                gottype = True;
    
    
    ######INTERPRET INSTRUCTIONS#####
    ShapeID = '';
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
    #################################
    
    ########################### STATIC FILE DIRECTION SYSTEM (ONLY WORKS HERE ON OGP)
    folder_path = Folder_Path(ShapeID)
    ###########################################################################################
    
    #Example Result:
    print(); print("Batch?:", BatchBool, ",  Shape?:", ShapeID)
    print("Location?:", folder_path); print();
    

    OperableBatch = False; 
    while OperableBatch == False:
        modulename, key, suffix, full_location, Matches, query = RetreiveList(folder_path, ShapeID);
        if Matches == 1:
            OperableBatch = True;
            print(f"Query of key: ({key}) Returned with Match: {modulename}")
        elif Matches > 1:
            print(f"Error: Matched with {Matches} Modules... Only One Module per Batch. (Be More Specific...)"); print()
        else: 
            print("Error: No Modules with {key}"); print()
    
    print();
    #print();  print("Successs:        ","modulename:", modulename, "key: ", key, "Suffix: ", suffix, "Location: ", full_location, "Number of Search Matches: ", Matches)
    
    ##### Get Data Breakdown #######################
    Items = GetDataBreakDown(modulename, folder_path, ShapeID)
    
    #table = measurement_matrix(Items)
    
    DataShape = []
    #print("\nCollected measurements:")
    for mtype, entries in Items.items():   # <-- use .items() here
        count = len(entries)
        first = True;
        for suffix, labeled_info in entries:
            IndivLoco = str(folder_path) + str(modulename) + ' ' + str(suffix)
            if first:
                DataShape.append([mtype, count, IndivLoco])
                first = False;

        
    #DATA SHAPE IS NOT A GOOD INPUT FOR THE BATCH, IT ONLY GIVES GOOD INSTRUCTIONS
    OldMainLocations = []; count = 0; 
    for mtype, entries in Items.items():
        if entries:  # Only proceed if entries is not empty
            for dat in entries: 
                count += 1; 
                loco = str(folder_path) + str(modulename) + ' ' + str(dat[0])
                if os.path.exists(loco):
                    present = "(Found)";
                else: present = "(Not Found)";
                print(f"{count}: "  + loco + " - " + present)
                OldMainLocations.append([loco, mtype])
                
    print();
    ################# BY THIS POINT A MODULE HAS BEEN FOUND AND A LOOP DIRECTING THE OLD MAIN MUST OPERATE #################
    total = 0; pairs = []
    for pair in DataShape:
        total = total + int(pair[1]);    
        
    #Run a Check for if there's any data --- May not Be nessecary
    if total < 1:
        print(f"Can't Make Difference Plots, Not Enough Data: ([{total}] items)")
    elif total >= 1:
        
        #BATCH HERE
        #Start a Batch: 1. Shapes for All Data 2. Difference Between Relevant Measurements
        label = 0
        for data in OldMainLocations:
            # Location Changes, Module Name Is STATIC, Batch Bool is STATIC, ShapeID is STATIC, DiffPlot, ShapePlot
            label += 1
            Labels = [label, count] 
            #print(location, modulename, ShapeID, False, True, Labels)
            OldMain(data[0], modulename, ShapeID, False, True, Labels, data[1], Comments, data[0], modulename)
        print(f"- {count} Shape Plots Made -"); print()
        
        cycle_buckets = {
            'coldbox_rt': {},
            'coldbox_cold': {},
            'barestage': {},
            'unconstrained': {},
        }

        for loco, mtype in OldMainLocations:
            cycle = CycleParse(loco)
            if mtype in cycle_buckets:
                cycle_buckets[mtype][cycle] = loco

        def add_pair(left_loco, right_loco, pair_type):
            left_loco, right_loco = OrderThermalPair(left_loco, right_loco)
            pair_key = tuple(sorted([(left_loco, right_loco), (right_loco, left_loco)]))
            if pair_key in seen_pairs:
                return
            seen_pairs.add(pair_key)
            F1 = [left_loco, modulename, ShapeID, False, True, Labels, pair_type, Comments]
            F2 = [right_loco, modulename, ShapeID, False, True, Labels, pair_type, Comments]
            pairs.append([F1, F2, pair_type])

        seen_pairs = set()

        def add_all_pairs_for_condition(condition_type):
            cycles = sorted(cycle_buckets[condition_type].keys(), key=lambda c: (c < 0, c))
            for idx, cycle in enumerate(cycles):
                for other_cycle in cycles[idx + 1:]:
                    add_pair(cycle_buckets[condition_type][cycle], cycle_buckets[condition_type][other_cycle], condition_type)

        def add_same_cycle_cross_condition_pairs():
            condition_types = ['coldbox_rt', 'coldbox_cold', 'barestage', 'unconstrained']
            for left_idx, left_type in enumerate(condition_types):
                for right_type in condition_types[left_idx + 1:]:
                    shared_cycles = sorted(set(cycle_buckets[left_type].keys()) & set(cycle_buckets[right_type].keys()), key=lambda c: (c < 0, c))
                    for cycle in shared_cycles:
                        add_pair(
                            cycle_buckets[left_type][cycle],
                            cycle_buckets[right_type][cycle],
                            f"{left_type}_vs_{right_type}"
                        )

        add_all_pairs_for_condition('coldbox_rt')
        add_all_pairs_for_condition('coldbox_cold')
        add_same_cycle_cross_condition_pairs()
        add_all_pairs_for_condition('barestage')
        add_all_pairs_for_condition('unconstrained')

        numpairs = len(pairs)
        if Comments: print(f"{numpairs} Pairs Found for Difference Batch. ")     
            
        for Pair in pairs:
            OldMain(Pair[0][0], Pair[0][1], ShapeID, True, False, Labels, Pair[2], Comments, Pair[1][0], Pair[1][1])
            
#OldMain();
if __name__ == "__main__":
    NewMain()
    
