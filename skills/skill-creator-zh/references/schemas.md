# JSON 数据结构参考

本文档定义了技能创建器使用的所有 JSON 数据结构。

---

## evals.json

定义技能的评测用例。位于技能目录下的 `evals/evals.json`。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的示例 prompt",
      "expected_output": "预期结果描述",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "输出包含 X",
        "技能使用了脚本 Y"
      ]
    }
  ]
}
```

**字段：**
- `skill_name`：与技能前置元数据中的名称匹配
- `evals[].id`：唯一整数标识符
- `evals[].prompt`：要执行的任务
- `evals[].expected_output`：人类可读的成功描述
- `evals[].files`：可选的输入文件路径列表（相对于技能根目录）
- `evals[].expectations`：可验证的陈述列表

---

## history.json

在改进模式中追踪版本演进。位于工作区根目录。

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "pdf",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

**字段：**
- `started_at`：改进开始的 ISO 时间戳
- `skill_name`：被改进的技能名称
- `current_best`：最佳表现者的版本标识符
- `iterations[].version`：版本标识符（v0、v1、...）
- `iterations[].parent`：此版本派生自的父版本
- `iterations[].expectation_pass_rate`：来自评分的通过率
- `iterations[].grading_result`："baseline"、"won"、"lost" 或 "tie"
- `iterations[].is_current_best`：是否为当前最佳版本

---

## eval_metadata.json

每个评测运行目录中的元数据文件。

```json
{
  "eval_id": 0,
  "eval_name": "描述性名称",
  "prompt": "用户的任务 prompt",
  "assertions": [
    "输出包含 X",
    "格式为 PDF"
  ]
}
```

---

## grading.json

评分 Agent 的输出。位于 `<run-dir>/grading.json`。

```json
{
  "expectations": [
    {
      "text": "输出包含姓名'张三'",
      "passed": true,
      "evidence": "在执行记录步骤 3 中找到：'提取的姓名：张三、李四'"
    },
    {
      "text": "电子表格在 B10 单元格中有 SUM 公式",
      "passed": false,
      "evidence": "没有创建电子表格。输出是一个文本文件。"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  },
  "execution_metrics": {
    "tool_calls": {
      "Read": 5,
      "Write": 2,
      "Bash": 8
    },
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450,
    "transcript_chars": 3200
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "表单有 12 个可填写字段",
      "type": "factual",
      "verified": true,
      "evidence": "在 field_info.json 中统计到 12 个字段"
    }
  ],
  "user_notes_summary": {
    "uncertainties": ["使用了 2023 年的数据，可能已过时"],
    "needs_review": [],
    "workarounds": ["对不可填写字段使用了文本覆盖作为替代方案"]
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "输出包含姓名'张三'",
        "reason": "一个虚构的文档只要提到了名字就能通过"
      }
    ],
    "overall": "断言检查存在性但不检查正确性。"
  }
}
```

**字段：**
- `expectations[]`：已评分的预期及证据
- `summary`：汇总的通过/失败计数
- `execution_metrics`：工具使用和输出大小（来自执行器的 metrics.json）
- `timing`：挂钟时间（来自 timing.json）
- `claims`：从输出中提取和验证的声明
- `user_notes_summary`：执行器标记的问题
- `eval_feedback`：（可选）评测改进建议，仅在评分员发现值得提出的问题时出现

---

## metrics.json

执行器 Agent 的输出。位于 `<run-dir>/outputs/metrics.json`。

```json
{
  "tool_calls": {
    "Read": 5,
    "Write": 2,
    "Bash": 8,
    "Edit": 1,
    "Glob": 2,
    "Grep": 0
  },
  "total_tool_calls": 18,
  "total_steps": 6,
  "files_created": ["filled_form.pdf", "field_values.json"],
  "errors_encountered": 0,
  "output_chars": 12450,
  "transcript_chars": 3200
}
```

**字段：**
- `tool_calls`：每种工具类型的调用次数
- `total_tool_calls`：所有工具调用的总和
- `total_steps`：主要执行步骤数
- `files_created`：创建的输出文件列表
- `errors_encountered`：执行期间的错误数
- `output_chars`：输出文件的总字符数
- `transcript_chars`：执行记录的字符数

---

## timing.json

运行的挂钟时间。位于 `<run-dir>/timing.json`。

**如何捕获：** 当子 agent 任务完成时，任务通知包含 `total_tokens` 和 `duration_ms`。立即保存——它们不会在其他地方持久化，事后无法恢复。

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:32:45Z",
  "executor_duration_seconds": 165.0,
  "grader_start": "2026-01-15T10:32:46Z",
  "grader_end": "2026-01-15T10:33:12Z",
  "grader_duration_seconds": 26.0
}
```

---

## benchmark.json

基准测试模式的输出。位于 `benchmarks/<timestamp>/benchmark.json`。

