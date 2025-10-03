#!/bin/bash

# FastGPT 沙盒服务镜像构建脚本
# 使用方法: ./build_image.sh [镜像名称] [标签]

set -e

# 默认参数
IMAGE_NAME=${1:-"fastgpt-sandbox"}
TAG=${2:-"latest"}
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

echo "🚀 开始构建 FastGPT 沙盒服务镜像..."
echo "📦 镜像名称: ${FULL_IMAGE_NAME}"
echo "📁 构建上下文: $(pwd)"

# 检查是否在正确的目录
if [ ! -f "projects/sandbox/Dockerfile" ]; then
    echo "❌ 错误: 请在 FastGPT 项目根目录下运行此脚本"
    exit 1
fi

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，正在安装..."
    
    # 检测系统类型
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y docker.io docker-compose
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker $USER
    elif [ -f /etc/redhat-release ]; then
        # CentOS/RHEL
        sudo yum install -y docker docker-compose
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker $USER
    else
        echo "❌ 不支持的系统类型，请手动安装 Docker"
        exit 1
    fi
    
    echo "✅ Docker 安装完成，请重新登录或运行 'newgrp docker' 后再次执行此脚本"
    exit 0
fi

# 检查Docker服务是否运行
if ! docker info &> /dev/null; then
    echo "❌ Docker 服务未运行，尝试启动..."
    sudo systemctl start docker || {
        echo "❌ 无法启动 Docker 服务，请检查系统配置"
        exit 1
    }
fi

echo "✅ Docker 环境检查通过"

# 构建镜像
echo "🔨 开始构建镜像..."
docker build \
    -t "${FULL_IMAGE_NAME}" \
    -f projects/sandbox/Dockerfile \
    . || {
    echo "❌ 镜像构建失败"
    exit 1
}

echo "✅ 镜像构建成功: ${FULL_IMAGE_NAME}"

# 显示镜像信息
echo "📊 镜像信息:"
docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# 测试镜像
echo "🧪 测试镜像是否可以正常启动..."
CONTAINER_ID=$(docker run -d -p 3000:3000 "${FULL_IMAGE_NAME}")

sleep 5

if docker ps | grep -q "${CONTAINER_ID}"; then
    echo "✅ 镜像测试成功，容器正在运行"
    echo "🌐 服务地址: http://localhost:3000"
    echo "📋 容器ID: ${CONTAINER_ID}"
    
    # 测试API
    echo "🔍 测试API接口..."
    sleep 2
    if curl -s -f http://localhost:3000/health > /dev/null 2>&1; then
        echo "✅ API接口测试成功"
    else
        echo "⚠️  API接口测试失败，但容器正在运行"
    fi
    
    echo "🛑 停止测试容器..."
    docker stop "${CONTAINER_ID}" > /dev/null
    docker rm "${CONTAINER_ID}" > /dev/null
else
    echo "❌ 镜像测试失败，容器无法正常启动"
    docker logs "${CONTAINER_ID}"
    docker rm "${CONTAINER_ID}" > /dev/null
    exit 1
fi

echo ""
echo "🎉 镜像构建和测试完成！"
echo ""
echo "📝 使用说明:"
echo "   启动容器: docker run -d -p 3000:3000 ${FULL_IMAGE_NAME}"
echo "   查看日志: docker logs <container_id>"
echo "   进入容器: docker exec -it <container_id> /bin/sh"
echo ""
echo "🏷️  推送到仓库:"
echo "   docker tag ${FULL_IMAGE_NAME} your-registry/${IMAGE_NAME}:${TAG}"
echo "   docker push your-registry/${IMAGE_NAME}:${TAG}"