# -*- coding: utf-8 -*-
import inspect

from qgis.core import QgsProject

from .utils import qgsDebug
from .spatial.layers.paddock_layer import PaddockLayer

# def makePaddockLayer():

#     paddockLayerName = f"Current Paddocks"
#     gpkgFile="C:/Users/tom.lynch/dev/trm/paddock-power-data/Mathison-0.9/Mathison - Clean/Mathison - Testing.gpkg"

#     paddockLayer = PaddockLayer(sourceType=FeatureLayerSourceType.Detect, layerName=paddockLayerName, gpkgFile=gpkgFile)
#     QgsProject.instance().addMapLayer(paddockLayer, False)
#     return paddockLayer

# class A:
#     def __new__(cls, *args, **kwargs):
#         qgsDebug("A.__new__")

#         qgsDebug(f"inspect.getmembers(cls): {inspect.getmembers(cls)}")

#         qgsDebug(f"args: {str(args)}")
#         qgsDebug(f"kwargs: {str(kwargs)}")

#         return super().__new__(cls)

#     @classmethod
#     def doNothing(cls):
#         pass

#     def __init__(self, a, b):
#         qgsDebug(f"A.__init__(a={a}, b={b})")

#         self.a = a
#         self.b = b

# # Tom = A("Tom", "Lynch")

# class B(A):
#     def __new__(cls, *args, **kwargs):
#         qgsDebug("B.__new__")

#         qgsDebug(f"inspect.getmembers(cls): {inspect.getmembers(cls)}")

#         qgsDebug(f"args: {str(args)}")
#         qgsDebug(f"kwargs: {str(kwargs)}")

#         # if args[0] == "Tom":
#         #     return Tom

#         return super().__new__(cls, *args, **kwargs)

#     @classmethod
#     def alsoDoNothing(cls):
#         pass

#     def __init__(self, a, b, c):
#         qgsDebug(f"B.__init__(a={a}, b={b}, c={c})")


#         qgsDebug(f"inspect.getmembers(self): {inspect.getmembers(self)}")

#         super().__init__(a, b)
#         self.c = c

# Tommo = B("Tom", "Eitelhuber", "Moore")


from mlapp.src.models.state import State

State().detectProject()
fenceLayer = State().getMilestone().fenceLayer
paddockLayer = State().getMilestone().paddockLayer
# testFence = [f for f in fenceLayer.getFeatures() if f.name == "Test"][0]
# anotherFence = [f for f in fenceLayer.getFeatures() if f.name == "Another"][0]
