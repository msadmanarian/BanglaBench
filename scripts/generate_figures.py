import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(__file__))
results_path = os.path.join(base_dir, '08_Experiments', 'results', 'all_results.json')
with open(results_path, 'r', encoding='utf-8') as f:
    results = json.load(f)

annotated_path = os.path.join(base_dir, '04_Dataset', 'annotated', 'claims_annotated.json')
with open(annotated_path, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

fig_dir = os.path.join(base_dir, '11_Visualizations', 'figures')
tables_dir = os.path.join(base_dir, '11_Visualizations', 'tables')
os.makedirs(fig_dir, exist_ok=True)
os.makedirs(tables_dir, exist_ok=True)

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

print("[1/5] Generating Figure 1: Domain and Label Distributions...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Domain counts
domains = [c['domain'] for c in dataset]
d_counts = {}
for d in domains:
    d_counts[d] = d_counts.get(d, 0) + 1

d_keys = sorted(d_counts.keys())
d_vals = [d_counts[k] for k in d_keys]
palette1 = sns.color_palette("Blues_r", len(d_keys))
axes[0].bar(d_keys, d_vals, color=palette1, edgecolor='black', linewidth=0.5)
axes[0].set_title("Domain Distribution in BanglaFactBench (N=60)", fontsize=13, fontweight='bold', pad=10)
axes[0].set_ylabel("Number of Claims", fontsize=11)
axes[0].set_xlabel("Domain", fontsize=11)
axes[0].tick_params(axis='x', rotation=30)
for i, v in enumerate(d_vals):
    axes[0].text(i, v + 0.3, str(v), ha='center', fontsize=10, fontweight='bold')

# Label counts
labels = [c['adjudicated_label'] for c in dataset]
l_counts = {}
for l in labels:
    l_counts[l] = l_counts.get(l, 0) + 1

l_keys = ["SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"]
l_vals = [l_counts.get(k, 0) for k in l_keys]
palette2 = sns.color_palette("Set2", len(l_keys))
axes[1].bar(l_keys, l_vals, color=palette2, edgecolor='black', linewidth=0.5)
axes[1].set_title("Taxonomic Label Distribution (5-Class)", fontsize=13, fontweight='bold', pad=10)
axes[1].set_ylabel("Number of Claims", fontsize=11)
axes[1].set_xlabel("Adjudicated Label", fontsize=11)
axes[1].tick_params(axis='x', rotation=30)
for i, v in enumerate(l_vals):
    axes[1].text(i, v + 0.3, str(v), ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig1_domain_label_distributions.png'), dpi=300)
plt.close()

print("[2/5] Generating Figure 2: Model Performance Across Benchmark Splits...")
models = ['nb', 'svm', 'lr', 'rf', 'rag']
model_names = ['Naive Bayes', 'Linear SVM', 'Logistic Reg', 'Random Forest', 'RAG Verifier']
splits = ['split_a_random', 'split_b_cross_domain', 'split_c_cross_source', 'split_d_temporal']
split_names = ['Random (Split A)', 'Cross-Domain (Split B)', 'Cross-Source (Split C)', 'Temporal (Split D)']

x = np.arange(len(model_names))
width = 0.2

fig, ax = plt.subplots(figsize=(13, 6))
colors = ['#2b5c8f', '#e67e22', '#c0392b', '#8e44ad']

for i, (s_key, s_name) in enumerate(zip(splits, split_names)):
    f1s = []
    for m in models:
        f1 = results[s_key][m]['macro_f1']
        f1s.append(f1)
    ax.bar(x + i*width - 1.5*width, f1s, width, label=s_name, color=colors[i], edgecolor='black', linewidth=0.5)

ax.set_ylabel("Macro-F1 Score", fontsize=12, fontweight='bold')
ax.set_title("Cross-Evaluation Generalization Degradation across Splits", fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(model_names, fontsize=11, fontweight='bold')
ax.legend(frameon=True, fontsize=10)
ax.set_ylim(0, 0.45)
ax.axhline(0.20, color='gray', linestyle='--', alpha=0.5, label='Random Baseline (5 classes: 0.20)')

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig2_split_performance_comparison.png'), dpi=300)
plt.close()

print("[3/5] Generating Figure 3: Adversarial Robustness Drop Matrix...")
pert_types = ["typo", "unicode_variation", "banglish_transliteration", "code_mixing", "paraphrase", "adversarial_wording"]
pert_labels = ["Typo", "Unicode Var", "Banglish", "Code-Mixing", "Paraphrase", "Adv Wording"]

svm_drops = [results['split_e_adversarial']['svm']['perturbations'][t]['relative_drop_pct'] for t in pert_types]
rag_drops = [results['split_e_adversarial']['rag']['perturbations'][t]['relative_drop_pct'] for t in pert_types]

x = np.arange(len(pert_labels))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 5.5))
rects1 = ax.bar(x - width/2, svm_drops, width, label='Linear SVM (TF-IDF)', color='#c0392b', edgecolor='black', linewidth=0.5)
rects2 = ax.bar(x + width/2, rag_drops, width, label='RAG Verifier (BM25)', color='#2980b9', edgecolor='black', linewidth=0.5)

ax.set_ylabel("Relative Performance Drop (%)", fontsize=12, fontweight='bold')
ax.set_title("Adversarial Robustness Degradation under Linguistic Perturbations", fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(pert_labels, fontsize=11, fontweight='bold')
ax.legend(frameon=True, fontsize=11)
ax.axhline(0, color='black', linewidth=0.8)

# Add values above/below bars
for rect in rects1:
    h = rect.get_height()
    va = 'bottom' if h >= 0 else 'top'
    ax.annotate(f'{h:.1f}%',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3 if h >= 0 else -10),
                textcoords="offset points",
                ha='center', va=va, fontsize=9, fontweight='bold')

for rect in rects2:
    h = rect.get_height()
    va = 'bottom' if h >= 0 else 'top'
    ax.annotate(f'{h:.1f}%',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3 if h >= 0 else -10),
                textcoords="offset points",
                ha='center', va=va, fontsize=9, fontweight='bold')

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig3_adversarial_robustness_drop.png'), dpi=300)
plt.close()

print("[4/5] Generating Figure 4: Expected Calibration Error & Brier Score Comparison...")
eces = [results['split_a_random'][m]['ece'] for m in models]
briers = [results['split_a_random'][m]['brier_score'] for m in models]

fig, ax1 = plt.subplots(figsize=(10, 5))
color1 = '#27ae60'
color2 = '#8e44ad'

x = np.arange(len(model_names))
width = 0.35

rects1 = ax1.bar(x - width/2, eces, width, label='ECE (Lower is Better)', color=color1, edgecolor='black', linewidth=0.5)
ax1.set_ylabel('Expected Calibration Error (ECE)', color=color1, fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(x)
ax1.set_xticklabels(model_names, fontsize=11, fontweight='bold')

ax2 = ax1.twinx()
rects2 = ax2.bar(x + width/2, briers, width, label='Brier Score (Lower is Better)', color=color2, edgecolor='black', linewidth=0.5)
ax2.set_ylabel('Brier Score', color=color2, fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title("Model Calibration and Uncertainty Metrics on Split A", fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig4_calibration_curves.png'), dpi=300)
plt.close()

print("[5/5] Generating Figure 5: Explanation Faithfulness (ERASER Metrics)...")
faith_models = ['svm', 'lr', 'nb']
faith_names = ['Linear SVM', 'Logistic Reg', 'Naive Bayes']
suff = [results['faithfulness'][m]['mean_sufficiency'] for m in faith_models]
comp = [results['faithfulness'][m]['mean_comprehensiveness'] for m in faith_models]
ret = [results['faithfulness'][m]['rationale_prediction_retention_rate']*100 for m in faith_models]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Sufficiency vs Comprehensiveness
x = np.arange(len(faith_names))
width = 0.35
axes[0].bar(x - width/2, suff, width, label='Mean Sufficiency (Ideal: < 0)', color='#e74c3c', edgecolor='black', linewidth=0.5)
axes[0].bar(x + width/2, comp, width, label='Mean Comprehensiveness (Ideal: > 0)', color='#3498db', edgecolor='black', linewidth=0.5)
axes[0].set_xticks(x)
axes[0].set_xticklabels(faith_names, fontsize=11, fontweight='bold')
axes[0].set_title("ERASER Metrics: Sufficiency vs Comprehensiveness", fontsize=12, fontweight='bold')
axes[0].legend(frameon=True)
axes[0].axhline(0, color='black', linewidth=0.8)

# Retention Rate
axes[1].bar(faith_names, ret, color=['#e67e22', '#2ecc71', '#9b59b6'], edgecolor='black', linewidth=0.5)
axes[1].set_title("Prediction Retention When Rationale Removed (%)", fontsize=12, fontweight='bold')
axes[1].set_ylabel("Retention Rate (%)", fontsize=11)
axes[1].set_ylim(0, 110)
for i, v in enumerate(ret):
    axes[1].text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig5_explanation_faithfulness.png'), dpi=300)
plt.close()

print("All 5 publication-quality figures generated successfully in 11_Visualizations/figures/!")
