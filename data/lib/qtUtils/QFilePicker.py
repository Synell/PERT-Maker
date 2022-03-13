#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSignal
from enum import Enum
import os
import types
#----------------------------------------------------------------------

    # Class
class QFilePicker(QWidget):
    class Type(Enum):
        OpenFileName = 0
        OpenFileNames = 1
        OpenFileUrl = 2
        OpenFileUrls = 3
        SaveFileName = 4
        SaveFileUrl = 5
        ExistingDirectory = 6
        ExistingDirectoryUrl = 7

    class Extension:
        class Image(Enum):
            def ALL(title: str = '') -> str:
                return QFilePicker.Extension.combineSingle(title, *(ext.value for ext in QFilePicker.Extension.Image))

            def get() -> types.GeneratorType:
                return (ext.value for ext in QFilePicker.Extension.Image)

            BMP = 'BMP (*.bmp *.dib *.rle)'
            CUR = 'CUR (*.cur)'
            GIF = 'GIF (*.gif)'
            ICNS = 'ICNS (*.icns)'
            ICO = 'ICO (*.ico)'
            JPEG = 'JPEG (*.jpeg *.jpg)'
            PBM = 'PBM (*.pbm)'
            PGM = 'PGM (*.pgm)'
            PNG = 'PNG (*.png)'
            PPM = 'PPM (*.ppm)'
            SVG = 'SVG (*.svg *.svgz)'
            TGA = 'TGA (.tga)'
            TIFF = 'TIFF (*.tif *.tiff)'
            WBMP = 'WBMP (*.wbmp)'
            WEBP = 'WEBP (*.webp)'
            XBM = 'XBM (*.xbm)'
            XPM = 'XPM (*.xpm)'
            HEIC = 'HEIC (*.heic)'
            JPEGXR = 'JPEG XR (*.jxr *.wdp *.wmp)'
            DDS = 'Surface DirectDraw (*.dds)'

        class Audio(Enum):
            def ALL(title: str = '') -> str:
                return QFilePicker.Extension.combineSingle(title, *(ext.value for ext in QFilePicker.Extension.Audio))

            def get() -> types.GeneratorType:
                return (ext.value for ext in QFilePicker.Extension.Audio)

            """RIFF = 'RIFF (*.riff)'
            BWF = 'BWF (*.bwf)'
            CAF = 'CAF (*.caf)'
            AC3 = 'AC-3 (*.ac3)'
            VQF = 'VQF / TwinVQ (*.vqf *.vql *.vqe)'
            ASF = 'ASF (*.asf)'
            ATRAC = 'ATRAC (*.aa3 *.oma *.at3)'"""
            _3GP = '3GP (*.3gp)'
            AA = 'AA (*.aa)'
            AAC = 'AAC (*.aac)'
            AAX = 'AAX (*.aax)'
            ACT = 'ACT (*.act)'
            AIFF = 'AIFF (*.aiff)'
            ALAC = 'ALAC (*.alac)'
            AMR = 'AMR (*.amr)'
            APE = 'APE (*.ape)'
            AU = 'AU (*.au)'
            AWB = 'AWB (*.awb)'
            DSS = 'DSS (*.dss)'
            DVF = 'DVF (*.dvf)'
            FLAC = 'FLAC (*.flac)'
            GSM = 'GSM (*.gsm)'
            IKLAX = 'IKLAX (*.iklax)'
            IVS = 'IVS (*.ivs)'
            M4A = 'M4A (*.m4a)'
            M4B = 'M4B (*.m4b)'
            M4P = 'M4P (*.m4p)'
            MMF = 'MMF (*.mmf)'
            MP3 = 'MP3 (*.mp3)'
            MPC = 'MPC (*.mpc)'
            MSV = 'MSV (*.msv)'
            NMF = 'NMF (*.nmf)'
            OGG = 'OGG (*.ogg *.oga *.mogg)'
            OPUS = 'OPUS (*.opus)'
            RA = 'RA (*.ra *.rm)'
            RAW = 'RAW (*.raw)'
            RF64 = 'RF64 (*.rf64)'
            SLN = 'SLN (*.sln)'
            TTA = 'TTA (*.tta)'
            VOC = 'VOC (*.voc)'
            VOX = 'VOX (*.vox)'
            WAV = 'WAV (*.wav)'
            WMA = 'WMA (*.wma)'
            WV = 'WV (*.wv)'
            WEBM = 'WEBM (*.webm)'
            _8SVX = '8SVX (*.8svx)'
            CDA = 'CDA (*.cda)'

        class Video(Enum):
            def ALL(title: str = '') -> str:
                return QFilePicker.Extension.combineSingle(title, *(ext.value for ext in QFilePicker.Extension.Video))
            
            def get() -> types.GeneratorType:
                return (ext.value for ext in QFilePicker.Extension.Video)

            WEBM = 'WebM (*.webm)'
            MKV = 'Matroska (*.mkv)'
            FLV = 'Flash Video (*.flv *.f4v *.f4p *.f4a *.f4b)'
            VOB = 'Vob (*.vob)'
            OGG = 'Ogg Video (*.ogv *.ogg)'
            DRC = 'Dirac (*.drc)'
            GIF = 'GIF (*.gif)'
            GIFV = 'Video alternative to GIF (*.gifv)'
            MNG = 'Multiple-image Network Graphics (*.mng)'
            AVI = 'AVI (*.avi)'
            MPEG = 'MPEG Transport Stream (*.mts *.m2ts *.ts)'
            MOV = 'QuickTime File Format (*.mov *.qt)'
            WMV = 'Windows Media Video (*.wmv)'
            YUV = 'Raw video format (*.yuv)'
            RM = 'RealMedia (*.rm)'
            RMVB = 'RealMedia Variable Bitrate (*.rmvb)'
            VIV = 'VivoActive (*.viv)'
            ASF = 'Advanced Systems Format (*.asf)'
            AMV = 'AMV video format (*.amv)'
            MP4 = 'MPEG-4 Part 14 (*.mp4 *.m4p *.m4v)'
            MPEG1 = 'MPEG-1 (*.mpg *.mp2 *.mpeg *.mpe *.mpv)'
            MPEG2 = 'MPEG-2 – Video (*.mpg *.mpeg *.m2v)'
            M4V = 'M4V (*.m4v)'
            SVI = 'SVI (*.svi)'
            _3GP = '3GPP (*.3gp)'
            _3G2 = '3GPP2 (*.3g2)'
            MXF = 'Material Exchange Format (*.mxf)'
            ROQ = 'ROQ (*.roq)'
            NSV = 'Nullsoft Streaming Video (*.nsv)'



        def combine(*extensions: Image|Audio|Video) -> str:
            return ';;'.join(list(ext.value for ext in extensions))

        def combineSingle(title: str = '', *extensions: Image|Audio|Video) -> str:
            extStr = ''
            for ext in extensions:
                extStr += ext.value.split('(')[-1][:-1] + ' '
            extStr = extStr[:-1]

            return f'{title} ({extStr})'

        def combineAll(title: str = '', *extensions: Image|Audio|Video) -> str:
            if len(extensions) > 1:
                return QFilePicker.Extension.combineSingle(title, *extensions) + ';;' + QFilePicker.Extension.combine(*extensions)
            return QFilePicker.Extension.combineSingle(title, *extensions)

        def combineByCategory(category: Image|Audio|Video):
            return ';;'.join(list(ext.value for ext in category))

        def combineByCategoryAll(title: str = '', category: Image|Audio|Video = None) -> str:
            if not category: return ''
            return QFilePicker.Extension.combineSingle(title, *(ext for ext in category)) + ';;' + QFilePicker.Extension.combineByCategory(category)



    pathChanged = pyqtSignal(str, name = 'pathChanged')

    def __init__(self, filePickerData: dict = {}, type: Type = Type.OpenFileName, defaultPath = None, extensions: str = '', showFullPath = False):
        super().__init__()
        self.__layout__ = QGridLayout(self)
        self.__layout__.setSpacing(1)

        self.__layout__.setColumnStretch(1, 1)
        self.__layout__.setRowStretch(3, 1)

        self.__type__ = type
        self.__path__ = defaultPath
        self.__extensions__ = extensions
        self.__showFullPath__ = showFullPath

        self.__titleLabel__ = QLabel(filePickerData['title'])
        self.__titleLabel__.setProperty('class', 'small')

        self.__filePickerData__ = filePickerData
        self.__openButton__ = QPushButton(filePickerData['QPushButton']['selectFile'])
        self.__openButton__.clicked.connect(self.__buttonClicked__)

        self.__label__ = QLabel()
        self.__updateText__()
        self.__label__.setProperty('class', 'file')

        self.__layout__.addWidget(self.__titleLabel__, 0, 0)
        self.__layout__.addWidget(self.__openButton__, 1, 0)
        self.__layout__.addWidget(self.__label__, 2, 0)

    def getCurrentDir(self):
        if not self.__path__: return './'
        if os.path.isfile(self.__path__):
            return '/'.join(self.__path__.split('/')[:-1])
        elif os.path.isdir(self.__path__):
            return '/'.join(self.__path__.split('/')[:-2])
        return './'

    def __buttonClicked__(self):
        match self.__type__:
            case QFilePicker.Type.OpenFileName:
                path = QFileDialog.getOpenFileName(
                    parent = self,
                    directory = self.getCurrentDir(),
                    caption = self.__filePickerData__['QFileDialog']['title'],
                    filter = self.__extensions__
                )[0]
            case QFilePicker.Type.ExistingDirectory:
                path = QFileDialog.getExistingDirectory(
                    parent = self,
                    directory = self.getCurrentDir(),
                    caption = self.__filePickerData__['QFileDialog']['title']
                )

        if path == '': path = None

        if path:
            self.pathChanged.emit(path)
            self.__path__ = path
            self.__updateText__()

    def __updateText__(self):
        if self.__path__:
            if self.__showFullPath__:
                self.__label__.setText(f'{self.__path__}')
            else:
                path = self.__path__.split('/')[-1]
                if path == '': path = self.__path__.split('/')[-2] + '/'
                if self.__type__ == QFilePicker.Type.ExistingDirectory and self.__type__ == QFilePicker.Type.ExistingDirectoryUrl : path += + '/'
                self.__label__.setText(f'{path}')
        else:
            self.__label__.setText(self.__filePickerData__['QLabel']['noFile'])

    def setPath(self, path):
        self.__path__ = path
        self.__updateText__()

    def path(self):
        return self.__path__

    def get(self):
        return self.__path__
#----------------------------------------------------------------------

    # Set Up
'''def setup():
    files = ''
    for attr in QFilePicker.Extension.Image:
        if attr.value: files += attr.value.split('(')[-1][:-1] + ' '
    QFilePicker.Extension.Image.ALL = f'Supported Files ({files[:-1]})'

    files = ''
    for attr in QFilePicker.Extension.Audio:
        if attr.value: files += attr.value.split('(')[-1][:-1] + ' '
    QFilePicker.Extension.Audio.ALL = f'Supported Files ({files[:-1]})'

    files = ''
    for attr in QFilePicker.Extension.Video:
        if attr.value: files += attr.value.split('(')[-1][:-1] + ' '
    QFilePicker.Extension.Video.ALL = f'Supported Files ({files[:-1]})'

setup()
del setup'''
#----------------------------------------------------------------------
