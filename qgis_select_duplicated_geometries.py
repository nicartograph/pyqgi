from qgis.core import *
import qgis.utils

layer = iface.activeLayer()

index = QgsSpatialIndex(layer.getFeatures())
features = layer.getFeatures()

selection = []
for feat in features:
    inGeom = feat.geometry()
    idsList = index.intersects(inGeom.boundingBox())
    if len(idsList) > 1:
        for id in idsList:
            selection.append(next(layer.getFeatures(QgsFeatureRequest().setFilterFid(id))))

layer.selectByIds([k.id() for k in selection])