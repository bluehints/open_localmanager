# Open LocalManager

一款基于Python+PySide6技术栈的本地文件管理器应用，采用类似PC微信的三段式极简布局，提供强大的文件管理功能和清晰的层级关系展示。

## 项目概述

Open LocalManager 是一款功能强大的本地文件管理器，旨在提供更高效、更直观的文件管理体验。项目借鉴了XYplorer等优秀文件管理器的功能特点，并针对工程资料管理进行了优化。

### 核心特性

- **三段式布局**：左侧结构树侧边栏、中间文件管理区、右侧文件预览区
- **强大的结构树**：清晰的层级关系展示，支持"+-"符号展开/收起
- **完整的文件操作**：支持创建、删除、重命名、复制、移动等操作
- **实时预览**：支持文本、图片等多种文件格式的预览
- **跨平台支持**：支持Windows、macOS、Linux系统

## 技术栈

- **主框架**：Python 3.8+
- **GUI框架**：PySide6
- **文件操作**：os、shutil、pathlib
- **图片处理**：Pillow
- **测试框架**：pytest、pytest-qt
- **代码质量**：black、flake8、mypy

## 项目结构

```
open_localmanager/
├── docs/                    # 文档目录
│   ├── 01_需求分析.md
│   ├── 02_系统架构设计.md
│   ├── 03_模块设计.md
│   ├── 04_API接口说明.md
│   ├── 05_开发环境配置.md
│   └── 06_测试计划.md
├── src/                     # 源代码目录
│   ├── main.py             # 主程序入口
│   ├── controllers/        # 控制器
│   ├── models/             # 数据模型
│   ├── services/           # 业务服务
│   ├── widgets/            # UI组件
│   └── utils/              # 工具函数
├── tests/                   # 测试目录
│   ├── test_controllers/
│   ├── test_models/
│   ├── test_services/
│   └── test_widgets/
├── resources/               # 资源目录
│   ├── icons/              # 图标
│   ├── images/             # 图片
│   └── styles/             # 样式
├── config/                  # 配置目录
│   ├── default_config.json # 默认配置
│   └── config.py           # 配置模块
├── requirements.txt         # 依赖列表
├── README.md               # 项目说明
└── .gitignore             # Git忽略文件
```

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器
- 虚拟环境（推荐）

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/yourusername/open_localmanager.git
   cd open_localmanager
   ```

2. **创建虚拟环境**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   python src/main.py
   ```

### 开发环境配置

详细的开发环境配置请参考 [开发环境配置文档](docs/05_开发环境配置.md)。

## 功能说明

### 结构树侧边栏

- 使用"+-"符号实现节点的展开与收起
- 支持设置项目主文件路径
- 自动按层级关系加载文件和文件夹
- 提供右键菜单，支持完整的文件编辑功能
- 清晰的层级关系展示

### 文件管理区

- 显示当前文件夹的所有文件
- 支持文件的各种操作（复制、移动、删除、重命名等）
- 文件操作后自动同步更新结构树
- 支持文件排序和过滤

### 文件预览区

- 实时显示文件预览内容
- 支持常见文件格式（文本、图片等）
- 提供预览内容的缩放功能
- 显示文件基本信息

## 文档

项目包含完整的技术文档，位于 `docs/` 目录：

- [需求分析文档](docs/01_需求分析.md) - 详细的需求分析和功能规格
- [系统架构设计文档](docs/02_系统架构设计.md) - 系统架构和设计模式
- [模块设计文档](docs/03_模块设计.md) - 各模块的详细设计
- [API接口说明文档](docs/04_API接口说明.md) - API接口的详细说明
- [开发环境配置文档](docs/05_开发环境配置.md) - 开发环境配置指南
- [测试计划文档](docs/06_测试计划.md) - 测试策略和测试用例

## 开发指南

### 代码规范

项目遵循以下代码规范：

- **PEP 8**：Python代码风格指南
- **Black**：代码格式化工具
- **Flake8**：代码检查工具
- **MyPy**：类型检查工具

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_file_service.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 代码格式化

```bash
# 格式化代码
black src/

# 检查代码风格
flake8 src/

# 类型检查
mypy src/
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 提交规范

提交信息应遵循以下格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- `feat`：新功能
- `fix`：修复bug
- `docs`：文档更新
- `style`：代码格式调整
- `refactor`：重构
- `test`：测试相关
- `chore`：构建/工具相关

## 版本历史

### v1.0.0 (开发中)

- 初始版本发布
- 实现基本的三段式布局
- 实现结构树侧边栏功能
- 实现文件管理区功能
- 实现文件预览功能
- 实现基本的文件操作

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目主页：https://github.com/yourusername/open_localmanager
- 问题反馈：https://github.com/yourusername/open_localmanager/issues
- 邮箱：your.email@example.com

## 致谢

感谢以下开源项目：

- [PySide6](https://wiki.qt.io/Qt_for_Python) - Qt for Python
- [XYplorer](https://www.xyplorer.com/) - 功能强大的文件管理器（参考）

## 常见问题

### Q: 如何更改项目主文件路径？

A: 在应用菜单中选择"设置" -> "项目路径"，然后选择新的项目路径。

### Q: 支持哪些文件格式的预览？

A: 目前支持文本文件（txt、md、csv、json、xml、html、css、js、py、java、c、cpp等）和图片文件（jpg、jpeg、png、gif、bmp、svg、webp等）。

### Q: 如何自定义主题？

A: 在 `resources/styles/` 目录下创建新的主题文件，然后在应用设置中选择该主题。

### Q: 应用崩溃了怎么办？

A: 请查看日志文件（位于用户目录下的 `.localmanager/logs/` 目录），然后提交问题报告。

## 更新日志

### [1.0.0] - 2026-01-29

#### 新增
- 初始版本发布
- 三段式布局实现
- 结构树侧边栏功能
- 文件管理区功能
- 文件预览功能
- 基本文件操作功能

## 路线图

### v1.1.0 (计划中)
- 添加文件搜索功能
- 支持多标签浏览
- 添加文件颜色标记
- 支持快捷键自定义

### v1.2.0 (计划中)
- 添加文件比较功能
- 支持文件同步
- 添加压缩/解压功能
- 支持云存储集成

### v2.0.0 (计划中)
- 支持插件系统
- 添加多语言支持
- 优化性能和内存占用
- 支持更多文件格式预览