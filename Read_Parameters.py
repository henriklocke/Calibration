

import pypyodbc #used to run Access queries

import arcpy
from arcpy import env #used to create mdb
import shutil #For copy file
import ctypes
import os # for file operations
import pandas as pd
import sqlite3



def readQuery(SQL, fullPath):
    queryOutput = []
    if ".mdb" in fullPath:
        conn = pypyodbc.win_connect_mdb(fullPath)
    elif ".sqlite" in fullPath:
        conn = sqlite3.connect(fullPath)
        print "connection established with ",fullPath
    else:
        MessageBox(None, "Tool ends." + fullPath + " not recognized as mdb or sqlite", 'Info', 0)
        exit()
    ###################
    cur = conn.cursor()
    print SQL
    cur.execute(SQL)
    while True:
        row = cur.fetchone()
        if not row:
            break
        queryOutput.append(row)
    cur.close()
    conn.commit()
    conn.close()
##    return queryOutput
    columns = [column[0].lower() for column in cur.description]
    return [columns,queryOutput]



working_folder = os.getcwd()
use_accumulation = True
mu_path = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\MODEL\FSA_Base_2021pop_New_Zones.mdb"


def main(working_folder,mu_path,use_accumulation):
##if 1 == 1:

    print 'use_accumulation: ' + str(use_accumulation)

    wwf_columns = ['Location','Imp. cal. factor ICF', 'Imp. san. factor ISF', 'Length factor LF', \
           'Slope factor SF', 'RDII Factor RF', 'Umax (mm)', 'Lmax (mm)', \
           'Overland coeff. Cqof', 'Groundwater coefficient GwCarea', \
           'TC overland flow (h)', 'TC interflow (h)', 'TC baseflow (h)', \
           'Threshold overland flow', 'Threshold interflow', 'Threshold GW flow', \
           'Specific groundwater yield', 'Minimum groundwater depth', \
           'Maximum groundwater depth causing baseflow', \
           'Groundwater depth for unit capilary flux', 'Number sanitary', \
           'Number combined', 'Number stormwater', 'Total number of catchments', \
           'Area sanitary (ha)', 'Area combined (ha)', 'Area stormwater (ha)', \
           'Drainage area (ha)', 'RDII Area (ha)', 'Steep Impervious area (ha)', \
           'Flat Impervious area (ha)', 'Total', 'Average Length (m)', \
           'Average slope (m/m)']

    dwf_columns = ['Zone','Mixed_Rate', 'ResHD_Rate', 'ResLD_Rate', 'Commercial_Rate',\
           'Industrial_Rate', 'Institutional_Rate', 'Mixed_Population',\
           'ResHD_Population', 'ResLD_Population', 'Commercial_Area',\
           'Industrial_Area', 'Institutional_Area', 'Mixed_WaterLoad',\
           'ResHD_WaterLoad', 'ResLD_WaterLoad', 'Commercial_WaterLoad',\
           'Industrial_WaterLoad', 'Institutional_WaterLoad', 'Baseflow_WaterLoad',\
           'Total_WaterLoad']
    if use_accumulation == True or use_accumulation == 'True': #Bat file seems to parse it in as string
        print 'Yes we append acc!'
        dwf_columns += ['Mixed_Population_Upstream',\
           'ResHD_Population_Upstream', 'ResLD_Population_Upstream',\
           'Commercial_Area_Upstream', 'Industrial_Area_Upstream',\
           'Institutional_Area_Upstream', 'Mixed_WaterLoad_Upstream',\
           'ResHD_WaterLoad_Upstream', 'ResLD_WaterLoad_Upstream',\
           'Commercial_WaterLoad_Upstream', 'Industrial_WaterLoad_Upstream',\
           'Institutional_WaterLoad_Upstream', 'Baseflow_WaterLoad_Upstream',\
           'Total_WaterLoad_Upstream']

    dwf_types = ['Mixed','ResHD','ResLD','Commercial','Industrial','Institutional','Baseflow','Total']

    for wwf_column in wwf_columns:
        print wwf_column

    if '.mdb' in mu_path:
        sql = "SELECT ms_Catchment.Location, "
        sql  += "Avg(Base_Hydrology_Settings.ICF) AS AvgOfImp_F, "
        sql  += "Avg(Base_Hydrology_Settings.ISF) AS AvgOfImp_San_F, "
        sql  += "Avg(Base_Hydrology_Settings.LF) AS AvgOfLength_F, "
        sql  += "Avg(Base_Hydrology_Settings.SF) AS AvgOfSlope_F, "
        sql  += "Avg(Base_Hydrology_Settings.RF) AS AvgOfSRdii_F, "
        sql  += "Avg(msm_HParRDII.Umax) AS AvgOfUmax, "
        sql  += "Avg(msm_HParRDII.Lmax) AS AvgOfLmax, "
        sql  += "Avg(msm_HParRDII.Cqof) AS AvgOfCqof, "
        sql  += "Avg(msm_HParRDII.GwCarea) AS AvgOfGwCarea, "
        sql  += "Avg(msm_HParRDII.Ck) AS AvgOfCk, "
        sql  += "Avg(msm_HParRDII.Ckif) AS AvgOfCkif, "
        sql  += "Avg(msm_HParRDII.Ckbf) AS AvgOfCkbf, "
        sql  += "Avg(msm_HParRDII.Tof) AS AvgOfTof, "
        sql  += "Avg(msm_HParRDII.Tif) AS AvgOfTif, "
        sql  += "Avg(msm_HParRDII.Tg) AS AvgOfTg, "
        sql  += "Avg(msm_HParRDII.GwSy) AS AvgOfGwSy, "
        sql  += "Avg(msm_HParRDII.GwLmin) AS AvgOfGwLmin, "
        sql  += "Avg(msm_HParRDII.GWLbf0) AS AvgOfGWLbf0, "
        sql  += "Avg(msm_HParRDII.GWLfl1) AS AvgOfGWLfl1, "
        sql  += "Sum(IIf(ms_Catchment.NetTypeNo=1,1,0)) AS CountSan, "
        sql  += "Sum(IIf(ms_Catchment.NetTypeNo>2,1,0)) AS CountComb, "
        sql  += "Sum(IIf(ms_Catchment.NetTypeNo=2,1,0)) AS CountStorm, "
        sql  += "Count(ms_Catchment.MUID) AS CountAll, "
        sql  += "Sum(IIf(ms_Catchment.NetTypeNo=1, "
        sql  += "ms_Catchment.Area,0)) AS AreaSan, "
        sql  += "Sum(IIf(ms_Catchment.NetTypeNo>2, "
        sql  += "ms_Catchment.Area,0)) AS AreaComb, "
        sql  += "Sum(IIf(ms_Catchment.NetTypeNo=2,ms_Catchment.Area,0)) AS AreaStorm, "
        sql  += "Sum(ms_Catchment.Area) AS AreaAll, "
        sql  += "Sum(msm_HModCRC.RdiiArea*ms_Catchment.Area/100) AS AreaRDII, "
        sql  += "Sum(msm_HModB.AISteep*ms_Catchment.Area/100) AS AreaSteep, "
        sql  += "Sum(msm_HModB.AIFlat*ms_Catchment.Area/100) AS AreaFlat, "
        sql  += "Sum(msm_HModCRC.RdiiArea*ms_Catchment.Area/100 "
        sql  += "+msm_HModB.AISteep*ms_Catchment.Area/100 "
        sql  += "+msm_HModB.AIFlat*ms_Catchment.Area/100) AS AreaHydrology, "
        sql  += "Avg(msm_HModB.Length) AS AvgOfLength, "
        sql  += "Avg(msm_HModB.Slope) AS AvgOfSlope "
        sql  += "FROM (((ms_Catchment INNER JOIN msm_HParRDII ON ms_Catchment.Location = msm_HParRDII.MUID) "
        sql  += "INNER JOIN msm_HModCRC ON ms_Catchment.MUID = msm_HModCRC.CatchID) "
        sql  += "INNER JOIN msm_HModB ON ms_Catchment.MUID = msm_HModB.CatchID) "
        sql  += "INNER JOIN Base_Hydrology_Settings ON "
        sql  += "msm_HParRDII.MUID = Base_Hydrology_Settings.Location "
        sql  += "GROUP BY ms_Catchment.Location "
    else:
        sql = "SELECT msm_Catchment.Location, "
        sql += "Avg(Base_Hydrology_Settings.ICF) AS AvgOfImp_F, Avg(Base_Hydrology_Settings.ISF) AS AvgOfImp_San_F, Avg(Base_Hydrology_Settings.LF) AS AvgOfLength_F, "
        sql += "Avg(Base_Hydrology_Settings.SF) AS AvgOfSlope_F, Avg(Base_Hydrology_Settings.RF) AS AvgOfSRdii_F, "
        sql += "Avg(msm_HParRDII.Umax) AS AvgOfUmax, Avg(msm_HParRDII.Lmax) AS AvgOfLmax, "
        sql += "Avg(msm_HParRDII.Cqof) AS AvgOfCqof, Avg(msm_HParRDII.GwCarea) AS AvgOfGwCarea, Avg(msm_HParRDII.Ck) AS AvgOfCk, Avg(msm_HParRDII.Ckif) AS AvgOfCkif, "
        sql += "Avg(msm_HParRDII.Ckbf) AS AvgOfCkbf, "
        sql += "Avg(msm_HParRDII.Tof) AS AvgOfTof, Avg(msm_HParRDII.Tif) AS AvgOfTif, Avg(msm_HParRDII.Tg) AS AvgOfTg, Avg(msm_HParRDII.GwSy) AS AvgOfGwSy, "
        sql += "Avg(msm_HParRDII.GwLmin) AS AvgOfGwLmin, "
        sql += "Avg(msm_HParRDII.GWLbf0) AS AvgOfGWLbf0, Avg(msm_HParRDII.GWLfl1) AS AvgOfGWLfl1, "
        sql += "Sum(CASE WHEN msm_Catchment.NetTypeNo=1 THEN 1 ELSE 0 END) AS CountSan, Sum(CASE WHEN msm_Catchment.NetTypeNo>2 THEN 1 ELSE 0 END) AS CountComb, "
        sql += "Sum(CASE WHEN msm_Catchment.NetTypeNo=2 THEN 1 ELSE 0 END) AS CountStorm, Count(msm_Catchment.MUID) AS CountAll, Sum(CASE WHEN msm_Catchment.NetTypeNo=1 THEN msm_Catchment.Area ELSE 0 END) AS AreaSan, "
        sql += "Sum(CASE WHEN msm_Catchment.NetTypeNo>2 THEN msm_Catchment.Area ELSE 0 END) AS AreaComb, Sum(CASE WHEN msm_Catchment.NetTypeNo=2 THEN msm_Catchment.Area ELSE 0 END) AS AreaStorm, "
        sql += "Sum(msm_Catchment.Area) AS AreaAll, Sum(msm_Catchment.RdiiArea*msm_Catchment.Area/100) AS AreaRDII, Sum(msm_Catchment.modelbaisteep*msm_Catchment.Area/100) AS AreaSteep, "
        sql += "Sum(msm_Catchment.modelbaiflat*msm_Catchment.Area/100) AS AreaFlat, "
        sql += "Sum(msm_Catchment.RdiiArea*msm_Catchment.Area/100 +msm_Catchment.modelbaisteep*msm_Catchment.Area/100 +msm_Catchment.modelbaiflat*msm_Catchment.Area/100) AS AreaHydrology, "
        sql += "Avg(msm_Catchment.modelblength) AS AvgOfLength, Avg(msm_Catchment.modelbslope) AS AvgOfSlope "
        sql += "FROM (msm_Catchment INNER JOIN msm_HParRDII ON msm_Catchment.Location = msm_HParRDII.MUID) INNER JOIN Base_Hydrology_Settings ON msm_HParRDII.MUID = Base_Hydrology_Settings.Location "
        sql += "GROUP BY msm_Catchment.Location"

    wwf_specs = readQuery(sql,mu_path)[1]

    cols = wwf_specs[0]
    wwf_spec = wwf_specs[1]

    wwf_spec = pd.DataFrame(wwf_specs,columns=wwf_columns)
    wwf_spec.to_csv(working_folder + '\\WWF_Specs.csv',index=False)


    dwf_frames = []

    sqls = []
    if '.mdb' in mu_path:
        sqls.append(["TRANSFORM Avg(PerCapitaLoad) AS AvgOfPerCapitaLoad SELECT LoadLocation FROM ms_LALoadAlloc WHERE LoadCategory='ResHD' Or LoadCategory='Mixed' Or LoadCategory='ResLD' GROUP BY LoadLocation PIVOT LoadCategory",'Rate'])
        sqls.append(["TRANSFORM Avg(PerAreaLoad) AS AvgOfPerAreaLoad SELECT LoadLocation FROM ms_LALoadAlloc WHERE LoadCategory='Commercial' Or LoadCategory='Industrial' Or LoadCategory='Institutional' GROUP BY LoadLocation PIVOT LoadCategory",'Rate'])
        sqls.append(["TRANSFORM Sum(Population) AS SumPersons SELECT LoadLocation FROM ms_LALoadAlloc WHERE LoadCategory='ResHD' Or LoadCategory='Mixed' Or LoadCategory='ResLD' GROUP BY LoadLocation PIVOT LoadCategory",'Population'])
        sqls.append(["TRANSFORM SUM(ICIArea) AS SumArea SELECT LoadLocation FROM ms_LALoadAlloc WHERE LoadCategory='Commercial' Or LoadCategory='Industrial' Or LoadCategory='Institutional' GROUP BY LoadLocation PIVOT LoadCategory",'Area'])
        sqls.append(["TRANSFORM SUM(WaterLoad) AS SumWaterLoad SELECT LoadLocation FROM ms_LALoadAlloc WHERE LEFT(LoadCategory,4) <> 'Load' GROUP BY LoadLocation PIVOT LoadCategory",'WaterLoad'])
        sqls.append(["SELECT LoadLocation, SUM(WaterLoad) AS Total FROM ms_LALoadAlloc GROUP BY LoadLocation ORDER BY LoadLocation",'WaterLoad'])
    else:
        sql = "SELECT LoadLocation, "
        sql += "Avg(CASE WHEN loadcategory = 'Baseflow' THEN PerCapitaLoad END) AS Baseflow, "
        sql += "Avg(CASE WHEN loadcategory = 'Commercial' THEN PerCapitaLoad END) AS Commercial, "
        sql += "Avg(CASE WHEN loadcategory = 'Industrial' THEN PerCapitaLoad END) AS Industrial, "
        sql += "Avg(CASE WHEN loadcategory = 'Institutional' THEN PerCapitaLoad END) AS Institutional, "
        sql += "Avg(CASE WHEN loadcategory = 'Load_10' THEN PerCapitaLoad END) AS Load_10, "
        sql += "Avg(CASE WHEN loadcategory = 'Load_8' THEN PerCapitaLoad END) AS Load_8, "
        sql += "Avg(CASE WHEN loadcategory = 'Load_9' THEN PerCapitaLoad END) AS Load_9, "
        sql += "Avg(CASE WHEN loadcategory = 'Mixed' THEN PerCapitaLoad END) AS Mixed, "
        sql += "Avg(CASE WHEN loadcategory = 'ResHD' THEN PerCapitaLoad END) AS ResHD, "
        sql += "Avg(CASE WHEN loadcategory = 'ResLD' THEN PerCapitaLoad END) AS ResLD "
        sql += "FROM msm_LoadPoint GROUP BY LoadLocation"
        sqls.append([sql,'Rate'])

        sql = "SELECT LoadLocation, "
        sql += "Avg(CASE WHEN loadcategory = 'Baseflow' THEN PerAreaLoad END) AS Baseflow, "
        sql += "Avg(CASE WHEN loadcategory = 'Commercial' THEN PerAreaLoad END) AS Commercial, "
        sql += "Avg(CASE WHEN loadcategory = 'Industrial' THEN PerAreaLoad END) AS Industrial, "
        sql += "Avg(CASE WHEN loadcategory = 'Institutional' THEN PerAreaLoad END) AS Institutional, "
        sql += "Avg(CASE WHEN loadcategory = 'Load_10' THEN PerAreaLoad END) AS Load_10, "
        sql += "Avg(CASE WHEN loadcategory = 'Load_8' THEN PerAreaLoad END) AS Load_8, "
        sql += "Avg(CASE WHEN loadcategory = 'Load_9' THEN PerAreaLoad END) AS Load_9, "
        sql += "Avg(CASE WHEN loadcategory = 'Mixed' THEN PerAreaLoad END) AS Mixed, "
        sql += "Avg(CASE WHEN loadcategory = 'ResHD' THEN PerAreaLoad END) AS ResHD, "
        sql += "Avg(CASE WHEN loadcategory = 'ResLD' THEN PerAreaLoad END) AS ResLD "
        sql += "FROM msm_LoadPoint GROUP BY LoadLocation"
        sqls.append([sql,'LoadCategory'])

        sql = "SELECT LoadLocation, "
        sql += "SUM(CASE WHEN loadcategory = 'Baseflow' THEN Population END) AS Baseflow, "
        sql += "SUM(CASE WHEN loadcategory = 'Commercial' THEN Population END) AS Commercial, "
        sql += "SUM(CASE WHEN loadcategory = 'Industrial' THEN Population END) AS Industrial, "
        sql += "SUM(CASE WHEN loadcategory = 'Institutional' THEN Population END) AS Institutional, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_10' THEN Population END) AS Load_10, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_8' THEN Population END) AS Load_8, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_9' THEN Population END) AS Load_9, "
        sql += "SUM(CASE WHEN loadcategory = 'Mixed' THEN Population END) AS Mixed, "
        sql += "SUM(CASE WHEN loadcategory = 'ResHD' THEN Population END) AS ResHD, "
        sql += "SUM(CASE WHEN loadcategory = 'ResLD' THEN Population END) AS ResLD "
        sql += "FROM msm_LoadPoint GROUP BY LoadLocation"
        sqls.append([sql,'Population'])

        sql = "SELECT LoadLocation, "
        sql += "SUM(CASE WHEN loadcategory = 'Baseflow' THEN ICIArea END) AS Baseflow, "
        sql += "SUM(CASE WHEN loadcategory = 'Commercial' THEN ICIArea END) AS Commercial, "
        sql += "SUM(CASE WHEN loadcategory = 'Industrial' THEN ICIArea END) AS Industrial, "
        sql += "SUM(CASE WHEN loadcategory = 'Institutional' THEN ICIArea END) AS Institutional, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_10' THEN ICIArea END) AS Load_10, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_8' THEN ICIArea END) AS Load_8, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_9' THEN ICIArea END) AS Load_9, "
        sql += "SUM(CASE WHEN loadcategory = 'Mixed' THEN ICIArea END) AS Mixed, "
        sql += "SUM(CASE WHEN loadcategory = 'ResHD' THEN ICIArea END) AS ResHD, "
        sql += "SUM(CASE WHEN loadcategory = 'ResLD' THEN ICIArea END) AS ResLD "
        sql += "FROM msm_LoadPoint GROUP BY LoadLocation"
        sqls.append([sql,'Area'])

        sql = "SELECT LoadLocation, "
        sql += "SUM(CASE WHEN loadcategory = 'Baseflow' THEN loadflow END)*100000 AS Baseflow, "
        sql += "SUM(CASE WHEN loadcategory = 'Commercial' THEN loadflow END)*100000 AS Commercial, "
        sql += "SUM(CASE WHEN loadcategory = 'Industrial' THEN loadflow END)*100000 AS Industrial, "
        sql += "SUM(CASE WHEN loadcategory = 'Institutional' THEN loadflow END)*100000 AS Institutional, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_10' THEN loadflow END)*100000 AS Load_10, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_8' THEN loadflow END)*100000 AS Load_8, "
        sql += "SUM(CASE WHEN loadcategory = 'Load_9' THEN loadflow END)*100000 AS Load_9, "
        sql += "SUM(CASE WHEN loadcategory = 'Mixed' THEN loadflow END)*100000 AS Mixed, "
        sql += "SUM(CASE WHEN loadcategory = 'ResHD' THEN loadflow END)*100000 AS ResHD, "
        sql += "SUM(CASE WHEN loadcategory = 'ResLD' THEN loadflow END)*100000 AS ResLD "
        sql += "FROM msm_LoadPoint GROUP BY LoadLocation"
        sqls.append([sql,'WaterLoad'])

        sql = "SELECT LoadLocation, SUM (loadflow)*100000 AS Total FROM msm_LoadPoint GROUP BY LoadLocation"
        sqls.append([sql,'WaterLoad'])

    if use_accumulation == True or use_accumulation == 'True': #Bat file seems to parse it in as string

        if '.mdb' in mu_path:
            sql = "TRANSFORM Sum(ms_LALoadAlloc.Population) AS SumOfPopulation "
            sql += "SELECT Accumulation.Downstream "
            sql += "FROM Accumulation INNER JOIN ms_LALoadAlloc ON Accumulation.Upstream = ms_LALoadAlloc.LoadLocation "
            sql += "WHERE LoadCategory='ResHD' Or LoadCategory='Mixed' Or LoadCategory='ResLD' "
            sql += "GROUP BY Accumulation.Downstream "
            sql += "PIVOT ms_LALoadAlloc.LoadCategory"
            sqls.append([sql,'Population_Upstream'])

            sql = "TRANSFORM Sum(ms_LALoadAlloc.ICIArea) AS SumOfArea "
            sql += "SELECT Accumulation.Downstream "
            sql += "FROM Accumulation INNER JOIN ms_LALoadAlloc ON Accumulation.Upstream = ms_LALoadAlloc.LoadLocation "
            sql += "WHERE LoadCategory='Commercial' Or LoadCategory='Industrial' Or LoadCategory='Institutional' "
            sql += "GROUP BY Accumulation.Downstream "
            sql += "PIVOT ms_LALoadAlloc.LoadCategory"
            sqls.append([sql,'Area_Upstream'])

            sql = "TRANSFORM Sum(ms_LALoadAlloc.WaterLoad) AS SumOfWaterLoad "
            sql += "SELECT Accumulation.Downstream "
            sql += "FROM Accumulation INNER JOIN ms_LALoadAlloc ON Accumulation.Upstream = ms_LALoadAlloc.LoadLocation "
            sql += "WHERE LEFT(LoadCategory,4) <> 'Load' "
            sql += "GROUP BY Accumulation.Downstream "
            sql += "PIVOT ms_LALoadAlloc.LoadCategory"
            sqls.append([sql,'WaterLoad_Upstream'])

            sql = "SELECT Accumulation.Downstream, Sum(ms_LALoadAlloc.WaterLoad) AS Total "
            sql += "FROM ms_LALoadAlloc INNER JOIN Accumulation ON ms_LALoadAlloc.LoadLocation = Accumulation.Upstream "
            sql += "GROUP BY Accumulation.Downstream "
            sql += "ORDER BY Accumulation.Downstream"
            sqls.append([sql,'WaterLoad_Upstream'])
        else:
            sql = "SELECT Downstream, "
            sql += " SUM(CASE WHEN loadcategory = 'Baseflow' THEN Population END) AS Baseflow, "
            sql += " SUM(CASE WHEN loadcategory = 'Commercial' THEN Population END) AS Commercial, "
            sql += " SUM(CASE WHEN loadcategory = 'Industrial' THEN Population END) AS Industrial, "
            sql += " SUM(CASE WHEN loadcategory = 'Institutional' THEN Population END) AS Institutional, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_10' THEN Population END) AS Load_10, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_8' THEN Population END) AS Load_8, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_9' THEN Population END) AS Load_9, "
            sql += " SUM(CASE WHEN loadcategory = 'Mixed' THEN Population END) AS Mixed, "
            sql += " SUM(CASE WHEN loadcategory = 'ResHD' THEN Population END) AS ResHD, "
            sql += " SUM(CASE WHEN loadcategory = 'ResLD' THEN Population END) AS ResLD "
            sql += " FROM Accumulation INNER JOIN msm_LoadPoint ON Accumulation.Upstream = msm_LoadPoint.LoadLocation "
            sql += " GROUP BY Accumulation.Downstream"
            sqls.append([sql,'Population_Upstream'])

            sql = "SELECT Downstream, "
            sql += " SUM(CASE WHEN loadcategory = 'Baseflow' THEN ICIArea END) AS Baseflow, "
            sql += " SUM(CASE WHEN loadcategory = 'Commercial' THEN ICIArea END) AS Commercial, "
            sql += " SUM(CASE WHEN loadcategory = 'Industrial' THEN ICIArea END) AS Industrial, "
            sql += " SUM(CASE WHEN loadcategory = 'Institutional' THEN ICIArea END) AS Institutional, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_10' THEN ICIArea END) AS Load_10, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_8' THEN ICIArea END) AS Load_8, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_9' THEN ICIArea END) AS Load_9, "
            sql += " SUM(CASE WHEN loadcategory = 'Mixed' THEN ICIArea END) AS Mixed, "
            sql += " SUM(CASE WHEN loadcategory = 'ResHD' THEN ICIArea END) AS ResHD, "
            sql += " SUM(CASE WHEN loadcategory = 'ResLD' THEN ICIArea END) AS ResLD "
            sql += " FROM Accumulation INNER JOIN msm_LoadPoint ON Accumulation.Upstream = msm_LoadPoint.LoadLocation "
            sql += " GROUP BY Accumulation.Downstream"
            sqls.append([sql,'Area_Upstream'])

            sql = "SELECT Downstream, "
            sql += " SUM(CASE WHEN loadcategory = 'Baseflow' THEN loadflow END)*100000 AS Baseflow, "
            sql += " SUM(CASE WHEN loadcategory = 'Commercial' THEN loadflow END)*100000 AS Commercial, "
            sql += " SUM(CASE WHEN loadcategory = 'Industrial' THEN loadflow END)*100000 AS Industrial, "
            sql += " SUM(CASE WHEN loadcategory = 'Institutional' THEN loadflow END)*100000 AS Institutional, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_10' THEN loadflow END)*100000 AS Load_10, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_8' THEN loadflow END)*100000 AS Load_8, "
            sql += " SUM(CASE WHEN loadcategory = 'Load_9' THEN loadflow END)*100000 AS Load_9, "
            sql += " SUM(CASE WHEN loadcategory = 'Mixed' THEN loadflow END)*100000 AS Mixed, "
            sql += " SUM(CASE WHEN loadcategory = 'ResHD' THEN loadflow END)*100000 AS ResHD, "
            sql += " SUM(CASE WHEN loadcategory = 'ResLD' THEN loadflow END)*100000 AS ResLD "
            sql += " FROM Accumulation INNER JOIN msm_LoadPoint ON Accumulation.Upstream = msm_LoadPoint.LoadLocation "
            sql += " GROUP BY Accumulation.Downstream"
            sqls.append([sql,'WaterLoad_Upstream'])

            sql = "SELECT Downstream, SUM(loadflow)*100000 AS Total "
            sql += " FROM msm_LoadPoint INNER JOIN Accumulation ON msm_LoadPoint.LoadLocation = Accumulation.Upstream"
            sql += " GROUP BY Accumulation.Downstream"
            sqls.append([sql,'WaterLoad_Upstream'])

    else:
        print 'Not True'

    for i, sql in enumerate(sqls):

        suffix = sql[1]

        dwf_specs = readQuery(sql[0],mu_path)

        columns = dwf_specs[0]

        columns = ['Zone'] + [column + '_' + suffix.lower() for column in columns[1:]]

        dwf_output = dwf_specs[1]

        dwf_df = pd.DataFrame(dwf_output,columns=columns)

        if i == 0:
            dwf_df_all = dwf_df.copy()
        else:
            dwf_df_all = pd.merge(dwf_df_all,dwf_df,how='left',on='Zone')


    a = list(dwf_df_all.columns)


    for dwf_column in dwf_columns:
        dwf_column_lower = dwf_column.lower()
        dwf_df_all.rename(columns={dwf_column_lower:dwf_column},inplace=True)
        print dwf_column

    a = list(dwf_df_all.columns)





    dwf_df_all = dwf_df_all[dwf_columns]
    dwf_df_all.to_csv(working_folder + '\\DWF_Specs.csv',index=False)

if __name__ == "__main__":
    print sys.argv[3]
    main(sys.argv[1],sys.argv[2],sys.argv[3])


