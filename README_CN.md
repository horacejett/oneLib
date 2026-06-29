![oneLib banner](brand-source/generated/onelib-banner.png)

# oneLib / 一知

oneLib（一知）是面向企业知识库、智能体应用与生成式 AI 工作流的一体化平台。

<p align="center">
  <a href="https://github.com/horacejett/oneLib"><img src="https://img.shields.io/badge/docs-GitHub-brightgreen" alt="docs"></a>
  <a href="https://github.com/horacejett/oneLib"><img src="https://img.shields.io/github/license/horacejett/oneLib" alt="license"></a>
  <a href="https://github.com/horacejett/oneLib"><img src="https://img.shields.io/github/last-commit/horacejett/oneLib" alt="last commit"></a>
  <a href="https://github.com/horacejett/oneLib"><img src="https://img.shields.io/github/stars/horacejett/oneLib?color=yellow" alt="stars"></a>
</p>

<p align="center">
  <a href="./README_CN.md">简体中文</a> |
  <a href="./README.md">English</a> |
  <a href="./README_JPN.md">日本語</a>
</p>

## 特点

1. **智能体应用**：支持将领域知识、业务规则、工具调用与多轮协作组合为面向任务的智能体应用。
2. **工作流编排**：支持循环、并行、批量执行、条件判断和人工反馈，适合复杂生成式 AI 流程。
3. **企业知识库**：覆盖文档导入、解析、检索、审核与知识挖掘，服务内部业务场景。
4. **企业级管控**：支持 RBAC、用户组、分组流量控制、SSO/LDAP、监控、统计与高可用部署。
5. **文档智能**：提供 OCR、表格识别、版式分析和文档解析能力，支持私有化部署。
6. **最佳实践库**：沉淀文档审核、固定版式报告生成、客服辅助、制度比对、数据分析等场景方案。

## 快速安装

安装 oneLib 前请先确保满足以下条件：

- CPU >= 4 virtual cores
- RAM >= 16 GB
- Docker 19.03.9+
- Docker Compose 1.25.1+

推荐硬件：18 virtual cores，48 GB RAM。默认部署会同时启动 ES、Milvus、OnlyOffice 等第三方组件。

下载 oneLib 代码：

```bash
git clone https://github.com/horacejett/oneLib.git
cd oneLib/docker

# 如果系统没有 git 命令，可以下载 zip 包：
wget https://github.com/horacejett/oneLib/archive/refs/heads/main.zip
unzip main.zip && cd oneLib-main/docker
```

启动 oneLib：

```bash
docker compose -f docker-compose.yml -p onelib up -d
```

启动后，在浏览器中访问 `http://IP:3001` 并注册账号。默认第一个注册用户会成为系统管理员。

安装、部署和 API 文档暂时统一查看 [oneLib 仓库](https://github.com/horacejett/oneLib)。

## 致谢

oneLib 使用并受益于 [LangChain](https://github.com/langchain-ai/langchain)、[Langflow](https://github.com/logspace-ai/langflow)、[Unstructured](https://github.com/Unstructured-IO/unstructured)、[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) 等开源项目。

## 社区与支持

问题反馈、讨论与版本信息统一使用 [GitHub](https://github.com/horacejett/oneLib)。
