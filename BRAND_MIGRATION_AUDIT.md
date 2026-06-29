# oneLib / 一知 品牌迁移报告

生成时间：2026-06-27

## 当前状态

已从上游原项目导入源码，并完成第一轮深度品牌迁移。当前仓库的用户界面文案、README、Docker/Compose、CI、Python 包路径、前端静态资源路径、链接和素材命名已统一到 oneLib / 一知。

详细改动台账见 `BRAND_MIGRATION_LOG.md`，真实验证报告见 `BRAND_VALIDATION_REPORT.md`。

## 品牌信息

- 英文品牌：`oneLib`
- 中文品牌：`一知`
- 仓库地址：`https://github.com/horacejett/oneLib`
- 一句话介绍：`oneLib（一知）是面向企业知识库、智能体应用与生成式 AI 工作流的一体化平台。`
- 官网、文档、API 文档链接：暂时统一指向 `https://github.com/horacejett/oneLib`

## 已完成

- 导入上游源码，保留本地 `brand-source/` 品牌素材目录。
- 将品牌源文件重命名为 `onelib-*` 风格。
- 将品牌资源生成脚本改为 `oneLib` / `onelib` 命名。
- 新增 `brand-migration/brand_migrate.py`，支持扫描、文本替换、路径重命名和验证。
- 执行自动文本替换：681 个文件。
- 补充链接、镜像仓库、锁文件、前端配置等规则后，追加替换 18 个文件。
- 执行路径重命名：13 个路径。
- 将前端自有 `bs-*` 技术前缀迁移为 `onelib-*`，包括组件目录、UI 目录、图标目录、样式类名和确认弹窗工具函数。
- 将平台前端 i18n namespace 从旧缩写迁移为 `onelib`，并重命名 locale 文件。
- 清理旧官网、旧文档、旧 registry、旧示例 API 域名；文档类链接暂时指向 `https://github.com/horacejett/oneLib`。
- 重写英文、中文、日文 README，改为 oneLib / 一知 自有产品叙事。
- 生成 `brand-source/generated/` 品牌展示图，并将 README banner 指向本地品牌图。
- 覆盖平台登录页大图、深色登录图、小 logo、favicon、报表 logo、应用启动图。
- 覆盖客户端 PWA icon、maskable icon、apple touch icon 和 `logo.svg`。
- 清理客户端聊天子系统中的继承品牌文案、链接、包元信息、条款占位、帮助入口和 locale key。
- 将 Docker 日志标签统一为 `oneLib`，保留 `ONELIB_*` 环境变量和工程枚举。
- 将平台 locale 中的继承功能展示名统一为“一知”与“一知洞察”。
- 新增 `BRAND_MIGRATION_LOG.md`，记录迁移范围和后续接力点。
- 验证发布相关源码中不再存在已知旧品牌、旧中文名、旧组织、旧域名、自有旧缩写明文 token。
- 删除源码树 Python 编译缓存 915 个，并清理客户端 MP4 素材元数据旧路径片段。
- 生成本地 oneLib Python wheelhouse，解决改名后外部依赖在包源中不存在的问题。
- 初始化本地 Git 仓库，绑定远端 `https://github.com/horacejett/oneLib.git`，未自动提交或推送。

## 验证结果

- 品牌扫描：通过。
- 文件名扫描：通过。
- 后端 import 残留扫描：通过。
- 三语 README 残留扫描：通过。
- 核心品牌图片尺寸抽查：通过。
- 客户端聊天子系统继承品牌扫描：通过。
- 平台前端依赖安装：通过，见 `brand-migration/validation-evidence/10_platform_npm_ci.log`。
- 平台前端生产构建：通过，见 `brand-migration/validation-evidence/11_platform_npm_build.log`。
- 客户端前端依赖安装：通过，见 `brand-migration/validation-evidence/20_client_npm_ci.log`。
- 客户端前端生产构建：通过，见 `brand-migration/validation-evidence/21_client_npm_build.log`。
- 前端构建产物旧品牌扫描：通过，见 `brand-migration/validation-evidence/12_platform_build_output_scan.log` 与 `brand-migration/validation-evidence/22_client_build_output_scan.log`。
- Docker Compose 配置解析：通过，见 `brand-migration/validation-evidence/50_docker_compose_config.log`。
- Python 编译检查：通过。已使用 `uv` 下载并运行 CPython 3.10.20，见 `brand-migration/validation-evidence/30_backend_compileall_uv_py310.log`。
- 后端依赖安装：已通过本地 oneLib wheelhouse 解决。`onelib-pyautogen==0.3.2` 与 `onelib-ragas==1.0.3` 已重打包到 `brand-migration/python-repackage/dist/`，并通过 `uv sync --frozen --no-dev` 与 import smoke test。
- oneLib 依赖包扫描：通过。两个 wheel 解包后 0 命中，后端虚拟环境中已安装依赖 0 命中，见 `brand-migration/python-repackage/logs/12_unpacked_wheel_legacy_scan.log` 与 `brand-migration/python-repackage/logs/13_installed_dependency_legacy_scan.log`。
- 源码树缓存清理：通过。源码树 `.pyc` 数量为 0，见 `brand-migration/validation-evidence/74_final_cleanliness_scan.log`。
- 全库二进制/文本旧品牌扫描：通过。排除 `.git`、`node_modules`、虚拟环境、构建产物、大词表和压缩 JS 后为 0 命中，见 `brand-migration/validation-evidence/73_full_legacy_scan_after_binary_cleanup.log`。

## 后续建议

- 使用 PyPI token 或私有制品库 token 发布 `onelib-pyautogen` 与 `onelib-ragas`，发布说明见 `brand-migration/python-repackage/PUBLISH.md`。
- 发布后重新生成 `src/backend/uv.lock`，将当前本地 wheelhouse 锁定切换到正式包源。
- 处理前端依赖审计中的 high/critical 漏洞。
- 再跑后端服务启动和 Docker Compose 启动验证。
- 发布前决定是否移除 `brand-migration/` 目录。
