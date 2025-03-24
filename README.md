# 微博传播分析工具

## 项目功能
通过DeepSeek API自动分析微博文本的：
- 主要/次要传播动机
- 情感倾向及强度
- 用户认知程度
- 自动生成结构化分析报告（Excel格式）

## 核心配置
在<mcsymbol name="main" filename="main.py" path="d:\PycharmProj\Weibo_deepseek_analysis\main.py" startline="89" type="function"></mcsymbol>中设置：
```python
input_file = "C:\\Users\\wqwan\\Desktop\\weibo_data_01_28_1.txt"  # 支持绝对路径或相对路径
```

## 快速使用
1. 安装依赖
```bash
pip install openai pandas openpyxl
```

2. 准备输入文件
- 创建txt文件（如：weibo_input.txt）
- 每行放置一条待分析的微博原文
- 文件路径支持：
  - 绝对路径：`D:\\data\\input.txt`
  - 相对路径：`data/input.txt`（相对于main.py）

3. 配置API密钥
在<mcsymbol name="ask_deepseek" filename="main.py" path="d:\PycharmProj\Weibo_deepseek_analysis\main.py" startline="6" type="function"></mcsymbol>中替换：
```python
api_key = "sk-57a7a273cae24c3cbfc879240e327782"  # 替换为有效密钥
```

4. 运行程序
```bash
python main.py
```

## 结果输出
生成文件：`analysis_results.xlsx`
数据结构：
| 编号 | 分析时间          | 原文 | 主要动机         | 次要动机         | 情感 | 强度 | 认知程度 |
|------|-------------------|------|------------------|------------------|------|------|----------|
| 1    | 2024-02-01 14:30 | [微博文本] | 娱乐消遣型动机   | 信息共享型动机   | 积极 | 强   | 3        |
