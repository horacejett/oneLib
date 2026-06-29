# oneLib Python Wheel 发布说明

已生成可发布 wheel：

- `brand-migration/python-repackage/dist/onelib_pyautogen-0.3.2-py3-none-any.whl`
- `brand-migration/python-repackage/dist/onelib_ragas-1.0.3-py3-none-any.whl`

本地验证：

- `uv sync --frozen --no-dev` 已通过。
- `onelib-pyautogen==0.3.2` 与 `onelib-ragas==1.0.3` 可在后端虚拟环境中安装和导入。
- `onelib_ragas.metrics.AnswerCorrectnessOneLib`、`onelib_ragas.metrics.AnswerRecallOneLib` 和 `autogen.ConversableAgent` 导入通过。

发布到 PyPI：

```bash
UV_PUBLISH_TOKEN="pypi-..." uv publish brand-migration/python-repackage/dist/*.whl
```

发布到私有制品库：

```bash
UV_PUBLISH_URL="https://your-package-host/legacy/" \
UV_PUBLISH_TOKEN="..." \
uv publish brand-migration/python-repackage/dist/*.whl
```

发布后建议重新生成公开源锁文件：

```bash
cd src/backend
uv lock --upgrade-package onelib-pyautogen --upgrade-package onelib-ragas
uv sync --frozen --no-dev
```

当前仓库的 `uv.lock` 使用本地 wheelhouse，以保证在尚未完成远程发布前仍可复现安装。
