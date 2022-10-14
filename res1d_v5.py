#!/usr/bin/env python
# coding: utf-8

import clr
import sys
import os.path
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.append(r"C:\Program Files (x86)\DHI\2020\bin\x64")

clr.AddReference("DHI.Mike1D.ResultDataAccess")
from DHI.Mike1D.ResultDataAccess import ResultData

clr.AddReference("DHI.Mike1D.Generic")
from DHI.Mike1D.Generic import Connection

clr.AddReference("System")

def dataframeIntegral(df, columns = None, rounding = 8):
    # this function integrate columns using index as time
    # this function assumes the columns are in unit of quantity per second
    if df.shape[0] == 0:
        return [0] * df.shape[1]
    if df.shape[1] == 0:
        return []
    if columns is not None:
        columns = [col for col in df.columns]
        if len(columns) > 0:
            df = df[columns]
    if type(df.index) == pd.core.indexes.datetimes.DatetimeIndex:
        df = dataframeIntegralByTimedelta(df)
        sums = df.sum(0)
    else:
        sums = df.sum(0)
    return [i for i in sums.round(rounding)]

def dataframeIntegralByTimedelta(df, timedelta = '1D'):
    # this function integrate columns using index as time
    # this function assumes the columns are in unit of quantity per second
    if type(df.index) == pd.core.indexes.datetimes.DatetimeIndex:
        original_index = df.index
        df_index = df.reset_index(level=0)
        df_index = df_index - df_index.shift(1)
        df_index = df_index.iloc[:, 0].apply(lambda x: x.total_seconds())
        df = (df + df.shift(1))/2
        df = df.reset_index(drop=True)
        for icol in range(df.shape[1]):
            df.iloc[:, icol] = df.iloc[:, icol].multiply(df_index, fill_value=0)
        
        df.index = original_index

        df = df.resample(timedelta, closed = 'right').sum() #include 24:00 not 0:00
        return df
    else:
        return None

def drawGraph(dfList, yaxisTitle = '', xaxisRange = [], width = None, height = None):
    fig = go.Figure()
    
    for df in dfList:
        for column in df:
            # Add traces for results
            fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))
    if width is not None:
        fig.update_layout(width=width)
    if height is not None:
        fig.update_layout(height=height)
    if len(xaxisRange) > 0:
        fig.update_xaxes(range = xaxisRange)
    if len(yaxisTitle) > 0:
        fig.update_layout(yaxis_title = yaxisTitle)        
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    fig.show()

def drawSubGraphs(dfLists, title = '', width = None, height = None, ylim = True):
    subplots = len(dfLists)
    maxs = []
    mins = []
    
    fig = make_subplots(rows = 1, cols = subplots, horizontal_spacing = 0.03)
    
    for icol, dfList in enumerate(dfLists):
        icolor = 0
        for df in dfList:
            maxs.extend(list(df.max(axis = 0)))
            mins.extend(list(df.min(axis = 0)))
            for column in df:
                # Add traces for results
                fig.add_trace(go.Scatter(x = df.index, y = df[column], mode = 'lines', name = column, 
                                         line=dict(color=['red', 'blue', 'green','orange', 'brown', 'purple', 'yellow', 'cyan', 'magenta', 'grey'][icolor])), 
                              row = 1, col = icol + 1)
                icolor = (icolor + 1)
    if width is not None:
        fig.update_layout(width=width)
    if height is not None:
        fig.update_layout(height=height)        
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig.update_layout(showlegend=False,  title=title,)
    if isinstance(ylim, tuple) or isinstance(ylim, list):
        if len(ylim) == 2:
            fig.update_yaxes(range=list(ylim))
        else:
            pass
    elif ylim:
        if(len(maxs) > 0 and len(mins) > 0):
            maxofmaxs = np.nanmax(maxs)
            minofmins = np.nanmin(mins)
            if maxofmaxs == minofmins:
                if maxofmaxs == 0:
                    fig.update_yaxes(range=[-1, 1])
                else:
                    fig.update_yaxes(range=[maxofmaxs - 0.5 * abs(maxofmaxs), maxofmaxs + 0.5 * abs(maxofmaxs)])
            else:
                fig.update_yaxes(range=[minofmins - 0.1 * (maxofmaxs - minofmins), maxofmaxs + 0.1 * (maxofmaxs - minofmins)])
    else:
        pass
    fig.show()

