# SVG 卡片生成器

一个基于 Streamlit 和 Claude API 的智能 SVG 卡片生成工具，支持多种风格的卡片生成、预览和管理。

## 功能特点

- 🎨 多种预设风格
  - 吐槽大师：生成带有幽默批判性的卡片
  - 文案宣传：生成类似苹果风格的营销文案卡片
- ✨ 自定义 System Prompt
- 👀 实时预览生成效果
- 💾 SVG 源代码查看和下载
- 📝 历史记录管理
- 🖼 最近生成记录快速预览

## 安装要求
```bash
pip install -r requirements.txt
```


## 环境配置

1.创建 `.streamlit` 目录： 

```bash
mkdir .streamlit
```

2. 在 `.streamlit` 目录下创建 `secrets.toml` 文件：

```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```



## 使用方法

1. 启动应用：

```bash

streamlit run app.py
```


2. 访问应用（默认地址：http://localhost:8501）

3. 使用流程：
   - 选择预设风格或自定义 System Prompt
   - 输入卡片内容描述
   - 点击"生成卡片"按钮
   - 在预览标签页查看生成结果
   - 下载 SVG 文件或查看历史记录

## 技术栈

- Streamlit：Web 应用框架
- Anthropic Claude API：AI 模型服务
- Python：编程语言
- SVG：图形格式

## 主要功能模块

### 1. 预设 Prompts
- 吐槽大师：生成幽默风格的评论卡片
- 文案宣传：生成专业营销风格的文案卡片

### 2. 卡片生成
- 支持 400x600 像素的 SVG 卡片
- 现代设计风格
- 渐变背景
- 圆角边框
- 使用霞鹜文楷字体

### 3. 界面功能
- 预览标签页：显示当前生成的卡片和最近历史记录
- SVG 代码标签页：查看和下载源代码
- 历史记录标签页：查看所有生成记录

## 部署说明

### 本地开发
1. 确保 `.streamlit/secrets.toml` 文件配置正确
2. 运行 `streamlit run app.py`

### Streamlit Cloud 部署
1. 在 Streamlit Cloud 项目设置中配置 Secrets
2. 添加 `ANTHROPIC_API_KEY` 到 Secrets 配置中

## 注意事项

- 需要有效的 Anthropic API key
- 历史记录存储在会话中，刷新页面后将清空
- SVG 预览区域会根据图片尺寸自动调整高度

