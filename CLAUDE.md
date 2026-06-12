# ReproPilot — agent conventions

技术栈: Python 3.10+, Typer, Pydantic, Jinja2, pytest, ruff.

硬性规则:
- 默认绝不执行用户的训练代码;smoke test 只能通过 --run-smoke-test 显式开启。
- 每条评分规则都必须包含: id, category, weight, evidence_level, checklist_refs, fix。
- 默认模式下总分只按 static + semantic 证据归一化到 100;报告里必须标注 "runnable evidence: not assessed"。
- 生成的模板仓库,用 repropilot check 自检必须 ≥ 90 分。
- 核心路径: 只用 CPU、不需要 API key、不需要真实数据集。

完成的标准 (Definition of done):
- 本地 `pytest -q` 和 `ruff check .` 都通过。
- 新增规则要带 fixture 测试 (bad/medium/good 三种仓库)。
- 公开行为有变化时,更新 docs/scoring.md。
