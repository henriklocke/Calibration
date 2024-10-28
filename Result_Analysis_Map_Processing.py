import arcpy
import os
import ctypes
import pypyodbc #used to run Access queries
import datetime
from datetime import timedelta

def executeQuery(sqls, fullPath):
    if ".mdb" in fullPath:
        conn = pypyodbc.win_connect_mdb(fullPath)
    elif ".sqlite" in fullPath:
        conn = sqlite3.connect(fullPath)
    cur = conn.cursor()
    if type(sqls) == list:
        for sql in sqls:
            print sql
            cur.execute(sql)
    else:
        sql = sqls
        print sql
        cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

def readQuery(SQL, fullPath):
    queryOutput = []
    if ".mdb" in fullPath:
        conn = pypyodbc.win_connect_mdb(fullPath)
    elif ".sqlite" in fullPath:
        conn = sqlite3.connect(fullPath)
    cur = conn.cursor()
    print SQL
    cur.execute(SQL)
    while True:
        row = cur.fetchone()
        if not row:
            break
        #queryOutput.append(row[0])
        queryOutput.append(row)
    cur.close()
    conn.commit()
    conn.close()
    return queryOutput


preprocessing = False
maps = True

originalMxd = "FSA_North_Template.mxd"
textSearchText = "FSA North"
newMaps = []
working_folder = os.getcwd()
process_mdb = "Zones.mdb"
model = 'FSA_Base_2021pop_V171.sqlite'

events = ['DWF Calibration','WWF Calibration','WWF Validation']
stats = ['Weighted','Max HGL','Max Flow','Acc Volume']



#mxdo.dataDrivenPages.exportToPDF(working_folder + "\\" + originalMxd[:-4] +  ".pdf", "ALL", "NORMAL")

if preprocessing:

    model_path = working_folder + '\\' + model

    #Delete mdb if it exists and create a new
    full_path = working_folder + '\\' + process_mdb

    os.remove(full_path) if os.path.exists(full_path) else None
    arcpy.CreatePersonalGDB_management(working_folder, process_mdb)

    layers = ['m_Station','msm_Link','msm_Catchment']
    for layer in layers:
        feature_class_path = model_path + "\\" + layer
        arcpy.MakeFeatureLayer_management(feature_class_path, "temp_layer", "altid = 0")
        arcpy.FeatureClassToFeatureClass_conversion("temp_layer", full_path, layer)
        arcpy.Delete_management("temp_layer")

    arcpy.management.RepairGeometry(full_path + '\\msm_Catchment')
    arcpy.Dissolve_management(full_path + "\\msm_Catchment", full_path + "\\Zones_Template", ["Location"])

    sql = 'ALTER TABLE Zones_Template ADD COLUMN Zone_Key TEXT, Event TEXT, Stat TEXT'
    executeQuery(sql, full_path)


    first = True
    for event in events:
        for stat in stats:
            sql = "UPDATE Zones_Template SET Zone_Key = Location & ' " + event + " " +  stat + "', Event = '" + event + "', Stat = '" + stat + "'"
            executeQuery(sql, full_path)

            if first:
                arcpy.FeatureClassToFeatureClass_conversion (full_path + "\\Zones_Template", full_path, 'Zones')
            else:
                arcpy.Append_management([full_path + "\\Zones_Template"], full_path + "\\Zones", "NO_TEST","","")

            first = False

if maps:


    arcpy.env.workspace = working_folder

    mxdo = arcpy.mapping.MapDocument(working_folder + "\\" + originalMxd)

    i = 0
    for event in events:
        for stat in stats:

            filenameNoExt = textSearchText.replace(' ','_') + '_' + event.replace(' ','_')  + '_' + stat.replace(' ','_')
            pdfName = filenameNoExt + '.pdf'
            mxdNewName = filenameNoExt + ".mxd"
##            zoneLayerPrefix = "Zones ("
##            QALayerPrefix = "QA ("

            if mxdNewName <> originalMxd.lower():

                mxdo.saveACopy(working_folder + "\\" + mxdNewName)
                mxd = arcpy.mapping.MapDocument(working_folder + "\\" + mxdNewName)

                for lyr in arcpy.mapping.ListLayers(mxd):
                    if lyr.name in ['Zones','QA']:
                        lyr.definitionQuery = "Zones.Event = '" +  event + "' AND Zones.Stat = '" + stat + "'"

                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):

                    if textSearchText in elm.text:
                        elm.text = textSearchText + "\n" + event + ' Review\n' + stat + ' Zone Statistics'

                mxd.save()

                #arcpy.mapping.ExportToPDF(mxd, working_folder + "\\" + pdfName )
                #mxd.dataDrivenPages.exportToPDF(working_folder + "\\" + pdfName, "ALL", "NORMAL")
                arcpy.mapping.ExportToPDF(mxd,working_folder + "\\" + pdfName)

                i+=1


MessageBox = ctypes.windll.user32.MessageBoxA
MessageBox(None, "Finished", 'Info', 0)

