#----------------------------------------------------------------------

    # Libraries
from ..QtUtils import QColorSet, QUtilsColor
import os
#----------------------------------------------------------------------

    # Class
class Info:
    def __new__(cls) -> None:
        return None

    build: str = '07e83f83'
    version: str = 'Experimental'

    application_name: str = 'PERT Maker'

    save_path: str = os.path.abspath('./data/save.dat').replace('\\', '/')

    main_color_set: QColorSet = QColorSet(
        'magenta',
        QUtilsColor.from_hex('#E614DC'),
        QUtilsColor.from_hex('#D00DC9'),
        QUtilsColor.from_hex('#FC1BF1'),
        QUtilsColor.from_hex('#A53CA1'),
    )
    neutral_color_set: QColorSet = QColorSet(
        'white',
        QUtilsColor.from_hex('#E3E3E3'),
        QUtilsColor.from_hex('#D7D7D7'),
        QUtilsColor.from_hex('#EFEFEF'),
        QUtilsColor.from_hex('#CACACA'),
    )

    icon_path: str = './data/icons/PERTMaker.svg'
#----------------------------------------------------------------------
