// Public LLM benchmark scores, collected 2026-10-08. Source of truth: sources/public-scores.md
window.PUBLIC = {
 "meta": {
  "collected": "2026-10-08",
  "note": "Every number has src/url/date. Percent values are 0-100. Vendor = self-reported; AA/Epoch/Scale/Arena/swebench.com = measured by a third party."
 },
 "models": [
  {
   "id": "claude-opus-5-5",
   "name": "Claude Opus 5.5",
   "maker": "Anthropic",
   "released": "2026-09-22",
   "open": false,
   "aa": {
    "aaName": "Claude Opus 5.5 (Max, Default Fallback)",
    "setting": "max effort, default fallback",
    "intelligenceIndex": 57.6,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": null,
    "hle": 61.4,
    "priceInPerM": 4,
    "priceOutPerM": 20,
    "outputTokensPerSec": 95,
    "contextWindow": 1000000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 90.6,
    "stderr": 1.9,
    "setting": "max",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1503.7,
    "ci": [
     1494.6,
     1512.8
    ],
    "votes": 4552,
    "variant": "claude-opus-5.5-high",
    "rank": 4,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "vendor": [
    {
     "benchmark": "Humanity's Last Exam (with tools)",
     "value": 67.7,
     "setting": "adaptive thinking, max effort",
     "src": "Anthropic, Claude Opus 5.5 launch (vendor)",
     "url": "https://www.anthropic.com/claude-opus-5-5",
     "date": "2026-09-22"
    }
   ],
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "SWE-bench Verified (not in launch post; OpenAI and swebench.com no longer track new frontier models)",
    "AA GPQA (AA no longer reports GPQA for this model)"
   ]
  },
  {
   "id": "claude-sonnet-5-5",
   "name": "Claude Sonnet 5.5",
   "maker": "Anthropic",
   "released": "2026-09-28",
   "open": false,
   "aa": {
    "aaName": "Claude Sonnet 5.5 (Max, Default Fallback)",
    "setting": "max effort, default fallback",
    "intelligenceIndex": 56.0,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": null,
    "hle": 55.0,
    "priceInPerM": 2,
    "priceOutPerM": 10,
    "outputTokensPerSec": 129,
    "contextWindow": 1000000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 95.6,
    "stderr": 1.4,
    "setting": "max",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1471.0,
    "votes": 3145,
    "variant": "claude-sonnet-5.5-xhigh",
    "rank": 45,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "SWE-bench Verified",
    "vendor scores (launch post not fetched)"
   ]
  },
  {
   "id": "claude-fable-5-1",
   "name": "Claude Fable 5.1",
   "maker": "Anthropic",
   "released": "2026-09-01",
   "open": false,
   "aa": {
    "aaName": "Claude Fable 5.1 (Max, Default Fallback)",
    "setting": "max effort, default fallback",
    "intelligenceIndex": 53.4,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": 93.7,
    "hle": 59.1,
    "priceInPerM": 10,
    "priceOutPerM": 50,
    "outputTokensPerSec": 66,
    "contextWindow": 1000000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "scaleHle": {
    "value": 46.5,
    "ci": 2.0,
    "setting": "xhigh; full HLE incl. multimodal",
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   "arena": {
    "elo": 1501.1,
    "ci": [
     1494.7,
     1507.5
    ],
    "votes": 11800,
    "variant": "claude-fable-5.1-max",
    "rank": 6,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "vendor": [
    {
     "benchmark": "Humanity's Last Exam (no tools)",
     "value": 60.9,
     "setting": "effort level not stated",
     "src": "Anthropic, Claude Fable 5.1 launch (vendor)",
     "url": "https://www.anthropic.com/claude-fable-and-mythos-5-1",
     "date": "2026-09 (page shows month only)"
    },
    {
     "benchmark": "Humanity's Last Exam (with tools)",
     "value": 65.0,
     "setting": "effort level not stated",
     "src": "Anthropic, Claude Fable 5.1 launch (vendor)",
     "url": "https://www.anthropic.com/claude-fable-and-mythos-5-1",
     "date": "2026-09 (page shows month only)"
    }
   ],
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "SWE-bench Verified",
    "Epoch GPQA"
   ]
  },
  {
   "id": "gpt-6-astra",
   "name": "GPT-6 Astra",
   "maker": "OpenAI",
   "released": "2026-09-03",
   "open": false,
   "aa": {
    "aaName": "GPT-6 Astra (Max)",
    "setting": "max reasoning effort",
    "intelligenceIndex": 52.7,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": 96.1,
    "hle": 54.7,
    "priceInPerM": 10,
    "priceOutPerM": 50,
    "outputTokensPerSec": 48,
    "contextWindow": 1000000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 95.8,
    "stderr": 1.4,
    "setting": "max",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "scaleHle": {
    "value": 54.8,
    "ci": 1.94,
    "setting": "full HLE",
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   "arena": {
    "elo": 1477.1,
    "votes": 9156,
    "variant": "gpt-6-astra-max",
    "rank": 29,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "SWE-bench Verified (OpenAI stopped reporting it, 2026-02-23)",
    "vendor launch post (not fetched)"
   ]
  },
  {
   "id": "gpt-6-1-sol",
   "name": "GPT-6.1 Sol",
   "maker": "OpenAI",
   "released": "2026-09-29",
   "open": false,
   "aa": {
    "aaName": "GPT-6.1 Sol (Max)",
    "setting": "max reasoning effort",
    "intelligenceIndex": 51.8,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": null,
    "hle": 52.9,
    "priceInPerM": 2,
    "priceOutPerM": 10,
    "outputTokensPerSec": 55,
    "contextWindow": 1000000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 95.4,
    "stderr": 1.4,
    "setting": "max",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1483.2,
    "votes": 3071,
    "variant": "gpt-6.1-sol-max",
    "rank": 21,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "SWE-bench Verified"
   ]
  },
  {
   "id": "gemini-4-argon",
   "name": "Gemini 4 Argon",
   "maker": "Google",
   "released": "2026-09-30",
   "open": false,
   "aa": {
    "aaName": "Gemini 4 Argon (High)",
    "setting": "high thinking",
    "intelligenceIndex": 52.6,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": null,
    "hle": 57.1,
    "priceInPerM": 2,
    "priceOutPerM": 10,
    "outputTokensPerSec": null,
    "contextWindow": 1000000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "arena": {
    "elo": 1525.2,
    "ci": null,
    "votes": 4932,
    "variant": "gemini-4-argon-high",
    "rank": 1,
    "note": "marked pre_release (preliminary) on Arena",
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "SWE-bench Verified",
    "Epoch GPQA",
    "AA output speed (not yet measured)",
    "vendor launch post (not fetched)"
   ]
  },
  {
   "id": "grok-4-7",
   "name": "Grok 4.7",
   "maker": "xAI (listed as SpaceXAI on AA)",
   "released": "2026-09-21",
   "open": false,
   "aa": {
    "aaName": "Grok 4.7 (Xhigh)",
    "setting": "xhigh reasoning",
    "intelligenceIndex": 46.4,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": null,
    "hle": 43.1,
    "priceInPerM": 2,
    "priceOutPerM": 6,
    "outputTokensPerSec": 73,
    "contextWindow": 500000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 92.7,
    "stderr": 1.6,
    "setting": "xhigh",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1442.5,
    "votes": 6405,
    "variant": "grok-4.7-xhigh",
    "rank": 91,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "SWE-bench Verified"
   ]
  },
  {
   "id": "deepseek-v4-pro-0813",
   "name": "DeepSeek V4 Pro 0813",
   "maker": "DeepSeek",
   "released": "2026-08-13",
   "open": true,
   "aa": {
    "aaName": "DeepSeek V4 Pro 0813 (Max)",
    "setting": "max reasoning",
    "intelligenceIndex": 36.0,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": 92.8,
    "hle": 41.0,
    "priceInPerM": 1.32,
    "priceOutPerM": 3.96,
    "outputTokensPerSec": 100,
    "contextWindow": 1000000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 91.7,
    "stderr": 1.5,
    "setting": "max",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1464.3,
    "votes": 9780,
    "variant": "deepseek-v4-pro-high-20260813",
    "rank": 56,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "SWE-bench Verified for 0813 (Epoch has 77.6 for the April V4 Pro, max)"
   ]
  },
  {
   "id": "deepseek-v4-1-flash",
   "name": "DeepSeek V4.1 Flash (newest DeepSeek)",
   "maker": "DeepSeek",
   "released": "2026-09-10",
   "open": true,
   "aa": {
    "aaName": "DeepSeek V4.1 Flash (Max)",
    "setting": "max reasoning",
    "intelligenceIndex": 39.5,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": null,
    "hle": 39.2,
    "priceInPerM": 0.3,
    "priceOutPerM": 1.2,
    "outputTokensPerSec": 216,
    "contextWindow": 1000000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "arena": {
    "elo": 1474.4,
    "votes": 8728,
    "variant": "deepseek-v4.1-flash-max",
    "rank": 38,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "notFound": [
    "MMLU",
    "MMLU-Pro",
    "GPQA",
    "SWE-bench Verified"
   ]
  },
  {
   "id": "qwen3-8b",
   "name": "Qwen3-8B",
   "maker": "Alibaba (Qwen)",
   "released": "2025-04-28",
   "open": true,
   "local": true,
   "aa": {
    "aaName": "Qwen3 8B (Reasoning)",
    "setting": "thinking mode",
    "intelligenceIndex": 7.3,
    "intelligenceIndexEstimated": true,
    "gpqaDiamond": 58.9,
    "hle": 3.9,
    "priceInPerM": 0.18,
    "priceOutPerM": 2.1,
    "outputTokensPerSec": 40,
    "contextWindow": 131072,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "aaAlt": {
    "aaName": "Qwen3 8B (Non-reasoning)",
    "setting": "non-thinking mode",
    "intelligenceIndex": 6.0,
    "intelligenceIndexEstimated": true,
    "gpqaDiamond": 45.2,
    "hle": 1.9,
    "priceInPerM": 0.18,
    "priceOutPerM": 0.7,
    "outputTokensPerSec": 42,
    "contextWindow": 131072,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 56.8,
    "stderr": 2.9,
    "setting": "thinking (default)",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "epochGpqaAlt": {
    "value": 47.5,
    "stderr": 2.6,
    "setting": "thinking off (qwen3-8b_none)",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "vendor": [
    {
     "benchmark": "GPQA Diamond",
     "value": 62.0,
     "setting": "thinking mode, Table 17",
     "src": "Qwen3 Technical Report (vendor)",
     "url": "https://arxiv.org/abs/2505.09388",
     "date": "2025-05-14"
    },
    {
     "benchmark": "GPQA Diamond",
     "value": 39.3,
     "setting": "non-thinking mode, Table 18",
     "src": "Qwen3 Technical Report (vendor)",
     "url": "https://arxiv.org/abs/2505.09388",
     "date": "2025-05-14"
    },
    {
     "benchmark": "MMLU",
     "value": 76.89,
     "setting": "Qwen3-8B-Base, 5-shot, Table 6",
     "src": "Qwen3 Technical Report (vendor)",
     "url": "https://arxiv.org/abs/2505.09388",
     "date": "2025-05-14"
    },
    {
     "benchmark": "MMLU-Pro",
     "value": 56.73,
     "setting": "Qwen3-8B-Base, 5-shot CoT, Table 6",
     "src": "Qwen3 Technical Report (vendor)",
     "url": "https://arxiv.org/abs/2505.09388",
     "date": "2025-05-14"
    },
    {
     "benchmark": "MMLU-Redux",
     "value": 87.5,
     "setting": "thinking",
     "src": "Qwen3 Technical Report (vendor)",
     "url": "https://arxiv.org/abs/2505.09388",
     "date": "2025-05-14"
    },
    {
     "benchmark": "MMLU-Redux",
     "value": 79.5,
     "setting": "non-thinking",
     "src": "Qwen3 Technical Report (vendor)",
     "url": "https://arxiv.org/abs/2505.09388",
     "date": "2025-05-14"
    }
   ],
   "notFound": [
    "Arena text Elo (Qwen3-8B not on the board)",
    "SWE-bench Verified"
   ]
  },
  {
   "id": "llama-3-1-8b",
   "name": "Llama 3.1 8B Instruct",
   "maker": "Meta",
   "released": "2024-07-23",
   "open": true,
   "local": true,
   "aa": {
    "aaName": "Llama 3.1 Instruct 8B",
    "setting": "instruct",
    "intelligenceIndex": 6.9,
    "intelligenceIndexEstimated": true,
    "gpqaDiamond": 25.9,
    "hle": 5.3,
    "priceInPerM": 0.02,
    "priceOutPerM": 0.05,
    "outputTokensPerSec": 138,
    "contextWindow": 128000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 27.0,
    "stderr": 1.9,
    "setting": "default",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1211.2,
    "votes": 49605,
    "variant": "llama-3.1-8b-instruct",
    "rank": 340,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "vendor": [
    {
     "benchmark": "MMLU",
     "value": 69.4,
     "setting": "5-shot, macro_avg/acc",
     "src": "Meta Llama 3.1 8B Instruct model card (vendor)",
     "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
     "date": "2024-07-23"
    },
    {
     "benchmark": "MMLU (CoT)",
     "value": 73.0,
     "setting": "0-shot CoT",
     "src": "Meta Llama 3.1 8B Instruct model card (vendor)",
     "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
     "date": "2024-07-23"
    },
    {
     "benchmark": "MMLU-Pro (CoT)",
     "value": 48.3,
     "setting": "5-shot",
     "src": "Meta Llama 3.1 8B Instruct model card (vendor)",
     "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
     "date": "2024-07-23"
    },
    {
     "benchmark": "GPQA",
     "value": 30.4,
     "setting": "0-shot, em",
     "src": "Meta Llama 3.1 8B Instruct model card (vendor)",
     "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
     "date": "2024-07-23"
    }
   ],
   "other": [
    {
     "benchmark": "MMLU",
     "value": 56.1,
     "setting": "5-shot, HELM Lite, \"Llama 3.1 Instruct Turbo (8B)\" endpoint (Epoch notes Turbo looks quantized)",
     "src": "Stanford HELM Lite MMLU (via Epoch AI external data)",
     "url": "https://crfm.stanford.edu/helm/lite/latest/#/leaderboard/mmlu",
     "date": "accessed via Epoch 2026-10-08"
    }
   ],
   "notFound": [
    "SWE-bench Verified"
   ]
  },
  {
   "id": "llama-3-3-70b",
   "name": "Llama 3.3 70B Instruct",
   "maker": "Meta",
   "released": "2024-12-06",
   "open": true,
   "local": true,
   "aa": {
    "aaName": "Llama 3.3 Instruct 70B",
    "setting": "instruct",
    "intelligenceIndex": 7.7,
    "intelligenceIndexEstimated": true,
    "gpqaDiamond": 49.8,
    "hle": 3.6,
    "priceInPerM": 0.71,
    "priceOutPerM": 0.72,
    "outputTokensPerSec": 83,
    "contextWindow": 128000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 47.4,
    "stderr": 2.9,
    "setting": "default (run 2025-01-27)",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1317.8,
    "votes": 54366,
    "variant": "llama-3.3-70b-instruct",
    "rank": 261,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "vendor": [
    {
     "benchmark": "MMLU (CoT)",
     "value": 86.0,
     "setting": "0-shot",
     "src": "Meta Llama 3.3 70B Instruct model card (vendor)",
     "url": "https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct",
     "date": "2024-12-06"
    },
    {
     "benchmark": "MMLU-Pro (CoT)",
     "value": 68.9,
     "setting": "5-shot",
     "src": "Meta Llama 3.3 70B Instruct model card (vendor)",
     "url": "https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct",
     "date": "2024-12-06"
    },
    {
     "benchmark": "GPQA Diamond (CoT)",
     "value": 50.5,
     "setting": "0-shot",
     "src": "Meta Llama 3.3 70B Instruct model card (vendor)",
     "url": "https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct",
     "date": "2024-12-06"
    }
   ],
   "other": [
    {
     "benchmark": "MMLU",
     "value": 79.1,
     "setting": "5-shot, HELM Lite, Turbo endpoint",
     "src": "Stanford HELM Lite MMLU (via Epoch AI external data)",
     "url": "https://crfm.stanford.edu/helm/lite/latest/#/leaderboard/mmlu",
     "date": "accessed via Epoch 2026-10-08"
    }
   ],
   "notFound": [
    "SWE-bench Verified"
   ]
  },
  {
   "id": "phi-4-mini",
   "name": "Phi-4-mini-instruct (3.8B)",
   "maker": "Microsoft",
   "released": "2025-02",
   "open": true,
   "local": true,
   "aa": {
    "aaName": "Phi-4 Mini Instruct",
    "setting": "instruct; AA lists price $0 (no paid endpoint)",
    "intelligenceIndex": 6.3,
    "intelligenceIndexEstimated": true,
    "gpqaDiamond": 33.1,
    "hle": 4.5,
    "priceInPerM": 0,
    "priceOutPerM": 0,
    "outputTokensPerSec": 46,
    "contextWindow": 128000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "vendor": [
    {
     "benchmark": "MMLU",
     "value": 67.3,
     "setting": "5-shot",
     "src": "Microsoft Phi-4-mini-instruct model card (vendor)",
     "url": "https://huggingface.co/microsoft/Phi-4-mini-instruct",
     "date": "2025-02"
    },
    {
     "benchmark": "MMLU-Pro",
     "value": 52.8,
     "setting": "0-shot, CoT",
     "src": "Microsoft Phi-4-mini-instruct model card (vendor)",
     "url": "https://huggingface.co/microsoft/Phi-4-mini-instruct",
     "date": "2025-02"
    },
    {
     "benchmark": "GPQA",
     "value": 25.2,
     "setting": "0-shot, CoT",
     "src": "Microsoft Phi-4-mini-instruct model card (vendor)",
     "url": "https://huggingface.co/microsoft/Phi-4-mini-instruct",
     "date": "2025-02"
    }
   ],
   "notFound": [
    "Arena Elo (only Phi-4 14B is listed: 1256.3)",
    "Epoch GPQA",
    "SWE-bench Verified"
   ]
  },
  {
   "id": "gemma-3-4b",
   "name": "Gemma 3 4B IT",
   "maker": "Google",
   "released": "2025-03-12",
   "open": true,
   "local": true,
   "aa": {
    "aaName": "Gemma 3 4B Instruct",
    "setting": "instruct; AA lists price $0 (no paid endpoint)",
    "intelligenceIndex": 4.8,
    "intelligenceIndexEstimated": true,
    "gpqaDiamond": 29.1,
    "hle": 5.3,
    "priceInPerM": 0,
    "priceOutPerM": 0,
    "outputTokensPerSec": null,
    "contextWindow": 128000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 23.2,
    "stderr": 1.9,
    "setting": "default",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1303.2,
    "votes": 4171,
    "variant": "gemma-3-4b-it",
    "rank": 281,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "vendor": [
    {
     "benchmark": "GPQA Diamond",
     "value": 30.8,
     "setting": "IT, 0-shot",
     "src": "Gemma 3 Technical Report, Table 6 (vendor)",
     "url": "https://arxiv.org/abs/2503.19786",
     "date": "2025-03-25"
    },
    {
     "benchmark": "MMLU-Pro",
     "value": 43.6,
     "setting": "IT, 0-shot",
     "src": "Gemma 3 Technical Report, Table 6 (vendor)",
     "url": "https://arxiv.org/abs/2503.19786",
     "date": "2025-03-25"
    }
   ],
   "notFound": [
    "MMLU (IT)",
    "SWE-bench Verified"
   ]
  },
  {
   "id": "gemma-3-12b",
   "name": "Gemma 3 12B IT",
   "maker": "Google",
   "released": "2025-03-12",
   "open": true,
   "local": true,
   "aa": {
    "aaName": "Gemma 3 12B Instruct",
    "setting": "instruct; AA lists price $0 (no paid endpoint)",
    "intelligenceIndex": 3.8,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": 34.9,
    "hle": 4.2,
    "priceInPerM": 0,
    "priceOutPerM": 0,
    "outputTokensPerSec": null,
    "contextWindow": 128000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 39.5,
    "stderr": 2.5,
    "setting": "default",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1341.8,
    "votes": 3829,
    "variant": "gemma-3-12b-it",
    "rank": 230,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "vendor": [
    {
     "benchmark": "GPQA Diamond",
     "value": 40.9,
     "setting": "IT, 0-shot",
     "src": "Gemma 3 Technical Report, Table 6 (vendor)",
     "url": "https://arxiv.org/abs/2503.19786",
     "date": "2025-03-25"
    },
    {
     "benchmark": "MMLU-Pro",
     "value": 60.6,
     "setting": "IT, 0-shot",
     "src": "Gemma 3 Technical Report, Table 6 (vendor)",
     "url": "https://arxiv.org/abs/2503.19786",
     "date": "2025-03-25"
    }
   ],
   "notFound": [
    "MMLU (IT)",
    "SWE-bench Verified"
   ]
  },
  {
   "id": "gemma-3-27b",
   "name": "Gemma 3 27B IT",
   "maker": "Google",
   "released": "2025-03-12",
   "open": true,
   "local": true,
   "aa": {
    "aaName": "Gemma 3 27B Instruct",
    "setting": "instruct; AA lists price $0 (no paid endpoint)",
    "intelligenceIndex": 4.9,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": 42.8,
    "hle": 4.4,
    "priceInPerM": 0,
    "priceOutPerM": 0,
    "outputTokensPerSec": null,
    "contextWindow": 128000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 47.7,
    "stderr": 2.7,
    "setting": "default",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1365.4,
    "votes": 46425,
    "variant": "gemma-3-27b-it",
    "rank": 197,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "vendor": [
    {
     "benchmark": "GPQA Diamond",
     "value": 42.4,
     "setting": "IT, 0-shot",
     "src": "Gemma 3 Technical Report, Table 6 (vendor)",
     "url": "https://arxiv.org/abs/2503.19786",
     "date": "2025-03-25"
    },
    {
     "benchmark": "MMLU-Pro",
     "value": 67.5,
     "setting": "IT, 0-shot",
     "src": "Gemma 3 Technical Report, Table 6 (vendor)",
     "url": "https://arxiv.org/abs/2503.19786",
     "date": "2025-03-25"
    },
    {
     "benchmark": "LMSys Chatbot Arena Elo",
     "value": 1338,
     "setting": "preliminary, received 2025-03-08 (older rating scale)",
     "src": "Gemma 3 Technical Report, Table 6 (vendor)",
     "url": "https://arxiv.org/abs/2503.19786",
     "date": "2025-03-25"
    }
   ],
   "notFound": [
    "MMLU (IT)",
    "SWE-bench Verified"
   ]
  },
  {
   "id": "mistral-small-3-2",
   "name": "Mistral Small 3.2 (24B, 2506)",
   "maker": "Mistral AI",
   "released": "2025-06-20",
   "open": true,
   "local": true,
   "aa": {
    "aaName": "Mistral Small 3.2",
    "setting": "instruct",
    "intelligenceIndex": 8.2,
    "intelligenceIndexEstimated": true,
    "gpqaDiamond": 50.5,
    "hle": 4.3,
    "priceInPerM": 0.075,
    "priceOutPerM": 0.2,
    "outputTokensPerSec": null,
    "contextWindow": 128000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "epochGpqa": {
    "value": 49.1,
    "stderr": 2.8,
    "setting": "default",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   "arena": {
    "elo": 1356.5,
    "votes": 17348,
    "variant": "mistral-small-2506",
    "rank": 207,
    "src": "Arena (ex-LMArena), text, style control default",
    "url": "https://arena.ai/leaderboard/text",
    "date": "snapshot published 2026-10-02, accessed 2026-10-08"
   },
   "vendor": [
    {
     "benchmark": "MMLU",
     "value": 80.5,
     "setting": "shots not stated",
     "src": "Mistral Small 3.2 model card (vendor)",
     "url": "https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506",
     "date": "2025-06-20"
    },
    {
     "benchmark": "MMLU-Pro",
     "value": 69.06,
     "setting": "5-shot CoT",
     "src": "Mistral Small 3.2 model card (vendor)",
     "url": "https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506",
     "date": "2025-06-20"
    },
    {
     "benchmark": "GPQA Diamond",
     "value": 46.13,
     "setting": "5-shot CoT",
     "src": "Mistral Small 3.2 model card (vendor)",
     "url": "https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506",
     "date": "2025-06-20"
    }
   ],
   "notFound": [
    "SWE-bench Verified"
   ]
  },
  {
   "id": "mistral-small-4",
   "name": "Mistral Small 4 (newest Mistral Small)",
   "maker": "Mistral AI",
   "released": "2026-03-16",
   "open": true,
   "aa": {
    "aaName": "Mistral Small 4 (Reasoning)",
    "setting": "reasoning",
    "intelligenceIndex": 11.3,
    "intelligenceIndexEstimated": false,
    "gpqaDiamond": 76.9,
    "hle": 9.9,
    "priceInPerM": 0.15,
    "priceOutPerM": 0.6,
    "outputTokensPerSec": 160,
    "contextWindow": 256000,
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   "notFound": [
    "vendor scores",
    "Arena Elo",
    "Epoch GPQA"
   ]
  }
 ],
 "selfVsIndependent": [
  {
   "model": "Claude Fable 5.1",
   "benchmark": "Humanity's Last Exam, no tools",
   "vendor": {
    "value": 60.9,
    "setting": "effort not stated",
    "src": "Anthropic, Claude Fable 5.1 launch (vendor)",
    "url": "https://www.anthropic.com/claude-fable-and-mythos-5-1",
    "date": "2026-09 (page shows month only)"
   },
   "independent": [
    {
     "value": 46.5,
     "setting": "xhigh; all 2,500 public questions incl. multimodal; o3-mini grader; ±2.0",
     "src": "Scale Labs HLE leaderboard",
     "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
     "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
    },
    {
     "value": 59.1,
     "setting": "max effort; 2,158 text-only questions; pass@1",
     "src": "Artificial Analysis",
     "url": "https://artificialanalysis.ai/evaluations/humanitys-last-exam",
     "date": "accessed 2026-10-08"
    }
   ],
   "lesson": "Same model, same benchmark name, three numbers: 46.5 / 59.1 / 60.9. Subset (text-only vs full) and effort level explain most of it."
  },
  {
   "model": "Qwen3-8B",
   "benchmark": "GPQA Diamond",
   "vendor": {
    "value": 62.0,
    "setting": "thinking mode (Table 17); non-thinking 39.3 (Table 18)",
    "src": "Qwen3 Technical Report (vendor)",
    "url": "https://arxiv.org/abs/2505.09388",
    "date": "2025-05-14"
   },
   "independent": [
    {
     "value": 56.8,
     "setting": "thinking; ±2.9 (non-thinking: 47.5 ±2.6)",
     "src": "Epoch AI (GPQA Diamond)",
     "url": "https://epoch.ai/benchmarks/gpqa-diamond",
     "date": "last updated 2026-09-29"
    },
    {
     "value": 58.9,
     "setting": "reasoning (non-reasoning: 45.2)",
     "src": "Artificial Analysis",
     "url": "https://artificialanalysis.ai/leaderboards/models",
     "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
    }
   ],
   "lesson": "Vendor is higher in thinking mode but LOWER than both independents in non-thinking mode: the gap is not always in the vendor's favour."
  },
  {
   "model": "Gemma 3 4B IT",
   "benchmark": "GPQA Diamond",
   "vendor": {
    "value": 30.8,
    "setting": "IT, 0-shot",
    "src": "Gemma 3 Technical Report, Table 6 (vendor)",
    "url": "https://arxiv.org/abs/2503.19786",
    "date": "2025-03-25"
   },
   "independent": [
    {
     "value": 23.2,
     "setting": "±1.9 (below the 25% random-guess line)",
     "src": "Epoch AI (GPQA Diamond)",
     "url": "https://epoch.ai/benchmarks/gpqa-diamond",
     "date": "last updated 2026-09-29"
    },
    {
     "value": 29.1,
     "setting": "",
     "src": "Artificial Analysis",
     "url": "https://artificialanalysis.ai/leaderboards/models",
     "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
    }
   ],
   "lesson": "Near the 25% floor of a 4-option test, small setup differences decide whether a model looks better than chance."
  },
  {
   "model": "Llama 3.1 8B Instruct",
   "benchmark": "MMLU (5-shot)",
   "vendor": {
    "value": 69.4,
    "setting": "5-shot, macro_avg/acc",
    "src": "Meta Llama 3.1 8B Instruct model card (vendor)",
    "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
    "date": "2024-07-23"
   },
   "independent": [
    {
     "value": 56.1,
     "setting": "5-shot, HELM Lite, served \"Turbo\" endpoint (likely quantized)",
     "src": "Stanford HELM Lite MMLU (via Epoch AI external data)",
     "url": "https://crfm.stanford.edu/helm/lite/latest/#/leaderboard/mmlu",
     "date": "accessed via Epoch 2026-10-08"
    },
    {
     "value": 68.1,
     "setting": "5-shot, measured by Microsoft in the Phi-4-mini card (a competitor, not independent)",
     "src": "Microsoft Phi-4-mini-instruct model card (vendor)",
     "url": "https://huggingface.co/microsoft/Phi-4-mini-instruct",
     "date": "2025-02"
    }
   ],
   "lesson": "The model you test is the model as served: a quantized endpoint can cost 13 points."
  },
  {
   "model": "Phi-4-mini-instruct",
   "benchmark": "GPQA (Diamond)",
   "vendor": {
    "value": 25.2,
    "setting": "0-shot CoT",
    "src": "Microsoft Phi-4-mini-instruct model card (vendor)",
    "url": "https://huggingface.co/microsoft/Phi-4-mini-instruct",
    "date": "2025-02"
   },
   "independent": [
    {
     "value": 33.1,
     "setting": "GPQA Diamond",
     "src": "Artificial Analysis",
     "url": "https://artificialanalysis.ai/leaderboards/models",
     "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
    }
   ],
   "lesson": "Independent higher than vendor; vendors sometimes under-report."
  },
  {
   "model": "Gemini 3 Pro (Preview)",
   "benchmark": "SWE-bench Verified",
   "vendor": {
    "value": 76.2,
    "setting": "harness not stated in blog",
    "src": "Google, Gemini 3 launch blog (vendor)",
    "url": "https://blog.google/products/gemini/gemini-3/",
    "date": "2025-11-18"
   },
   "independent": [
    {
     "value": 74.2,
     "setting": "mini-SWE-agent v1.15.0 (bash only), 2025-11-18",
     "src": "SWE-bench Verified leaderboard (swebench.com)",
     "url": "https://www.swebench.com/",
     "date": "accessed 2026-10-08; latest entry 2026-02-26"
    },
    {
     "value": 69.6,
     "setting": "mini-SWE-agent v2.0.0, high, 2026-02-26",
     "src": "SWE-bench Verified leaderboard (swebench.com)",
     "url": "https://www.swebench.com/",
     "date": "accessed 2026-10-08; latest entry 2026-02-26"
    },
    {
     "value": 72.9,
     "setting": "Epoch run 2026-02-13",
     "src": "Epoch AI Benchmarking Hub",
     "url": "https://epoch.ai/data/benchmark_data.zip",
     "date": "hub updated 2026-10-08"
    }
   ],
   "lesson": "Contrast: the same launch reported HLE 37.5% (no tools) and Scale measured 37.52% - sometimes vendor and independent agree exactly."
  },
  {
   "model": "Mistral Small 3.1 (2503)",
   "benchmark": "GPQA Diamond",
   "vendor": {
    "value": 45.96,
    "setting": "5-shot CoT",
    "src": "Mistral Small 3.2 model card (vendor)",
    "url": "https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506",
    "date": "2025-06-20"
   },
   "independent": [
    {
     "value": 47.5,
     "setting": "Epoch run 2025-03-18 (mistral-small-2503), ±2.8",
     "src": "Epoch AI (GPQA Diamond)",
     "url": "https://epoch.ai/benchmarks/gpqa-diamond",
     "date": "last updated 2026-09-29"
    },
    {
     "value": 41.9,
     "setting": "Epoch run 2026-08-30 (mistral-small-3.1-2503), ±2.3",
     "src": "Epoch AI (GPQA Diamond)",
     "url": "https://epoch.ai/benchmarks/gpqa-diamond",
     "date": "last updated 2026-09-29"
    }
   ],
   "lesson": "Even one independent evaluator gets 47.5 and 41.9 for the same weights, 17 months apart."
  }
 ],
 "settings": {
  "thinking": [
   {
    "model": "Qwen3-8B",
    "benchmark": "AIME'24",
    "on": 76.0,
    "off": 29.1,
    "src": "Qwen3 Technical Report (vendor)",
    "url": "https://arxiv.org/abs/2505.09388",
    "date": "2025-05-14"
   },
   {
    "model": "Qwen3-8B",
    "benchmark": "AIME'25",
    "on": 67.3,
    "off": 20.9,
    "src": "Qwen3 Technical Report (vendor)",
    "url": "https://arxiv.org/abs/2505.09388",
    "date": "2025-05-14"
   },
   {
    "model": "Qwen3-8B",
    "benchmark": "GPQA Diamond",
    "on": 62.0,
    "off": 39.3,
    "src": "Qwen3 Technical Report (vendor)",
    "url": "https://arxiv.org/abs/2505.09388",
    "date": "2025-05-14"
   },
   {
    "model": "Qwen3-8B",
    "benchmark": "LiveCodeBench v5",
    "on": 57.5,
    "off": 22.8,
    "src": "Qwen3 Technical Report (vendor)",
    "url": "https://arxiv.org/abs/2505.09388",
    "date": "2025-05-14"
   },
   {
    "model": "Qwen3-8B",
    "benchmark": "MMLU-Redux",
    "on": 87.5,
    "off": 79.5,
    "src": "Qwen3 Technical Report (vendor)",
    "url": "https://arxiv.org/abs/2505.09388",
    "date": "2025-05-14"
   },
   {
    "model": "Qwen3-8B",
    "benchmark": "IFEval strict prompt",
    "on": 85.0,
    "off": 83.0,
    "src": "Qwen3 Technical Report (vendor)",
    "url": "https://arxiv.org/abs/2505.09388",
    "date": "2025-05-14"
   },
   {
    "model": "Qwen3-8B",
    "benchmark": "Mock AIME 2024-25 (Epoch)",
    "on": 56.1,
    "off": 22.2,
    "src": "Epoch AI Benchmarking Hub",
    "url": "https://epoch.ai/data/benchmark_data.zip",
    "date": "hub updated 2026-10-08"
   },
   {
    "model": "Claude Opus 4.6",
    "benchmark": "HLE (Scale)",
    "on": 34.44,
    "off": 19.0,
    "note": "thinking-max vs non-thinking",
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "model": "Claude Opus 4.5",
    "benchmark": "HLE (Scale)",
    "on": 25.2,
    "off": 14.16,
    "note": "thinking vs non-thinking",
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "model": "Claude Sonnet 4.5",
    "benchmark": "HLE (Scale)",
    "on": 13.72,
    "off": 7.52,
    "note": "thinking vs non-thinking",
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "model": "DeepSeek V4 Pro (0424)",
    "benchmark": "GPQA Diamond (Epoch)",
    "on": 90.9,
    "off": 73.2,
    "note": "high vs none",
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   {
    "model": "DeepSeek V4 Pro (0424)",
    "benchmark": "Mock AIME 2024-25 (Epoch)",
    "on": 95.6,
    "off": 46.7,
    "note": "high vs none",
    "src": "Epoch AI Benchmarking Hub",
    "url": "https://epoch.ai/data/benchmark_data.zip",
    "date": "hub updated 2026-10-08"
   },
   {
    "model": "GPT-6 Sol",
    "benchmark": "AA Intelligence Index",
    "on": 47.6,
    "off": 28.5,
    "note": "max vs non-reasoning",
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   {
    "model": "DeepSeek V4 Pro 0813",
    "benchmark": "AA Intelligence Index",
    "on": 36.0,
    "off": 20.4,
    "note": "max vs non-reasoning",
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   }
  ],
  "effort": [
   {
    "model": "Claude Opus 5.5",
    "benchmark": "AA Intelligence Index",
    "levels": {
     "low": 42.3,
     "medium": 51.2,
     "high": 53.6,
     "xhigh": 56.0,
     "max": 57.6
    },
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   {
    "model": "Claude Opus 5.5",
    "benchmark": "HLE (AA, text-only)",
    "levels": {
     "low": 48.3,
     "medium": 54.7,
     "high": 55.6,
     "xhigh": 57.5,
     "max": 61.4
    },
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   {
    "model": "Claude Sonnet 5.5",
    "benchmark": "AA Intelligence Index",
    "levels": {
     "low": 35.9,
     "medium": 40.8,
     "high": 46.8,
     "xhigh": 51.9,
     "max": 56.0
    },
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   {
    "model": "GPT-6 Astra",
    "benchmark": "GPQA Diamond (AA)",
    "levels": {
     "low": 93.1,
     "medium": 93.9,
     "high": 94.9,
     "xhigh": 96.3,
     "max": 96.1
    },
    "note": "saturated: max is not above xhigh",
    "src": "Artificial Analysis",
    "url": "https://artificialanalysis.ai/leaderboards/models",
    "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
   },
   {
    "model": "Claude Opus 5",
    "benchmark": "GPQA Diamond (Epoch)",
    "levels": {
     "low": 87.9,
     "default": 92.9,
     "max": 93.9
    },
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   },
   {
    "model": "Claude Fable 5",
    "benchmark": "GPQA Diamond (Epoch)",
    "levels": {
     "low": 78.8,
     "high": 83.3,
     "max": 85.9
    },
    "src": "Epoch AI (GPQA Diamond)",
    "url": "https://epoch.ai/benchmarks/gpqa-diamond",
    "date": "last updated 2026-09-29"
   }
  ],
  "passk": [
   {
    "model": "DeepSeek-R1-Zero",
    "benchmark": "AIME 2024",
    "pass1": 71.0,
    "consk": 86.7,
    "k": 64,
    "src": "DeepSeek-R1 paper (vendor)",
    "url": "https://arxiv.org/abs/2501.12948",
    "date": "2025-01-22"
   },
   {
    "model": "OpenAI o1-0912",
    "benchmark": "AIME 2024",
    "pass1": 74.4,
    "consk": 83.3,
    "k": 64,
    "note": "as reported in the DeepSeek-R1 paper",
    "src": "DeepSeek-R1 paper (vendor)",
    "url": "https://arxiv.org/abs/2501.12948",
    "date": "2025-01-22"
   },
   {
    "model": "OpenAI o1-mini",
    "benchmark": "AIME 2024",
    "pass1": 63.6,
    "consk": 80.0,
    "k": 64,
    "note": "as reported in the DeepSeek-R1 paper",
    "src": "DeepSeek-R1 paper (vendor)",
    "url": "https://arxiv.org/abs/2501.12948",
    "date": "2025-01-22"
   },
   {
    "model": "DeepSeek-R1",
    "benchmark": "how pass@1 is computed",
    "note": "temperature 0.6, top-p 0.95, k = 4 to 64 samples per question, pass@1 = mean correctness over the k samples; R1 AIME 2024 pass@1 = 79.8",
    "src": "DeepSeek-R1 paper (vendor)",
    "url": "https://arxiv.org/abs/2501.12948",
    "date": "2025-01-22"
   },
   {
    "model": "Qwen3-235B-A22B",
    "benchmark": "AIME'24",
    "pass1": 85.7,
    "note": "footnote: \"we sample 64 times for each query and report the average of the accuracy\"",
    "src": "Qwen3 launch blog (vendor)",
    "url": "https://qwenlm.github.io/blog/qwen3/",
    "date": "2025-04-29"
   }
  ],
  "shots": [
   {
    "model": "Llama 3.1 8B Instruct",
    "benchmark": "MMLU",
    "fewShot": {
     "shots": 5,
     "value": 69.4
    },
    "zeroShotCoT": {
     "shots": 0,
     "value": 73.0
    },
    "src": "Meta Llama 3.1 8B Instruct model card (vendor)",
    "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
    "date": "2024-07-23"
   },
   {
    "model": "Llama 3.1 70B Instruct",
    "benchmark": "MMLU",
    "fewShot": {
     "shots": 5,
     "value": 83.6
    },
    "zeroShotCoT": {
     "shots": 0,
     "value": 86.0
    },
    "src": "Meta Llama 3.1 8B Instruct model card (vendor)",
    "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
    "date": "2024-07-23"
   },
   {
    "model": "Llama 3.1 405B Instruct",
    "benchmark": "MMLU",
    "fewShot": {
     "shots": 5,
     "value": 87.3
    },
    "zeroShotCoT": {
     "shots": 0,
     "value": 88.6
    },
    "src": "Meta Llama 3.1 8B Instruct model card (vendor)",
    "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
    "date": "2024-07-23"
   }
  ],
  "tools": [
   {
    "model": "Claude Fable 5.1",
    "benchmark": "HLE",
    "noTools": 60.9,
    "withTools": 65.0,
    "src": "Anthropic, Claude Fable 5.1 launch (vendor)",
    "url": "https://www.anthropic.com/claude-fable-and-mythos-5-1",
    "date": "2026-09 (page shows month only)"
   },
   {
    "model": "Claude Fable 5",
    "benchmark": "HLE",
    "noTools": 57.8,
    "withTools": 63.8,
    "src": "Anthropic, Claude Fable 5.1 launch (vendor)",
    "url": "https://www.anthropic.com/claude-fable-and-mythos-5-1",
    "date": "2026-09 (page shows month only)"
   },
   {
    "model": "Claude Opus 5",
    "benchmark": "HLE",
    "noTools": 56.6,
    "withTools": 63.6,
    "src": "Anthropic, Claude Fable 5.1 launch (vendor)",
    "url": "https://www.anthropic.com/claude-fable-and-mythos-5-1",
    "date": "2026-09 (page shows month only)"
   }
  ],
  "harness": [
   {
    "model": "Claude Sonnet 4 (20250514)",
    "benchmark": "SWE-bench Verified",
    "runs": [
     {
      "agent": "SWE-agent",
      "value": 66.6,
      "date": "2025-05-22"
     },
     {
      "agent": "mini-SWE-agent 1.0.0 (bash only)",
      "value": 64.93,
      "date": "2025-07-26"
     },
     {
      "agent": "OpenHands",
      "value": 70.4,
      "date": "2025-05-24"
     },
     {
      "agent": "Moatless Tools",
      "value": 70.8,
      "date": "2025-06-11"
     },
     {
      "agent": "Bloop",
      "value": 71.2,
      "date": "2025-07-10"
     },
     {
      "agent": "Tools (Anthropic)",
      "value": 72.4,
      "date": "2025-05-22"
     },
     {
      "agent": "Lingxi v1.5",
      "value": 74.6,
      "date": "2025-07-20"
     },
     {
      "agent": "EPAM AI/Run Developer Agent (2+ attempts)",
      "value": 76.8,
      "date": "2025-08-04"
     }
    ],
    "src": "SWE-bench Verified leaderboard (swebench.com)",
    "url": "https://www.swebench.com/",
    "date": "accessed 2026-10-08; latest entry 2026-02-26"
   },
   {
    "model": "GPT-4o (2024-05-13)",
    "benchmark": "SWE-bench Verified",
    "runs": [
     {
      "agent": "SWE-agent",
      "value": 23.2,
      "date": "2024-07-28"
     },
     {
      "agent": "AppMap Navie",
      "value": 26.2,
      "date": "2024-06-15"
     },
     {
      "agent": "AutoCodeRover v20240620",
      "value": 38.4,
      "date": "2024-06-28"
     },
     {
      "agent": "Agentless-1.5",
      "value": 38.8,
      "date": "2024-10-28"
     }
    ],
    "src": "SWE-bench Verified leaderboard (swebench.com)",
    "url": "https://www.swebench.com/",
    "date": "accessed 2026-10-08; latest entry 2026-02-26"
   },
   {
    "model": "Gemini 3 Pro Preview",
    "benchmark": "SWE-bench Verified",
    "runs": [
     {
      "agent": "mini-SWE-agent 2.0.0",
      "value": 69.6,
      "date": "2026-02-26"
     },
     {
      "agent": "mini-SWE-agent 1.15.0",
      "value": 74.2,
      "date": "2025-11-18"
     },
     {
      "agent": "live-SWE-agent (UIUC)",
      "value": 77.4,
      "date": "2025-11-20"
     }
    ],
    "src": "SWE-bench Verified leaderboard (swebench.com)",
    "url": "https://www.swebench.com/",
    "date": "accessed 2026-10-08; latest entry 2026-02-26"
   },
   {
    "model": "Claude Opus 4.5",
    "benchmark": "SWE-bench Verified",
    "runs": [
     {
      "agent": "mini-SWE-agent 1.16.0, medium",
      "value": 74.4,
      "date": "2025-11-24"
     },
     {
      "agent": "mini-SWE-agent 2.0.0, high",
      "value": 76.8,
      "date": "2026-02-17"
     },
     {
      "agent": "live-SWE-agent (UIUC), medium",
      "value": 79.2,
      "date": "2025-12-15"
     },
     {
      "agent": "Sonar Foundation Agent",
      "value": 79.2,
      "date": "2025-12-05"
     }
    ],
    "src": "SWE-bench Verified leaderboard (swebench.com)",
    "url": "https://www.swebench.com/",
    "date": "accessed 2026-10-08; latest entry 2026-02-26"
   }
  ]
 },
 "timeline": {
  "arenaNo1": [
   {
    "on": "2023-05-10",
    "model": "GPT-4",
    "org": "OpenAI",
    "elo": 1274,
    "src": "LMSYS blog",
    "url": "https://lmsys.org/blog/2023-05-10-leaderboard/",
    "date": "2023-05-10",
    "note": "Elo scale (pre-2024)"
   },
   {
    "on": "2023-12-07",
    "model": "GPT-4-Turbo",
    "org": "OpenAI",
    "elo": 1217,
    "src": "LMSYS blog",
    "url": "https://lmsys.org/blog/2023-12-07-leaderboard/",
    "date": "2023-12-07",
    "note": "Elo scale; ratings were recomputed between posts"
   },
   {
    "on": "2024-02-02",
    "model": "gpt-4-0125-preview",
    "org": "OpenAI",
    "elo": 1253.0,
    "note": "raw text leaderboard (no style control); Bradley-Terry since 2024-01-09",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2024-02-15",
    "model": "gpt-4-1106-preview",
    "org": "OpenAI",
    "elo": 1253.6,
    "note": "raw text leaderboard (no style control); Bradley-Terry since 2024-01-09",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2024-03-26",
    "model": "claude-3-opus-20240229",
    "org": "Anthropic",
    "elo": 1253.2,
    "note": "raw text leaderboard (no style control); Bradley-Terry since 2024-01-09",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2024-04-11",
    "model": "gpt-4-turbo-2024-04-09",
    "org": "OpenAI",
    "elo": 1260.7,
    "note": "raw text leaderboard (no style control); Bradley-Terry since 2024-01-09",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2024-05-15",
    "model": "gpt-4o-2024-05-13",
    "org": "OpenAI",
    "elo": 1289.2,
    "note": "raw text leaderboard (no style control); Bradley-Terry since 2024-01-09",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2024-08-22",
    "model": "chatgpt-4o-latest",
    "org": "OpenAI",
    "elo": 1316.8,
    "note": "raw text leaderboard (no style control); Bradley-Terry since 2024-01-09",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2024-08-28",
    "model": "chatgpt-4o-latest",
    "org": "OpenAI",
    "elo": 1288.8,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2024-09-17",
    "model": "o1-preview",
    "org": "OpenAI",
    "elo": 1325.7,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2024-12-30",
    "model": "o1-2024-12-17",
    "org": "OpenAI",
    "elo": 1327.9,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-03-03",
    "model": "gpt-4.5-preview-2025-02-27",
    "org": "OpenAI",
    "elo": 1369.8,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-03-26",
    "model": "chatgpt-4o-latest-20250326",
    "org": "OpenAI",
    "elo": 1358.8,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-04-23",
    "model": "o3-2025-04-16",
    "org": "OpenAI",
    "elo": 1380.3,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-06-24",
    "model": "gemini-2.5-pro",
    "org": "Google",
    "elo": 1466.6,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-08-07",
    "model": "gpt-5-high",
    "org": "OpenAI",
    "elo": 1481.4,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-08-21",
    "model": "gemini-2.5-pro",
    "org": "Google",
    "elo": 1457.1,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-10-03",
    "model": "claude-sonnet-4-5-thinking-32k",
    "org": "Anthropic",
    "elo": 1453.0,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-10-07",
    "model": "gemini-2.5-pro",
    "org": "Google",
    "elo": 1451.8,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-11-16",
    "model": "gemini-3-pro",
    "org": "Google",
    "elo": 1500.6,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-02-06",
    "model": "claude-opus-4-6-thinking",
    "org": "Anthropic",
    "elo": 1503.5,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-04-17",
    "model": "claude-opus-4-7-thinking",
    "org": "Anthropic",
    "elo": 1504.5,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-05-12",
    "model": "claude-opus-4-6-thinking",
    "org": "Anthropic",
    "elo": 1501.7,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-06-10",
    "model": "claude-fable-5",
    "org": "Anthropic",
    "elo": 1510.4,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-09-25",
    "model": "claude-opus-5.5-high",
    "org": "Anthropic",
    "elo": 1508.6,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-09-30",
    "model": "gemini-4-argon-high",
    "org": "Google",
    "elo": 1524.8,
    "note": "style control leaderboard (site default)",
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   }
  ],
  "arenaTop5": [
   {
    "on": "2023-12-07",
    "top5": [
     {
      "model": "GPT-4-Turbo",
      "elo": 1217
     },
     {
      "model": "GPT-4-0613",
      "elo": 1153
     },
     {
      "model": "Claude-2.1",
      "elo": 1118
     }
    ],
    "note": "top 3 only, Elo scale",
    "src": "LMSYS blog",
    "url": "https://lmsys.org/blog/2023-12-07-leaderboard/",
    "date": "2023-12-07"
   },
   {
    "on": "2024-08-28",
    "top5": [
     {
      "model": "chatgpt-4o-latest",
      "org": "openai",
      "elo": 1288.8,
      "rank": 1,
      "votes": 24023
     },
     {
      "model": "gpt-4o-2024-05-13",
      "org": "openai",
      "elo": 1261.3,
      "rank": 2,
      "votes": 82934
     },
     {
      "model": "claude-3-5-sonnet-20240620",
      "org": "anthropic",
      "elo": 1258.4,
      "rank": 3,
      "votes": 53352
     },
     {
      "model": "gemini-advanced-0514",
      "org": "google",
      "elo": 1250.8,
      "rank": 4,
      "votes": 52225
     },
     {
      "model": "grok-2-2024-08-13",
      "org": "xai",
      "elo": 1250.1,
      "rank": 5,
      "votes": 10019
     }
    ],
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-01-05",
    "top5": [
     {
      "model": "o1-2024-12-17",
      "org": "openai",
      "elo": 1322.8,
      "rank": 1,
      "votes": 5223
     },
     {
      "model": "o1-preview",
      "org": "openai",
      "elo": 1303.2,
      "rank": 2,
      "votes": 33195
     },
     {
      "model": "claude-3-5-sonnet-20241022",
      "org": "anthropic",
      "elo": 1285.4,
      "rank": 3,
      "votes": 44399
     },
     {
      "model": "deepseek-v3",
      "org": "deepseek",
      "elo": 1277.5,
      "rank": 4,
      "votes": 6639
     },
     {
      "model": "gemini-1.5-pro-002",
      "org": "google",
      "elo": 1269.1,
      "rank": 5,
      "votes": 42041
     }
    ],
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2025-06-01",
    "top5": [
     {
      "model": "o3-2025-04-16",
      "org": "openai",
      "elo": 1441.8,
      "rank": 1,
      "votes": 13133
     },
     {
      "model": "chatgpt-4o-latest-20250326",
      "org": "openai",
      "elo": 1429.4,
      "rank": 2,
      "votes": 17656
     },
     {
      "model": "gpt-4.5-preview-2025-02-27",
      "org": "openai",
      "elo": 1423.8,
      "rank": 3,
      "votes": 15271
     },
     {
      "model": "claude-opus-4-20250514",
      "org": "anthropic",
      "elo": 1413.6,
      "rank": 4,
      "votes": 7729
     },
     {
      "model": "gpt-4.1-2025-04-14",
      "org": "openai",
      "elo": 1399.5,
      "rank": 5,
      "votes": 11773
     }
    ],
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-01-09",
    "top5": [
     {
      "model": "gemini-3-pro",
      "org": "google",
      "elo": 1489.6,
      "rank": 1,
      "votes": 25178
     },
     {
      "model": "grok-4.1-thinking",
      "org": "xai",
      "elo": 1476.8,
      "rank": 2,
      "votes": 25440
     },
     {
      "model": "gemini-3-flash",
      "org": "google",
      "elo": 1471.2,
      "rank": 3,
      "votes": 10204
     },
     {
      "model": "claude-opus-4-5-20251101-thinking-32k",
      "org": "anthropic",
      "elo": 1468.9,
      "rank": 4,
      "votes": 17570
     },
     {
      "model": "grok-4.1",
      "org": "xai",
      "elo": 1466.4,
      "rank": 5,
      "votes": 29539
     }
    ],
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-06-03",
    "top5": [
     {
      "model": "claude-opus-4-6-thinking",
      "org": "anthropic",
      "elo": 1503.3,
      "rank": 1,
      "votes": 38094
     },
     {
      "model": "claude-opus-4-7-thinking",
      "org": "anthropic",
      "elo": 1499.2,
      "rank": 2,
      "votes": 23928
     },
     {
      "model": "claude-opus-4-6",
      "org": "anthropic",
      "elo": 1498.3,
      "rank": 3,
      "votes": 40597
     },
     {
      "model": "claude-opus-4-7",
      "org": "anthropic",
      "elo": 1494.0,
      "rank": 4,
      "votes": 24801
     },
     {
      "model": "muse-spark",
      "org": "meta",
      "elo": 1488.9,
      "rank": 5,
      "votes": 12840
     }
    ],
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   },
   {
    "on": "2026-10-02",
    "top5": [
     {
      "model": "gemini-4-argon-high",
      "org": "google",
      "elo": 1525.2,
      "rank": 1,
      "votes": 4932
     },
     {
      "model": "claude-opus-4-6-high",
      "org": "anthropic",
      "elo": 1504.7,
      "rank": 2,
      "votes": 77636
     },
     {
      "model": "claude-fable-5-high",
      "org": "anthropic",
      "elo": 1504.3,
      "rank": 3,
      "votes": 38387
     },
     {
      "model": "claude-opus-5.5-high",
      "org": "anthropic",
      "elo": 1503.7,
      "rank": 4,
      "votes": 4552
     },
     {
      "model": "claude-opus-4-7-high",
      "org": "anthropic",
      "elo": 1501.3,
      "rank": 5,
      "votes": 64946
     }
    ],
    "src": "Arena Leaderboard Dataset (lmarena-ai)",
    "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
    "date": "dataset updated 2026-10-08; leaderboards 2023-05-08 to 2026-10-02"
   }
  ],
  "hleBest": [
   {
    "modelRelease": "2024-09-24",
    "model": "Gemini 1.5 Pro 002",
    "best": 4.6,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2024-12-17",
    "model": "o1 (Dec 2024)",
    "best": 7.96,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2025-02-24",
    "model": "Claude 3.7 Sonnet (Thinking)",
    "best": 8.04,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2025-03-19",
    "model": "o1 Pro",
    "best": 8.12,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2025-03-25",
    "model": "Gemini 2.5 Pro Exp (Mar 2025)",
    "best": 18.16,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2025-04-16",
    "model": "o3 (high)",
    "best": 20.32,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2025-06-05",
    "model": "Gemini 2.5 Pro Preview 06-05",
    "best": 21.64,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2025-08-07",
    "model": "GPT-5",
    "best": 25.32,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2025-10-07",
    "model": "GPT-5 Pro",
    "best": 31.64,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2025-11-18",
    "model": "Gemini 3 Pro Preview",
    "best": 37.52,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2026-02-19",
    "model": "Gemini 3.1 Pro Preview (thinking high)",
    "best": 46.44,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2026-09-01",
    "model": "Claude Fable 5.1 (xhigh)",
    "best": 46.5,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   },
   {
    "modelRelease": "2026-09-03",
    "model": "GPT-6 Astra",
    "best": 54.8,
    "src": "Scale Labs HLE leaderboard",
    "url": "https://labs.scale.com/leaderboard/humanitys_last_exam",
    "date": "accessed 2026-10-08 (latest update note 2026-09-17)"
   }
  ],
  "releases": {
   "note": "Models from Anthropic, OpenAI, Google, xAI and DeepSeek listed in Artificial Analysis' model catalogue with their release dates (includes minor variants such as mini/nano/Codex and open models like Gemma; 2026 Q4 = Oct 1-7 only).",
   "perQuarter": [
    {
     "q": "2025-Q1",
     "count": 26
    },
    {
     "q": "2025-Q2",
     "count": 18
    },
    {
     "q": "2025-Q3",
     "count": 18
    },
    {
     "q": "2025-Q4",
     "count": 12
    },
    {
     "q": "2026-Q1",
     "count": 11
    },
    {
     "q": "2026-Q2",
     "count": 20
    },
    {
     "q": "2026-Q3",
     "count": 23
    },
    {
     "q": "2026-Q4 (to Oct 7)",
     "count": 1
    }
   ],
   "flagships": [
    {
     "date": "2025-01-20",
     "model": "DeepSeek R1"
    },
    {
     "date": "2025-02-19",
     "model": "Grok 3"
    },
    {
     "date": "2025-02-24",
     "model": "Claude 3.7 Sonnet"
    },
    {
     "date": "2025-02-27",
     "model": "GPT-4.5 (Preview)"
    },
    {
     "date": "2025-03-25",
     "model": "Gemini 2.5 Pro Preview"
    },
    {
     "date": "2025-04-16",
     "model": "o3"
    },
    {
     "date": "2025-05-22",
     "model": "Claude 4 Opus / Sonnet"
    },
    {
     "date": "2025-07-10",
     "model": "Grok 4"
    },
    {
     "date": "2025-08-07",
     "model": "GPT-5"
    },
    {
     "date": "2025-08-21",
     "model": "DeepSeek V3.1"
    },
    {
     "date": "2025-09-29",
     "model": "Claude 4.5 Sonnet"
    },
    {
     "date": "2025-11-13",
     "model": "GPT-5.1"
    },
    {
     "date": "2025-11-18",
     "model": "Gemini 3 Pro Preview"
    },
    {
     "date": "2025-11-24",
     "model": "Claude Opus 4.5"
    },
    {
     "date": "2025-12-01",
     "model": "DeepSeek V3.2"
    },
    {
     "date": "2025-12-11",
     "model": "GPT-5.2"
    },
    {
     "date": "2026-02-05",
     "model": "Claude Opus 4.6"
    },
    {
     "date": "2026-02-19",
     "model": "Gemini 3.1 Pro Preview"
    },
    {
     "date": "2026-03-05",
     "model": "GPT-5.4"
    },
    {
     "date": "2026-03-10",
     "model": "Grok 4.20"
    },
    {
     "date": "2026-04-16",
     "model": "Claude Opus 4.7"
    },
    {
     "date": "2026-04-23",
     "model": "GPT-5.5"
    },
    {
     "date": "2026-04-24",
     "model": "DeepSeek V4 Pro"
    },
    {
     "date": "2026-05-28",
     "model": "Claude Opus 4.8"
    },
    {
     "date": "2026-06-09",
     "model": "Claude Fable 5"
    },
    {
     "date": "2026-07-08",
     "model": "Grok 4.5"
    },
    {
     "date": "2026-07-09",
     "model": "GPT-5.6 Sol"
    },
    {
     "date": "2026-07-24",
     "model": "Claude Opus 5"
    },
    {
     "date": "2026-08-12",
     "model": "Grok 4.6"
    },
    {
     "date": "2026-08-13",
     "model": "DeepSeek V4 Pro 0813"
    },
    {
     "date": "2026-09-01",
     "model": "Claude Fable 5.1"
    },
    {
     "date": "2026-09-03",
     "model": "GPT-6 Astra"
    },
    {
     "date": "2026-09-21",
     "model": "Grok 4.7"
    },
    {
     "date": "2026-09-22",
     "model": "Claude Opus 5.5"
    },
    {
     "date": "2026-09-29",
     "model": "GPT-6.1 Sol"
    },
    {
     "date": "2026-09-30",
     "model": "Gemini 4 Argon"
    }
   ],
   "src": "Artificial Analysis",
   "url": "https://artificialanalysis.ai/leaderboards/models",
   "date": "accessed 2026-10-08 (Intelligence Index v4.3.2)"
  }
 },
 "whoRuns": [
  {
   "name": "MMLU",
   "who": "Dan Hendrycks et al. (UC Berkeley lead, 7 authors)",
   "what": "57-subject 4-option multiple choice, ~14k test questions",
   "funding": "academic paper; dataset static",
   "independence": "static public test set, now saturated and contamination-prone",
   "updates": "none since 2020 (arXiv 2020-09-07)",
   "url": "https://arxiv.org/abs/2009.03300",
   "date": "2020-09-07"
  },
  {
   "name": "MMLU-Pro",
   "who": "TIGER-Lab, Yubo Wang, Wenhu Chen et al. (University of Waterloo-led, 17 authors)",
   "what": "harder 10-option version of MMLU, 12k questions",
   "funding": "academic",
   "independence": "static public set",
   "updates": "static (arXiv 2024-06-03)",
   "url": "https://arxiv.org/abs/2406.01574",
   "date": "2024-06-03"
  },
  {
   "name": "GPQA (Diamond)",
   "who": "David Rein et al. (NYU-led, 8 authors)",
   "what": "448 \"Google-proof\" graduate science questions; Diamond = 198-question subset",
   "funding": "academic",
   "independence": "static public set; authors ask not to post questions online",
   "updates": "static (arXiv 2023-11-20)",
   "url": "https://arxiv.org/abs/2311.12022",
   "date": "2023-11-20"
  },
  {
   "name": "Humanity's Last Exam",
   "who": "Center for AI Safety (CAIS) + Scale AI; 1,158 listed authors",
   "what": "2,500 expert questions (14% need an image); HLE-Rolling fork maintained by CAIS since 2026-09-17",
   "funding": "Scale AI and CAIS; $500k prize pool for question writers",
   "independence": "public questions plus private held-out set; Scale (co-creator) also runs a leaderboard",
   "updates": "finalized 2,500 q 2025-04-03; HLE-Rolling updated continually",
   "url": "https://arxiv.org/abs/2501.14249",
   "date": "2025-01-24"
  },
  {
   "name": "SWE-bench",
   "who": "Carlos Jimenez, John Yang et al. (Princeton)",
   "what": "2,294 real GitHub issues from 12 Python repos; model must produce a patch that passes tests",
   "funding": "SWE-bench team thanks Open Philanthropy, AWS, Modal, a16z, OpenAI and Anthropic",
   "independence": "academic team, but funded partly by labs it ranks",
   "updates": "leaderboard updated on submissions",
   "url": "https://arxiv.org/abs/2310.06770",
   "date": "2023-10-10"
  },
  {
   "name": "SWE-bench Verified",
   "who": "OpenAI with the SWE-bench authors",
   "what": "500 human-filtered SWE-bench tasks",
   "funding": "OpenAI paid for the human annotation",
   "independence": "OpenAI itself stopped reporting it on 2026-02-23 (flawed tests, contamination) and recommends SWE-bench Pro (Scale AI)",
   "updates": "swebench.com list: latest entry 2026-02-26",
   "url": "https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/",
   "date": "2024-08 (launch); 2026-02-23 (OpenAI stops)"
  },
  {
   "name": "LiveCodeBench",
   "who": "Naman Jain, ..., Koushik Sen, Ion Stoica (UC Berkeley, MIT, Cornell)",
   "what": "new contest problems from LeetCode, AtCoder, Codeforces, scored only on problems released after a model's cutoff",
   "funding": "academic",
   "independence": "contamination-resistant by time window",
   "updates": "rolling releases of new problems",
   "url": "https://livecodebench.github.io/",
   "date": "arXiv 2024-03-12"
  },
  {
   "name": "Arena (formerly LMArena / Chatbot Arena)",
   "who": "started as a UC Berkeley research project (LMSYS, 2023); company since April 2025; renamed Arena (arena.ai) 2026-01-28",
   "what": "crowd pairwise votes -> Bradley-Terry rating (Elo until 2024-01-09); style control default since 2025-05-16",
   "funding": "VC-backed: $100M seed (May 2025, $600M valuation, a16z + UC Investments); $150M Series A 2026-01-06 (~$1.7B, led by Felicis + UC Investments); sells paid evaluations to labs",
   "independence": "company that also sells services to the labs it ranks; new models can be pre-tested privately",
   "updates": "multiple published leaderboards per week",
   "url": "https://arena.ai/blog/lmarena-is-now-arena/",
   "date": "2026-01-28"
  },
  {
   "name": "Artificial Analysis",
   "who": "independent company, co-founders Micah Hill-Smith and George Cameron (started 2023, public 2024)",
   "what": "runs its own evals (Intelligence Index v4.3.2) plus price, speed and latency per provider",
   "funding": "seed from AI Grant (Nat Friedman, Daniel Gross); Andrew Ng investor; revenue from enterprise subscriptions, data API and private benchmarking - founders say nobody pays to be listed",
   "independence": "self-run evals; methodology public; models scored within days of release",
   "updates": "continuous",
   "url": "https://artificialanalysis.ai/",
   "date": "accessed 2026-10-08",
   "note": "funding details are from founder interviews (Latent Space podcast), not filings"
  },
  {
   "name": "Epoch AI",
   "who": "research nonprofit, started 2021",
   "what": "Benchmarking Hub: runs GPQA Diamond, FrontierMath, SWE-bench Verified, Mock AIME etc. and collects external results; publishes stderr and logs",
   "funding": "donor-funded nonprofit (primarily Open Philanthropy per TechCrunch); FrontierMath was funded by OpenAI, disclosed only in Dec 2024",
   "independence": "open data (CC BY 4.0) and Inspect logs; FrontierMath funding disclosure was criticised",
   "updates": "continuous (hub updated 2026-10-08)",
   "url": "https://epoch.ai/about",
   "date": "accessed 2026-10-08"
  },
  {
   "name": "Scale Labs (SEAL) leaderboards",
   "who": "Scale AI (company)",
   "what": "~26 leaderboards incl. HLE, SWE-Bench Pro, MultiChallenge, Remote Labor Index",
   "funding": "commercial; Scale sells training data to the labs",
   "independence": "uses private datasets \"to prevent overfitting\"; co-created HLE and SWE-bench Pro",
   "updates": "per new model release",
   "url": "https://labs.scale.com/leaderboard",
   "date": "accessed 2026-10-08"
  },
  {
   "name": "Vals AI",
   "who": "company, \"the independent evaluator of artificial intelligence\"",
   "what": "professional-work benchmarks (finance, legal, medical, public benefits)",
   "funding": "not stated on its about page",
   "independence": "\"Scores are based on our privately held test sets\"",
   "updates": "not stated",
   "url": "https://www.vals.ai/about",
   "date": "accessed 2026-10-08"
  },
  {
   "name": "Hugging Face Open LLM Leaderboard",
   "who": "Hugging Face (Clementine Fourrier et al.)",
   "what": "open-weight models on lm-eval-harness; v1 (ARC, HellaSwag, MMLU, TruthfulQA, Winogrande, GSM8K), v2 from June 2024",
   "funding": "Hugging Face",
   "independence": "same harness for everyone; open-weight models only",
   "updates": "v1 archived June 2024; v2 retired 2025-03-13 after evaluating 13k+ models",
   "url": "https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard/discussions/1135",
   "date": "2025-03-13"
  }
 ],
 "samples": {
  "mmlu": {
   "subject": "high_school_computer_science",
   "split": "test",
   "index": 0,
   "question": "Let x = 1. What is x << 3 in Python 3?",
   "choices": [
    "1",
    "3",
    "8",
    "16"
   ],
   "answer": "C",
   "answerText": "8",
   "src": "cais/mmlu (Hugging Face)",
   "url": "https://huggingface.co/datasets/cais/mmlu",
   "date": "accessed 2026-10-08"
  },
  "humaneval": {
   "task_id": "HumanEval/0",
   "entry_point": "has_close_elements",
   "prompt": "from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    \"\"\"\n",
   "canonical_solution": "    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False\n",
   "tests": 7,
   "testExample": "assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True",
   "src": "openai/openai_humaneval (Hugging Face)",
   "url": "https://huggingface.co/datasets/openai/openai_humaneval",
   "date": "accessed 2026-10-08"
  },
  "swebenchVerified": {
   "instance_id": "astropy__astropy-12907",
   "repo": "astropy/astropy",
   "issueTitle": "Modeling's `separability_matrix` does not compute separability correctly for nested CompoundModels",
   "created": "2022-03-03",
   "difficulty": "15 min - 1 hour",
   "failToPass": 2,
   "summary": "Nesting a compound model (Pix2Sky_TAN() & (Linear1D & Linear1D)) makes separability_matrix report the inner linear models as coupled; the fix must make 2 failing tests in astropy/modeling/tests/test_separable.py pass without breaking others.",
   "src": "princeton-nlp/SWE-bench_Verified (Hugging Face), row 0",
   "url": "https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified",
   "date": "accessed 2026-10-08"
  }
 },
 "gpqaPair": {
  "a": {
   "model": "Grok 4.7 (xhigh)",
   "value": 92.7,
   "stderr": 1.6
  },
  "b": {
   "model": "DeepSeek V4 Pro 0813 (max)",
   "value": 91.7,
   "stderr": 1.5
  },
  "gap": 1.1,
  "questions": 198,
  "note": "1.1 points = about 2 of 198 questions; each score carries roughly +/-1.5 standard error, so the 95% intervals overlap almost completely.",
  "alt": {
   "a": {
    "model": "Claude Opus 5.5 (max)",
    "value": 90.6,
    "stderr": 1.9
   },
   "b": {
    "model": "GPT-6 Luna (max)",
    "value": 90.5,
    "stderr": 1.9
   },
   "gap": 0.1
  },
  "src": "Epoch AI (GPQA Diamond)",
  "url": "https://epoch.ai/benchmarks/gpqa-diamond",
  "date": "last updated 2026-09-29"
 }
};
