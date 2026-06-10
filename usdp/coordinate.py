# Copyright 2026 Eorld (汉中记忆仓库网络科技有限公司)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
P003 Coordinate Normalization

USDP standard coordinate system definition:
  - Y-up, right-handed
  - Unit: meter
  - Origin: center of the scene bounding box bottom plane
  - X axis: longest dimension of the scene
  - Z axis: shortest dimension of the scene
"""

from typing import Callable
from .protocol import (
    SpaceDescription,
    SpaceElement,
    Point3D,
    CoordinateSystem,
)

TransformFunc = Callable[[Point3D], Point3D]


COORDINATE_TRANSFORMS: dict[CoordinateSystem, dict[str, float | TransformFunc | None]] = {
    CoordinateSystem.USDP_STANDARD: {
        "name": "USDP Standard",
        "description": "Y-up, meters, origin at bounding box bottom center",
    },
    CoordinateSystem.UNITY: {
        "name": "Unity",
        "description": "Y-up, meters, left-handed",
        "transform": lambda p: Point3D(p.x, p.y, -p.z),
    },
    CoordinateSystem.UNREAL: {
        "name": "Unreal Engine",
        "description": "Z-up, cm, left-handed",
        "transform": lambda p: Point3D(p.x * 100, p.z * 100, p.y * 100),
    },
    CoordinateSystem.COLMAP: {
        "name": "COLMAP/SfM",
        "description": "Y-down (image convention), arbitrary unit",
        "transform": lambda p: Point3D(p.x, -p.y, -p.z),
    },
    CoordinateSystem.ROOM_PLAN: {
        "name": "Apple RoomPlan",
        "description": "Y-up, meters, right-handed",
        "transform": None,
    },
    CoordinateSystem.OPENCV: {
        "name": "OpenCV",
        "description": "Y-down (image convention)",
        "transform": lambda p: Point3D(p.x, -p.y, p.z),
    },
}


class CoordinateTransform:
    """Transforms coordinates between different coordinate systems"""

    def __init__(self, from_system: CoordinateSystem, to_system: CoordinateSystem):
        self.from_system = from_system
        self.to_system = to_system

    def transform_point(self, point: Point3D) -> Point3D:
        """Transform a single point"""
        if self.from_system == self.to_system:
            return point
        func = COORDINATE_TRANSFORMS[self.from_system].get("transform")
        if func:
            return func(point)
        return point

    def transform_element(self, element: SpaceElement) -> SpaceElement:
        """Transform all vertices and position of a spatial element"""
        element.vertices = [self.transform_point(v) for v in element.vertices]
        element.position = self.transform_point(element.position)
        return element


def normalize_coordinates(
    space: SpaceDescription,
    target: CoordinateSystem = CoordinateSystem.USDP_STANDARD,
) -> SpaceDescription:
    """
    Normalize a SpaceDescription to the target coordinate system.

    Args:
        space: The space description to normalize.
        target: Target coordinate system (default: USDP_STANDARD).

    Returns:
        The normalized SpaceDescription (modified in place).
    """
    if space.coordinate_system == target:
        return space

    transform = CoordinateTransform(space.coordinate_system, target)
    for element in space.elements:
        transform.transform_element(element)

    space.coordinate_system = target
    return space
