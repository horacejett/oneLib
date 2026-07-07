FROM python:3.10-slim

ARG PANDOC_ARCH=amd64
ENV PANDOC_ARCH=$PANDOC_ARCH
ENV PATH="${PATH}:/root/.local/bin"
ENV NLTK_DATA=/root/nltk_data

WORKDIR /app

# 安装依赖（合并指令、清理缓存、禁用推荐包）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc g++ curl build-essential libreoffice \
    wget procps vim fonts-wqy-zenhei \
    libglib2.0-0 libsm6 libxrender1 libxext6 libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 安装 FFmpeg
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*


# 安装 pandoc。使用 Debian 源，避免构建时依赖 GitHub release 下载。
RUN apt-get update && \
    apt-get install -y --no-install-recommends pandoc && \
    rm -rf /var/lib/apt/lists/*

# 安装 uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Poetry
#RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.2

# 拷贝项目依赖文件
COPY ./vendor/wheels ./vendor/wheels
COPY ./pyproject.toml ./

# 安装 Python 依赖
RUN python -m pip install --upgrade pip && \
    uv pip compile pyproject.toml --find-links vendor/wheels --output-file requirements.txt && \
    uv pip install -r requirements.txt --find-links vendor/wheels --system --no-cache-dir && \
    uv cache clean



#RUN python -m pip install --upgrade pip && \
#    pip install shapely==2.0.1 && \
#    poetry config virtualenvs.create false && \
#    poetry install --no-interaction --no-ansi --without dev

# 安装 NLTK 数据。使用随源码提供的 vendor 包，避免构建时依赖 raw.githubusercontent.com。
COPY ./vendor/nltk_data ./vendor/nltk_data
RUN python vendor/nltk_data/install.py

# 安装 Playwright Chromium 运行库。
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libatk1.0-0t64 libatk-bridge2.0-0t64 libatspi2.0-0t64 \
    libxcomposite1 libxdamage1 && \
    rm -rf /var/lib/apt/lists/*

# 安装 playwright chromium
RUN playwright install chromium

COPY . .

CMD ["sh", "entrypoint.sh"]
