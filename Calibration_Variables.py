##AFTER UPDATE AND SAVE YOU MUST RESTART THE KERNEL IN JUPYTER NOTEBOOK TO UPDATE VARIABLES!

##Remember to insert r in front of all paths, e.g. r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\MODEL"

python_installation = r"C:\Python27\ArcGIS10.7\python.exe"


#FSA WWF
model_area = "FSA"
generate_confidence_csvs = False
map_point_spacing = 100
use_accumulation = True
slope_source_unit_meter_per_meter = True #This is the case for NSSA and FSA, in VSA it is per thousand
model_area_strict_match = True #If True, accept 'VSA' but not 'VSA-2019'. If False, accept both.

#Leave as empty list [] if all zones to be plotted 
zone_filter = []
# zone_filter = ['HT4','MH20']

#CHANGE THE BELOW PATHS TO YOUR C DRIVE
output_folder = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\WWF_Calibration_Reports"
result_folder = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Model_WWF_Calibration_Full_Package\FSA_Base_2021pop_V140_Step1_m1d - Result Files"
calibration_sheet = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Model_WWF_Calibration_Full_Package\FSA_Calibration_Specs\Calibration_Specifications.xlsx"
model = r"\\prdsynfile01\lws_modelling\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Model_WWF_Calibration_Full_Package\FSA_Base_2021pop_V140_Step1.sqlite"

#DO NOT CHANGE THE PATHS BELOW
summation_csv = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Model_WWF_Calibration_Full_Package\FSA_Calibration_Specs\Summation.csv"
node_csv = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Model_WWF_Calibration_Full_Package\FSA_Calibration_Specs\MH_Zones.csv"
outfall_csv = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Model_WWF_Calibration_Full_Package\FSA_Calibration_Specs\Outfall_Summary.csv"

rainfall_dfs0_file = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\DATA\RAINFALL\FSA_Rainfall_Data_PDT.dfs0"
map_folder = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\WWF_Calibration_Reports\FSA_Report_Maps"
dfs0_folders = []
dfs0_folders.append(r"J:\SEWER_AREA_MODELS\FSA\02_MODEL_COMPONENTS\04_DATA\11.Dfs0\Non-PS")
dfs0_folders.append(r"J:\SEWER_AREA_MODELS\FSA\02_MODEL_COMPONENTS\04_DATA\11.Dfs0\PS")
dfs0_folders.append(r"J:\SEWER_AREA_MODELS\FSA\02_MODEL_COMPONENTS\04_DATA\11.Dfs0\CSO-SSO")

######################################################################################################################################



























# #FSA DWF
# model_area = "FSA"
# generate_confidence_csvs = True
# map_point_spacing = 100
# use_accumulation = True
# slope_source_unit_meter_per_meter = True #This is the case for NSSA and FSA, in VSA it is per thousand
# model_area_strict_match = True #If True, accept 'VSA' but not 'VSA-2019'. If False, accept both.

# #Leave as empty list [] if all zones to be plotted 
# zone_filter = []
# # zone_filter = ['HT4','MH20','ML2','ML7','NC1','NR4B','NRT20','POC8D','Port_Coquitlam_PS'] #Vaillant

# #CHANGE THE BELOW PATHS TO YOUR C DRIVE
# output_folder = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Calibration_Reports"
# result_folder = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Model_Post_Calibration"
# calibration_sheet = r"\\prdsynfile01\LWS_Modelling\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Calibration_Reports\FSA_Calibration_Specs\Calibration_Specifications.xlsx"
# model = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Model_Post_Calibration\FSA_Base_2021_Calibration_Only.mdb"

# #DO NOT CHANGE THE PATHS BELOW
# summation_csv = r"\\prdsynfile01\LWS_Modelling\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Calibration_Reports\FSA_Calibration_Specs\Summation.csv"
# node_csv = r"\\prdsynfile01\LWS_Modelling\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Calibration_Reports\FSA_Calibration_Specs\MH_Zones.csv"
# outfall_csv = r"\\prdsynfile01\LWS_Modelling\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Calibration_Reports\FSA_Calibration_Specs\Outfall_Summary.csv"

