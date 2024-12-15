"""
Model exported as python.
Name : Analise da Logica Booleana para Aterro Sanitário
Group : Builder
With QGIS : 33408
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing


class AnaliseDaLogicaBooleanaParaAterroSanitrio(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('aerdromos', 'Aeródromos', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('aglomerado_rural', 'Aglomerado Rural', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('declividade', 'Declividade', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('ferrovias', 'Ferrovias', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('hidrografia', 'Hidrografia', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('limite_geogrfico', 'Limite Geográfico', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('limite_geogrfico2', 'Limite Geográfico', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('limite_geogrfico3', 'Limite Geográfico', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('mancha_urbana', 'Mancha Urbana', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('massa_dagua', "Massa d'agua", types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('povoado', 'Povoado', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('rea_de_proteo_ambiental_apa', 'Área de Proteção Ambiental (APA)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('rodovias', 'Rodovias', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('sede', 'Sede', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('unidade_de_conservao_estadual', 'Unidade de Conservação Estadual', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('unidade_de_conservao_federal', 'Unidade de Conservação Federal', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('uso_e_ocupao_da_terra', 'Uso e Ocupação da Terra', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('vila', 'Vila', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Multiparte', 'Multiparte', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LocaisAptosParaAterroSanitrio', 'Locais aptos para aterro sanitário ', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('LocaisInaptosParaAterroSanitrio', 'Locais inaptos para aterro sanitário ', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('AterrosSanitrios', 'Aterros Sanitários', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterRasterDestination('MapaDeCalorEstimativaDeDensidadeKernel', 'Mapa de calor (Estimativa de densidade Kernel)', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(51, model_feedback)
        results = {}
        outputs = {}

        # Aglomerado Rural (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['aglomerado_rural'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AglomeradoRuralReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Aeródromos (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['aerdromos'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AerdromosReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Massa D'agua (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['massa_dagua'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MassaDaguaReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Mancha Urbana (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['mancha_urbana'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ManchaUrbanaReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Rodovias (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['rodovias'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RodoviasReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Ferrovias (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['ferrovias'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FerroviasReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Área de Proteção Ambiental (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['rea_de_proteo_ambiental_apa'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReaDeProteoAmbientalReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Hidrografia (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['hidrografia'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['HidrografiaReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Uso e Ocupação da Terra (Reprojetado)
        alg_params = {
            'DATA_TYPE': 0,  # Use Camada de entrada Tipo Dado
            'EXTRA': '',
            'INPUT': parameters['uso_e_ocupao_da_terra'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Vizinho mais próximo
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UsoEOcupaoDaTerraReprojetado'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Unidade de Conservação Estadual (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['unidade_de_conservao_estadual'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnidadeDeConservaoEstadualReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Massa d'água (Buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 200,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['MassaDaguaReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 20,
            'SEGMENTS': 200,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MassaDguaBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Vila (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['vila'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['VilaReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Povoado (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['povoado'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PovoadoReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Rodovia (Buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 15,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['RodoviasReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 15,
            'SEGMENTS': 15,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RodoviaBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Aeródromo (buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 20000,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['AerdromosReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 200,
            'SEGMENTS': 200,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AerdromoBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Unidade de Conservação Federal (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['unidade_de_conservao_federal'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnidadeDeConservaoFederalReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Sede (Reprojetado)
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['sede'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:31983'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SedeReprojetado'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Povoado (Buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 500,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['PovoadoReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 50,
            'SEGMENTS': 50,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PovoadoBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Mancha Urbana (Buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 500,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['ManchaUrbanaReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 50,
            'SEGMENTS': 50,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ManchaUrbanaBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Declividade (Reprojetado)
        alg_params = {
            'DATA_TYPE': 0,  # Use Camada de entrada Tipo Dado
            'EXTRA': '',
            'INPUT': parameters['declividade'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Vizinho mais próximo
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem(''),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeclividadeReprojetado'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Uso e Ocupação (Recortar raster pela extensão)
        alg_params = {
            'DATA_TYPE': 0,  # Use Camada de entrada Tipo Dado
            'EXTRA': '',
            'INPUT': outputs['UsoEOcupaoDaTerraReprojetado']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': '',
            'OVERCRS': False,
            'PROJWIN': parameters['limite_geogrfico2'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UsoEOcupaoRecortarRasterPelaExtenso'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Hidrografia (Buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 200,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['HidrografiaReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 20,
            'SEGMENTS': 20,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['HidrografiaBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # União dos dados Zonamento Ambiental
        alg_params = {
            'INPUT': outputs['HidrografiaBuffer']['OUTPUT'],
            'OVERLAYS': [outputs['MassaDguaBuffer']['OUTPUT'],outputs['HidrografiaBuffer']['OUTPUT'],outputs['UnidadeDeConservaoFederalReprojetado']['OUTPUT'],outputs['UnidadeDeConservaoEstadualReprojetado']['OUTPUT'],outputs['ReaDeProteoAmbientalReprojetado']['OUTPUT']],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnioDosDadosZonamentoAmbiental'] = processing.run('native:multiunion', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Aglomerado Rural (Buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 500,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['AglomeradoRuralReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 50,
            'SEGMENTS': 50,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AglomeradoRuralBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Declividade (Recortar raster pela extensão)
        alg_params = {
            'DATA_TYPE': 0,  # Use Camada de entrada Tipo Dado
            'EXTRA': '',
            'INPUT': outputs['DeclividadeReprojetado']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': '',
            'OVERCRS': False,
            'PROJWIN': parameters['limite_geogrfico2'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeclividadeRecortarRasterPelaExtenso'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Ferrovias (Buffer)
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 15,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['FerroviasReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 15,
            'SEGMENTS': 15,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FerroviasBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Declividade (Vetor)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['DeclividadeRecortarRasterPelaExtenso']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeclividadeVetor'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Sede (Buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 500,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['SedeReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 50,
            'SEGMENTS': 50,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SedeBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Vila (Buffer)
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 500,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['VilaReprojetado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 50,
            'SEGMENTS': 50,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['VilaBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Zonamento Ambiental
        alg_params = {
            'INPUT': outputs['UnioDosDadosZonamentoAmbiental']['OUTPUT'],
            'OVERLAY': parameters['limite_geogrfico3'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ZonamentoAmbiental'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Uso e Ocupação da Terra (Vetor)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['UsoEOcupaoRecortarRasterPelaExtenso']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UsoEOcupaoDaTerraVetor'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Declividade (Restrição)
        alg_params = {
            'EXPRESSION': '"DN"  <= 1 OR "DN" >= 30',
            'INPUT': outputs['DeclividadeVetor']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeclividadeRestrio'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Dados Topográficos
        alg_params = {
            'FIELD': [''],
            'INPUT': outputs['DeclividadeRestrio']['OUTPUT'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DadosTopogrficos'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Uso e Ocupação da Terra (Restrição)
        alg_params = {
            'EXPRESSION': '"DN" = 3 OR "DN" = 4 OR "DN" = 9 OR "DN" = 11 OR "DN" = 12 OR "DN" = 20 OR "DN" = 21 OR "DN" = 24 OR "DN" = 29 OR "DN" = 30 OR "DN" = 33 OR "DN" = 39 OR "DN" = 41 OR "DN" = 46 OR "DN" = 47 OR "DN" = 48 ',
            'INPUT': outputs['UsoEOcupaoDaTerraVetor']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UsoEOcupaoDaTerraRestrio'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # União dos dados Infraestrutura de Transportes
        alg_params = {
            'INPUT': outputs['AerdromoBuffer']['OUTPUT'],
            'OVERLAYS': [outputs['AerdromoBuffer']['OUTPUT'],outputs['FerroviasBuffer']['OUTPUT'],outputs['RodoviaBuffer']['OUTPUT']],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnioDosDadosInfraestruturaDeTransportes'] = processing.run('native:multiunion', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # União dos dados Núcleos Populacionais
        alg_params = {
            'INPUT': outputs['PovoadoBuffer']['OUTPUT'],
            'OVERLAYS': [outputs['VilaBuffer']['OUTPUT'],outputs['SedeBuffer']['OUTPUT'],outputs['PovoadoBuffer']['OUTPUT'],outputs['ManchaUrbanaBuffer']['OUTPUT'],outputs['AglomeradoRuralBuffer']['OUTPUT']],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnioDosDadosNcleosPopulacionais'] = processing.run('native:multiunion', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Uso e Ocupação da Terra
        alg_params = {
            'FIELD': [''],
            'INPUT': outputs['UsoEOcupaoDaTerraRestrio']['OUTPUT'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UsoEOcupaoDaTerra'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Infraestrutura de Transportes
        alg_params = {
            'INPUT': outputs['UnioDosDadosInfraestruturaDeTransportes']['OUTPUT'],
            'OVERLAY': parameters['limite_geogrfico3'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['InfraestruturaDeTransportes'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Núcleos Populacionais
        alg_params = {
            'INPUT': outputs['UnioDosDadosNcleosPopulacionais']['OUTPUT'],
            'OVERLAY': parameters['limite_geogrfico3'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['NcleosPopulacionais'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Mesclar camadas vetoriais
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['UsoEOcupaoDaTerra']['OUTPUT'],outputs['DadosTopogrficos']['OUTPUT'],outputs['NcleosPopulacionais']['OUTPUT'],outputs['ZonamentoAmbiental']['OUTPUT'],outputs['InfraestruturaDeTransportes']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MesclarCamadasVetoriais'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Áreas inviáveis (parciais)
        alg_params = {
            'FIELD': [''],
            'INPUT': outputs['MesclarCamadasVetoriais']['OUTPUT'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReasInviveisParciais'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Áreas viáveis (parciais)
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['ReasInviveisParciais']['OUTPUT'],
            'OVERLAY': parameters['limite_geogrfico'],
            'OVERLAY_FIELDS_PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReasViveisParciais'] = processing.run('native:symmetricaldifference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # Multipartes para partes simples
        alg_params = {
            'INPUT': outputs['ReasViveisParciais']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MultipartesParaPartesSimples'] = processing.run('native:multiparttosingleparts', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Área (ha)',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '$area/10000',
            'INPUT': outputs['MultipartesParaPartesSimples']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampo'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # Áreas viáveis
        alg_params = {
            'EXPRESSION': '"Área (ha)" >= 3',
            'INPUT': outputs['CalculadoraDeCampo']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReasViveis'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # Locais aptos para aterro sanitário
        alg_params = {
            'INPUT': parameters['limite_geogrfico'],
            'OVERLAY': outputs['ReasViveis']['OUTPUT'],
            'OUTPUT': parameters['LocaisAptosParaAterroSanitrio']
        }
        outputs['LocaisAptosParaAterroSanitrio'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LocaisAptosParaAterroSanitrio'] = outputs['LocaisAptosParaAterroSanitrio']['OUTPUT']

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # Locais inaptos para aterro sanitário
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['LocaisAptosParaAterroSanitrio']['OUTPUT'],
            'OVERLAY': parameters['limite_geogrfico'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['LocaisInaptosParaAterroSanitrio']
        }
        outputs['LocaisInaptosParaAterroSanitrio'] = processing.run('native:symmetricaldifference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LocaisInaptosParaAterroSanitrio'] = outputs['LocaisInaptosParaAterroSanitrio']['OUTPUT']

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}

        # Multiparte
        alg_params = {
            'INPUT': outputs['LocaisAptosParaAterroSanitrio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Multiparte'] = processing.run('native:multiparttosingleparts', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}

        # Centroides
        alg_params = {
            'ALL_PARTS': True,
            'INPUT': outputs['Multiparte']['OUTPUT'],
            'OUTPUT': parameters['Multiparte']
        }
        outputs['Centroides'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Multiparte'] = outputs['Centroides']['OUTPUT']

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # Aterro Sanitário no limite geográfico definido
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['LocaisInaptosParaAterroSanitrio']['OUTPUT'],
            'OVERLAY': outputs['LocaisAptosParaAterroSanitrio']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['AterrosSanitrios']
        }
        outputs['AterroSanitrioNoLimiteGeogrficoDefinido'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['AterrosSanitrios'] = outputs['AterroSanitrioNoLimiteGeogrficoDefinido']['OUTPUT']

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # Mapa de calor (Estimativa de densidade Kernel)
        alg_params = {
            'DECAY': 0,
            'INPUT': outputs['Centroides']['OUTPUT'],
            'KERNEL': 0,  # Quartico
            'OUTPUT_VALUE': 0,  # Bruto
            'PIXEL_SIZE': 30,
            'RADIUS': 2000,
            'RADIUS_FIELD': None,
            'WEIGHT_FIELD': None,
            'OUTPUT': parameters['MapaDeCalorEstimativaDeDensidadeKernel']
        }
        outputs['MapaDeCalorEstimativaDeDensidadeKernel'] = processing.run('qgis:heatmapkerneldensityestimation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['MapaDeCalorEstimativaDeDensidadeKernel'] = outputs['MapaDeCalorEstimativaDeDensidadeKernel']['OUTPUT']
        return results

    def name(self):
        return 'Analise da Logica Booleana para Aterro Sanitário'

    def displayName(self):
        return 'Analise da Logica Booleana para Aterro Sanitário'

    def group(self):
        return 'Builder'

    def groupId(self):
        return 'Builder'

    def createInstance(self):
        return AnaliseDaLogicaBooleanaParaAterroSanitrio()
