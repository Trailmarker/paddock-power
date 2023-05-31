# -*- coding: utf-8 -*-
from contextlib import contextmanager
from csv import writer
from datetime import datetime


def timestampedCsvFilename(baseFilename):
    """Return a path with a timestamp appended."""
    return f"{baseFilename}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"


@contextmanager
def makeCsvWriter(csvFilename):
    """Return a CSV writer for the given path."""
    with open(csvFilename, "w", newline="") as csvFile:
        yield writer(csvFile)


def __writeFeature(csvWriter, feature):
    """Write a Feature to CSV as a row."""
    values = [field.getValue(feature) for field in feature.getSchema()]
    csvWriter.writerow(values)


def writeHeader(csvWriter, featureType):
    """Write a Feature Type's header to CSV as a row."""
    csvWriter.writerow([field.name() for field in featureType.getSchema()])


def writeFeature(csvWriter, feature):
    """Write a Feature to CSV."""
    writeHeader(csvWriter, type(feature))
    __writeFeature(csvWriter, feature)


def writeFeatureLayer(csvWriter, featureLayer):
    """Write a Feature Layer to CSV."""
    writeHeader(csvWriter, featureLayer.getFeatureType())
    for feature in featureLayer.getFeatures():
        __writeFeature(csvWriter, feature)
