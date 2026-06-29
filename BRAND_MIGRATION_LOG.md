# oneLib / 一知 品牌迁移台账

记录日期：2026-06-27

## 目标

把上游项目迁移为 oneLib / 一知 的独立商业发布版本，并尽量清除用户可见与工程可见的旧品牌痕迹。本文只记录迁移点，不保留旧品牌明文。

## 品牌基准

- 英文品牌：`oneLib`
- 中文品牌：`一知`
- 仓库地址：`https://github.com/horacejett/oneLib`
- 一句话介绍：`oneLib（一知）是面向企业知识库、智能体应用与生成式 AI 工作流的一体化平台。`
- 文档、官网、社区、API 文档临时统一入口：`https://github.com/horacejett/oneLib`

## 已执行改动

- 导入上游源码到当前仓库，并初始化本地 Git 仓库。
- 设置远端仓库为 `https://github.com/horacejett/oneLib.git`，当前未自动提交或推送。
- 将后端 Python 包路径迁移为 `src/backend/onelib` 与 `src/backend/onelib_langchain`。
- 将 Docker、Compose、配置目录、镜像命名和部署项目名迁移为 `onelib` 风格。
- 将平台前端品牌静态资源目录迁移为 `assets/onelib`。
- 将前端自有组件、UI、图标、样式类名、确认弹窗工具函数和 i18n namespace 迁移为 `onelib` 风格。
- 将平台前端 locale 文件统一为 `onelib.json`。
- 将 README、配置、脚本、CI、文档中的官网、文档、仓库、API 示例和社区链接统一指向 oneLib 仓库。
- 将品牌源文件统一重命名为 `onelib-*` 风格。
- 新增 `brand-migration/brand_migrate.py`，用于后续扫描、替换、路径迁移和验证。
- 新增 `brand-source/generated/`，集中输出 README banner、OpenGraph 图、PWA icon、favicon、登录页图和应用内 logo。
- 更新 `brand-source/tools/gen_assets.py`，使其从 `brand-source/onelib-mark-white.png` 生成当前 Web 项目实际使用的品牌素材。
- 覆盖平台登录页大图、深色登录图、小 logo、favicon、报表 logo、应用启动图。
- 覆盖客户端 PWA icon、maskable icon、apple touch icon 和 `logo.svg`。
- 重写英文、中文、日文 README，去掉继承典故、无效图片链接、空链接、旧社区入口和未确认宣传表述。
- 清理客户端聊天子系统中的继承品牌文案、链接、包元信息、条款占位、帮助入口和 locale key，统一迁移到 oneLib / onelib。
- 将客户端 HTML 描述、默认启动标题、PWA 注释、登录图标 fallback 文案统一为 oneLib。
- 将 Docker 日志标签从全大写展示改为 `oneLib`，保留 `ONELIB_*` 环境变量和工程枚举。
- 将平台 locale 中的继承功能展示名统一为“一知”与“一知洞察”。
- 修复平台本地研发环境图标上传预览：`/onelib` 与 `/tmp-dir` 文件服务代理默认指向本地 MinIO，图标上传组件兼容空值、完整 URL 与上传失败响应。
- 将两个外部 Python 依赖重打包为 `onelib-pyautogen` 与 `onelib-ragas` wheel，并把后端锁文件改为本地 oneLib wheelhouse。
- 删除源码树中的 Python 编译缓存文件 915 个，避免编译产物携带旧品牌字符串进入发布物。
- 清理客户端 MP4 素材元数据中的旧品牌路径片段，保持视频容器类型不变。
- 修复本地研发环境工作台入口：平台 dev server 将 `/workspace` 代理到客户端 dev server，平台菜单与预览 iframe 统一使用工作台 URL 工具函数，避免 `/workspace` 落入平台路由后显示 404。

## 验证记录

- 已执行品牌迁移脚本验证，已知旧品牌、旧中文名、旧组织、旧域名和旧仓库地址扫描通过。
- 已执行文件名扫描，未发现旧品牌文件名残留。
- 已抽查 README、登录页图、banner、favicon 和客户端图标尺寸。
- 已扫描客户端聊天子系统继承品牌关键字，公开文案与包元信息已清理。
- 后端 Python 3.10.20 编译检查通过。
- 后端依赖安装在本地 oneLib wheelhouse 下通过。
- 后端最终依赖安装与改名包 import smoke test 通过。
- 改名后的两个 oneLib wheel 解包扫描通过，后端虚拟环境中已安装依赖扫描通过。
- 平台前端和客户端前端生产构建已通过。
- 清理后源码树 `.pyc` 数量为 0。
- 清理后全库二进制/文本旧品牌扫描为 0 命中。
- 本地工作台链路复测通过：`http://127.0.0.1:3002/workspace/` 实际渲染后进入 `http://127.0.0.1:3002/workspace/c/new`，浏览器控制台无 404；`/workspace/api/v1/all` 返回 200，未登录状态下 `/workspace/api/v1/workstation/config` 返回 401 属于正常鉴权。
- 2026-06-29 修复平台侧 dashboard 工作台链路：补齐研发期 `/telemetry/dashboard` 内存接口，修复平台 dashboard 数据解包、默认选中副作用和侧栏 dashboard 路由空格。
- 2026-06-29 修复工作台配置空值崩溃：`assistantIcon`、`sidebarIcon`、`fileUpload`、`knowledgeBase`、`webSearch` 均改为缺省安全访问。
- 2026-06-29 修复工作台深点点击崩溃：个人知识库用户信息空数组不再读取 `[0]`，空会话不再渲染分享入口，分享接口缺少 `share_token` 时不再抛运行时异常。
- 2026-06-29 新增 Playwright 真实 UI 巡检脚本：`output/playwright/onelib_site_smoke.js` 与 `output/playwright/onelib_deep_clicks.js`。
- 2026-06-29 真实 Chromium 主路径巡检通过：36 项路由/点击，failure/pageError/failedRequest/badResponse 均为 0，证据见 `brand-migration/validation-evidence/80_ui_playwright_smoke_2026-06-29.log`。
- 2026-06-29 真实 Chromium 深点点击巡检通过：13 项弹层/创建页/工作台交互，failure 为 0，证据见 `brand-migration/validation-evidence/81_ui_playwright_deep_clicks_2026-06-29.log`。
- 2026-06-29 客户端前端 `npm run build` 通过，平台前端 `npm run build` 通过，后端 dashboard 路由文件 `py_compile` 通过。
- 2026-06-29 图标上传预览链路复测通过：真实上传返回的 `/onelib/icon/...` 签名地址经 `http://127.0.0.1:3002` 返回 200，PNG 文件头正确；MinIO 直连 `http://127.0.0.1:9100` 同样返回 200；平台前端 `npm run build` 通过。
- 2026-06-29 修复工作台配置保存无反馈：保存前校验失败时会弹出具体错误提示，并修正模型行、联网搜索与知识库区域的错误定位。

## 后续接力点

- 使用 PyPI token 或私有制品库 token 发布 `onelib-pyautogen` 与 `onelib-ragas`。
- 发布后重新生成 `src/backend/uv.lock`，切换到正式包源。
- 启动 Docker Compose，检查登录页、工作流页、知识库页、聊天页和报表导出中的品牌显示。
- 决定是否保留 `brand-migration/` 与 `BRAND_MIGRATION_LOG.md` 作为内部工程材料，正式发布包中可以移除。
- 若后续有官网、文档站、社区、镜像仓库和 API 域名，需要把当前统一指向 GitHub 的链接再替换为正式地址。
