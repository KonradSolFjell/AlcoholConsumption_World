def lese_inn(filbane):
    import csv
    global data_landene
    data_landene = {}
    
    with open(filbane, "r") as fil:
        data = csv.reader(fil, delimiter=",")
        
        overskrifter = next(data)
    
        for linje in data:
            if linje[0] not in data_landene:
                if not len(linje[1]) == 3:
                    continue    
                else:
                    data_landene[linje[0]] = {linje[2] : linje[3]}
            else:
                if not len(linje[1]) == 3:
                    continue    
                else:
                    data_landene[linje[0]][linje[2]] = linje[3] 
                    
    
    return data_landene
    
                

            
