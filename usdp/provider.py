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
USDP Provider Interface — Abstract plugin interface for spatial data sources.

Any 3D reconstruction tool or hardware device can implement the
USDPProvider interface to convert its output into USDP format
and connect to the Eorld spatial ecosystem.
"""

from abc import ABC, abstractmethod
from .protocol import SpaceDescription


class USDPProvider(ABC):
    """
    Abstract interface for spatial data source providers.

    Usage example:
        class MyScannerProvider(USDPProvider):
            name = "MyScanner"
            version = "1.0"
            source_type = "lidar"

            def load(self, source_path: str, **kwargs) -> SpaceDescription:
                ...
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name"""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Provider version string"""
        ...

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Data source type: lidar, sfm, nerf, roomplan, manual"""
        ...

    @abstractmethod
    def load(self, source_path: str, **kwargs) -> SpaceDescription:
        """
        Load and convert data to USDP format.

        Args:
            source_path: Path to the data source (directory or file).
            **kwargs: Provider-specific parameters.

        Returns:
            A SpaceDescription in USDP format.
        """
        ...

    def validate(self, space: SpaceDescription) -> bool:
        """Validate USDP output (may be overridden)"""
        if space.version != "1.0":
            return False
        for element in space.elements:
            if not element.id:
                return False
        return True
