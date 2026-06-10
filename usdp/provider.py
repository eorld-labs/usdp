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
USDP Provider 接口 - 空间源插件抽象接口

任何 3D 重建工具或硬件只需实现 USDPProvider 接口，
即可将其输出转换为 USDP 格式，接入 Eorld 空间生态。
"""

from abc import ABC, abstractmethod
from .protocol import SpaceDescription


class USDPProvider(ABC):
    """
    空间源 Provider 抽象接口

    实现示例：
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
        """Provider 名称"""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Provider 版本"""
        ...

    @property
    @abstractmethod
    def source_type(self) -> str:
        """数据源类型：lidar, sfm, nerf, roomplan, manual"""
        ...

    @abstractmethod
    def load(self, source_path: str, **kwargs) -> SpaceDescription:
        """
        加载并转换为 USDP 格式

        Args:
            source_path: 数据源路径（目录或文件）
            **kwargs: Provider 特定参数

        Returns:
            SpaceDescription: USDP 格式的空间描述
        """
        ...

    def validate(self, space: SpaceDescription) -> bool:
        """校验 USDP 输出是否合法（可重写）"""
        if space.version != "1.0":
            return False
        for element in space.elements:
            if not element.id:
                return False
        return True
