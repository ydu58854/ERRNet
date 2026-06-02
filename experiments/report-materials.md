# Report And PPT Material Pool

Last updated: 2026-05-30

Purpose: organize currently available ERRNet evidence as reusable material for
the final paper and PPT. This is not the final report. It is the current
evidence pool after Phase B fixed full runs, Phase C exclusion-loss screening,
and Phase D gamma data-strategy screening.

## Current Use Policy

- Use these notes as report material, but keep final submission wording tied to
  the exact comparison being claimed.
- Do not claim that aligned improved retraining, Phase B fixed full runs,
  Phase C, or Phase D gamma screening are broadly better than baseline.
- Custom images have no reflection-free ground truth; use them only for
  qualitative discussion.
- The strongest positive evidence so far is local: Phase B quick-screen
  `improved + ctx_vgg` improves average SSIM and LMSE against its aligned
  improved source, improves all four metrics on `wild`, and gives the best
  custom p5/p4 qualitative scores. Treat it as a controlled ablation unless a
  follow-up method improves the full benchmark average.
- The original full `improved + ctx_vgg` epoch-70 result is historical evidence
  for mixed/unstable behavior. The post-fix full-training results are stable but
  still mixed, so they should not replace the quick-screen local-improvement
  story.

## Paper Evidence Outline

| Paper Section | Current Material | Evidence Source | Current Claim Level | Later Update Needed |
| --- | --- | --- | --- | --- |
| Background and task | Single-image reflection removal; ERRNet baseline; metrics PSNR/SSIM/NCC/LMSE | `improvement.md`, `results-baseline.md` | stable background | no, unless final framing changes |
| Baseline reproduction | Six benchmark metrics and custom outputs from official baseline checkpoint | `results-baseline.md` | reproducible baseline | no |
| Aligned improved retraining | epoch-60 checkpoint, six benchmark metrics, mixed/inconclusive comparison | `results-improved.md` | diagnostic material | possibly only summarize if final method changes |
| Phase A checkpoint selection | epoch 10/20/30/40/50/60 comparison; epoch 60 remains most balanced | `results-improved.md`, `improvement.md` | supports checkpoint choice | no |
| Phase B quick-screen | six-run `baseline/improved x vgg/ctx/ctx_vgg` matrix; `improved + ctx_vgg` selected as screening candidate | `results-improved.md` TODO-006 compact tables | local improvement evidence, not full-training proof | no |
| Original full `ctx_vgg` epoch 70 | epoch 80/latest NaN/Inf rejected; epoch 70 finite but mixed | `results-improved.md`, `improvement.md` | instability/ablation evidence | no |
| CX loss stability fix | dataset scan clean; CX numerical instability fixed with stable exp/normalize/log clamps; fixed full runs finite | `improvement.md`, code diff in `ERRNet/models/CX/CX_distance.py`, `results-improved.md` | debugging and reproducibility evidence | no |
| Phase B fixed full runs | `ctx_vgg_fixed` and `ctx_fixed` epoch-80 checkpoints finite; six benchmarks/custom complete | `results-improved.md` | stable but mixed; no broad improvement | no |
| Phase C exclusion loss | default-disabled `--lambda_exclusion`; 10/20/30epoch candidate finite but below baseline/aligned-60 | `results-improved.md`, `specs/003-phasec-exclusion-loss/` | negative screening evidence | no |
| Phase D gamma data strategy | default-compatible `--phase_d_candidate`; `gamma_1p1_1p5` finite but below Phase C/baseline/aligned-60 | `results-improved.md`, `specs/004-phase-d-data-strategy/` | negative screening evidence | no |
| Custom qualitative results | p5 success, p4 mixed, p3 failure; all custom claims qualitative only | `results-improved.md` TODO-003, visual-review sheets | qualitative support | yes, add final full-run outputs if visually stronger |
| Limitations | metric tradeoff, synthetic/full-reference degradation on `ceilnet_table2`, custom no-GT, fixed full runs still below baseline/aligned-60, Phase C/D negative screens | `improvement.md`, `results-improved.md` | ready | no |
| Next direction | low-cost post-processing/fusion or another tightly gated single-variable experiment to obtain measurable improvement | `todo.md`, this file | planned exploration | yes, after next experiment |

## PPT Slide Skeleton

