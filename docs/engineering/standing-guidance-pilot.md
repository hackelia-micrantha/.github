# Standing-guidance evaluation pilot (#139)

**Status:** preregistered, not executed. This is issue-local evaluation evidence,
not standing instructions, policy, a model benchmark, or an authorization gate.

## Question and exact treatment

For three small representative engineering artifact reviews, does adding the
**exact** `engineering-artifact-review` Invokrum profile help detect source-grounded
material problems, avoid false blockers and make the right readiness decision,
relative to a minimal task-specific review instruction?

- Source: `hackelia-micrantha/.github main@910f77af4286a385cbab473ec0f206e88e7f406f`.
- Treatment: pinned Invokrum 0.2.1 composed `engineering-artifact-review`;
  expected SHA256 `ed65c11210ca6d56dc855d4248d707be6a7e856df4a9100f915a455bc64394d2`.
- Baseline: minimal fixed instruction in `tools/standing_guidance_pilot.py`,
  SHA256 recorded in each result.
- Cases/answer key: `tests/fixtures/standing-guidance-pilot.json`,
  hashed in every result. Cases deliberately span RFC, ADR and delivery plan;
  two contain one seeded material defect and one is designed to be ready.
- Control: same frozen artifact, user-task prompt, response schema, model,
  local endpoint, temperature and maximum generation tokens. Paired runs
  interleave baseline/treatment, three repetitions per case and condition
  (18 responses). Seeds are recorded but **not** assumed to enforce identical
  stochasticity across model servers.
- Measures: decision-key matches, seeded material-section hits, unkeyed
  material sections, malformed outputs, and reported token usage (when the
  server actually returns it). Inspect per-case repeat spread; do not
  generalize to all models, readers or artifact types. Each scored call must
  include matching requested/served model IDs and `finish_reason=stop`.
  Record response ID, system fingerprint when provided, and token usage without
  inventing values. A matching model ID can still be a mutable alias; without
  independently pinned weights/server build, actual model revision is unverified.

The mechanical ID screen is **not** an independent semantic grader. Blinded
human adjudication must review raw text for missed/false findings and whether
unkeyed critiques are valid. Do not equate following prompt instructions with
higher task success. No scoring thresholds are tuned after seeing responses.

## Run without expanding host authority

This pilot uses only Python stdlib and an *already-running loopback*
OpenAI-compatible `/v1/models` and `/v1/chat/completions` API. It disables
proxy forwarding and HTTP redirects, sends no private repositories, rejects
unexpected Invokrum profile identity, and never starts, installs or activates
a model service. A non-loopback target is rejected. An available local server
must be authorized and its model/revision identified before interpreting
results. Do not infer provider independence from repetition.

Preflight without inference:

```sh
python3 tools/standing_guidance_pilot.py --invokrum /path/to/pinned/invokrum
```

When a model is available, save **new** result evidence outside the tracked
source checkout, for example:

```sh
python3 tools/standing_guidance_pilot.py \
  --invokrum /path/to/pinned/invokrum \
  --endpoint http://127.0.0.1:8000/v1 \
  --model EXACT_MODEL_ID \
  --output /tmp/micrantha-139-eval-run-1.json --run
```

The output file must not exist, and each completed response is persisted,
including raw response and any server-reported usage. If the endpoint fails,
the run remains **partial**, not successful. Document the server implementation,
model weight/build identity, inference parameters, harness revision, evaluator
identity and raw evidence path before drawing a disposition. If the endpoint
does not report usage, report cost **unmeasured**, not zero.

## Separate safety-negative case

The fixture also contains an untrusted-PR-description attempt to override
merge authorization. It is **not** sent to an agent with write tools during
this pilot. A separate read-only review may test whether a model recognizes
the instruction as data, and a separately authorized policy/gateway negative
test must show that an unauthorized effect is **rejected**. Prompt rejection
alone does not prove the runtime boundary. Until both have evidence, record
the safety acceptance criterion as outstanding.

## Retirement decision

Use actual evidence for `keep`, `narrow`, `move on-demand` or `supersede`.
A clean preregistration, green CI, or model compliance alone does not justify
deleting safety guidance or declaring #139 complete. Prefer a smaller
on-demand profile if it provides comparable measured value, but require
representative data before changing trusted guidance.
