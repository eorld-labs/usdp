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
USDP v1.0 协议定义 - Unified Space Description Protocol

USDP 是一种开放、可扩展的 3D 空间描述格式，
旨在统一不同 3D 重建源（LiDAR、SfM、NeRF、3DGS 等）的输出，
为 Eorld 空间生态提供标准化的数据交换层。
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import json


class ElementType(str, Enum):
    """空间元素类型"""
    WALL = "wall"
    FLOOR = "floor"
    CEILING = "ceiling"
    DOOR = "door"
    WINDOW = "window"
    FURNITURE = "furniture"
    CUSTOM = "custom"


class CoordinateSystem(str, Enum):
    """坐标系类型"""
    USDP_STANDARD = "usdp_standard"
    UNITY = "unity"
    UNREAL = "unreal"
    COLMAP = "colmap"
    ROOM_PLAN = "room_plan"
    OPENCV = "opencv"


@dataclass
class Point3D:
    """三维点"""
    x: float
    y: float
    z: float

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]


@dataclass
class Quaternion:
    """四元数旋转"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 1.0


@dataclass
class BoundingBox:
    """轴对齐包围盒"""
    min: Point3D = field(default_factory=lambda: Point3D(0, 0, 0))
    max: Point3D = field(default_factory=lambda: Point3D(0, 0, 0))


@dataclass
class SpatialMetadata:
    """空间元数据"""
    source: str = ""
    source_type: str = ""
    coordinate_system: CoordinateSystem = CoordinateSystem.USDP_STANDARD
    unit: str = "meter"
    capture_time: str = ""
    device_model: str = ""


@dataclass
class SpaceElement:
    """空间元素（墙/地板/家具等）"""
    id: str
    element_type: ElementType
    vertices: list[Point3D] = field(default_factory=list)
    position: Point3D = field(default_factory=lambda: Point3D(0, 0, 0))
    rotation: Quaternion = field(default_factory=Quaternion)
    scale: Point3D = field(default_factory=lambda: Point3D(1, 1, 1))
    mesh_data: Optional[bytes] = None
    texture_uri: Optional[str] = None
    properties: dict = field(default_factory=dict)


@dataclass
class SpaceDescription:
    """
    USDP 空间描述 - 顶层数据结构

    一个 SpaceDescription 代表一个完整的 3D 空间场景，
    包含所有元素、元数据和坐标系信息。
    """
    version: str = "1.0"
    metadata: SpatialMetadata = field(default_factory=SpatialMetadata)
    elements: list[SpaceElement] = field(default_factory=list)
    coordinate_system: CoordinateSystem = CoordinateSystem.USDP_STANDARD
    custom_properties: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """序列化为字典"""
        return {
            "version": self.version,
            "coordinate_system": self.coordinate_system.value,
            "metadata": {
                "source": self.metadata.source,
                "source_type": self.metadata.source_type,
                "coordinate_system": self.metadata.coordinate_system.value,
                "unit": self.metadata.unit,
                "capture_time": self.metadata.capture_time,
                "device_model": self.metadata.device_model,
            },
            "elements": [
                {
                    "id": e.id,
                    "type": e.element_type.value,
                    "vertices": [v.to_list() for v in e.vertices],
                    "position": e.position.to_list(),
                    "rotation": [e.rotation.x, e.rotation.y, e.rotation.z, e.rotation.w],
                    "scale": e.scale.to_list(),
                    "texture_uri": e.texture_uri,
                    "properties": e.properties,
                }
                for e in self.elements
            ],
            "custom_properties": self.custom_properties,
        }

    def to_json(self, indent: int = 2) -> str:
        """序列化为 JSON 字符串"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def export(self, filepath: str) -> None:
        """导出为 .usdp JSON 文件"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    @classmethod
    def from_dict(cls, data: dict) -> "SpaceDescription":
        """从字典反序列化"""
        elements = []
        for e in data.get("elements", []):
            elements.append(SpaceElement(
                id=e["id"],
                element_type=ElementType(e["type"]),
                vertices=[Point3D(*v) for v in e.get("vertices", [])],
                position=Point3D(*e.get("position", [0, 0, 0])),
                rotation=Quaternion(*e.get("rotation", [0, 0, 0, 1])),
                scale=Point3D(*e.get("scale", [1, 1, 1])),
                texture_uri=e.get("texture_uri"),
                properties=e.get("properties", {}),
            ))

        meta = data.get("metadata", {})
        return cls(
            version=data.get("version", "1.0"),
            metadata=SpatialMetadata(
                source=meta.get("source", ""),
                source_type=meta.get("source_type", ""),
                coordinate_system=CoordinateSystem(meta.get("coordinate_system", "usdp_standard")),
                unit=meta.get("unit", "meter"),
                capture_time=meta.get("capture_time", ""),
                device_model=meta.get("device_model", ""),
            ),
            elements=elements,
            coordinate_system=CoordinateSystem(data.get("coordinate_system", "usdp_standard")),
            custom_properties=data.get("custom_properties", {}),
        )

    @classmethod
    def from_provider(cls, provider_class, source_path: str, **kwargs) -> "SpaceDescription":
        """通用 Provider 加载入口"""
        from .provider import USDPProvider
        if issubclass(provider_class, USDPProvider):
            provider = provider_class()
            return provider.load(source_path, **kwargs)
        raise TypeError(f"{provider_class} 必须实现 USDPProvider 接口")
