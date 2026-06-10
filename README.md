# Eorld USDP SDK

USDP (Unified Space Description Protocol) v1.0 — 开源 3D 空间数据协议与开发者工具包。

## 概述

Eorld USDP SDK 提供统一的 3D 空间描述协议，任何 3D 重建工具只需实现一个 Provider，即可将空间数据转换为 USDP 格式，进入 Eorld 空间生态。

## 协议组成

| 模块 | 说明 |
|------|------|
| **USDP 协议** | 统一空间描述协议规范 (v1.0) |
| **P003 坐标归一化** | 多源坐标系统一转换 |
| **Provider 接口** | 空间源插件抽象接口 |
| **参考实现** | COLMAP/SfM 转换器 |

## 安装

```bash
pip install eorld-usdp
```

## 快速开始

```python
from usdp import SpaceDescription, CoordinateSystem
from usdp.provider import USDPProvider
from usdp.coordinate import normalize_coordinates

# 加载任意 3D 重建结果
space = SpaceDescription.from_provider(MyProvider, source_path="scan/")

# 归一化坐标系
space = normalize_coordinates(space, target=CoordinateSystem.USDP_STANDARD)

# 导出为 USDP 格式
space.export("output.usdp")
```

## 商标

Eorld 及其 Logo 是大效果科技有限公司在中华人民共和国及海外的注册商标/使用商标。

USDP 是大效果科技有限公司的未注册商标/服务标记，用于其统一空间描述协议产品和服务。

本项目包含的商标和商业外观未经明确书面许可不得以任何可能导致混淆的方式使用。


## 许可证

Copyright 2026 Eorld (大效果科技有限公司)

本项目基于 Apache License 2.0 开源，详见 [LICENSE](LICENSE) 文件。
