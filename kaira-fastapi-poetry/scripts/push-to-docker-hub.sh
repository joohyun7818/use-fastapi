#!/bin/bash

# Docker Hub에 이미지 푸시하는 스크립트

set -e  # 에러 발생 시 중단

# 설정
DOCKER_USERNAME="joohyun7818"  # ← Docker Hub username으로 변경
IMAGE_NAME="kaira-fastapi"
VERSION="${1:-latest}"

echo "🔨 Docker 이미지 빌드 시작..."
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$VERSION -f Dockerfile .

echo "✅ 빌드 완료: $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"

# Docker Hub 로그인 (처음 한 번만)
echo ""
echo "🔐 Docker Hub 로그인..."
docker login

echo ""
echo "📤 Docker Hub에 푸시 중..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION

# latest 태그도 함께 푸시
if [ "$VERSION" != "latest" ]; then
    echo ""
    echo "📌 latest 태그 업데이트..."
    docker tag $DOCKER_USERNAME/$IMAGE_NAME:$VERSION $DOCKER_USERNAME/$IMAGE_NAME:latest
    docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
fi

echo ""
echo "✅ 푸시 완료!"
echo ""
echo "클라우드에서 다음 명령으로 pull 받을 수 있습니다:"
echo "docker pull $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
echo ""
echo "docker-compose.yml에서 다음과 같이 사용:"
echo "image: $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