| Slide | Title | Main Visual/Table | Suggested Message | Status |
| ---: | --- | --- | --- | --- |
| 1 | Task And Baseline | one input/output example plus baseline metric row | ERRNet baseline is reproducible on six benchmark sets. | material ready |
| 2 | Aligned Improved Retraining | baseline vs epoch-60 improved comparison table | The aligned retrain is mixed and does not justify a broad improvement claim. | material ready |
| 3 | Phase A Checkpoint Selection | epoch average table | epoch 60 is still the most balanced aligned checkpoint. | material ready |
| 4 | Phase B Quick-Screen Design | small matrix: source checkpoint x loss | We tested the ERRNet unaligned real-data path as a quick-screen ablation. | material ready |
| 5 | Phase B Quick-Screen Result | TODO-006 compact average table | `improved + ctx_vgg` is the best quick-screen candidate, mainly via SSIM/LMSE. | material ready |
| 6 | Dataset-Specific Signal | `wild` highlight and `ceilnet_table2` limitation tables | Gains are dataset-specific; full-reference synthetic-table metrics drop. | material ready |
| 7 | Full `ctx_vgg` Instability | checkpoint health summary | Original full run had healthy epoch 70 but NaN/Inf at epoch 80/latest. | material ready |
| 8 | Stability Diagnosis And Fix | CX loss root-cause plus fixed-run health | The numerical fix made epoch-80 full runs finite, but did not produce broad metric improvement. | material ready |
| 9 | Phase C/D Negative Screens | compact average table | Exclusion loss and gamma data strategy were technically successful but below references, so they were stopped. | material ready |
| 10 | Custom Visual Cases | p5 success, p4 mixed, p3 failure comparison sheets | Qualitative results show useful cases and clear limitations. | material ready |
| 11 | Current Conclusion And Next Step | evidence ladder plus next experiment | Current defensible improvement is local/qualitative; next step targets a measurable average gain. | update after next experiment |

## Compact Quantitative Material

Use the compact tables in `results-improved.md` under
`TODO-006 paper/PPT compact tables`.

Recommended wording for current paper/PPT drafts:

```text
Phase B is treated as a quick-screen ablation rather than final training. It
uses ERRNet's unaligned finetuning path with `--max_dataset_size 100`, producing
the fusion dataset 389 [50, 250, 89]. Among the six quick-screen runs,
improved + ctx_vgg has the smallest average PSNR drop, the only positive
average SSIM delta, and the best average LMSE. The strongest positive signal is
on wild, where all four metrics improve, and custom p5/p4 show the best
qualitative scores. However, ceilnet_table2 degrades and the full default-data
continuations remain mixed, so this is reported as a local improvement signal
rather than a broad benchmark win.
```

Current compact final-evidence table:

| Method / Phase | Avg PSNR | Avg SSIM | Avg NCC | Avg LMSE | Report Use |
| --- | ---: | ---: | ---: | ---: | --- |
| Baseline checkpoint | 24.5689 | 0.8864 | 0.9486 | 0.0075 | primary reference |
| Aligned improved epoch 60 | 24.4020 | 0.8858 | 0.9488 | 0.0071 | best aligned retrain; mixed vs baseline |
| Phase B quick `improved + ctx_vgg` | 24.3502 | 0.8868 | 0.9469 | 0.0069 | local improvement: SSIM/LMSE vs aligned source, best custom |
| Phase B full `improved + ctx_vgg` epoch 70 | 24.2730 | 0.8853 | 0.9487 | 0.0075 | historical unstable full run |
| Phase B full `ctx_vgg_fixed` epoch 80 | 24.0870 | 0.8820 | 0.9488 | 0.0074 | finite but mixed |
| Phase C `lambda=0.001` epoch 30 | 23.2722 | 0.8774 | 0.9363 | 0.0080 | negative loss-screen result |
| Phase D `gamma_1p1_1p5` epoch 10 | 21.6452 | 0.8671 | 0.9336 | 0.0081 | negative data-screen result |

Defensible improvement wording:

```text
The project did not obtain a broad full-reference benchmark improvement over
the official baseline. The most useful positive signal is local: unaligned
finetuning from the aligned improved checkpoint with contextual+VGG loss
improves average SSIM from 0.8858 to 0.8868 and LMSE from 0.0071 to 0.0069
relative to its source checkpoint, improves all four metrics on wild, and gives
the best qualitative result on the custom p5/p4 cases. Later full-data and
loss/data-strategy experiments were used as controlled negative evidence to
avoid overclaiming.
```

## Custom Figure Checklist

Primary comparison sheets:

