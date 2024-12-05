import NemAll_Python_Geometry as Geometry
import NemAll_Python_BaseElements as BaseElements
import NemAll_Python_Reinforcement as Reinforcement
import NemAll_Python_Basis as Basis
import math
import sys





def check_allplan_version(build_ele: BuildingElement,
                          version: float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        build_ele: building element with the parameter properties
        version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True

Parameters:

build_ele (BuildingElement) #building element with the parameter properties
version (float) #current Allplan version
Returns:
bool – True if #current Allplan version is supported and PythonPart script can be run, False otherwise

def create_element(build_ele: BuildingElement,
                   doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Function for the element creation

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    return CreateElementResult()












