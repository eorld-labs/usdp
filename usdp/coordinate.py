# Copyright 2026 Eorld (大效果科技有限公司)
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
P003 坐标归一化 - Coordinate Normalization

USDP 标准坐标系定义：
  - Y-up 右手坐标系
  - 单位：米 (meter)
  - 原点：场景包围盒底面中心
  - X 轴：场景长边方向
  - Z 轴：场景短边方向
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
    """坐标系转换器"""
    
    def __init__(self, from_system: CoordinateSystem, to_system: CoordinateSystem):
        self.from_system = from_system
        self.to_system = to_system

    def transform_point(self, point: Point3D) -> Point3D:
        """转换单个点"""
        if self.from_system == self.to_system:
            return point
        func = COORDINATE_TRANSFORMS[self.from_system].get("transform")
        if func:
            return func(point)
        return point

    def transform_element(self, element: SpaceElement) -> SpaceElement:
        """转换空间元素的所有顶点和位置"""
        element.vertices = [self.transform_point(v) for v in element.vertices]
        element.position = self.transform_point(element.position)
        return element


def normalize_coordinates(
    space: SpaceDescription,
    target: CoordinateSystem = CoordinateSystem.USDP_STANDARD,
) -> SpaceDescription:
    """
    将 SpaceDescription 的坐标系归一化到目标坐标系

    Args:
        space: 待归一化的空间描述
        target: 目标坐标系，默认 USDP_STANDARD

    Returns:
        归一化后的 SpaceDescription（原地修改）
    """
    if space.coordinate_system == target:
        return space

    transform = CoordinateTransform(space.coordinate_system, target)
    for element in space.elements:
        transform.transform_element(element)

    space.coordinate_system = target
    return space
