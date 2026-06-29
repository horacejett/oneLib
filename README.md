![oneLib banner](brand-source/generated/onelib-banner.png)

# oneLib / 一知

oneLib is an integrated AI platform for enterprise knowledge bases, agent applications, and generative AI workflows.

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

## Features

1. **Agent applications**: Build task-oriented agents with domain knowledge, business rules, tool usage, and multi-turn collaboration.
2. **Workflow orchestration**: Compose complex AI workflows with loops, parallel branches, batch execution, conditional logic, and human feedback.
3. **Enterprise knowledge bases**: Manage document ingestion, parsing, retrieval, review, and knowledge mining for internal business scenarios.
4. **Enterprise controls**: Support RBAC, user groups, traffic control, SSO/LDAP integration, monitoring, statistics, and high-availability deployment.
5. **Document intelligence**: Provide OCR, table recognition, layout analysis, and document parsing capabilities for private deployment.
6. **Best-practice library**: Collect reusable application patterns for document review, report generation, support assistance, policy comparison, data analysis, and more.

## Quick Start

Please ensure the following conditions are met before installing oneLib:

- CPU >= 4 virtual cores
- RAM >= 16 GB
- Docker 19.03.9+
- Docker Compose 1.25.1+

Recommended hardware: 18 virtual cores and 48 GB RAM. The default deployment also starts third-party components such as ES, Milvus, and OnlyOffice.

Download oneLib:

```bash
git clone https://github.com/horacejett/oneLib.git
cd oneLib/docker

# If git is unavailable:
wget https://github.com/horacejett/oneLib/archive/refs/heads/main.zip
unzip main.zip && cd oneLib-main/docker
```

Start oneLib:

```bash
docker compose -f docker-compose.yml -p onelib up -d
```

After startup, open `http://IP:3001` in your browser and register an account. The first registered user becomes the system admin by default.

For installation, deployment, and API documentation, see [the oneLib repository](https://github.com/horacejett/oneLib).

## Acknowledgement

oneLib benefits from open source projects including [LangChain](https://github.com/langchain-ai/langchain), [Langflow](https://github.com/logspace-ai/langflow), [Unstructured](https://github.com/Unstructured-IO/unstructured), and [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory).

## Community

For issues, discussions, and release information, use [GitHub](https://github.com/horacejett/oneLib).
