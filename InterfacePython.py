from bokeh.plotting import *
from bokeh.io import output_file, show
from bokeh.events import ButtonClick
from bokeh.layouts import widgetbox, layout, row, column
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap, dodge
from bokeh.palettes import YlGnBu6
from bokeh.models.widgets import Select, Panel, Tabs, Button, Div, DataTable, DateFormatter, TableColumn
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from numpy import pi
import operator
from bokeh.core.properties import value

def x_genre():
    x= dataFrame[sheetColumns[5]];
    data={};
    som=0;
    for gender in x:
        if gender in data:
            data[gender]=data[gender]+1;
        else:
            data[gender]=1;
        som=som+1;
    return data,som;

def x_histo():
    histologies= dataFrame[sheetColumns[6]];
    data={};
    som=0;
    for histology in histologies:
        histologyLower= histology.lower();
        if "squamous" in histologyLower:
            if 'Squamous Cell Carcinoma' in data:
                data['Squamous Cell Carcinoma']=data['Squamous Cell Carcinoma']+1;
            else:
                data['Squamous Cell Carcinoma']=1;
        elif "adenocarcinoma" in histologyLower or "papillary" in histologyLower or "micropapillary" in histologyLower or "mucinous" in histologyLower or "acinar" in histologyLower or "solid"in histologyLower:
            if 'Adenocarcinoma' in data:
                data['Adenocarcinoma']=data['Adenocarcinoma']+1;
            else:
                data['Adenocarcinoma']=1;
        else:
            if 'Unspecified' in data:
                data['Unspecified']=data['Unspecified']+1;
            else:
                data['Unspecified']=1;
        som=som+1;
    return data,som;

def x_position():
    locations= dataFrame[sheetColumns[3]];
    data={};
    som=0;
    for locationR in locations:
        locationRS = locationR.split();
        for location in locationRS:
            if location in data:
                data[location]= data[location]+1;
            else:
                data[location]=1;
            som=som+1;
    return data,som;

def x_stade():
    primaries= dataFrame[sheetColumns[8]];
    nodes= dataFrame[sheetColumns[9]];
    mets= dataFrame[sheetColumns[10]];
    primariesData=[0,0,0,0];
    nodesData=[0,0,0,0];
    metsData=[0,0,0,0];
    for primary in primaries:
        primaryLower= primary.lower();
        if "pt0" in primaryLower:
            primariesData[0]=primariesData[0]+1;
        elif "pt1" in primaryLower:
            primariesData[1]=primariesData[1]+1;
        elif "pt2" in primaryLower:
            primariesData[2]=primariesData[2]+1;
        elif "pt3" in primaryLower:
            primariesData[3]=primariesData[3]+1;
            
    for node in nodes:
        nodeLower= node.lower();
        if "pn0" in nodeLower:
            nodesData[0]=nodesData[0]+1;
        elif "pn1" in nodeLower:
            nodesData[1]=nodesData[1]+1;
        elif "pn2" in nodeLower:
            nodesData[2]=nodesData[2]+1;
        elif "pn3" in nodeLower:
            nodesData[3]=nodesData[3]+1;
            
    for met in mets:
        metLower= met.lower();
        if "pm0" in metLower:
            metsData[0]=metsData[0]+1;
        elif "pm1" in metLower:
            metsData[1]=metsData[1]+1;
        elif "pm2" in metLower:
            metsData[2]=metsData[2]+1;
        elif "pm3" in metLower:
            metsData[3]=metsData[3]+1;
    return primariesData,nodesData,metsData;


dataFrame = pd.read_excel('Data/Lung3.metadata.xls', sheet_name='Lung3.metadata')
sheetColumns= dataFrame.columns;
dataFrameNameIndexed= dataFrame.set_index(sheetColumns[0]);
sampleSerie= dataFrame[sheetColumns[0]];
sampleList= sampleSerie.tolist();

