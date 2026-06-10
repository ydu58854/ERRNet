# Research: Phase C Exclusion-Loss Experiment

## Decision 1: Implement Phase C Before Phase D

**Decision**: Start with default-disabled exclusion loss. Keep Phase D data
strategy as a documented follow-up only.

**Rationale**: A local loss option has smaller blast radius than loader,
synthetic data, augmentation, or curriculum changes. It can be verified with
tensor and smoke-training checks while preserving existing experiment evidence.

**Alternatives considered**:

- Start Phase D data strategy immediately. Rejected because it changes data
  semantics and would require a wider plan, stronger verification, and more
  time before any reliable signal.
- Add a new network output for reflection. Rejected because it changes
  architecture and checkpoint compatibility.

## Decision 2: Use `input - output` As Residual Proxy

**Decision**: Compute the exclusion term from the current input, transmission
output, and residual proxy `input - output`.

**Rationale**: Existing ERRNet already exposes these tensors in training and
visuals. The proxy is cheap, does not require new labels, and matches the Phase
C hypothesis in `improvement.md`.

**Alternatives considered**:

- Require ground-truth reflection layer. Rejected because current paired custom
  and benchmark workflows do not provide this signal consistently.
- Add a reflection branch. Rejected as out of scope for a loss-only experiment.

## Decision 3: Penalize Shared Normalized Gradient Magnitudes

**Decision**: Build exclusion loss from normalized absolute gradients of
transmission and residual proxy, using a small epsilon to avoid division by
zero.

**Rationale**: The goal is to discourage transmission and residual from sharing
strong local edge structure. Normalizing gradient magnitudes limits scale
sensitivity and keeps degenerate tensors finite.

**Alternatives considered**:

- Raw gradient product without normalization. Rejected because large gradient
  scale could dominate the existing loss.
- Correlation coefficient. Rejected for MVP because it needs additional
  centering and zero-variance handling while providing no clear smoke-stage
  benefit.

## Decision 4: Additive CLI Option With Default `0.0`

**Decision**: Add `--lambda_exclusion` to training options, default `0.0`.

**Rationale**: Existing commands remain unchanged by default. Positive values
create an explicit Phase C experiment.

**Alternatives considered**:

- Reuse `gradient_loss_weight`. Rejected because it changes an existing aligned
  pixel-loss semantic and makes experiment attribution unclear.
- Enable exclusion by default. Rejected because it would invalidate prior
  baseline-compatible behavior.

## Decision 5: Smoke Before Long Training

**Decision**: Verify tensor finite behavior, option parsing, short training,
checkpoint load, and log output before starting any long Phase C run.

**Rationale**: Previous Phase B work showed that training can appear healthy
until later numerical failures. Smoke checks catch integration errors cheaply,
but long runs still need full benchmark/custom evaluation before claims.

**Alternatives considered**:

- Start full training immediately. Rejected because it risks wasting GPU time
  on an unverified loss path.
