from openai import OpenAI
import json
import pandas as pd
from datetime import datetime


def ask_deepseek(system_prompt, user_input):
    client = OpenAI(
        api_key="sk-57a7a273cae24c3cbfc879240e327782",  # 请替换为您的API密钥
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        stream=False,
    )

    return response.choices[0].message.content


def save_to_excel(result, custom_input):
    """将分析结果保存至Excel文件，包含自动编号和列顺序管理"""
    df = pd.DataFrame([result])
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["原文"] = custom_input  # 添加原文字段

    filename = "analysis_results.xlsx"
    existing_df = None

    # 读取现有数据
    try:
        existing_df = pd.read_excel(filename, dtype=str)
    except FileNotFoundError:
        pass

    # 生成自增编号
    if (
        existing_df is not None
        and not existing_df.empty
        and "编号" in existing_df.columns
    ):
        max_id = existing_df["编号"].astype(int).max()
        new_id = max_id + 1
    else:
        new_id = 1
    df["编号"] = new_id

    # 定义列顺序
    columns_order = [
        "编号",
        "timestamp",
        "原文",
        "主要传播动机",
        "次要传播动机",
        "情感",
        "情绪烈度",
        "了解程度",
    ]
    df = df[columns_order]

    # 合并数据
    if existing_df is not None:
        existing_df = existing_df[columns_order]
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        updated_df = df

    # 保存文件
    updated_df.to_excel(filename, index=False)
    print(f"结果已保存至 {filename}")


# 使用示例
if __name__ == "__main__":
    custom_system = """分析以下有关deepseek的博文内容，分析用户的主要传播动机，次要传播动机，情感（积极、中立，消极），情绪烈度（强，中，弱），猜测用户对deepseek了解程度（专家到仅听说打分5-0或输出未知），博文内容：“玩了一下deepseek让它给我写同人文大纲看得我one愣one愣的。。。 ​”严格按照以下JSON格式输出，禁止任何其他内容：
    {
        "主要传播动机": "",
        "次要传播动机": "",
        "情感": "",
        "情绪烈度": "",
        "了解程度": ""
    }
    示例：{"主要传播动机": "娱乐消遣型动机", "次要传播动机": "信息共享型动机", "情感": "积极", "情绪烈度": "强", "了解程度": "3"}传播动机分类方式：1. 信息共享型动机核心需求：认知需求（消除不确定性/获取知识）行为特征：传播事实、数据、新闻、科普内容细分场景： 危机信息共享（如疫情动态） 知识传递（如科普文章转发） 经验分享（如产品使用心得）学术支持： Ruggiero (2000) 扩展的U&G理论中"信息控制"维度 操作定义：内容含客观数据、解决方案或降低不确定性的描述 2. 社交资本型动机核心需求：归属与尊重需求（建立/维护社会关系）行为特征：点赞、评论、转发熟人内容、参与话题标签细分场景： 关系维护（如转发朋友动态） 群体认同（如加入“宝妈群”并分享育儿内容） 地位彰显（如晒高端活动邀请函）学术支持： Putnam (2000) 社会资本理论中的“桥接型/黏合型资本” 操作定义：内容直接提及他人（@某人）或使用群体专属符号（如#饭圈用语） 3. 自我建构型动机核心需求：自我实现需求（塑造身份/价值观表达）行为特征：发布原创观点、人生感悟、政治立场细分场景： 人设打造（如职场博主分享自律日常） 价值观宣言（如环保主义者传播低碳倡议） 文化身份表达（如汉服爱好者展示传统服饰）学术支持： Goffman (1959) 拟剧理论中的“印象管理” 操作定义：内容含第一人称叙述（“我认为”“我的经历”）或身份标签（如“作为XX群体的一员”） 4. 情绪驱动型动机核心需求：情感释放（宣泄/共鸣）行为特征：传播带有强烈情绪符号的内容（表情包、感叹号、情绪词）细分类型： 高唤醒正向（如狂喜时转发中奖信息） 高唤醒负向（如愤怒时传播社会不公事件） 低唤醒共鸣（如分享治愈系图文缓解焦虑）学术支持： Berger & Milkman (2012) 病毒传播中的“情绪唤醒度”模型 操作定义：文本含情绪词密度>5%（如LIWC词典中的“anger”“joy”类词汇） 5. 工具理性型动机核心需求：功利目标（获取物质回报/解决具体问题）行为特征：传播促销信息、求助内容、功能性教程细分场景： 经济激励（如转发抽奖链接） 问题解决（如转发“寻人启事”） 资源交换（如拼多多砍价链接）学术支持： Fishbein & Ajzen (1975) 理性行为理论中的“工具性态度” 操作定义：内容含明确行动指令（“点击领取”“帮忙转发”）或物质回报承诺 6. 利他公益型动机核心需求：超越性需求（帮助他人/社会福祉）行为特征：传播慈善信息、公益倡议、预警提示细分场景： 保护他人（如转发暴雨避险指南） 社会倡导（如动物保护组织传播反虐待视频） 知识普惠（如免费分享考研资料）学术支持： Batson (1998) 利他主义中的“共情-帮助”模型 操作定义：内容含利他语义框架（“为了孩子”“拯救地球”）且无个人获益暗示 7. 娱乐消遣型动机核心需求：感官刺激（追求愉悦/消磨时间）行为特征：传播段子、八卦、游戏、挑战性内容细分场景： 即时娱乐（如转发搞笑短视频） 参与式娱乐（如加入“冰桶挑战”） 虚拟沉浸（如分享元宇宙活动邀请）学术支持： Zillmann (2000) 情绪管理理论中的“情绪调节” 操作定义：内容含娱乐标记词（“笑死”“爆笑”）或参与门槛低的互动机制（如“转发接好运”）"""

    input_file = (
        "C:\\Users\\wqwan\\Desktop\\weibo_data_01_28_1.txt"  # 指定的输入文件路径
    )
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            inputs = [line.strip() for line in f if line.strip()]  # 读取非空行
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
        exit(1)

    # 处理每个输入
    for idx, custom_input in enumerate(inputs, 1):
        print(f"\n处理第 {idx} 条输入...")
        answer = ask_deepseek(custom_system, custom_input)

        try:
            if answer is not None:
                cleaned_answer = answer.strip().strip("```json").strip("```").strip()
                result = json.loads(cleaned_answer)
                save_to_excel(result, custom_input)
            else:
                print(f"第 {idx} 条请求返回空响应")
        except json.JSONDecodeError:
            print(f"第 {idx} 条响应解析失败：{answer}")
