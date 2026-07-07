# oneLib 可构建源码包处理报告

## 产物

- 源码包：`output/onelib-buildable-source-20260702.tar.gz`
- 使用说明：`output/onelib-buildable-source-20260702-USAGE.md`
- 排除清单：`output/onelib-buildable-source-20260702-excludes.txt`
- 构建脚本：`output/build-local-images.sh`

## 本次处理点

- 增加 `scripts/build-local-images.sh`，对方无需拉取私有镜像，可本地构建：
  - `horacejett/onelib-backend:base.v8`
  - `horacejett/onelib-backend:v2.4.0-beta1-fix`
  - `horacejett/onelib-frontend:v2.4.0-beta1-fix`
- `src/backend/base.Dockerfile` 中 Pandoc 改为 Debian 源安装，避免构建期依赖 GitHub release 资产下载。
- `src/backend/vendor/wheels` 内置：
  - `onelib_pyautogen-0.3.2-py3-none-any.whl`
  - `onelib_ragas-1.0.3-py3-none-any.whl`
- 后端 `pyproject.toml` 使用本地 wheel 解析 `onelib-pyautogen`、`onelib-ragas`。
- DB2 驱动 `ibm-db`、`ibm-db-sa` 从默认依赖移到可选依赖组 `db2`，避免 ARM/Linux 构建时编译失败阻断整体镜像。
- `src/backend/vendor/nltk_data` 内置 NLTK 数据包，Docker 构建时本地解压并校验：
  - `punkt`
  - `punkt_tab`
  - `averaged_perceptron_tagger`
  - `averaged_perceptron_tagger_eng`
- 补齐 Playwright Chromium 运行库，避免基础镜像构建时出现浏览器依赖缺失警告。
- 压缩包排除 `.git`、`node_modules`、后端 `.venv`、前端 build 产物、Docker 数据卷和缓存目录。
- 修正排除规则：根目录 `output` 改为 `/output/`，避免误排 `src/backend/onelib/workflow/nodes/output/` 业务源码目录。
- 加固排除规则：`src/backend/.venv`、前端 `node_modules`/`build`、`brand-migration/.../dist`、`docker/.../data` 等根路径规则均改为 `/...` 锚定写法，避免误排同名业务目录。

## 已验证

- 从仓库源码运行 `./output/build-local-images.sh` 成功。
- 从 `output/onelib-buildable-source-20260702.tar.gz` 解压到 `/tmp` 后，运行包内 `./scripts/build-local-images.sh` 成功。
- 压缩包内关键构建文件、Dockerfile、本地 wheel、本地 NLTK 数据均存在。
- 压缩包内已验证存在 `src/backend/onelib/workflow/nodes/output/__init__.py`、`output.py`、`output_fake.py`。
- 已复查其他高风险同名路径：`src/backend/onelib/database/data` 和前端 `public/vditor/dist` 均正常进入压缩包；全量差异过滤后没有发现其他正常源码/资源遗漏。
- 压缩包内未发现 `.git`、`node_modules`、后端 `.venv`、前端 build 产物、Docker 数据卷目录。
- 镜像内验证 NLTK 资源可被 `nltk.data.find()` 找到。
- 镜像内验证 Playwright Chromium 可启动并渲染页面。

## 给同事的使用方式

```bash
tar -xzf onelib-buildable-source-20260702.tar.gz
cd oneLib-buildable-20260702
./scripts/build-local-images.sh
cd docker
docker compose -f docker-compose.yml -p onelib up -d
```

访问：

```text
http://localhost:3001
```

如果对方机器完全不能访问公共源，还需要额外提供 Docker 镜像离线包；当前源码包解决的是“私有镜像不可拉、本地可构建”的问题。