patientSelect = Select(title="Patient:", value=sampleList[0], options=sampleList);
patientInfo= Div(text="""<br><h1 style="color:gray;",'display:inline'</h1> Numero du patient  :""" +patientSelect.value+"""</h1><br>
    <div><div style='float:left'><div><h4 style="color:red;",'display:inline'>Location : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[3]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Organism : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[4]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Gender : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[5]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Histology : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[6]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Tumor Size : </h4><p style='display:inline; font-size:12px'>"""+str(dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[7]])+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Primary Tumor Stage: </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[8]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Node Stage : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[9]]+"""</p></div><br>
    </div><div style='float:right'><div><h4 style="color:red;",'display:inline'>Mets Stage : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[10]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Primary/Mets : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[11]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Grade : </h4><p style='display:inline; font-size:12px'>"""+str(dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[12]])+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Test Molecule : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[13]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Label : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[14]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Platform : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[15]]+"""</p></div></div></div>""",width=900);


histologyRawData,histologyTotal=x_histo();
histologyMode=max(histologyRawData, key=histologyRawData.get);
histologyKeys=list(histologyRawData.keys());
histologyValues=list(histologyRawData.values());
histologyData = dict(
        data1=histologyKeys+['Total','Mode'],
        data2=histologyValues+[histologyTotal,histologyMode],
    )
histologySource = ColumnDataSource(histologyData)

histologyColumns = [
        TableColumn(field="data1", title='Histologie'),
        TableColumn(field="data2", title='Value'),
    ]
histologyTable = DataTable(source=histologySource, columns=histologyColumns,height=200, width=500)

histologyHistogramSource = ColumnDataSource(data=dict(data1=histologyKeys, data2=histologyValues));

histologyHistogram = figure(x_range=histologyKeys, plot_height=350,width=400, toolbar_location=None, title="Histologie")
histologyHistogram.vbar(x='data1', top='data2', width=0.9, source=histologyHistogramSource, legend="data1",
       line_color='white', fill_color=factor_cmap('data1', palette=YlGnBu6, factors=histologyKeys));

histologyLayout = row(histologyTable,histologyHistogram);
histologyTab= Panel(child=histologyLayout, title="2.2/Histologie");

primaryRawData,nodeRawData,metRawData= x_stade();
cancerStage = ['0', '1', '2', '3'];
cancerCharac = ["Primary", "Node", "Mets"];
charaColors = ["#DC143C", "#9400D3", "#228B22"];

stageData = {'Stage' : cancerStage,
        'Primary'   : primaryRawData,
        'Node'   : nodeRawData,
        'Mets'   : metRawData}

stageSource = ColumnDataSource(stageData)

stageColumns = [
        #TableColumn(field="Stage", title='Stage'),
        TableColumn(field="Primary", title=' Stage_Primary'),
        TableColumn(field="Node", title='Stage_Node'),
        TableColumn(field="Mets", title='Stage_Mets'),
    ]
stageTable = DataTable(source=stageSource,columns=stageColumns,height=300,width=350)

stageHistogram = figure(x_range=cancerStage, y_range=(0, 90), plot_height=350, title="Stade du cancer du poumon",
           toolbar_location=None, tools="")

stageHistogram.vbar(x=dodge('Stage', -0.25, range=stageHistogram.x_range), top='Primary', width=0.2, source=stageSource,
       color="#DC143C", legend=value("Primary"))

stageHistogram.vbar(x=dodge('Stage',  0.0,  range=stageHistogram.x_range), top='Node', width=0.2, source=stageSource,
       color="#9400D3", legend=value("Node"))

stageHistogram.vbar(x=dodge('Stage',  0.25, range=stageHistogram.x_range), top='Mets', width=0.2, source=stageSource,
       color="#228B22", legend=value("Mets"))

stageHistogram.x_range.range_padding = 0.1
stageHistogram.xgrid.grid_line_color = None
stageHistogram.legend.location = "top_center"
stageHistogram.legend.orientation = "horizontal"

stageLayout = row([stageTable,stageHistogram]);
stageTab= Panel(child=stageLayout, title="2.4/Stade");

