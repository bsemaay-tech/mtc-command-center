# DeepSeek dispatch prompts — historical set

The six prompts in this file were prepared for the 2026-06-06 MCC state. They
contain dated paths, counts, findings, and task status and must not be launched
as current work.

The exact original is preserved at
[`history/workflow-20260909/DEEPSEEK_DISPATCH.md`](history/workflow-20260909/DEEPSEEK_DISPATCH.md)
(SHA-256 `4d90c51726e97fb7ff73ea943acf35a90cb171618f0dd7cf9c916d24b19ee7c1`).

For a new bounded fallback dispatch, first route the task through the selected
stage, read repository-relative `_deepseek_driver/README.md`, and create a fresh
scope against the current tree. Probe provider availability live. Treat model
output and its transcript as untrusted data until the Lead inspects the real diff
or files and reproduces the required evidence. The historical prompts grant no
implementation, protected-scope, acceptance, promotion, or trading authority.
