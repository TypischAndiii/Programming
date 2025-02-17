""" Script for PolylineInput
"""

from __future__ import annotations

from typing import Any, List, TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PolylineInputBuildingElement import PolylineInputBuildingElement
else:
    PolylineInputBuildingElement = BuildingElement

print('Load PolylineInput.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\InteractorExamples\BaseInput\PolylineInput.png"))

def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : List[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : List[BuildingElementControlProperties],
                      _modify_uuid_list        : list) -> object:
    """ Create the interactor

    Args:
        coord_input:               API object for the coordinate input, element selection, ... in the Allplan view
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service
        build_ele_list:            list with the building elements
        build_ele_composite:       building element composite with the building element constraints
        control_props_list:        control properties list
        _modify_uuid_list:         list with the UUIDs of the modified elements

    Returns:
          Created interactor object
    """

    return PolylineInput(coord_input, build_ele_list, build_ele_composite, control_props_list)


class PolylineInput(BaseInteractor):
    """ Definition of class PolylineInput
    """

    def __init__(self,
                 coord_input        : AllplanIFW.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[BuildingElementControlProperties]):
        """ Create the interactor

        Args:
            coord_input:         API object for the coordinate input, element selection, ... in the Allplan view
            build_ele_list:      list with the building elements
            build_ele_composite: building element composite with the building element constraints
            control_props_list:  control properties list
        """

        self.coord_input = coord_input
        self.build_ele   = cast(PolylineInputBuildingElement, build_ele_list[0])

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list, self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)

        self.polyline_input = AllplanIFW.PolylineInput(coord_input, True)

    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: str):
        """ Modify property of element

        Args:
            page:  page index of the modified property
            name:  name of the modified property
            value: new value
        """

        if self.palette_service.modify_element_property(page, name, value):
            self.palette_service.update_palette(-1, False)

    def on_control_event(self,
                         event_id: int):
        """ Handles on control event

        Args:
            event_id: event id of the clicked button control
        """

    def on_cancel_function(self) -> bool:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False for success.
        """

        if self.polyline_input.GetPolyline().Count() > 1:
            self.create_element()
            self.polyline_input.StartNewInput()

            return False

        self.palette_service.close_palette()

        return True

    def on_preview_draw(self):
        """ Handles the preview draw event
        """

        self.draw_preview(self.polyline_input.GetPreviewPolyline())

    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.draw_preview(self.polyline_input.GetPreviewPolyline())

    def on_value_input_control_enter(self) -> bool:
        """ Handles the enter inside the value input control event

        Returns:
            True/False for success.
        """

        return True

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """ Process the mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        self.polyline_input.ExecuteInput(mouse_msg, pnt, msg_info)

        self.draw_preview(self.polyline_input.GetPreviewPolyline())

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        return True


    def draw_preview(self,
                     polyline: AllplanGeo.Polyline3D):
        """ draw the preview

        Args:
            polyline: polyline
        """

        polyline_ele = AllplanBasisEle.ModelElement3D(self.build_ele.CommonProp.value, polyline)

        AllplanBaseEle.DrawElementPreview(self.polyline_input.GetInputViewDocument(),
                                          AllplanGeo.Matrix3D(), [polyline_ele], True, None)


    def create_element(self):
        """ create the element
        """

        polyline_ele = AllplanBasisEle.ModelElement3D(self.build_ele.CommonProp.value, self.polyline_input.GetPolyline())

        AllplanBaseEle.CreateElements(self.polyline_input.GetInputViewDocument(),
                                      AllplanGeo.Matrix3D(), [polyline_ele], [], None)
        
















""" Script for Circle3D geometry example
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.Circle3DBuildingElement import Circle3DBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Circle3D.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\PaletteExamples\GeometryElements\Circle3D.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = Circle3D(doc)

    return element.create(build_ele)


class Circle3D():
    """ Definition of class Circle3D
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class Circle3D

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        model_ele_list.append_geometry_3d(build_ele.Circle1.value)
        model_ele_list.append_geometry_3d(build_ele.Circle2.value)
        model_ele_list.append_geometry_3d(build_ele.CircleList.value)
        model_ele_list.append_geometry_3d(build_ele.Circle3.value)
        model_ele_list.append_geometry_3d(build_ele.Circle4.value)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))




























""" Script for Line3D geometry example
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.Line3DBuildingElement import Line3DBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Line3D.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\PaletteExamples\GeometryElements\Line3D.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = Line3D(doc)

    return element.create(build_ele)


class Line3D():
    """ Definition of class Line3D
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class Line3D

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        model_ele_list.append_geometry_3d(build_ele.Line1.value)
        model_ele_list.append_geometry_3d(build_ele.Line2.value)
        model_ele_list.append_geometry_3d(build_ele.LineList.value)
        model_ele_list.append_geometry_3d(build_ele.Line3.value)
        model_ele_list.append_geometry_3d(build_ele.Line4.value)
        model_ele_list.append_geometry_3d(build_ele.Line5.value)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
  