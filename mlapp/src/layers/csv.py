# -*- coding: utf-8 -*-
from csv import writer
from datetime import datetime

from ..utils import resolveProjectPath


def writeFeature(csvWriter, feature):
    """Write a Feature to CSV as a row."""
    values = [field.getValue(feature) for field in feature.getSchema()]
    csvWriter.writerow(values)


def writeHeader(csvWriter, featureType):
    """Write a Feature Type's header to CSV as a row."""
    csvWriter.writerow([field.name() for field in featureType.getSchema()])


def writeFeatureLayer(csvWriter, featureLayer):
    """Write a Feature Layer to CSV."""
    writeHeader(csvWriter, featureLayer.getFeatureType())
    for feature in featureLayer.getFeatures():
        writeFeature(csvWriter, feature)


def extractCsv(featureLayer):
    """Extract a Feature Layer to CSV."""
    csvPath = resolveProjectPath(f"{featureLayer.name()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv")

    with open(csvPath, "w", newline='', encoding='utf-8') as file:
        csvWriter = writer(file)
        writeFeatureLayer(csvWriter, featureLayer)
