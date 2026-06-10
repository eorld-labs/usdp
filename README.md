# Eorld USDP SDK

USDP (Unified Space Description Protocol) v1.0 — an open-source 3D spatial data protocol and developer toolkit.

## Overview

The Eorld USDP SDK provides a unified 3D spatial description protocol. Any 3D reconstruction tool can implement a single Provider to convert its output into USDP format and enter the Eorld spatial ecosystem.

## Components

| Module | Description |
|--------|-------------|
| **USDP Protocol** | Unified Space Description Protocol specification (v1.0) |
| **P003 Coordinate Normalization** | Multi-source coordinate system unification |
| **Provider Interface** | Abstract plugin interface for spatial data sources |
| **Reference Implementation** | COLMAP/SfM converter |

## Installation

```bash
pip install eorld-usdp
```

## Quick Start

```python
from usdp import SpaceDescription, CoordinateSystem
from usdp.provider import USDPProvider
from usdp.coordinate import normalize_coordinates

# Load any 3D reconstruction output
space = SpaceDescription.from_provider(MyProvider, source_path="scan/")

# Normalize to USDP standard coordinate system
space = normalize_coordinates(space, target=CoordinateSystem.USDP_STANDARD)

# Export to USDP format
space.export("output.usdp")
```

## Trademarks

"Eorld" in all its forms — including but not limited to **Eorld**, **EORLD**, **eorld**, and **E-WORLD** — whether used as a word mark, stylized logo, or trade name, are trademarks and/or service marks of Hanzhong Eorld Technology Co., Ltd. (汉中记忆仓库网络科技有限公司) in the People's Republic of China and internationally, and are protected under applicable trademark and unfair competition laws, including as common law marks in jurisdictions where federal registration has not yet been obtained.

USDP is a trademark/service mark of Hanzhong Eorld Technology Co., Ltd., used in connection with its Unified Space Description Protocol products and services.

Eorld has adopted, is using, and intends to continue using the Eorld mark and its variants (EORLD, eorld, E-WORLD) in interstate and international commerce in connection with computer software, SaaS/PaaS platforms, 3D spatial data protocols, and related goods and services. This public repository serves as documentary evidence of such use and of Eorld's claim of ownership over the full visual spectrum of its brand identifiers.

No trademark or trade dress contained in this project may be used in any manner likely to cause confusion, mistake, or deception, without prior express written permission from Hanzhong Eorld Technology Co., Ltd.

## License

Copyright 2026 Eorld (汉中记忆仓库网络科技有限公司)

This project is open-sourced under the Apache License 2.0. See [LICENSE](LICENSE) for details.
