from qgis.core import *
import qgis.utils
from PyQt5.QtCore import QVariant

layer = iface.activeLayer()
layer_data = layer.dataProvider()
if layer_data.fieldNameIndex("classid") == -1:   
        layer_data.addAttributes([QgsField("clasid", QVariant.Int, typeName = 'Int', len = 10)])
        layer.startEditing()
        layer.updateFields()
        print("field added")
else:
    print ("field already exists")
features = layer.getFeatures()
spIndex = QgsSpatialIndex(features)
features = layer.getFeatures() # так надо

id_set = set()
n_class = 0
classid = layer.fields().indexFromName('classid')


for feature in features:
    if feature.id() not in id_set:
        id_set.add(feature.id())
        layer.changeAttributeValue(feature.id(), classid, n_class)
        sum_lab = feature['Label']
        nearestId = spIndex.nearestNeighbor(feature.geometry().asPoint(), 500)
        for nId in nearestId[1:]:
            if nId not in id_set : 
                if sum_lab < 1100 :
                    id_set.add(nId)
                    feat = layer.getFeatures(QgsFeatureRequest().setFilterFid(nId))
                    f = next(feat)
                    layer.changeAttributeValue(f.id(), classid, n_class)
                    sum_lab = sum_lab + f['Label']
                    
        
        n_class = n_class + 1
        
layer.commitChanges()
print('The end')