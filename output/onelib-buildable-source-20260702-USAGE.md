# oneLib 可构建源码包说明

这个包用于解决私有镜像无法拉取的问题。包内包含前端构建必需的 `public`、`local-packages`，以及后端运行中需要的 tokenizer 资源和构建脚本。

## 解压

```bash
tar -xzf onelib-buildable-source-20260702.tar.gz
cd oneLib-buildable-20260702
```

## 包内包含

- 后端源码与 Dockerfile：`src/backend`
- 后端基础镜像 Dockerfile：`src/backend/base.Dockerfile`
- 前端源码与 Dockerfile：`src/frontend`
- 前端构建必需资源：`src/frontend/*/public`、`src/frontend/*/local-packages`
- 后端 tokenizer 资源：`src/backend/onelib_langchain/linsight/resource`
- 后端本地 wheel：`src/backend/vendor/wheels`，用于解析 `onelib-pyautogen`、`onelib-ragas`
- 后端 NLTK 数据包：`src/backend/vendor/nltk_data`，用于离线安装 `punkt`、`punkt_tab` 和词性标注资源
- Docker Compose 配置：`docker/docker-compose.yml`
- 本地构建脚本：`scripts/build-local-images.sh`

## 包内不包含

为控制体积，仍然没有包含：

- `.git`
- `node_modules`
- `src/backend/.venv`
- 前端 `build` 产物
- Docker 数据卷：MySQL、Redis、Milvus、MinIO、ES 数据
- Python/Node 缓存

## 有网络环境：本地构建镜像

先确认机器安装了 Docker / Docker Compose，然后运行：

```bash
./scripts/build-local-images.sh
```

后端基础镜像中的 Pandoc 已改为从 Debian 源安装，不再依赖 GitHub release 资产下载。`onelib-pyautogen`、`onelib-ragas` 已随源码包提供本地 wheel，构建时会通过 `vendor/wheels` 解析。NLTK 数据已随源码包提供，构建时不会再访问 `raw.githubusercontent.com` 下载 `punkt` 等资源，并会在镜像构建阶段强制校验资源是否存在。Playwright Chromium 运行库也已补齐，构建时不应再出现浏览器依赖缺失警告。

DB2 驱动 `ibm-db`、`ibm-db-sa` 已从默认依赖移到可选依赖组，避免在 ARM/Linux 构建时因 DB2 驱动编译失败阻断整体镜像。确实需要 DB2 SQL Agent 时，在后端环境里额外安装：

```bash
uv pip install ".[db2]"
```

脚本会依次构建：

1. `horacejett/onelib-backend:base.v8`
2. `horacejett/onelib-backend:v2.4.0-beta1-fix`
3. `horacejett/onelib-frontend:v2.4.0-beta1-fix`

构建完成后启动：

```bash
cd docker
docker compose -f docker-compose.yml -p onelib up -d
```

浏览器访问：

```text
http://localhost:3001
```

## 架构说明

一般直接运行即可：

```bash
./scripts/build-local-images.sh
```

如果要在 ARM 机器上构建 amd64 镜像：

```bash
PLATFORM=linux/amd64 ./scripts/build-local-images.sh
```

`PANDOC_ARCH` 参数仍保留在脚本里兼容旧构建逻辑，但当前 Dockerfile 已不再需要手动指定它。

## 无网络环境

这个包仍然需要从公共源下载基础镜像和依赖，例如 `python:3.10-slim`、`node`、`nginx`、Python 包、npm 包等。

如果对方机器完全不能联网，需要另外提供 Docker 镜像离线包，例如：

```bash
docker save horacejett/onelib-backend:base.v8 \
  horacejett/onelib-backend:v2.4.0-beta1-fix \
  horacejett/onelib-frontend:v2.4.0-beta1-fix \
  -o onelib-private-images.tar
```

对方加载：

```bash
docker load -i onelib-private-images.tar
cd docker
docker compose -f docker-compose.yml -p onelib up -d
```
