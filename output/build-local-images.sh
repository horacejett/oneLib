#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker command not found" >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is not running or not reachable" >&2
  exit 1
fi

docker_build() {
  if [[ -n "${PLATFORM:-}" ]]; then
    docker build --platform "$PLATFORM" "$@"
  else
    docker build "$@"
  fi
}

detect_pandoc_arch() {
  local platform="${PLATFORM:-}"
  local docker_arch

  if [[ "$platform" == *"arm64"* || "$platform" == *"aarch64"* ]]; then
    echo "arm64"
    return
  fi

  if [[ "$platform" == *"amd64"* || "$platform" == *"x86_64"* ]]; then
    echo "amd64"
    return
  fi

  docker_arch="$(docker info --format '{{.Architecture}}' 2>/dev/null || true)"
  case "$docker_arch" in
    arm64|aarch64)
      echo "arm64"
      ;;
    amd64|x86_64)
      echo "amd64"
      ;;
    *)
      echo "amd64"
      ;;
  esac
}

PANDOC_ARCH="${PANDOC_ARCH:-$(detect_pandoc_arch)}"
echo "Using PANDOC_ARCH=${PANDOC_ARCH}"

echo "Building backend base image..."
docker_build \
  --build-arg "PANDOC_ARCH=${PANDOC_ARCH}" \
  -t horacejett/onelib-backend:base.v8 \
  -f src/backend/base.Dockerfile \
  src/backend

echo "Building backend image..."
docker_build \
  -t horacejett/onelib-backend:v2.4.0-beta1-fix \
  -f src/backend/Dockerfile \
  src/backend

echo "Building frontend image..."
docker_build \
  -t horacejett/onelib-frontend:v2.4.0-beta1-fix \
  -f src/frontend/Dockerfile \
  src/frontend

echo
echo "Images built. Start services with:"
echo "  cd docker && docker compose -f docker-compose.yml -p onelib up -d"
