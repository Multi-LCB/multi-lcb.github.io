---
header: Multi LiveCodeBench
navHome: Main
navLeaderboard: Leaderboard
navCompare: Compare
navNews: News
newsTitle: Updates
---

**Multi-LCB** extends **LiveCodeBench (LCB)** – a de-facto standard benchmark for contamination-aware code generation evaluation – from a **Python-only** setting to a **multi-language** one, covering **12 programming languages** (C++, C#, Python, Java, Rust, Go, TypeScript, JavaScript, Ruby, PHP, Kotlin, Scala) under a unified STDIN/STDOUT evaluation protocol.

---

Every original LiveCodeBench task is converted into equivalent tasks in all supported languages, preserving **contamination-aware evaluation** (release-date filtering), **live updates**, and the same **Pass@1** metric. When transitioning from the original functional-format evaluation to this unified STDIN/STDOUT interface, we observe only **minor changes in Pass@1**, which means the new format maintains task difficulty and model rankings while enabling consistent multi-language evaluation.

Evaluating **24+ modern LLMs** on Multi-LCB shows that:
- **Python is not a reliable proxy** for other languages: model rankings can change substantially outside Python.
- Many models exhibit **Python overfitting**, with strong Python scores but large performance drops on other languages.
- There is **language-specific contamination** and large cross-language performance gaps, especially for statically typed and less common languages.

Multi-LCB thus provides a more realistic, multi-language assessment of code generation capabilities and a solid benchmark for developing truly language-agnostic coding models.

<span class="inline-accept">This work has been accepted to ICLR 2026.<img class="inline-logo" src="./assets/ICLR-logo.svg" alt="ICLR logo" /></span>
Authors: Maria Ivanova, Pavel Zadorozhny, Rodion Levichev, Ivan Petrov, Pavel Adamenko, Ivan Lopatin, Alexey Kutalev, Dmitrii Babaev
