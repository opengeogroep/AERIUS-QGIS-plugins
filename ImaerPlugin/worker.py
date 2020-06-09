#import traceback
import time

from PyQt5.QtCore import QObject, pyqtSignal
from qgis.core import QgsFeature, QgsGeometry




class Worker(QObject):

    finished = pyqtSignal(object)
    error = pyqtSignal(Exception, basestring)
    progress = pyqtSignal(float)

    def __init__(self, featureCollection, attributes, pointProvider=None, hexagonProvider=None):
        QObject.__init__(self)
        self.killed = False
        self.featureCollection = featureCollection
        self.attributes = attributes
        self.pointProvider = pointProvider
        self.hexagonProvider = hexagonProvider
        self.doPoint = pointProvider is not None
        self.doHexagon = hexagonProvider is not None


    def run(self):
        self.featureCount = 0
        try:
            self.progress.emit(0)
            step = 10

            ft = self.featureCollection.nextFeature(doPoints=self.doPoint, doHexagons=self.doHexagon)
            pointFeatures = []
            hexagonFeatures = []

            while ft:
                self.featureCount += 1
                if self.killed is True:
                    break

                if ft is not None:
                    if self.doPoint:
                        pass
                        feat = self.getFeature(ft, dim=0)
                        pointFeatures.append(feat)
                    if self.doHexagon:
                        pass
                        feat = self.getFeature(ft, dim=2)
                        hexagonFeatures.append(feat)

                if self.featureCount % step == 0:
                    if self.doPoint:
                        self.pointProvider.addFeatures(pointFeatures)
                        pointFeatures = []
                    if self.doHexagon:
                        self.hexagonProvider.addFeatures(hexagonFeatures)
                        hexagonFeatures = []
                    self.progress.emit(ft[u'progress'] * 100.0)

                # increase step for large datasets
                if self.featureCount > 1000:
                    step = 100
                if self.featureCount > 10000:
                    step = 1000

                ft = self.featureCollection.nextFeature()

            if self.doPoint:
                self.pointProvider.addFeatures(pointFeatures)
            if self.doHexagon:
                self.hexagonProvider.addFeatures(hexagonFeatures)


            if self.killed is False:
                self.progress.emit(100)
        except Exception as e:
            self.error.emit(e, 'Error while reading xml file')

        self.finished.emit(self.featureCount)


    def getFeature(self, ft, dim=2):
        """Creates a QGIS feature from a feature returned by the imaerread parser

        :param ft: feature returned by the imaerread parser
        :type ft: dict

        :param dim: dimension of the geometry
        :type dim: int
        """
        feat = QgsFeature()
        if dim == 2:
            feat.setGeometry(QgsGeometry.fromWkt(ft['hexagon']))
        else:
            feat.setGeometry(QgsGeometry.fromWkt(ft['point']))
        featureAttributes = [ft['id']]
        for attr in self.attributes:
            try:
                featureAttributes.append(ft[attr])
            except:
                featureAttributes.append(None)
        feat.setAttributes(featureAttributes)
        return feat


    def kill(self):
        self.killed = True
