# Delivery Checklist

## Status

- Status: `runtime evidence prepared; material pool current; final submission artifacts pending`
- Deadline: `2026-06-16 17:00`
- Submission email: `qxiang24@m.fudan.edu.cn`
- Submission subject: `DIP课程论文-学号-姓名`

## Deliverables

| Deliverable | Status | Link / Evidence | Missing Reason / Notes |
| --- | --- | --- | --- |
| Course paper | partial | evidence mapping below; current material pool in `report-materials.md` | final paper authoring is still pending; current broad benchmark result remains mixed, with only local improvement evidence |
| Code repository link | missing | local repository only | external GitHub or equivalent link not provided |
| Model weight link | partial | baseline `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`; aligned improved `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt`; Phase B quick `ERRNet/checkpoints/errnet_phaseB_quick_improved_ctx_vgg/errnet_080_00478488.pt`; Phase B fixed full `ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_vgg_fixed/errnet_080_00632892.pt`; Phase D gamma `ERRNet/checkpoints/errnet_phaseD_gamma_1p1_1p5_10ep/errnet_010_00077320.pt` | local checkpoints exist; external download link for submitted weight is not provided |
| Project PPT | partial | evidence mapping below; current slide skeleton in `report-materials.md`; existing `副本2026-DIP课程项目-RR.pptx` not modified | final PPT authoring is still pending; current conclusion should say local improvement but no broad benchmark win unless next experiment succeeds |
| Member contributions | missing |  | group members and per-member contribution text not provided |
| Submission email subject/recipient | ready | `DIP26_ERRNet_实验指导.md` | actual sending is out of scope |

## Paper / PPT Evidence Mapping

| Section | Evidence Source | Status | Notes |
| --- | --- | --- | --- |
| Background | `DIP26_ERRNet_实验指导.md`, `ERRNet/README_DIP26.md` | ready | SIRR task, traditional prior, and ERRNet baseline context are documented |
| Baseline method | `results-baseline.md`, `ERRNet/README_DIP26.md` | ready | Commands, metric semantics, CPU/GPU execution, and outputs are recorded |
| Improved method | `results-improved.md`, `ERRNet/README_DIP26.md` | ready | Local loss-weight change, defaults, commands, compatibility, and risks are documented |
| Experiment setup | `environment.md`, `datasets.md` | ready | Environment, packed env, dataset counts, checkpoint, and custom images are recorded |
| Quantitative results | `results-baseline.md`, `results-improved.md`, `report-materials.md` | current material ready | Baseline, aligned improved, Phase A, Phase B quick-screen/full/fixed, Phase C, and Phase D are organized; next experiment may add a stronger improvement claim |
| Qualitative results | `results-baseline.md`, `results-improved.md`, `report-materials.md` | interim material ready | p1-p5 custom review sheets and current recommended cases are recorded; custom images remain qualitative-only |
| Success case | `report-materials.md`, `results-improved.md` | material ready | Current recommended success case is p5 with Phase B quick-screen `improved + ctx_vgg`; custom evidence remains qualitative only |
| Failure case | `report-materials.md`, `results-improved.md` | interim material ready | Current recommended failure/limitation case is p3; may be retained as final limitation evidence |
| Limitations | `report-materials.md`, `results-baseline.md`, `results-improved.md` | material ready | Mixed aligned retrain, quick-screen-only local gains, fixed full runs below baseline/aligned-60, Phase C/D negative screens, and qualitative-only custom images are recorded |
| Conclusion | `report-materials.md` plus next experiment | pending | Current conclusion is local improvement without broad benchmark win; final synthesis can improve if the next low-cost experiment succeeds |
| Member contributions | this checklist | missing | Group member names and roles not provided |

## Final Notes

- The previous missing-runtime-dependency blocker has been rerun and resolved in
  the documented `errnet` conda environment.
- Full improved retraining produced
  `ERRNet/checkpoints/errnet_improved_retrain_60ep/errnet_060_00470708.pt` on
  2026-05-27, and TODO-002 six-dataset benchmark evaluation is recorded in
  `results-improved.md`.
- T044 full-retrain custom-image outputs for `p1` through `p5` are generated
  under `ERRNet/results/custom_improved_retrain_60ep/`.
- `report-materials.md` organizes current evidence as a paper/PPT material
  pool, including slide skeleton, compact final-evidence table, p5/p4/p3 custom
  figure choices, Phase C/D negative screens, and a next-improvement slot. It is
  not a final report.
- Final paper/PPT authoring, artifact upload, repository/weight link creation,
  member contribution text, and email submission require a separate explicit
  request.
