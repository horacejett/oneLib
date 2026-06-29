# oneLib / 一知 真实验证报告

验证时间：2026-06-27

## 结论

前端、品牌扫描、构建产物扫描、Docker Compose 配置解析都通过；后端源码语法编译通过。此前后端依赖安装失败的两个 oneLib Python 发行包已重打包为本地 wheel，并通过后端完整依赖安装与 import smoke test。源码树缓存与视频素材元数据中的旧品牌痕迹已清理，最终二进制级全库扫描为 0 命中。公开 PyPI/私有制品库上传仍需要发布凭据。

完整日志在 `brand-migration/validation-evidence/`，并已生成 `99_evidence_manifest.log` 记录每个证据日志的 SHA-256。

## 通过项

- 环境记录已落盘：`00_environment.log`
- 品牌迁移脚本验证通过：`01_brand_migrate_verify.log`
- 旧品牌/继承品牌文本扫描无命中：`02_legacy_text_scan.log`
- 旧品牌/继承品牌文件名扫描无命中：`03_legacy_filename_scan.log`
- 修改过的 JSON、locale、package 文件解析通过：`04_modified_json_parse.log`
- 平台前端 `npm ci` 成功：`10_platform_npm_ci.log`
- 平台前端 `npm run build` 成功：`11_platform_npm_build.log`
- 平台前端构建产物旧品牌扫描无命中：`12_platform_build_output_scan.log`
- 平台前端构建产物包含 oneLib 品牌素材：`13_platform_build_brand_assets.log`
- 客户端前端 `npm ci` 成功：`20_client_npm_ci.log`
- 客户端前端 `npm run build` 成功：`21_client_npm_build.log`
- 客户端构建产物旧品牌扫描无命中：`22_client_build_output_scan.log`
- 客户端构建产物包含 oneLib 品牌素材：`23_client_build_brand_assets.log`
- 后端源码在 Python 3.10.20 下 `compileall` 通过：`30_backend_compileall_uv_py310.log`
- 已生成 `onelib-pyautogen==0.3.2` 与 `onelib-ragas==1.0.3` wheel：`brand-migration/python-repackage/dist/`
- 后端 `uv lock --find-links` 已改用本地 oneLib wheelhouse：`brand-migration/python-repackage/logs/03_uv_lock_find_links.log`
- 后端 `uv sync --frozen --no-dev` 已通过：`brand-migration/python-repackage/logs/05_backend_uv_sync_after_repackage.log`
- 后端 oneLib wheel 重装与 import smoke test 已通过：`brand-migration/python-repackage/logs/09_reinstall_and_import_clean_wheels.log`
- 后端最终 `uv sync --frozen --no-dev` 已通过：`brand-migration/python-repackage/logs/10_backend_uv_sync_final.log`
- 后端最终 import smoke test 已通过：`brand-migration/python-repackage/logs/11_backend_import_smoke_final.log`
- 两个 oneLib wheel 解包后的旧品牌扫描 0 命中：`brand-migration/python-repackage/logs/12_unpacked_wheel_legacy_scan.log`
- 后端虚拟环境中已安装的 oneLib 依赖旧品牌扫描 0 命中：`brand-migration/python-repackage/logs/13_installed_dependency_legacy_scan.log`
- 品牌图片尺寸抽查通过：`40_asset_dimensions.log`
- 4 个 Docker Compose 文件均可被 `docker compose config` 解析：`50_docker_compose_config.log`
- 构建后的 HTML 与品牌配置指向 oneLib / 一知：`60_build_html_brand_strings.log`
- 已删除源码树编译缓存 915 个：`71_removed_source_pyc_files.log`
- 已清理客户端 MP4 素材元数据中的旧品牌路径片段：`72_mp4_metadata_scrub.log`
- 清理后全库旧品牌二进制/文本扫描 0 命中：`73_full_legacy_scan_after_binary_cleanup.log`
- 最终清洁度复查通过，源码树 `.pyc` 数量为 0，旧品牌命中为 0：`74_final_cleanliness_scan.log`
- 2026-06-29 已执行真实 Chromium UI 主路径巡检，36 项路由/点击全部通过，failure/pageError/failedRequest/badResponse 均为 0：`80_ui_playwright_smoke_2026-06-29.log`
- 2026-06-29 已执行真实 Chromium UI 深点点击巡检，13 项弹层/创建页/工作台交互全部通过，failure 为 0：`81_ui_playwright_deep_clicks_2026-06-29.log`
- 2026-06-29 客户端前端 `npm run build` 通过；平台前端 `npm run build` 通过；后端 `onelib/telemetry_search/api/router.py` 语法编译通过。

## 发布待办

- 本机没有 `UV_PUBLISH_TOKEN` / `TWINE_*` / PyPI 相关发布凭据，因此未执行真实远程上传。
- 已执行 `uv publish --dry-run brand-migration/python-repackage/dist/*.whl`，见 `brand-migration/python-repackage/logs/07_uv_publish_dry_run.log`。
- 发布命令与私有制品库命令见 `brand-migration/python-repackage/PUBLISH.md`。
- 当前 `uv.lock` 指向本地 wheelhouse，以便远程发布前仍可复现安装。
- 远程发布完成后，应重新执行 `uv lock --upgrade-package onelib-pyautogen --upgrade-package onelib-ragas`，将锁文件切回正式包源。

## 风险说明

- 平台前端依赖安装成功，但 `npm audit` 报出 34 个漏洞，其中 19 个 high。
- 客户端依赖安装成功，但 `npm audit` 报出 52 个漏洞，其中 1 个 critical、22 个 high。
- 客户端构建通过，但 Vite/PWA 输出了若干既有警告，包括部分大 chunk、旧 Browserslist 数据、缺失 favicon glob、运行时字体路径保留等。
- 真实 UI 巡检仍记录到若干非阻断 React/构建警告，包括 DOM prop、key、validateDOMNesting、workspace 字体解码和 React Router future flag；这些不再导致 404 或运行时白屏。
- 后端依赖安装已通过，但依赖本地 wheelhouse；如果发布包不包含 `brand-migration/python-repackage/dist/` 且远程包源尚未发布，后端安装会再次失败。

## 下一步必须处理

- 使用 PyPI token 或私有制品库 token 发布 `onelib-pyautogen` 与 `onelib-ragas`。
- 发布后重新生成 `uv.lock`，并再跑 `uv sync --frozen --no-dev`。

当前可以宣称“前端构建通过，后端语法编译通过，后端依赖安装在本地 oneLib wheelhouse 下通过，源码树与已扫描发布文件无已知旧品牌命中”。不能宣称“oneLib Python 包已发布到公开 PyPI”，因为当前缺少发布凭据。
