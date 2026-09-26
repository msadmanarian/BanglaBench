#!/usr/bin/env python3
"""
BanglaFactBench Interactive Web Verification Dashboard
A standalone, zero-external-dependency web application serving an interactive
fact-checking workbench, live RAG evidence explorer, and adversarial simulator.
"""

import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding='utf-8')
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'src', 'data'))
sys.path.append(os.path.join(base_dir, 'src', 'models'))
sys.path.append(os.path.join(base_dir, 'src', 'retrieval'))
sys.path.append(os.path.join(base_dir, 'src', 'robustness'))

from normalizer import BengaliTextNormalizer
from rag_verifier import RAGVerificationSystem
from perturbation_engine import BengaliPerturbationEngine

# Initialize RAG system
print("Initializing BanglaFactBench Web Engine...")
data_path = os.path.join(base_dir, '04_Dataset', 'annotated', 'claims_annotated.json')
corpus = []
if os.path.exists(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

verifier = RAGVerificationSystem(top_k=3, seed=42)
if corpus:
    verifier.fit(corpus)
p_engine = BengaliPerturbationEngine(seed=42)
print(f"RAG Verifier ready with {len(corpus)} evidence documents.")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BanglaFactBench | Interactive Fact Verification Dashboard</title>
  <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --supported: #22c55e;
      --refuted: #ef4444;
      --unverifiable: #eab308;
      --misleading: #f97316;
      --opinion: #a855f7;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', 'Hind Siliguri', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 2rem 1rem;
    }
    .container { max-width: 1100px; margin: 0 auto; }
    header {
      text-align: center;
      margin-bottom: 2.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.5rem;
    }
    h1 { font-size: 2.2rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
    .badge {
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent);
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .subtitle { color: var(--text-muted); margin-top: 0.75rem; font-size: 1.05rem; }
    
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
    @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .card h2 { font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem; color: #fff; }
    
    textarea, select, button {
      width: 100%;
      padding: 0.75rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #090d16;
      color: var(--text);
      font-family: inherit;
      font-size: 1rem;
      margin-bottom: 1rem;
    }
    textarea:focus, select:focus { outline: none; border-color: var(--accent); }
    button {
      background: #0284c7;
      color: #fff;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: background 0.2s;
    }
    button:hover { background: #0369a1; }
    
    .result-box {
      margin-top: 1rem;
      padding: 1rem;
      border-radius: 8px;
      background: #090d16;
      border: 1px solid var(--border);
    }
    .verdict-badge {
      display: inline-block;
      padding: 0.4rem 1rem;
      border-radius: 6px;
      font-weight: 700;
      font-size: 1.1rem;
      text-transform: uppercase;
      margin-bottom: 0.5rem;
    }
    .SUPPORTED { background: rgba(34, 197, 94, 0.2); color: var(--supported); border: 1px solid var(--supported); }
    .REFUTED { background: rgba(239, 68, 68, 0.2); color: var(--refuted); border: 1px solid var(--refuted); }
    .UNVERIFIABLE { background: rgba(234, 179, 8, 0.2); color: var(--unverifiable); border: 1px solid var(--unverifiable); }
    .MISLEADING { background: rgba(249, 115, 22, 0.2); color: var(--misleading); border: 1px solid var(--misleading); }
    .OPINION { background: rgba(168, 85, 247, 0.2); color: var(--opinion); border: 1px solid var(--opinion); }
    
    .evidence-item {
      background: #1e293b;
      border-left: 3px solid var(--accent);
      padding: 0.75rem;
      margin-top: 0.75rem;
      border-radius: 0 6px 6px 0;
      font-size: 0.95rem;
    }
    .evidence-meta { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.3rem; }
    .evidence-meta a { color: var(--accent); text-decoration: none; }
    
    .pert-item {
      padding: 0.5rem 0.75rem;
      border-bottom: 1px solid var(--border);
      font-size: 0.9rem;
    }
    .pert-item:last-child { border-bottom: none; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">BanglaFactBench v1.0.5</span>
      <h1>বাংলা দাবি ও তথ্য যাচাইকরণ ড্যাশবোর্ড</h1>
      <p class="subtitle">A Multi-Domain Benchmark for Claim Verification, Misinformation Detection, and Adversarial Robustness</p>
    </header>

    <div class="grid">
      <!-- Input Panel -->
      <div class="card">
        <h2>দাবি ইনপুট / Claim Selection</h2>
        <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.3rem;">নমুনা সংরক্ষিত দাবি নির্বাচন করুন:</label>
        <select id="sampleSelect" onchange="loadSample()">
          <option value="">-- কাস্টম দাবি লিখুন --</option>
          <option value="পেঁপে পাতার রস খেলে ডেঙ্গু রোগীর প্লাটিলেট তাৎক্ষণিকভাবে স্বাভাবিক হয়ে যায় এবং ডেঙ্গু সম্পূর্ণ নিরাময় হয়।">পেঁপে পাতার রসে ডেঙ্গু নিরাময় (স্বাস্থ্য)</option>
          <option value="পদ্মা সেতুর নির্মাণ ব্যয়ের সম্পূর্ণ অর্থ বাংলাদেশ সরকার নিজস্ব তহবিল থেকে বহন করেছে।">পদ্মা সেতু নির্মাণ অর্থায়ন (অর্থনীতি)</option>
          <option value="বাংলাদেশ মহাকাশ গবেষণা ও দূর অনুধাবন প্রতিষ্ঠান ২০২৫ সালে নিজস্ব উপগ্রহ উৎক্ষেপণ করবে।">SPARSO উপগ্রহ উৎক্ষেপণ (বিজ্ঞান/প্রযুক্তি)</option>
          <option value="ঘূর্ণিঝড় রিমালের কারণে উপকূলীয় এলাকায় ১০ নম্বর মহাবিপদ সংকেত জারি করা হয়েছে।">ঘূর্ণিঝড় সংকেত (দুর্যোগ ব্যবস্থাপনা)</option>
        </select>

        <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.3rem;">যাচাই করার জন্য দাবি লিখুন:</label>
        <textarea id="claimText" rows="4" placeholder="যেকোনো বাংলা দাবি এখানে পেস্ট করুন..."></textarea>
        
        <button onclick="verifyClaim()">🔍 তথ্য যাচাই করুন (Verify with RAG)</button>
        <button onclick="runStressTest()" style="background: #475569; margin-top: -0.5rem;">⚡ বিপরীতমুখী স্ট্রেস টেস্ট (Adversarial Robustness)</button>
      </div>

      <!-- Verdict Panel -->
      <div class="card">
        <h2>যাচাইকরণ ফলাফল / Verification Verdict</h2>
        <div id="outputArea">
          <p style="color: var(--text-muted); text-align: center; padding: 3rem 0;">দাবি ইনপুট দিয়ে 'তথ্য যাচাই করুন' বাটনে ক্লিক করুন।</p>
        </div>
      </div>
    </div>

    <!-- Adversarial Test Panel -->
    <div class="card" style="margin-top: 1.5rem;" id="stressCard" style="display: none;">
      <h2>Adversarial Robustness Simulation (Split E)</h2>
      <div id="stressOutput">
        <p style="color: var(--text-muted);">স্ট্রেস টেস্ট বাটনে ক্লিক করলে ৬টি ভাষাতাত্ত্বিক পরিবর্তনের প্রভাব দেখা যাবে।</p>
      </div>
    </div>
  </div>

  <script>
    function loadSample() {
      const sel = document.getElementById("sampleSelect");
      if (sel.value) {
        document.getElementById("claimText").value = sel.value;
      }
    }

    async function verifyClaim() {
      const claim = document.getElementById("claimText").value.trim();
      if (!claim) return alert("দাবি লিখুন!");
      const out = document.getElementById("outputArea");
      out.innerHTML = "<p style='color: var(--accent);'>অনুসন্ধান চলছে...</p>";

      try {
        const resp = await fetch("/api/verify?claim=" + encodeURIComponent(claim));
        const data = await resp.json();

        let evHtml = "";
        if (data.evidence && data.evidence.length > 0) {
          data.evidence.forEach((ev, i) => {
            evHtml += `
              <div class="evidence-item">
                <strong>[প্রমাণ ${i+1}]</strong> ${ev.relevant_text}
                <div class="evidence-meta">উৎস: ${ev.source || 'Curated'} | BM25 স্কোর: ${ev.bm25_score || 0.0} | <a href="${ev.url}" target="_blank">লিংক</a></div>
              </div>`;
          });
        } else {
          evHtml = "<p style='color: var(--text-muted); margin-top: 0.5rem;'>কোনো সরাসরি প্রমাণ খুঁজে পাওয়া যায়নি।</p>";
        }

        out.innerHTML = `
          <div>
            <span class="verdict-badge ${data.label}">${data.label}</span>
            <span style="margin-left: 1rem; color: var(--text-muted);">বিশ্বাসযোগ্যতা স্কোর: ${(data.confidence * 100).toFixed(1)}%</span>
            <div style="margin-top: 1rem;">
              <h3 style="font-size: 1rem; color: #fff;">উদ্ধৃত প্রমাণ দলিল (Cited Evidence):</h3>
              ${evHtml}
            </div>
          </div>`;
      } catch (e) {
        out.innerHTML = "<p style='color: var(--refuted);'>ত্রুটি ঘটেছে: " + e.message + "</p>";
      }
    }

    async function runStressTest() {
      const claim = document.getElementById("claimText").value.trim();
      if (!claim) return alert("দাবি লিখুন!");
      const stressOut = document.getElementById("stressOutput");
      stressOut.innerHTML = "<p style='color: var(--accent);'>৬টি ভাষাতাত্ত্বিক পরিবর্তনের প্রভাব পরীক্ষা করা হচ্ছে...</p>";

      try {
        const resp = await fetch("/api/stress?claim=" + encodeURIComponent(claim));
        const data = await resp.json();

        let rows = "";
        data.forEach(p => {
          rows += `
            <div class="pert-item">
              <strong>[${p.type}]</strong>: <em>${p.text}</em>
              <div style="margin-top: 0.2rem;">
                <span class="verdict-badge ${p.verdict}" style="font-size: 0.75rem; padding: 0.2rem 0.5rem;">${p.verdict}</span>
                <span style="color: var(--text-muted); font-size: 0.8rem; margin-left: 0.5rem;">কনফিডেন্স: ${(p.confidence*100).toFixed(1)}%</span>
              </div>
            </div>`;
        });
        stressOut.innerHTML = rows;
      } catch (e) {
        stressOut.innerHTML = "<p style='color: var(--refuted);'>ত্রুটি: " + e.message + "</p>";
      }
    }
  </script>
</body>
</html>
"""

class BanglaFactHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        elif parsed.path == "/api/verify":
            qs = parse_qs(parsed.query)
            claim = qs.get("claim", [""])[0]
            norm = BengaliTextNormalizer.normalize_text(claim)
            res = verifier.verify_claim(norm) if norm else {"label": "UNVERIFIABLE", "confidence": 0.0, "evidence": []}
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
        elif parsed.path == "/api/stress":
            qs = parse_qs(parsed.query)
            claim = qs.get("claim", [""])[0]
            norm = BengaliTextNormalizer.normalize_text(claim)
            perturbations = p_engine.generate_all_perturbations(norm) if norm else []
            out = []
            for p in perturbations:
                vres = verifier.verify_claim(p["transformed_claim_text"])
                out.append({
                    "type": p["transformation_type"],
                    "text": p["transformed_claim_text"],
                    "verdict": vres["label"],
                    "confidence": vres["confidence"]
                })
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(out, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), BanglaFactHandler)
    print(f"\n=======================================================")
    print(f"BanglaFactBench Interactive Web UI running on port {port}")
    print(f"Open: http://localhost:{port}")
    print(f"=======================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()

if __name__ == '__main__':
    main()
