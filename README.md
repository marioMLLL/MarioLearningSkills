# 🎓 Mario Learning Skills

> 把论文变成漫画，让知识不进脑子的过程变得至少好看一点。

## 这是什么？

一个 Claude Code Skill 集合，专门用来**折磨论文**——不对，是**优雅地学习论文**。

每个 Skill 都是 Claude Code 的插件，帮你把枯燥的学术内容变成人类大脑真正愿意吸收的形式。

## 当前技能列表

### 🎨 [paper-comic-summary](paper-comic-summary/) — 论文漫画总结

**问题：** 论文太长不想看，看了记不住，记住了不会讲。

**解决方案：** 把论文变成漫画。对，就是那种带对话框的、有图画的、你愿意在朋友圈发的那种。

**工作流程：**
```
论文 (PDF/DOCX/DOC)
    ↓
📝 提取全文文本
    ↓
🧠 大模型总结精髓（背景、方法、结果、结论）
    ↓
🎨 生成 4-6 个关键场景的漫画 Prompt
    ↓
🖼️ OpenAI GPT Image 生成漫画面板
    ↓
📊 输出图文并茂的漫画总结报告
```

**使用姿势：**
```bash
# 确保依赖已安装
pip install openai python-docx PyMuPDF

# 设置 API Key
export OPENAI_API_KEY='your-api-key'

# 然后对 Claude Code 说：
# "帮我生成这篇论文的漫画总结：paper.pdf"
```

## 技能开发中...

这个仓库还在持续生长中。计划中的技能：

- [ ] **citation-checker** (已上线) — 帮你查论文引用是不是编的
- [ ] **paper-comic-summary** (已上线) — 把论文变成漫画
- [ ] _更多技能coming soon..._

如果你有好的想法，欢迎贡献！

## 如何使用这些 Skill

1. 克隆或下载你想要的 Skill 文件夹
2. 放到你的 `~/.claude/skills/` 目录下
3. 重启 Claude Code，技能自动生效

或者直接从仓库里参考修改，打造你自己的专属 Skill。

## 贡献

欢迎 PR！无论是新 Skill、改进现有代码、还是给 README 写更好笑的介绍，都欢迎。

---

*Powered by Claude Code & 一颗不想看长论文的心*
