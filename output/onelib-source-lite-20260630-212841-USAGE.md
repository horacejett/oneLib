# oneLib 轻量源码包使用说明

这个包是“源码传阅/协作开发用”的轻量包，不是完整离线运行包。

## 解压

```bash
mkdir oneLib-lite
tar -xzf onelib-source-lite-20260630-212841.tar.gz -C oneLib-lite
cd oneLib-lite
```

## 包里有什么

- 后端源码：`src/backend/onelib`、`src/backend/onelib_langchain`
- 前端源码：`src/frontend/platform/src`、`src/frontend/client/src`
- Docker Compose 和配置模板：`docker/`
- 品牌素材、迁移记录、README、当前未提交的源码改动

## 包里刻意没有什么

为了减小体积，已排除：

- Git 历史：`.git`
- Python 虚拟环境：`src/backend/.venv`
- 前端依赖：`node_modules`
- 前端构建产物：`build`
- 前端公共静态资源：`src/frontend/*/public`
- 前端本地包：`src/frontend/*/local-packages`
- Docker 数据卷：MySQL、Redis、Milvus、MinIO、ES 数据
- 后端模型 tokenizer 资源：`src/backend/onelib_langchain/linsight/resource`
- Pandoc 安装包：`src/backend/pandoc-3.10-x86_64-macOS.pkg`

完整排除项见 `onelib-source-lite-20260630-212841-excludes.txt`。

## 只看源码或合并代码

直接用编辑器打开 `oneLib-lite` 即可。

如果要放进 Git 仓库：

```bash
git init
git add .
git commit -m "import oneLib lightweight source"
```

## 想本地运行

这个轻量包不能直接完整运行，需要补齐被排除的公共组件。

### 后端

需要：

- Python 3.10+
- MySQL、Redis、Milvus、MinIO、Elasticsearch
- `src/backend/onelib/config.yaml`，可从 `docker/onelib/config/config.yaml` 复制后按本机环境改地址

安装依赖并启动：

```bash
cd src/backend
uv sync
config=/absolute/path/to/config.yaml .venv/bin/uvicorn onelib.main:app --host 0.0.0.0 --port 7860 --reload
```

### 前端

需要先补回：

- `src/frontend/platform/public`
- `src/frontend/client/public`
- `src/frontend/platform/local-packages/vditor-3.11.1.tgz`
- `src/frontend/client/local-packages/vditor-3.11.1.tgz`

然后安装依赖并启动：

```bash
cd src/frontend/platform
npm install
npm run start -- --host 0.0.0.0 --port 3002
```

`src/frontend/client` 同理。

## 想 Docker 运行

轻量包里保留了 `docker/docker-compose.yml` 和配置模板，但不包含数据库/对象存储/向量库数据。

```bash
cd docker
docker compose -f docker-compose.yml -p onelib up -d
```

注意：Compose 默认使用镜像启动后端/前端，不一定使用这个源码包里的源码。如果要基于源码重新构建镜像，需要另外补齐前端公共资源、本地包和后端运行依赖。
