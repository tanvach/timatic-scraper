import re
import sqlite3

db_path = "/tmp/Timatic.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

### Attempt to parse Timatic texts to obtain simple Yes/No visa requirements

def insertrow(nat,dest,visareq,desc):
    cur.execute('INSERT INTO VisaReq (National, Destination, Visareq, Desc) VALUES (?,?,?,?);', (nat, dest, visareq, desc))
    
### Drop table if exists and create a new one ###
cur.execute('DROP TABLE VisaReq;')
cur.execute('CREATE TABLE VisaReq (National text, Destination text, Visareq INTEGER, Desc Text, UNIQUE(National,Destination));')

### Get national codes to parse ###
nationals = cur.execute('SELECT DISTINCT National FROM Timatic_Raw;').fetchall()



### Unholy lump of Regex. We need your help!

for national in nationals:

    rows = cur.execute('SELECT * FROM Timatic_Raw WHERE National = ?;',national).fetchall()
    
    for row in rows:
        
        nat = row[0]
        dest = row[1]
        text = row[2]

        text = text.replace("British","United Kingdom")

        national = re.search("(?<=UTC.National.).{1,30}", text, re.IGNORECASE).group(0).split(" (")[0]
        destination = re.search("(?<=Destination ).{1,30}", text, re.IGNORECASE).group(0).split(" (")[0]
                
        r = re.search("visa on arrival", text, re.IGNORECASE)
        if r != None:
            visa_on_arrival = "(" + r.group(0) + ")"
        else:
            visa_on_arrival = ""

        r = re.search("\(ETA\)", text, re.IGNORECASE)
        if r != None:
            ETA_required = r.group(0)
        else:
            ETA_required = ""

        r = re.search("e-visa", text, re.IGNORECASE)
        if r != None:
            e_visa = "(" + r.group(0) + ")"
        else:
            e_visa = ""
            

        extra_conditions = visa_on_arrival + ETA_required + e_visa

        r = re.search("visa not required\.",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required" )
            insertrow(nat,dest,0,printstr)
            continue

        r = re.search("visa.{1,100}issued.{1,30}Schengen C", text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " Schengen visa Required" )
            insertrow(nat,dest,1,printstr)
            continue
        r = re.search("Visa required, except for Holders of Person of Indian Origin",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa Required (India)" )
            insertrow(nat,dest,1,printstr)
            continue
        
        r = re.search("Visa required, except for Holders of a Pakistan Origin",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa Required (Pakistan)" )
            insertrow(nat,dest,1,printstr)
            continue
          
        r = re.search("Visa required, except for Those of Yemeni origin",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa Required (Yemeni)" )
            insertrow(nat,dest,1,printstr)
            continue
            
        r = re.search("Visa required, except for Those of Turkish",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa Required (Trukish)" )
            insertrow(nat,dest,1,printstr)
            continue
            
        r = re.search("Visa required,.+former nationals of the Philippines",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa Required (Trukish)" )
            insertrow(nat,dest,1,printstr)
            continue
            
        r = re.search("Visa required, except for.{1,300}Hong Kong",text, re.IGNORECASE)
        if r != None and nat == "CN":
            printstr = ( nat + " to " + dest + " visa required" )
            insertrow(nat,dest,1,printstr)
            print(text)
            continue  
        
        r = re.search("Visa required, except for.{1,100}national.{1,30}" + national,text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required" )
            insertrow(nat,dest,0,printstr)
            #print(text)
            continue
            
        r = re.search("Visa required, except for.{1,100}Holders.{1,30}" + national,text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required" )
            insertrow(nat,dest,0,printstr)
            #print(text)
            continue
            
        r = re.search("Visa required, except for.{1,100}Holders.{1,30}United Kingdom",text, re.IGNORECASE)
        if r != None:
            if nat in ["GI","BS","FK","AI","BM","KY","MS","TC","VG"]:
                printstr = ( nat + " to " + dest + " visa not required" )
                insertrow(nat,dest,0,printstr)
                #print(text)
                continue
                
        r = re.search("Visa required, except for.{1,100}Holders.{1,30}Australian",text, re.IGNORECASE)
        if r != None:
            if nat in ["NF"]:
                printstr = ( nat + " to " + dest + " visa not required" )
                insertrow(nat,dest,0,printstr)
                #print(text)
                continue
                
        r = re.search("Visa required, except for.{1,100}Holders.{1,30}New Zealand",text, re.IGNORECASE)
        if r != None:
            if nat in ["NU"]:
                printstr = ( nat + " to " + dest + " visa not required" )
                insertrow(nat,dest,0,printstr)
                #print(text)
                continue
                
        r = re.search("Visa required, except for.{1,100}Nationals.{1,30}USA",text, re.IGNORECASE)
        if r != None:
            if nat in ["AS","GU","MP","PR","VI"]:
                printstr = ( nat + " to " + dest + " visa not required" )
                insertrow(nat,dest,0,printstr)
                #print(text)
                continue
            
        r = re.search("visa required\.", text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa Required" )
            insertrow(nat,dest,1,printstr)
            continue
        
        r = re.search("visa required, except.{1,30}V\\.I\\.P",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa Required" )
            insertrow(nat,dest,1,printstr)
            continue
            
        
        r = re.search("Although no visa requirements exist",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required (maybe)" )
            insertrow(nat,dest,1,printstr)
            continue
            
        r = re.search("except for Holders of a visa issued by.{1,5}EU.{1,5}Member",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " EU visa required" )
            insertrow(nat,dest,1,printstr)
            continue
        
        r = re.search("Visa required \\(Entry Permit\\)",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required" )
            insertrow(nat,dest,1,printstr)
            continue
          
        r = re.search("Visa required, except for Holders of a valid student or employment authorization",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required" )
            insertrow(nat,dest,1,printstr)
            continue
        
        r = re.search("Visa required, except for Those.{1,30}US",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required" )
            insertrow(nat,dest,1,printstr)
            continue
            
        r = re.search("Visa required, except for Holders of.{1,50}Hong Kong",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required" )
            insertrow(nat,dest,1,printstr)
            continue
                
        r = re.search("Visa required, except for.{1,30}(Spouses|Children|Sons|Daughters)",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required (Spouses/Children/Sons/Daughters)" )
            insertrow(nat,dest,1,printstr)
            continue

        r = re.search("(Admission|Addmission).{1,30}refused",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " no entry" )
            insertrow(nat,dest,1,printstr)
            continue 
        
        
        r = re.search("holding a letter.{1,30}sponsoring",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required (sponsor)" )
            insertrow(nat,dest,1,printstr)
            continue  
            
        r = re.search("Visa required, except for Holders of.{1,50}ABTC",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required (Except ABTC)" )
            insertrow(nat,dest,1,printstr)
            continue  
        
        r = re.search("Visa required, except for.{1,100}Dual Nationality",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required" )
            insertrow(nat,dest,1,printstr)
            continue 
        
        r = re.search("Visa required, except for Holders of a signed and stamped letter",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa required" )
            insertrow(nat,dest,1,printstr)
            continue 
        
        r = re.search("visa.{1,100}issued.{1,30}(Canada|USA)", text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " Canada or US visa required" )
            insertrow(nat,dest,1,printstr)
            continue

        r = re.search("visa.{1,100}issued.{1,30}(United Kingdom|UK)", text, re.IGNORECASE)
        if r != None and nat != "GB":
            printstr = ( nat + " to " + dest + " UK visa required" )
            insertrow(nat,dest,1,printstr)
            continue
        
        r = re.search("visa.{1,100}issued.{1,30}Schengen", text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " Schengen visa Required" )
            insertrow(nat,dest,1,printstr)
            continue
        
        r = re.search("visa.{1,100}issued.{1,30}EU Member", text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " EU visa Required" )
            insertrow(nat,dest,1,printstr)
            continue
            
        r = re.search("except for Holders of a Tourist Card", text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa Required" )
            insertrow(nat,dest,1,printstr)
            continue
            
            
        r = re.search("Holders of a valid on arrival NEXUS",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required (NEXUS)" )
            insertrow(nat,dest,0,printstr)
            continue  
        
        r = re.search("Visa required, except for Holders of normal",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required" )
            insertrow(nat,dest,0,printstr)
            continue  
        
        r = re.search("Visa required, except for Holders of Chinese Taipei",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required" )
            insertrow(nat,dest,0,printstr)
            continue  
        
            
        r = re.search("Visa required, except for Holders of biometric passports",text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required" )
            insertrow(nat,dest,0,printstr)
            continue  
        
        r = re.search("visa required.{1,5}except for nationals of.+" + national, text, re.IGNORECASE)
        if r != None:
            printstr = ( nat + " to " + dest + " visa not required (national)" + extra_conditions )
            insertrow(nat,dest,0,printstr)
            continue 

        r = re.search("visa required, except.{1,10}a max.{1,5}stay of.{1,5}[0-9]{1,5}\s{1,5}(hour|day|week|month|year)",text, re.IGNORECASE)
        if r != None:
            visa_req = r.group(0)
            time_unit = r.group(1)
            time = re.search("[0-9]+\s+(?="+time_unit+")",visa_req).group(0)
            printstr = ( nat + " to " + dest + " " + time + " " + time_unit + " " + extra_conditions )
            insertrow(nat,dest,0,printstr)
            continue

        r = re.search("visa required, except.{1,30}a max.{1,5}stay up to.{1,5}\s{1,5}(hour|day|week|month|year)",text, re.IGNORECASE)
        if r != None: 
            visa_req = r.group(0)
            time_unit = r.group(1)
            time = re.search("[0-9]+\s+(?="+time_unit+")",visa_req).group(0)
            printstr = ( nat + " to " + dest + " " + time + " " + time_unit + " " + extra_conditions )
            insertrow(nat,dest,0,printstr)
            continue

        r = re.search("visa required, except.{1,30}stay of max.{1,10}[0-9]{1,5}\s{1,5}(hour|day|week|month|year)",text, re.IGNORECASE)
        if r != None:
            visa_req = r.group(0)
            time_unit = r.group(1)
            time = re.search("[0-9]+\s+(?="+time_unit+")",visa_req).group(0)
            printstr = ( nat + " to " + dest + " " + time + " " + time_unit + extra_conditions )
            insertrow(nat,dest,0,printstr)
            continue
            
        r = re.search("visa required, except.{1,30}stay of max.{1,10}[0-9]{1,5}\s{1,5}(hour|day|week|month|year)",text, re.IGNORECASE)
        if r != None:
            visa_req = r.group(0)
            time_unit = r.group(1)
            time = re.search("[0-9]+\s+(?="+time_unit+")",visa_req).group(0)
            printstr = ( nat + " to " + dest + " " + time + " " + time_unit + extra_conditions )
            insertrow(nat,dest,0,printstr)
            continue
            
        r = re.search("visa required, except.{1,50}permit.{1,50}max.{1,20}[0-9]{1,5}\s{1,5}(hour|day|week|month|year)",text, re.IGNORECASE)
        if r != None:
            visa_req = r.group(0)
            time_unit = r.group(1)
            time = re.search("[0-9]+\s+(?="+time_unit+")",visa_req).group(0)
            printstr = ( nat + " to " + dest + " " + time + " " + time_unit + extra_conditions )
            insertrow(nat,dest,0,printstr)
            continue
            
        r = re.search("visa required, except.{1,50}arrival.{1,50}max.{1,20}[0-9]{1,5}\s{1,5}(hour|day|week|month|year)",text, re.IGNORECASE)
        if r != None:
            visa_req = r.group(0)
            time_unit = r.group(1)
            time = re.search("[0-9]+\s+(?="+time_unit+")",visa_req).group(0)
            printstr = ( nat + " to " + dest + " " + time + " " + time_unit + extra_conditions )
            insertrow(nat,dest,0,printstr)
            continue
            
        if extra_conditions != "":
            printstr = ( nat + " to " + dest + " " + extra_conditions )
            insertrow(nat,dest,0,printstr)
            continue
        
        print( "[Uncaught " + nat + " to " + dest + "]" )
        printstr = ( nat + " to " + dest + " visa Required" )
        insertrow(nat,dest,1,printstr)
        #print( text )
        
conn.commit()
        