```json
{
  "metadata": {
    "skill_name": "pdf",
    "skill_path": "/path/to/pdf",
    "executor_model": "claude-sonnet-4-20250514",
    "analyzer_model": "most-capable-model",
    "timestamp": "2026-01-15T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },

  "runs": [
    {
      "eval_id": 1,
      "eval_name": "Ocean",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 42.5,
        "tokens": 3800,
        "tool_calls": 18,
        "errors": 0
      },
      "expectations": [
        {"text": "...", "passed": true, "evidence": "..."}
      ],
      "notes": [
        "使用了 2023 年数据，可能已过时",
        "对不可填写字段使用了文本覆盖"
      ]
    }
  ],

  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 45.0, "stddev": 12.0, "min": 32.0, "max": 58.0},
      "tokens": {"mean": 3800, "stddev": 400, "min": 3200, "max": 4100}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08, "min": 0.28, "max": 0.45},
      "time_seconds": {"mean": 32.0, "stddev": 8.0, "min": 24.0, "max": 42.0},
      "tokens": {"mean": 2100, "stddev": 300, "min": 1800, "max": 2500}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0",
      "tokens": "+1700"
    }
  },

  "notes": [
    "断言'输出是 PDF 文件'在两种配置中都 100% 通过——可能无法区分技能价值",
    "评测 3 表现出高方差（50% ± 40%）——可能不稳定或与模型有关",
    "不使用技能的运行在表格提取预期上一致失败",
    "技能增加了平均 13 秒执行时间但通过率提升了 50%"
  ]
}
```

**字段：**
- `metadata`：基准测试运行的信息
  - `skill_name`：技能名称
  - `timestamp`：基准测试运行时间
  - `evals_run`：评测名称或 ID 列表
  - `runs_per_configuration`：每种配置的运行次数（例如 3）
- `runs[]`：各次运行的结果
  - `eval_id`：数字评测标识符
  - `eval_name`：人类可读的评测名称（在查看器中用作章节标题）
  - `configuration`：必须是 `"with_skill"` 或 `"without_skill"`（查看器使用这个确切字符串进行分组和着色）
  - `run_number`：整数运行编号（1、2、3...）
  - `result`：嵌套对象，包含 `pass_rate`、`passed`、`total`、`time_seconds`、`tokens`、`errors`
- `run_summary`：每种配置的统计汇总
  - `with_skill` / `without_skill`：各自包含 `pass_rate`、`time_seconds`、`tokens` 对象，带有 `mean` 和 `stddev` 字段
  - `delta`：差异字符串如 `"+0.50"`、`"+13.0"`、`"+1700"`
- `notes`：来自分析器的自由形式观察

**重要：** 查看器精确读取这些字段名。使用 `config` 而非 `configuration`，或把 `pass_rate` 放在 run 的顶层而非嵌套在 `result` 下，会导致查看器显示空/零值。手动生成 benchmark.json 时务必参考此 schema。

---

## comparison.json

盲评对比 Agent 的输出。位于 `<grading-dir>/comparison-N.json`。

```json
{
  "winner": "A",
  "reasoning": "输出 A 提供了完整的解决方案，格式正确且包含所有必需字段。输出 B 缺少日期字段且格式不一致。",
  "rubric": {
    "A": {
      "content": {
        "correctness": 5,
        "completeness": 5,
        "accuracy": 4
      },
      "structure": {
        "organization": 4,
        "formatting": 5,
        "usability": 4
      },
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {
        "correctness": 3,
        "completeness": 2,
        "accuracy": 3
      },
      "structure": {
        "organization": 3,
        "formatting": 2,
        "usability": 3
      },
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["完整的解决方案", "格式良好", "所有字段齐全"],
      "weaknesses": ["标题中有轻微样式不一致"]
    },
    "B": {
      "score": 5,
      "strengths": ["输出可读", "基本结构正确"],
      "weaknesses": ["缺少日期字段", "格式不一致", "数据提取不完整"]
    }
  },
  "expectation_results": {
    "A": {
      "passed": 4,
      "total": 5,
      "pass_rate": 0.80,
      "details": [
        {"text": "输出包含姓名", "passed": true}
      ]
    },
    "B": {
      "passed": 3,
      "total": 5,
      "pass_rate": 0.60,
      "details": [
        {"text": "输出包含姓名", "passed": true}
      ]
    }
  }
}
```

如果未提供预期，则完全省略 `expectation_results` 字段。

---

## analysis.json

事后分析 Agent 的输出。位于 `<grading-dir>/analysis.json`。

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "对比 Agent 选择胜出者的原因摘要"
  },
  "winner_strengths": [
    "处理多页文档的清晰分步指令",
    "包含了能捕获格式错误的验证脚本"
  ],
  "loser_weaknesses": [
    "模糊的指令'适当处理文档'导致了不一致的行为",
    "没有验证脚本，agent 不得不即兴发挥"
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": ["小问题：跳过了可选的日志记录步骤"]
    },
    "loser": {
      "score": 6,
      "issues": [
        "没有使用技能的格式模板",
        "自创方法而非遵循步骤 3"
      ]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "将'适当处理文档'替换为明确步骤",
      "expected_impact": "将消除导致不一致行为的模糊性"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "阅读技能 -> 遵循 5 步流程 -> 使用验证脚本",
    "loser_execution_pattern": "阅读技能 -> 方法不明确 -> 尝试 3 种不同方法"
  }
}
```

---

## feedback.json

用户通过查看器提交的反馈。

```json
{
  "reviews": [
    {
      "run_id": "eval-0-with_skill",
      "feedback": "图表缺少轴标签",
      "timestamp": "2026-03-13T12:30:00Z"
    },
    {
      "run_id": "eval-1-with_skill",
      "feedback": "",
      "timestamp": "2026-03-13T12:31:00Z"
    }
  ],
  "status": "complete"
}
```

- 空的 `feedback` 字符串表示用户认为该测试结果没问题
- `status` 为 `complete` 表示用户已完成所有审查
