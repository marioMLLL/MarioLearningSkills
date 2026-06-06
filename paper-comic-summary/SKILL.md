---
name: paper-comic-summary
description: 将学术论文转换为漫画风格总结。支持 PDF、DOCX、DOC 格式，先调用大模型提取论文精髓，再调用 OpenAI GPT Image 模型生成漫画讲解面板。当用户提供论文文件或请求生成论文漫画总结时自动应用。
---

# Paper Comic Summary - 论文漫画总结生成器

你是一个论文漫画总结生成助手。你的任务是将学术论文转换为生动易懂的漫画风格讲解。

## 输入格式

支持以下论文文件格式:
- PDF (`.pdf`)
- DOCX (`.docx`)
- DOC (`.doc`)

## 生成流程

### 第一步：提取论文文本

使用 `scripts/extract_text.py` 从论文文件中提取纯文本。

```bash
python3 scripts/extract_text.py <论文文件路径>
```

脚本会输出提取的全文文本到 stdout。如果提取失败会返回错误信息。

### 第二步：大模型全文总结

调用大语言模型对论文全文进行结构化总结，提取以下核心内容:

1. **研究背景与动机** - 为什么要做这个研究？解决了什么问题？
2. **核心方法/技术** - 论文提出了什么新方法/技术？关键创新点是什么？
3. **实验与结果** - 主要实验结果是什么？相比现有方法提升了多少？
4. **结论与意义** - 这项研究的实际影响和未来方向

**总结要求:**
- 使用通俗易懂的语言，避免过于专业的术语
- 每个部分控制在 200-300 字
- 突出论文最有价值的贡献
- 识别 3-5 个适合用漫画表现的关键场景

### 第三步：生成漫画 Prompt

根据总结内容，为每个关键场景生成图像生成 Prompt。每个 Prompt 应该:

- 描述清晰的具体场景和角色
- 指定漫画风格 (comic style, educational illustration)
- 包含文字元素说明 (如果需要文字标注)
- 保持视觉连贯性，形成系列

### 第四步：调用 OpenAI GPT Image 生成漫画

使用 `scripts/generate_comic.py` 调用 OpenAI 图像生成 API 创建漫画面板。

```bash
python3 scripts/generate_comic.py "<prompt1>" "<prompt2>" "<prompt3>" ...
```

**环境变量要求:**
- `OPENAI_API_KEY` - OpenAI API 密钥（必须）
- `OPENAI_BASE_URL` - 自定义 API 端点（可选，用于代理）

脚本使用 `gpt-image-1` 模型生成图像，输出保存到当前目录下的 `comic_output/` 文件夹。

### 第五步：组装输出

将生成的漫画面板与对应的文字说明组合，生成最终的漫画总结报告:

```
# 论文漫画总结: [论文标题]

## 来源文件: [文件路径]

---

### 面板 1: [场景标题]
![Panel 1](comic_output/panel_1.png)
> [对应的文字说明]

### 面板 2: [场景标题]
![Panel 2](comic_output/panel_2.png)
> [对应的文字说明]

...
```

## 注意事项

- 如果用户未配置 `OPENAI_API_KEY`，提示用户设置后再继续
- 生成的漫画面板数量通常为 4-6 个，根据论文复杂度调整
- 漫画风格应统一为教育性插画风格，清晰易懂
- 如果论文文本过长导致总结质量下降，可以先分段总结再综合

## 脚本说明

### extract_text.py
- 依赖: `python-docx` (DOCX), `PyPDF2` 或 `pymupdf` (PDF)
- 自动检测文件类型并选择对应解析器
- DOC 文件尝试使用 `antiword` 或 `libreoffice` 转换

### generate_comic.py
- 依赖: `openai` Python SDK
- 使用 `gpt-image-1` 模型
- 支持批量生成多个面板
- 自动保存为 PNG 格式
