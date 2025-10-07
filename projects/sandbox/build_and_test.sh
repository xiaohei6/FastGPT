#!/bin/bash

echo "🚀 开始构建和测试增强版Python沙盒..."
echo "=" * 60

# 1. 构建项目
echo "📦 构建TypeScript项目..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ TypeScript构建失败"
    exit 1
fi

echo "✅ TypeScript构建成功"

# 2. 构建Docker镜像
echo "🐳 构建Docker镜像..."
docker build -t fastgpt-sandbox-enhanced .

if [ $? -ne 0 ]; then
    echo "❌ Docker镜像构建失败"
    exit 1
fi

echo "✅ Docker镜像构建成功"

# 3. 停止旧容器（如果存在）
echo "🛑 停止旧容器..."
docker stop fastgpt-sandbox-test 2>/dev/null || true
docker rm fastgpt-sandbox-test 2>/dev/null || true

# 4. 启动新容器
echo "🚀 启动新容器..."
docker run -d --name fastgpt-sandbox-test -p 3005:3005 fastgpt-sandbox-enhanced

if [ $? -ne 0 ]; then
    echo "❌ 容器启动失败"
    exit 1
fi

echo "✅ 容器启动成功"

# 5. 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 6. 健康检查
echo "🏥 健康检查..."
for i in {1..30}; do
    if curl -s http://localhost:3005/sandbox > /dev/null; then
        echo "✅ 服务已启动"
        break
    fi
    echo "⏳ 等待服务启动... ($i/30)"
    sleep 2
done

# 7. 运行测试
echo "🧪 运行测试..."
python3 test_complete_api.py

# 8. 清理
echo "🧹 清理资源..."
docker stop fastgpt-sandbox-test
docker rm fastgpt-sandbox-test

echo "🎉 构建和测试完成！"
