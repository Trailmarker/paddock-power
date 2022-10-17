
# def makeGetterFromField(cls, field: Field):
#     if field.type() == QVariant.String:
#         return lambda self: self.get(field.name(), None)
    

# SCHEMA = [
#         Field(propertyName="", name=FID, type=QVariant.LongLong, typeName="Integer64",
#               len=0, prec=0, comment="", subType=QVariant.Invalid),
#         Field(propertyName="", name=NAME, type=QVariant.String, typeName="String",
#               len=0, prec=0, comment="", subType=QVariant.Invalid),
#         Field(propertyName="", name=STATUS, type=QVariant.String, typeName="String",
#               len=0, prec=0, comment="", subType=QVariant.Invalid,
#               domainType=FeatureStatus, defaultValue=FeatureStatus.Undefined)
# ]

# def makePropertyFromField(cls, field: Field):
#         """Create a property for the given attribute and attribute type."""
        
#         if field.typeName() == QVariant.String:
#             return lambda self: str(self[field.name()])
#         elif field.typeName() == 
#         if 

#         getterName = f"_{propertyName}"
#         setterName = f"set{propertyName[0].capitalize()}"

#         setattr(cls, getterName, lambda self : self.get(attributeName, None))
#         setattr(cls, setterName, lambda self, value: self.setItem(attributeName, value))

#         setattr(cls, propertyName, property(fget=getattr(cls, getterName), fset=getattr(cls, setterName)))
#         return cls

# class dictionaryKeyProperty:
#     """A decorator to create a property for the given attribute and attribute type."""
#     def __init__(self, propertyName, attributeName):
#         self.propertyName = propertyName
#         self.attributeName = attributeName

#     def __call__(self, cls):
#         return makePropertyFromDictionaryKey(cls, self.propertyName, self.attributeName)

# @dictionaryKeyProperty('foo', 'bar')
# class WildIdea(dict):
   
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def setItem(self, key, value):
#         self[key] = value