| Image | Review Sheet | Suggested Use | Current Selection | Note |
| --- | --- | --- | --- | --- |
| p5 | `ERRNet/experiments/visual-review/custom_p5_comparison.png` | main qualitative success slide or paper figure | success | Phase B `improved + ctx_vgg` suppresses large glass reflection texture best among current candidates. |
| p4 | `ERRNet/experiments/visual-review/custom_p4_comparison.png` | mixed/usable example | mixed | Outdoor transmission is clearer, but door/window reflection marks remain. |
| p3 | `ERRNet/experiments/visual-review/custom_p3_comparison.png` | limitation/failure example | failure | Reflected trees/road/facade content remains; no method convincingly removes it. |
| p1 | `ERRNet/experiments/visual-review/custom_p1_comparison.png` | optional neutral example | no strong winner | Avoid claiming visible improvement. |
| p2 | `ERRNet/experiments/visual-review/custom_p2_comparison.png` | optional weak-candidate example | weak candidate only | Slight cleanup at best; not central for final slides. |

All-method sheets:

| Image | Path | Use |
| --- | --- | --- |
| p1 | `ERRNet/experiments/visual-review/custom_p1_all_methods.png` | appendix or backup slide |
| p2 | `ERRNet/experiments/visual-review/custom_p2_all_methods.png` | appendix or backup slide |
| p3 | `ERRNet/experiments/visual-review/custom_p3_all_methods.png` | failure analysis backup |
| p4 | `ERRNet/experiments/visual-review/custom_p4_all_methods.png` | mixed-case backup |
| p5 | `ERRNet/experiments/visual-review/custom_p5_all_methods.png` | success-case backup |

Recommended output paths for the current selected Phase B quick-screen method:

| Case | Image | Output Path | Use In Paper/PPT |
| --- | --- | --- | --- |
| Success | p5 | `ERRNet/results/phaseB_quick_improved_ctx_vgg_custom/p5/errnet_phaseB_quick_improved_ctx_vgg_custom.png` | qualitative success figure |
| Mixed | p4 | `ERRNet/results/phaseB_quick_improved_ctx_vgg_custom/p4/errnet_phaseB_quick_improved_ctx_vgg_custom.png` | balanced analysis figure |
| Failure | p3 | `ERRNet/results/phaseB_quick_improved_ctx_vgg_custom/p3/errnet_phaseB_quick_improved_ctx_vgg_custom.png` | limitation figure |
| Aligned-retrain limitation | p5 | `ERRNet/results/custom_improved_retrain_60ep/p5/errnet_improved_retrain_60ep_custom.png` | explain why aligned retrain is not visually superior |

## Next Improvement Slot

The project needs a stronger measurable improvement before final claim wording
can be upgraded. The next direction should be low cost and tightly gated:

| Candidate | Why It Is Next | Gate |
| --- | --- | --- |
| Test-time output fusion between baseline and Phase B quick `improved + ctx_vgg` | Uses existing outputs/checkpoints; may retain baseline PSNR while borrowing Phase B SSIM/LMSE/custom gains; thumbnail sampling shows positive PSNR/SSIM/NCC movement | Accept only if six-dataset full-resolution average improves at least one target metric without broad PSNR regression |
| Single-variable sigma Phase D candidate | Gamma screen was negative; blur sigma directly targets reflection sharpness | Run 10epoch only after smoke; stop if below Phase C/baseline references |
| Lightweight post-processing on residual | Could reduce visible reflection residual without retraining | Must be evaluated on all six benchmarks and custom, with default off |

Fast exploration result on 2026-05-30:

| Probe | Scope | Best Observed Signal | Interpretation |
| --- | --- | --- | --- |
| Baseline/Phase B output fusion thumbnail sample | 10-20 samples per dataset, 128px grayscale thumbnails, alpha grid `0.0` to `1.0` | alpha `0.4-0.5` improved sampled PSNR by about `+0.38` to `+0.41`, SSIM by about `+0.0058`, and NCC by about `+0.0044` over alpha `0.0` | Promising enough for formal full-resolution validation; not a reportable metric yet |

Formal validation required before any claim:

1. Generate or evaluate fused outputs at alpha `0.4` and `0.5` on all six
   benchmark result sets.
2. Compute official full-resolution PSNR/SSIM/NCC/LMSE with the same metric
   implementation used by `test_errnet.py`.
3. Run custom p1-p5 fusion sheets against baseline and Phase B quick outputs.
4. Keep fusion as an explicitly named inference-time strategy, not a training
   improvement.