# rainfall_dfs0_file = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\DATA\RAINFALL\FSA_Rainfall_Data_PDT.dfs0"
# map_folder = r"J:\SEWER_AREA_MODELS\FSA\03_SIMULATION_WORK\Calibration_2022\Calibration_Reports\FSA_Report_Maps"
# dfs0_folders = []
# dfs0_folders.append(r"J:\SEWER_AREA_MODELS\FSA\02_MODEL_COMPONENTS\04_DATA\11.Dfs0\Non-PS")
# dfs0_folders.append(r"J:\SEWER_AREA_MODELS\FSA\02_MODEL_COMPONENTS\04_DATA\11.Dfs0\PS")


## ------ Below is for other sewer areas. Leave these commented out

# model_area = "VSA"
# generate_confidence_csvs = True
# map_point_spacing = 100
# use_accumulation = False
# slope_source_unit_meter_per_meter = False #This is the case for NSSA and FSA, in VSA it is per thousand
# model_area_strict_match = True #If True, accept 'VSA' but not 'VSA-2019'. If False, accept both.
# zone_filter = []

# result_specs_csv = r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Version_298\Calibration_Specs\Result_Specifications.csv"

# summation_csv = r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Version_298\Calibration_Specs\Summation.csv"
# node_csv = r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Version_298\Calibration_Specs\MH_Zones.csv"

# outfall_csv = r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Version_298\Calibration_Specs\Outfall_Summary.csv"

# calibration_sheet = r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Version_298\Calibration_Specs\Calibration_Specifications.xlsx"
# rainfall_dfs0_file = r"J:\SEWER_AREA_MODELS\VSA\01_MASTER_MODEL\DATA\RAINFALL\VSA_Rainfall_Data_PDT.dfs0"
# model = r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Version_298\Calibration_Specs\VSA_BASE_MODEL_2015_Backup298.mdb"

# map_folder = r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Report_Maps"
# output_folder = r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Version_298"
# result_folder = r"J:\SEWER_AREA_MODELS\VSA\01_MASTER_MODEL\MODEL\RESULTS\Results_v298\Model"

# dfs0_folders = []
# dfs0_folders.append(r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\04_DATA\15. Dfs0\PS")
# dfs0_folders.append(r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\04_DATA\15. Dfs0\Non_PS")
# dfs0_folders.append(r"J:\SEWER_AREA_MODELS\VSA\02_MODEL_COMPONENTS\04_DATA\15. Dfs0\CSO")

# model_area = "NSSA"
# generate_confidence_csvs = True
# map_point_spacing = 100
# use_accumulation = True
# slope_source_unit_meter_per_meter = True #This is the case for NSSA and FSA, in VSA it is per thousand
# model_area_strict_match = False #If true, accept 'VSA' but not 'VSA-2019' or 'FSA' but not 'FSA North'

# summation_csv = r"J:\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Latest_Backup49-Regenerate_Accumulation\Jupyter_Reports\Summation.csv"
# node_csv = r"J:\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Latest_Backup49-Regenerate_Accumulation\Jupyter_Reports\MH_Zones.csv"


# outfall_csv = r"J:\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Latest_Backup49-Regenerate_Accumulation\Jupyter_Reports\Outfall_Summary.csv"

# calibration_sheet = r"\\prdsynfile01\lws_modelling\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Latest_Backup49-Regenerate_Accumulation\Jupyter_Reports\Calibration_Specifications.xlsx"
# rainfall_dfs0_file = r"J:\SEWER_AREA_MODELS\NSSA\03_SIMULATION_WORK\SYSTEM_ASSESSMENT\DATA\RAINFALL\NSSA_Rainfall_Data_PDT.dfs0"
# model = r'J:\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Latest_Backup49-Regenerate_Accumulation\NSSA_Base.mdb'

# map_folder = r"\\prdsynfile01\lws_modelling\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Latest_Backup49-Regenerate_Accumulation\Report_Maps"
# output_folder = r"\\prdsynfile01\lws_modelling\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\03. CALIB_REPORT\Latest_Backup49-Regenerate_Accumulation\Jupyter_Reports"
# result_folder = r"\\prdsynfile01\lws_modelling\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\07_CALIBRATION\02. WWF_CALIBRATION\06. CALIB_RESULTS\Latest_Backup49"

# dfs0_folders = []
# dfs0_folders.append(r"\\prdsynfile01\lws_modelling\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\06_FLOW MONITORING\10. Dfs0s\Non-PS")
# dfs0_folders.append(r"\\prdsynfile01\lws_modelling\SEWER_AREA_MODELS\NSSA\02_MODEL_COMPONENTS\06_FLOW MONITORING\10. Dfs0s\PS")