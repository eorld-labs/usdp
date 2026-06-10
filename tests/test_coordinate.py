"""Coordinate normalization tests"""

import pytest
from usdp import (
    SpaceDescription,
    SpaceElement,
    ElementType,
    Point3D,
    CoordinateSystem,
    normalize_coordinates,
)


def test_normalize_identity():
    space = SpaceDescription(coordinate_system=CoordinateSystem.USDP_STANDARD)
    result = normalize_coordinates(space, target=CoordinateSystem.USDP_STANDARD)
    assert result.coordinate_system == CoordinateSystem.USDP_STANDARD


def test_normalize_colmap_to_standard():
    space = SpaceDescription(coordinate_system=CoordinateSystem.COLMAP)
    elem = SpaceElement(
        id="test_wall",
        element_type=ElementType.WALL,
        vertices=[Point3D(1, 2, 3)],
    )
    space.elements.append(elem)

    result = normalize_coordinates(space, target=CoordinateSystem.USDP_STANDARD)
    assert result.coordinate_system == CoordinateSystem.USDP_STANDARD
    v = result.elements[0].vertices[0]
    assert v.x == 1
    assert v.y == -2
    assert v.z == -3
