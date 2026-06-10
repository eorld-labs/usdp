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
COLMAP/SfM Provider — Reference implementation.

Converts COLMAP sparse/dense reconstruction output to USDP format.
COLMAP uses world coordinates (Y-down, image convention); this
provider automatically converts to the USDP standard (Y-up).
"""

import os
from usdp import SpaceDescription, SpaceElement, ElementType, Point3D, Quaternion, CoordinateSystem, SpatialMetadata
from usdp.coordinate import normalize_coordinates
from usdp.provider import USDPProvider


class ColmapProvider(USDPProvider):
    name = "COLMAP SfM Provider"
    version = "0.1.0"
    source_type = "sfm"

    def load(self, source_path: str, **kwargs) -> SpaceDescription:
        space = SpaceDescription(
            metadata=SpatialMetadata(
                source=source_path,
                source_type=self.source_type,
                coordinate_system=CoordinateSystem.COLMAP,
            ),
            coordinate_system=CoordinateSystem.COLMAP,
        )

        points3d_path = os.path.join(source_path, "points3D.txt")
        if os.path.exists(points3d_path):
            points = self._parse_points3d(points3d_path)
            for i, pt in enumerate(points):
                space.elements.append(SpaceElement(
                    id=f"colmap_point_{i}",
                    element_type=ElementType.CUSTOM,
                    position=Point3D(pt[0], pt[1], pt[2]),
                    properties={"color": [int(c) for c in pt[3:]]},
                ))

        space = normalize_coordinates(space, target=CoordinateSystem.USDP_STANDARD)
        return space

    def _parse_points3d(self, filepath: str) -> list:
        points = []
        with open(filepath, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.strip().split()
                if len(parts) >= 7:
                    points.append([float(x) for x in parts[1:7]])
        return points
