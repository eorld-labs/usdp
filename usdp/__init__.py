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
Eorld USDP SDK — Unified Space Description Protocol v1.0
"""

__version__ = "1.0.0"
__author__ = "Eorld"

from .protocol import (
    SpaceDescription,
    SpaceElement,
    ElementType,
    CoordinateSystem,
    SpatialMetadata,
    Point3D,
    Quaternion,
    BoundingBox,
)
from .coordinate import normalize_coordinates, CoordinateTransform

__all__ = [
    "SpaceDescription",
    "SpaceElement",
    "ElementType",
    "CoordinateSystem",
    "SpatialMetadata",
    "Point3D",
    "Quaternion",
    "BoundingBox",
    "normalize_coordinates",
    "CoordinateTransform",
]