def drawTable(headerValues, cellValues, height = None):
    aligns=['right']+['center']*(len(cellValues) - 1)
    fig = go.Figure(data=[go.Table(
        header=dict(values=headerValues, align = 'center'), 
        cells=dict(values=cellValues, align = aligns)
    )])
    if height is not None:
        fig.update_layout(height=height)
    fig.show()

def listCleanUp(inList, removeNone = True, unpackTuple = True, unpackList = True, unpackSet = True, unpackDictionary = True, removeDuplicates = True):
    if inList is None:
        return []
    else:
        outList = []
        for item in inList:
            if (removeNone) and (item is None):
                continue
            if (unpackTuple) and isinstance(item, tuple):
                tempList = listCleanUp(list(item), removeNone, unpackTuple, unpackList, unpackSet, unpackDictionary, removeDuplicates)
                outList.extend(tempList)
            elif (unpackList) and isinstance(item, list):
                tempList = listCleanUp(list(item), removeNone, unpackTuple, unpackList, unpackSet, unpackDictionary, removeDuplicates)
                outList.extend(tempList)
            elif (unpackSet) and isinstance(item, set):
                tempList = listCleanUp(list(item), removeNone, unpackTuple, unpackList, unpackSet, unpackDictionary, removeDuplicates)
                outList.extend(tempList)
            elif (unpackDictionary) and isinstance(item, dict):
                tempList = listCleanUp(list(item.values()), removeNone, unpackTuple, unpackList, unpackSet, unpackDictionary, removeDuplicates)
                outList.extend(tempList)
            else:
                outList.append(item)
        if removeDuplicates:
            outList = list(set(outList))
        return outList

