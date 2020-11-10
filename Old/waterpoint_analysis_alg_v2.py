import os
import inspect
from qgis.core import   (QgsProcessing,
                        QgsProcessingParameterBoolean,
                        QgsProcessingParameterString,
                        QgsProcessingAlgorithm, 
                        QgsProcessingParameterFeatureSource, 
                        QgsProcessingParameterVectorDestination,
                        QgsProcessingParameterEnum,
                        QgsProcessingMultiStepFeedback,
                        QgsCoordinateReferenceSystem)
from PyQt5.QtGui import QIcon
import processing


class WaterpointBuffers(QgsProcessingAlgorithm):
    CURWATERS = 'CURWATERS'
    NEWWATERS = 'NEWWATERS'
    PADDOCK = 'PADDOCK'
    LAND = 'LAND'
#    BUFFER_2KM = 'BUFFER_2KM'
#    BUFFER_3KM = 'BUFFER_3KM'
#    BUFFER_5KM = 'BUFFER_5KM'
#    BUFFER_8KM = 'BUFFER_8KM'
    PRESET = 'PRESET'
    CUSTOM = 'CUSTOM'
    OUTPUT = 'OUTPUT'
 
    def __init__(self):
        super().__init__()
 
    def name(self):
        return "Waterpoint Buffers"
 
    def displayName(self):
        return "Waterpoint Buffers"
        
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icons/buffer.png'))) # icon for the Paddock Power Tools Group in Toolbox
        return icon
        
    def group(self):
        return 'Waterpoint Tools'
    
    def groupId(self):
        return 'Waterpoint Tools'
 
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CURWATERS,
                'Current Waterpoints',
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.NEWWATERS,
                'New Waterpoints',
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PADDOCK,
                'Paddock',
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.LAND,
                'Land Units or Land Systems',
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        
        self.preset = (
            ('2km Buffer'),
            ('3km Buffer'),
            ('5km Buffer'),
            ('8km Buffer')
            )

        presets = QgsProcessingParameterEnum(self.PRESET,
                                               'Preset Buffers',
                                               options=self.preset,
                                               allowMultiple=True, defaultValue=[1,2])
        presets.setMetadata({
            'widget_wrapper': {
                'class': 'processing.gui.wrappers.EnumWidgetWrapper',
                'useCheckBoxes': True,
                'columns': 4}})
        self.addParameter(presets)
            
#        self.addParameter(QgsProcessingParameterBoolean(self.BUFFER_2KM,'2km Buffer', defaultValue=False))
#        self.addParameter(QgsProcessingParameterBoolean(self.BUFFER_3KM,'3km Buffer', defaultValue=True))
#        self.addParameter(QgsProcessingParameterBoolean(self.BUFFER_5KM, '5km Buffer', defaultValue=True))
#        self.addParameter(QgsProcessingParameterBoolean(self.BUFFER_8KM, '8km Buffer', defaultValue=False))

        self.addParameter(
            QgsProcessingParameterString(self.CUSTOM, 'Custom Buffers in Meters seperated with a space eg. 5000 2000', optional=True))

        self.addParameter(
            QgsProcessingParameterVectorDestination (
                self.OUTPUT,
                'Waterpoint Buffers'
            )
        )
    

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(62, model_feedback)
        results = {}
        outputs = {}
        buffers = []
        
#        buffer2km = self.parameterAsBoolean(parameters, self.BUFFER_2KM, context)
#        buffer3km = self.parameterAsBoolean(parameters, self.BUFFER_3KM, context)
#        buffer5km = self.parameterAsBoolean(parameters, self.BUFFER_5KM, context)
#        buffer8km = self.parameterAsBoolean(parameters, self.BUFFER_8KM, context)
        outputFile = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        customlist = self.parameterAsString(parameters, self.CUSTOM, context)

        
        if customlist != "":
            custombuffers = customlist.split(" ")
            for custom in custombuffers:
                buffers.append(int(custom))
        else:
            
            presetBuffers = [self.preset[i] for i in self.parameterAsEnums(parameters, self.PRESET, context)]

            if '2km Buffer' in presetBuffers:
                buffers.append(2000)
            
            if '3km Buffer' in presetBuffers:
                buffers.append(3000)
            
            if '5km Buffer' in presetBuffers:
                buffers.append(5000)
                
            if '8km Buffer' in presetBuffers:
                buffers.append(8000)
            

        buffers.sort(reverse=True)
        outputBuffers = []
        #print(parameters['CURWATERS'])
        for buffer in buffers:
            print('Running ' + str(buffer/1000)+'km buffer')
            buff = processing.run("native:buffer",
            {'INPUT':parameters['CURWATERS'],
            'DISTANCE':buffer,
            'SEGMENTS':25,
            'END_CAP_STYLE':0,
            'JOIN_STYLE':0,
            'MITER_LIMIT':2,
            'DISSOLVE':True,
            'OUTPUT':'TEMPORARY_OUTPUT'})
            outputBuffers.append(buff)
        
        return (outputBuffers)
        #return {self.OUTPUT : outputBuffers}
