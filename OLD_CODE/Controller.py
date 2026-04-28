
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
            if 'Unconstrained' in suffix or 'uncon' in suffix:
                #print('unconstrained')
                measurements["unconstrained"].append((suffix, labeled_info))
                Survey_Count += 1;
    
            elif 'bare' in suffix or 'Bare' in suffix or 'stage' in suffix:
                #print("barestage")
                measurements["barestage"].append((suffix, labeled_info))
                Survey_Count += 1;
    
            elif ('Cold' in suffix or 'cold' in suffix) and ('RT' not in suffix and 'rt' not in suffix):
                #print("coldbox at cold")
                measurements["coldbox_cold"].append((suffix, labeled_info))
                Survey_Count += 1;
    
            elif ('Cold' in suffix or 'cold' in suffix) and ('RT' in suffix or 'rt' in suffix):
                #print("coldbox at rt")
                measurements["coldbox_rt"].append((suffix, labeled_info))
                Survey_Count += 1;
                
    return measurements;



def get_recent_files(directory, num_files=200):
    # Get all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f)) and not (f.endswith('.png') or f.endswith('.pdf'))]
    # Sort files by modification time in descending order
    files.sort(key=os.path.getmtime, reverse=True)
    # Return the most recent files
    return files[:num_files]

def CycleParse(loco):
    if '100' in loco[-12:]: cycle = 100
    elif '50' in loco[-12:]: cycle = 50
    elif '30' in loco[-12:]: cycle = 30
    elif '10' in loco[-12:]: cycle = 10
    elif '5' in loco[-12:]: cycle = 5
    else: cycle = 0
    return cycle
    
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
        
        for data in OldMainLocations:
            cycle = CycleParse(data[0])
            F1 = [data[0], modulename, ShapeID, False, True, Labels, data[1], Comments]
            
            # Append - Same Cycle - Thermal Pairs
            if data[1] == 'coldbox_rt': 
                for SE_data in OldMainLocations: 
                    F2 = [SE_data[0], modulename, ShapeID, False, True, Labels, SE_data[1], Comments]
                    if SE_data[1] == 'coldbox_cold':
                        if cycle == CycleParse(SE_data[0]):
                            #print(cycle, 'vs', CycleParse(SE_data[0]))
                            pairs.append([F1,F2, "Cold - Roomtemp"])
                               
            # Append - Same Barestage - Different Cycles
            if data[1] == 'barestage':
                for SE_data in OldMainLocations:
                    F2 = [SE_data[0], modulename, ShapeID, False, True, Labels, SE_data[1], Comments]
                    if SE_data[1] == 'barestage':
                        if cycle > CycleParse(SE_data[0]):
                            pairs.append([F1,F2, data[1]])
                        
            # Append - Same RT - Different Cycles
            if data[1] == 'coldbox_rt':
                for SE_data in OldMainLocations:
                    F2 = [SE_data[0], modulename, ShapeID, False, True, Labels, SE_data[1], Comments]
                    if SE_data[1] == 'coldbox_rt':
                        if cycle > CycleParse(SE_data[0]):
                            pairs.append([F1,F2, data[1]])
                            
            # Append - Same Cold - Different Cycles
            if data[1] == 'coldbox_cold':
                for SE_data in OldMainLocations:
                    F2 = [SE_data[0], modulename, ShapeID, False, True, Labels, SE_data[1], Comments]
                    if SE_data[1] == 'coldbox_cold':
                        if cycle > CycleParse(SE_data[0]):
                            pairs.append([F1,F2, data[1]])
            
            # Append - Unconstrained - Different Cycles
            if data[1] == 'unconstrained':
                for SE_data in OldMainLocations:
                    F2 = [SE_data[0], modulename, ShapeID, False, True, Labels, SE_data[1], Comments]
                    if SE_data[1] == 'unconstrained':
                        if cycle > CycleParse(SE_data[0]):
                            pairs.append([F1,F2, data[1]])

        numpairs = len(pairs)
        if Comments: print(f"{numpairs} Pairs Found for Difference Batch. ")     
            
        for Pair in pairs:
            OldMain(Pair[0][0], Pair[0][1], ShapeID, True, False, Labels, Pair[2], Comments, Pair[1][0], Pair[1][1])
            
#OldMain();
NewMain()
    



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
        
   