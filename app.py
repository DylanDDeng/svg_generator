import streamlit as st
from anthropic import Anthropic
import os
import toml
from datetime import datetime
import re
from pathlib import Path

def get_api_key():
    """从配置文件获取 API key"""
    try:
        # 尝试从 config.toml 读取配置
        config_path = Path("config.toml")
        if config_path.exists():
            config = toml.load(config_path)
            api_key = config.get("api", {}).get("anthropic_key")
            if api_key:
                return api_key
    except Exception as e:
        st.error(f"读取配置文件失败: {str(e)}")
    
    # 如果没有找到配置，显示错误信息
    st.error("""
    未找到 API Key 配置。请确保：
    1. config.toml 文件存在于项目根目录
    2. 文件包含正确的配置格式
    示例 config.toml:
    [api]
    anthropic_key = "your-api-key-here"
    """)
    st.stop()

# 初始化 Anthropic 客户端
try:
    api_key = get_api_key()
    anthropic = Anthropic(api_key=api_key)
except Exception as e:
    st.error(f"初始化 Anthropic 客户端失败: {str(e)}")
    st.stop()

# 预设的 system prompts
PRESET_PROMPTS = {
    "吐槽大师": """
                You are an SVG card generation expert. Based on user input, you will:

Capture the essence behind the word according to the user's input language
Provide a critical interpretation in a sharp and humorous way 
Express your insights through concise metaphors according to the user's input language
Maintain appropriate subtlety in criticism, like "sprinkling painkillers on a sword blade"

Generate a 400x600 pixel SVG card with a modern design style, theuser input should be on the card, featuring gradient backgrounds and rounded corners. Please return only the SVG code.
For best practices, I'd suggest adding specific design parameters:
Additional technical specifications:

Canvas dimensions: 400x600 pixels
Border radius: 12px
Gradient background: Use modern design, different elegant color combinations
Typography: LXGW WenKai font
Layout: Maintain proper spacing and visual hierarchy
Design style: Minimalist and contemporary
Output format: Raw SVG code only, no additional explanation。
    """,
    
    "文案宣传": 
    """ 
你是一位苹果公司的资深文案创作专家，具备以下特质：
专业技能：

精准把握产品核心价值
出色的修辞能力
富有创意的表达方式

创作理念：

始终坚持极简主义美学
追求优雅的表达方式
注重传达产品价值

写作特色：

简练有力的句式
讲究语言的韵律感
善用矛盾修辞制造张力

你会参考这些经典案例作为文案范本：

iPhone 5: "多了更多，少了不少"
iPhone 6: "岂止于大"
iPhone 11: "性能刚刚好，不多也不少"
iPhone 6S: "唯一的不同，是处处都不同。"
iPhone 13 Pro: "强得很"

设计规范：

画布尺寸：400x600像素
视觉风格：现代高雅设计，微妙颜色相结合，渐进色背景
字体选择：使用霞鹜文楷字体
布局要求：用户输入、分隔线、文案响应
    
根据用户的输入，请只返回 svg 代码，不要包含任何其他内容。
    """
}

def generate_svg(system_prompt, user_input):
    try:
        # 调用 Anthropic API 生成 SVG 代码
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": user_input}]
        )
        return message.content[0].text, None
    except Exception as e:
        return None, str(e)

def get_svg_height(svg_code):
    """从 SVG 代码中提取高度"""
    height_match = re.search(r'height="(\d+)"', svg_code)
    if height_match:
        # 添加一些边距（例如 50px）
        return int(height_match.group(1)) + 50
    return 650  # 默认高度

# Streamlit 应用界面
st.set_page_config(page_title="SVG 卡片生成器", layout="wide")
st.title("SVG 卡片生成器")

# 初始化 session_state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'svg_code' not in st.session_state:
    st.session_state.svg_code = None
if 'custom_prompt' not in st.session_state:
    st.session_state.custom_prompt = ""

