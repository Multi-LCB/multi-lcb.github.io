---
header: 多语言 LiveCodeBench
navHome: 首页
navLeaderboard: 排行榜
navCompare: 对比
navNews: 新闻
newsTitle: 更新
---

**Multi-LCB** 将 **LiveCodeBench (LCB)**（用于污染感知 / contamination-aware 代码生成评估的事实标准基准）从 **仅 Python** 扩展到 **多语言** 版本，在统一的 STDIN/STDOUT 评测协议下覆盖 **12 种编程语言**（C++, C#, Python, Java, Rust, Go, TypeScript, JavaScript, Ruby, PHP, Kotlin, Scala）。

---

我们将原始 LiveCodeBench 的每一道题转换为所有支持语言的等价题目，同时保留 **污染感知评估**（按发布日期过滤）、**实时更新**，并使用相同的 **Pass@1** 指标。从原始 functional 格式迁移到统一的 STDIN/STDOUT 接口后，我们观察到 **Pass@1 仅有轻微变化**：这说明新格式在实现一致的多语言评测的同时，依然保持了任务难度与模型排名的稳定性。

在 Multi‑LCB 上评测 **24+ 个现代大模型** 表明：
- **Python 不是其他语言的可靠代理**：一旦离开 Python，模型排名可能明显变化；
- 许多模型存在 **对 Python 的过拟合**：在 Python 上得分很高，但在其他语言上显著下滑；
- 存在 **语言特定的污染** 以及显著的跨语言性能差距，尤其是在静态类型和较少使用的语言上。

因此，Multi‑LCB 提供了更贴近真实场景的多语言代码生成评估，并为训练真正 language‑agnostic 的代码模型提供了可靠基准。

<span class="inline-accept">本工作已被 ICLR 2026 接收。<img class="inline-logo" src="./assets/ICLR-logo.svg" alt="ICLR logo" /></span>
作者：Maria Ivanova, Pavel Zadorozhny, Rodion Levichev, Ivan Petrov, Pavel Adamenko, Ivan Lopatin, Alexey Kutalev, Dmitrii Babaev