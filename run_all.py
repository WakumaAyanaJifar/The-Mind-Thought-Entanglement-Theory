"""Reproduce every numerical result and generated figure of the MTE two-field-model paper.

Usage:  python run_all.py            # everything (dominated by the parameter-recovery study)
        python run_all.py --quick    # skip the slow parameter-recovery study

Each script runs with outputs/ as working directory; its printed output is saved to
outputs/logs/<script>.txt. Compare with expected_output/ (same file names).
"""
import subprocess, sys, time, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "outputs"; LOG = OUT / "logs"; LOG.mkdir(parents=True, exist_ok=True)
STEPS = [
    ("check1.py",        "Damped example of Section 3.3: k=0 resonances, kappa_pm, R_-, identity G1"),
    ("twofibre.py",      "Two-fibre competitor (Section 3.3, Suppl. S2): G1 and G3 hold; mixed sign gives a negative weight"),
    ("boundary.py",      "Boundary with cross term (Section 3.4, Suppl. S4): exponents, peak ratio, post-jump factor 4, bias crossover"),
    ("potential_splitting.py", "Lifting of vacuum degeneracy (Section 3.6, Fig. S4): Delta V = 0.2205 vs 0.2250"),
    ("fisher.py",        "Local identifiability (Section 3.8, Table S2): Jacobian rank, condition number, Cramer-Rao bounds"),
    ("static2d.py",      "Static threshold state on the sheet, d=2 (Suppl. S3, Fig. S3); writes static2d.npy"),
    ("static2d_conv.py", "Grid-convergence check of the d=2 state (Table S1)"),
    ("recovery7.py",     "Recovery of all seven dispersion parameters + amplitude (Table S3)  [slow]"),
    ("make_figs.py",     "Figures 1, 3 and S3 (PDF and PNG)"),
]
quick = "--quick" in sys.argv
for script, what in STEPS:
    if quick and script == "recovery7.py":
        print(f"-- skipping {script} (--quick)"); continue
    print(f"== {script}: {what}", flush=True)
    t = time.time()
    res = subprocess.run([sys.executable, str(ROOT / "code" / script)], cwd=OUT,
                         capture_output=True, text=True)
    (LOG / (script[:-3] + ".txt")).write_text(res.stdout + res.stderr)
    print(res.stdout.rstrip())
    if res.returncode != 0:
        print(res.stderr); sys.exit(f"{script} failed")
    print(f"   done in {time.time()-t:.0f} s\n", flush=True)
print("All steps finished. Results in outputs/, logs in outputs/logs/.")
