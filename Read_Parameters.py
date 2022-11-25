

import pypyodbc #used to run Access queries

import arcpy
from arcpy import env #used to create mdb
import shutil #For copy file
import ctypes
import os # for file operations
import pandas as pd



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
    columns = [column[0] for column in cur.description]
    return [columns,queryOutput]



working_folder = os.getcwd()
use_accumulation = True
mu_path = r'J:\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Latest_Backup49-Regenerate_Accumulation\NSSA_Base.mdb'


def main(working_folder,mu_path,use_accumulation):
##if 1==1:

    print use_accumulation


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
           'Total_WaterLoad', 'Mixed_Population_Upstream',\
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


    wwf_specs = readQuery(sql,mu_path)[1]

    cols = wwf_specs[0]
    wwf_spec = wwf_specs[1]

    wwf_spec = pd.DataFrame(wwf_specs,columns=wwf_columns)
    wwf_spec.to_csv(working_folder + '\\WWF_Specs.csv',index=False)

    ##d = ['Mixed_Rate', 'ResHD_Rate', 'ResLD_Rate', 'Commercial_Rate',
    ##       'Industrial_Rate', 'Institutional_Rate', 'Mixed_Population',
    ##       'ResHD_Population', 'ResLD_Population', 'Commercial_Area',
    ##       'Industrial_Area', 'Institutional_Area', 'Mixed_WaterLoad',
    ##       'ResHD_WaterLoad', 'ResLD_WaterLoad', 'Commercial_WaterLoad',
    ##       'Industrial_WaterLoad', 'Institutional_WaterLoad', 'Baseflow_WaterLoad',
    ##       'Total_WaterLoad', 'Mixed_Population_Upstream',
    ##       'ResHD_Population_Upstream', 'ResLD_Population_Upstream',
    ##       'Commercial_Area_Upstream', 'Industrial_Area_Upstream',
    ##       'Institutional_Area_Upstream', 'Mixed_WaterLoad_Upstream',
    ##       'ResHD_WaterLoad_Upstream', 'ResLD_WaterLoad_Upstream',
    ##       'Commercial_WaterLoad_Upstream', 'Industrial_WaterLoad_Upstream',
    ##       'Institutional_WaterLoad_Upstream', 'Baseflow_WaterLoad_Upstream',
    ##       'Total_WaterLoad_Upstream']

    dwf_frames = []

    sqls = []

    sqls.append(["TRANSFORM Avg(PerCapitaLoad) AS AvgOfPerCapitaLoad SELECT LoadLocation FROM ms_LALoadAlloc WHERE LoadCategory='ResHD' Or LoadCategory='Mixed' Or LoadCategory='ResLD' GROUP BY LoadLocation PIVOT LoadCategory",'Rate'])

    sqls.append(["TRANSFORM Avg(PerAreaLoad) AS AvgOfPerAreaLoad SELECT LoadLocation FROM ms_LALoadAlloc WHERE LoadCategory='Commercial' Or LoadCategory='Industrial' Or LoadCategory='Institutional' GROUP BY LoadLocation PIVOT LoadCategory",'Rate'])

    sqls.append(["TRANSFORM Sum(Population) AS SumPersons SELECT LoadLocation FROM ms_LALoadAlloc WHERE LoadCategory='ResHD' Or LoadCategory='Mixed' Or LoadCategory='ResLD' GROUP BY LoadLocation PIVOT LoadCategory",'Population'])

    sqls.append(["TRANSFORM SUM(ICIArea) AS SumArea SELECT LoadLocation FROM ms_LALoadAlloc WHERE LoadCategory='Commercial' Or LoadCategory='Industrial' Or LoadCategory='Institutional' GROUP BY LoadLocation PIVOT LoadCategory",'Area'])

    sqls.append(["TRANSFORM SUM(WaterLoad) AS SumWaterLoad SELECT LoadLocation FROM ms_LALoadAlloc WHERE LEFT(LoadCategory,4) <> 'Load' GROUP BY LoadLocation PIVOT LoadCategory",'WaterLoad'])

    sqls.append(["SELECT LoadLocation, SUM(WaterLoad) AS Total FROM ms_LALoadAlloc GROUP BY LoadLocation ORDER BY LoadLocation",'WaterLoad'])

    if use_accumulation == True or use_accumulation == 'True': #Bat file seems to parse it in as string/

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

    for dwf_column in dwf_columns:
        dwf_column_lower = dwf_column.lower()
        dwf_df_all.rename(columns={dwf_column_lower:dwf_column},inplace=True)

    dwf_df_all = dwf_df_all[dwf_columns]
    dwf_df_all.to_csv(working_folder + '\\DWF_Specs.csv',index=False)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