tumorSizeRawData=dataFrame[sheetColumns[7]].values.tolist();
del tumorSizeRawData[3];
tumorSizePlot=figure(plot_width=700,plot_height=400,title="Taille du tumeur");
tumorSizePlot.line(range(len(tumorSizeRawData)),tumorSizeRawData,color="#9400D3");
tumorSizeLayout = column(tumorSizePlot);
TumorSizeTab= Panel(child=tumorSizeLayout, title="2.5/Taille du tumeur");


patientLayout = layout([[patientInfo,patientSelect]]);
patientTab= Panel(child=patientLayout, title="1/Patients");

locationRawData,locationTotal=x_position();
locationMode=max(locationRawData, key=locationRawData.get);
locationKeys=list(locationRawData.keys());
locationValues=list(locationRawData.values());
locationData = dict(
        data1=locationKeys+['Total','Mode'],
        data2=locationValues+[locationTotal,locationMode],
    )
locationSource = ColumnDataSource(locationData)

locationColumns = [
        TableColumn(field="data1", title='Position'),
        TableColumn(field="data2", title='Value'),
    ]
locationTable = DataTable(source=locationSource, columns=locationColumns,height=250 ,width=500)

locationHistogramSource = ColumnDataSource(data=dict(data1=locationKeys, data2=locationValues));

locationHistogram = figure(x_range=locationKeys, plot_height=350, toolbar_location=None, title="Position")
locationHistogram.vbar(x='data1', top='data2', width=0.9, source=locationHistogramSource, legend="data1",
       line_color='white', fill_color=factor_cmap('data1', palette=YlGnBu6, factors=locationKeys));

locationLayout = row(locationTable,locationHistogram);
locationTab= Panel(child=locationLayout, title="2.3/Position");


genderRawData,genderTotal=x_genre();
genderMode=max(genderRawData, key=genderRawData.get);
genderKeys=list(genderRawData.keys());
genderValues=list(genderRawData.values());
genderData = dict(
        data1=genderKeys+['Total','Mode'],
        data2=genderValues+[genderTotal,genderMode],
    )
genderSource = ColumnDataSource(genderData)

genderColumns = [
        TableColumn(field="data1", title='Genre'),
        TableColumn(field="data2", title='Value'),
    ]
genderTable = DataTable(source=genderSource, columns=genderColumns,height=200, width=500)

genderHistogramSource = ColumnDataSource(data=dict(data1=genderKeys, data2=genderValues));

genderHistogram = figure(x_range=genderKeys, plot_height=400, toolbar_location=None, title="Genre")
genderHistogram.vbar(x='data1', top='data2', width=0.6, source=genderHistogramSource, legend="data1",
       line_color='white', fill_color=factor_cmap('data1', palette=YlGnBu6, factors=genderKeys));

genderLayout = row(genderTable,genderHistogram);
genderTab= Panel(child=genderLayout, title="2.1/Genre");    





webInterfaceLayout=Tabs(tabs=[patientTab,genderTab,histologyTab,locationTab,stageTab,TumorSizeTab]);
curdoc().add_root(webInterfaceLayout);

def select_pat(attr, old, new):
    patientInfo.text="""<br><h1 style="color:gray;",'display:inline'</h1> Numero du patient  :"""+patientSelect.value+"""</h1><br>
  <div><div style='float:left'><div><h4 style="color:red;",'display:inline'>Location : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[3]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Organism : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[4]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Gender : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[5]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Histology : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[6]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Tumor Size : </h4><p style='display:inline; font-size:12px'>"""+str(dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[7]])+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Primary Tumor Stage: </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[8]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Node Stage : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[9]]+"""</p></div><br>
    </div><div style='float:right'><div><h4 style="color:red;",'display:inline'>Mets Stage : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[10]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Primary/Mets : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[11]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Grade : </h4><p style='display:inline; font-size:12px'>"""+str(dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[12]])+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Test Molecule : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[13]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Label : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[14]]+"""</p></div><br>
    <div><h4 style="color:red;",'display:inline'>Platform : </h4><p style='display:inline; font-size:12px'>"""+dataFrameNameIndexed.loc[patientSelect.value,sheetColumns[15]]+"""</p></div>""";
        

patientSelect.on_change("value", select_pat);      
