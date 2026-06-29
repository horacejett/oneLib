![oneLib banner](brand-source/generated/onelib-banner.png)

# oneLib / 一知

oneLib（一知）は、企業ナレッジベース、エージェントアプリケーション、生成 AI ワークフロー向けの統合 AI プラットフォームです。

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

## 特徴

1. **エージェントアプリケーション**：ドメイン知識、業務ルール、ツール利用、複数ターンの協調を組み合わせたタスク指向のエージェントを構築できます。
2. **ワークフローオーケストレーション**：ループ、並列分岐、バッチ実行、条件分岐、人間によるフィードバックを含む複雑な AI ワークフローを構成できます。
3. **企業ナレッジベース**：文書の取り込み、解析、検索、レビュー、知識抽出を社内業務シナリオ向けに管理できます。
4. **エンタープライズ管理**：RBAC、ユーザーグループ、トラフィック制御、SSO/LDAP 連携、監視、統計、高可用性デプロイをサポートします。
5. **ドキュメントインテリジェンス**：OCR、表認識、レイアウト解析、文書解析機能を提供し、プライベート環境へのデプロイに対応します。
6. **ベストプラクティスライブラリ**：文書レビュー、固定レイアウトのレポート生成、サポート支援、規程比較、データ分析などの再利用可能なパターンを蓄積します。

## クイックスタート

oneLib をインストールする前に、以下の条件を満たしていることを確認してください。

- CPU >= 4 virtual cores
- RAM >= 16 GB
- Docker 19.03.9+
- Docker Compose 1.25.1+

推奨ハードウェアは 18 virtual cores、48 GB RAM です。標準デプロイでは ES、Milvus、OnlyOffice などのサードパーティコンポーネントも起動します。

oneLib をダウンロードします。

```bash
git clone https://github.com/horacejett/oneLib.git
cd oneLib/docker

# git が利用できない場合:
wget https://github.com/horacejett/oneLib/archive/refs/heads/main.zip
unzip main.zip && cd oneLib-main/docker
```

oneLib を起動します。

```bash
docker compose -f docker-compose.yml -p onelib up -d
```

起動後、ブラウザで `http://IP:3001` にアクセスしてアカウントを登録します。最初に登録されたユーザーがデフォルトでシステム管理者になります。

インストール、デプロイ、API ドキュメントは [oneLib リポジトリ](https://github.com/horacejett/oneLib) を参照してください。

## 謝辞

oneLib は [LangChain](https://github.com/langchain-ai/langchain)、[Langflow](https://github.com/logspace-ai/langflow)、[Unstructured](https://github.com/Unstructured-IO/unstructured)、[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) などのオープンソースプロジェクトから恩恵を受けています。

## コミュニティ

課題、議論、リリース情報は [GitHub](https://github.com/horacejett/oneLib) を利用してください。
