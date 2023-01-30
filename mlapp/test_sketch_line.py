from qgis.core import QgsGeometry


from .dev import *
from mlapp.src.tools.sketch_line_tool import SketchLineTool

p1 = workspace().pipelineLayer.makeFeature()
p2 = workspace().pipelineLayer.makeFeature()
p3 = workspace().pipelineLayer.makeFeature()


# def onSketchPipelineFinished(sketchLine):
#     testPipeline.GEOMETRY = sketchLine


# tool = SketchLineTool(workspace())
# tool.sketchFinished.connect(onSketchPipelineFinished)


wkt = "LineString (-363652.75268516730284318 -1888203.19256767281331122, -365386.5818168519763276 -1872772.11329567898064852, -357931.11655060778139159 -1876239.77155904844403267, -354810.22411357529927045 -1859248.24606853839941323, -342153.27145227702567354 -1879880.81273558619432151)"

testGeom = QgsGeometry.fromWkt(wkt)

# p1.planFeature1(testGeom)
def testCrash():
    p1.GEOM = testGeom
    p1.featureLayer.startEditing()
    p1.upsert()

#testPipeline.GEOMETRY = testGeom

