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