class Res1D_v5:
    _runoffTypeDict = {'RDI':' - RDI', 'ModB':' - Kinematic wave (B)', 'Total':''}
    _catchmentDataTypes = ['TotalRunOff', 'OverlandFlow', 'InterFlow','BaseFlow']
    
    def res1dTimeToPDTimeStamp(self, t):
        return pd.Timestamp(year=t.get_Year(), month=t.get_Month(), day=t.get_Day(), hour=t.get_Hour(), minute=t.get_Minute(), second=t.get_Second())
    
    def get_time(self, fromTimeStamp = None, toTimeStamp = None):
        timeStamps = [self.res1dTimeToPDTimeStamp(t) for t in list(self.resultData.TimesList)]
        if len(timeStamps) > 0:
            fromTimeStamp = timeStamps[0] if fromTimeStamp is None else fromTimeStamp
            toTimeStamp = timeStamps[-1] if toTimeStamp is None else toTimeStamp
        indicesTimeStamp = [i for i, t in enumerate(timeStamps) if t >= fromTimeStamp and t <= toTimeStamp]
        return indicesTimeStamp, pd.DatetimeIndex([timeStamps[i] for i in indicesTimeStamp])

    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileExistsError(f"File does not exist {file_path}")
        resultData = ResultData()
        resultData.Connection = Connection.Create(file_path)
        resultData.Load()
        self.resultData = resultData
        self.fromTimeStamp = self.res1dTimeToPDTimeStamp(resultData.StartTime)
        self.toTimeStamp = self.res1dTimeToPDTimeStamp(resultData.EndTime)
        self.indicesTimeStamp, self.dfTimeStamp = self.get_time()
        self.catchmentIDs, self.nodeIDs, self.reachIDs, self.weirIDs, self.pumpIDs, self.orificeIDs, self.valveIDs = self.get_elementIDs()
        self.catchmentCount = len(self.catchmentIDs)
        self.nodeCount = len(self.nodeIDs)
        self.reachCount = len(self.reachIDs)
        self.weirCount = len(self.weirIDs)
        self.pumpCount = len(self.pumpIDs)
        self.orificeCount = len(self.orificeIDs)
        self.valveCount = len(self.valveIDs)

    def setTimeRange(self, fromTimeStamp, toTimeStamp):
        self.indicesTimeStamp, self.dfTimeStamp = self.get_time(fromTimeStamp, toTimeStamp)
        self.fromTimeStamp = self.dfTimeStamp[0]
        self.toTimeStamp = self.dfTimeStamp[-1]

    def catchment2DF(self, catchmentExtIds, catchmentExtTypes = ['RDI', 'ModB', 'Total']):
        catchmentExtIds = listCleanUp(catchmentExtIds)
        dfCatchment = {}
        catchIds = []
        catchments = self.resultData.Catchments
        for extId in catchmentExtIds:
            for extType in catchmentExtTypes:
                if extType in self._runoffTypeDict:
                    catchIds.append(extId + self._runoffTypeDict[extType])
        for i, catchment in enumerate(catchments):
            if catchment.Id in catchIds:
                for di in catchment.DataItems:
                    if di.Quantity.Id in self._catchmentDataTypes:
                        values = list(di.CreateTimeSeriesData(0))
                        values = [values[tsi] for tsi in self.indicesTimeStamp]
                        name = catchment.Id + ' - ' + di.Quantity.Id
                        d = pd.Series(values, name = name)
                        dfCatchment[name] = d
        dfCatchment = pd.DataFrame(dfCatchment)
        dfCatchment.index = self.dfTimeStamp
        return dfCatchment

    def node2DF(self, nodeExtIds, quantityIds = ['WaterLevel', 'WaterVolume', 'WaterSpillDischarge']):
        nodeExtIds = listCleanUp(nodeExtIds)
        dfNode = {}
        for quantityId in quantityIds:
            dfNode[quantityId] = {}
        nodes = self.resultData.Nodes
        for i, node in enumerate(nodes):
            if node.Id in nodeExtIds:
                for di in node.DataItems:
                    quantityId = di.Quantity.Id
                    if quantityId in quantityIds:
                        values = list(di.CreateTimeSeriesData(0))
                        values = [values[tsi] for tsi in self.indicesTimeStamp]
                        name = node.Id
                        d = pd.Series(values, name = name)
                        dfNode[quantityId][name] = d
        for df in dfNode:
            dfNode[df] = pd.DataFrame(dfNode[df])
            dfNode[df].index = self.dfTimeStamp
        return dfNode

    def reach2DF(self, reachExtIds, quantityIds = ['WaterLevel', 'Discharge', 'FlowVelocity', 'Froude', 'WaterVolume']):
        reachExtIds = listCleanUp(reachExtIds)
        dfReach = {}
        for quantityId in quantityIds:
            dfReach[quantityId] = {}
        reaches = self.resultData.Reaches
        for i, reach in enumerate(reaches):
            reachId = reach.Id
            rid = reachId[:(-1 * len(str(i)) - 1)]
            # to accomodate new version of M1D, in which structures are saved with links, but not saved seperately
            rid2 = rid.split(':')[1] if rid.split(':')[0] in ['Weir', 'Pump', 'Orifice', 'Valve'] else rid
                
            if rid2 in reachExtIds:
                gps = [gp.Chainage for gp in reach.GridPoints.ToArray()]
                for di in reach.DataItems:
                    quantityId = di.Quantity.Id
                    if quantityId in quantityIds:
                        elemCount = di.NumberOfElements
                        adj = int((len(gps) - elemCount * 2 + 1)/2) #return 0 if water level, 1 if discharge, middle chainage if velocity, 0 if AD concentration, -1 if AD mass flux (kg/s), elemCount if quality transport accumulate  # might not always working, test with more or less output variables.
                        if adj == 0: #water levels, AD concentrations, at H points
                            names = [f'{rid} {round(chainage, 2)}' for chainage in gps[0::2]]
                        elif adj == -1: # AD mass flux or accumulated mass, at all Q points plus first and last H points
                            names = [f'{rid} {round(chainage, 2)}' for chainage in [gps[0]] + gps[1::2] + [gps[-1]]]
                        else : #discharge, at Q points if adj == 1; velocity, at middle chainage, if adj > 1; other type if adj < -1
                            elemCount = 1
                            names = [rid]
                        for elem in range(elemCount):
                            values = list(di.CreateTimeSeriesData(elem))
                            values = [values[tsi] for tsi in self.indicesTimeStamp]
                            name = names[elem]
                            d = pd.Series(values, name = name)
                            dfReach[quantityId][name] = d
        for df in dfReach:
            dfReach[df] = pd.DataFrame(dfReach[df])
            dfReach[df].index = self.dfTimeStamp
        return dfReach

    def structure2DF(self, structureExtIds, quantityIds = ['DischargeInStructure', 'CrestLevel', 'ValveOpening', 'GateLevel', 'ControlStrategyId']):
        structureExtIds = listCleanUp(structureExtIds)
        dfStructure = {}
        structureTypes = self.resultData.StructureTypes
        for quantityId in quantityIds:
            dfStructure[quantityId] = {}
        for di in self.resultData.DataItems:
            desc = di.Quantity.Description
            quantityId = di.Quantity.Id
            if quantityId in quantityIds:
                extIds = [sId for sId in structureExtIds if ' ' + sId + ' ' in desc]
                if len(extIds) == 1:
                    values = list(di.CreateTimeSeriesData(0))
                    values = [values[tsi] for tsi in self.indicesTimeStamp]
                    name = desc[(desc.find(':')+2):]
                    d = pd.Series(values, name = name)
                    dfStructure[quantityId][name] = d
        for df in dfStructure:
            dfStructure[df] = pd.DataFrame(dfStructure[df])
            dfStructure[df].index = self.dfTimeStamp
        return dfStructure

    def discharge2DF(self, extIds):
        extIds = listCleanUp(extIds)
        df0 = self.node2DF(extIds, ['WaterSpillDischarge'])
        df0 = df0['WaterSpillDischarge']
        df1 = self.reach2DF(extIds, ['Discharge'])
        df1 = df1['Discharge']
        df1cols = [col for col in df1.columns if ':' in col]
        extIds2 = [extId for extId in extIds if not any([extId in col for col in df1cols])]
        df2 = self.structure2DF(extIds2, ['DischargeInStructure'])
        df2 = df2['DischargeInStructure']
        df3 = self.catchment2DF(extIds, ['Total'])
        df = pd.concat([df0, df1, df2, df3], axis=1)
        return df
       
    def linkCoordinates2Df(self, gridpointH = True):
        #use gridpointH = True for H points and False for Q points
        dfReach = {'Link_MUID':[], 'Chainage':[], 'X':[], 'Y':[], 'Z':[]}
        reaches = self.resultData.Reaches
        for i, reach in enumerate(reaches):
            reachId = reach.Id
            reachId = reachId[:(-1 * len(str(i)) - 1)]
            extract_gp = gridpointH
            for gp in reach.GridPoints.ToArray():
                if extract_gp:
                    dfReach['Link_MUID'].append(str(reachId))
                    dfReach['Chainage'].append(round(gp.get_Chainage(), 2))
                    dfReach['X'].append(gp.get_X())
                    dfReach['Y'].append(gp.get_Y())
                    dfReach['Z'].append(gp.get_Z())
                extract_gp = not extract_gp
        return pd.DataFrame(data = dfReach)
    
    def nodeCoordinates2Df(self):
        #return node muid, x, and y
        dfNode = {'Node_MUID':[], 'IL':[], 'GL':[], 'X':[], 'Y':[]}
        nodes = self.resultData.Nodes
        for i, node in enumerate(nodes):
            dfNode['Node_MUID'].append(node.Id)
            dfNode['IL'].append(node.BottomLevel)
            dfNode['GL'].append(node.GroundLevel)
            dfNode['X'].append(node.XCoordinate)
            dfNode['Y'].append(node.YCoordinate)
        return pd.DataFrame(data = dfNode)
    
    def get_elementIDs(self):
        # catchment ids as an list
        catchmentIDs = [catchment.Id.split(' - ')[0] if ' - ' in catchment.Id else catchment.Id for catchment in self.resultData.Catchments]
        catchmentIDs = list(set(catchmentIDs))
        catchmentIDs.sort()
        # node ids as an list
        nodeIDs = [node.Id for node in self.resultData.Nodes]
        # reach and strucutre ids as an list
        reachIDs = []
        weirIDs = []
        pumpIDs = []
        orificeIDs = []
        valveIDs = []
        listOptions = {
            'Weir': weirIDs,
            'Pump': pumpIDs,
            'Orifice': orificeIDs,
            'Valve':valveIDs
        }
        reaches = self.resultData.Reaches
        for i, reach in enumerate(reaches):
            reachId = reach.Id
            rid = reachId[:(-1 * len(str(i)) - 1)]
            if ':' not in rid:
                reachIDs.append(rid)
            else:
                if rid.split(':')[0] in listOptions:
                    listOptions[rid.split(':')[0]].append(rid.split(':')[1])
                
        return [catchmentIDs, nodeIDs, reachIDs, weirIDs, pumpIDs, orificeIDs, valveIDs]