# 侧边栏配置
with st.sidebar:
    st.header("生成配置")

    # 使用说明
    with st.expander("使用说明"):
        st.markdown("""
        ### 如何使用
        1. 选择预设风格或自定义 **System Prompt**。
        2. 在 **用户输入** 中描述您想要的具体内容。
        3. 点击 **生成卡片** 按钮。
        4. 通过标签页切换查看生成的卡片预览和 SVG 代码。
        5. 在 **SVG 代码** 标签页中使用下载按钮保存 SVG 源文件。
        6. 在 **历史记录** 标签页中查看之前生成的卡片。
        """)

    # Prompt 选择和输入区域
    st.subheader("选择生成风格")
    
    # 添加一个选项："选择预设风格"
    prompt_type = st.radio(
        "选择 Prompt 类型",
        ["预设风格", "自定义输入"],
        horizontal=True
    )
    
    if prompt_type == "预设风格":
        selected_preset = st.selectbox(
            "选择预设风格",
            list(PRESET_PROMPTS.keys())
        )
        system_prompt = PRESET_PROMPTS[selected_preset]
        # 显示当前使用的 prompt（只读）
        st.text_area(
            "当前使用的 System Prompt",
            value=system_prompt,
            height=150,
            disabled=True
        )
    else:
        system_prompt = st.text_area(
            "自定义 System Prompt",
            value=st.session_state.custom_prompt if st.session_state.custom_prompt else (
                "你是一个 SVG 卡片生成专家。请生成一个尺寸为 400x200 像素的 SVG 卡片，"
                "具有现代设计风格，包含渐变背景和圆角边框。请只返回 SVG 代码。"
            ),
            height=150
        )
        st.session_state.custom_prompt = system_prompt

    st.subheader("卡片内容")
    user_input = st.text_area(
        "用户输入",
        value="请生成一张卡片，标题是 'Hello World'，副标题是 'Welcome to my website'",
        height=100
    )

    generate_button = st.button("生成卡片", type="primary")

# 生成卡片
if generate_button:
    with st.spinner('正在生成卡片...'):
        svg_code, error = generate_svg(system_prompt, user_input)
        if error:
            st.error(f"生成失败: {error}")
        else:
            st.session_state.svg_code = svg_code
            # 添加到历史记录
            st.session_state.history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'system_prompt': system_prompt,
                'user_input': user_input,
                'svg_code': svg_code
            })
            st.success('生成成功！')

# 创建标签页
if st.session_state.svg_code:
    tab1, tab2, tab3 = st.tabs(['预览', 'SVG 代码', '历史记录'])

    with tab1:
        st.header('预览')
        display_height = get_svg_height(st.session_state.svg_code)
        st.components.v1.html(st.session_state.svg_code, height=display_height)
        
        # 添加最近生成的卡片展示区域
        if len(st.session_state.history) > 1:  # 如果有超过1条历史记录
            st.markdown("---")  # 添加分隔线
            st.header("最近生成的卡片")
            # 显示最近的5张卡片（不包括当前的）
            for idx, record in enumerate(list(reversed(st.session_state.history[:-1]))[:5]):
                with st.expander(f"生成于: {record['timestamp']}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        display_height = get_svg_height(record['svg_code'])
                        st.components.v1.html(record['svg_code'], height=display_height)
                    with col2:
                        st.markdown("**生成参数:**")
                        st.markdown("*用户输入:*")
                        st.text(record['user_input'])
                        st.download_button(
                            label='下载此 SVG',
                            data=record['svg_code'],
                            file_name=f'card_{record["timestamp"].replace(":", "-")}.svg',
                            mime='image/svg+xml',
                            use_container_width=True,
                            key=f'download_preview_{idx}'  # 添加唯一的 key
                        )

    with tab2:
        st.header('SVG 代码')
        st.code(st.session_state.svg_code, language='xml')
        st.download_button(
            label='下载 SVG',
            data=st.session_state.svg_code,
            file_name='card.svg',
            mime='image/svg+xml',
            use_container_width=True,
            key='download_current'  # 添加唯一的 key
        )

    with tab3:
        st.header('历史记录')
        if not st.session_state.history:
            st.info('暂无历史记录')
        else:
            for i, record in enumerate(reversed(st.session_state.history)):
                with st.expander(f"记录 {len(st.session_state.history)-i}"):
                    st.subheader("预览")
                    display_height = get_svg_height(record['svg_code'])
                    st.components.v1.html(record['svg_code'], height=display_height)
                    
                    st.subheader("生成参数")
                    st.markdown("**System Prompt:**")
                    st.text(record['system_prompt'])
                    st.markdown("**用户输入:**")
                    st.text(record['user_input'])
                    
                    st.subheader("SVG 代码")
                    st.code(record['svg_code'], language='xml')
                    
                    st.download_button(
                        label='下载此 SVG',
                        data=record['svg_code'],
                        file_name=f'card_{record["timestamp"].replace(":", "-")}.svg',
                        mime='image/svg+xml',
                        use_container_width=True,
                        key=f'download_history_{i}'  # 添加唯一的 key
                    )
