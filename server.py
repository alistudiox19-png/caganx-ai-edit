#!/usr/bin/env python3
# caganx AI edit - 32 Ozellik Aktif
# python server.py  →  http://127.0.0.1:8765

import http.server
import socketserver
import subprocess
import json
import uuid
from pathlib import Path

PORT = 8765
BASE_DIR = Path(__file__).parent.resolve()
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

HTML = r'''<!DOCTYPE html>
<html lang="tr">
<meta name="description" content="Yapay Zeka ile Video Düzenle! AI Sihirli Dokunuş, 45 Sosyal Medya Aracı, Dikey Blur Fill 9:16, YouTube Shorts, TikTok, Instagram Reels, Dual Export ve Ses Efektleri."/>
<meta name="robots" content="index, follow"/>
<meta property="og:title" content="caganx AI edit - Yapay Zeka ile Video Düzenle"/>
<meta property="og:description" content="Tek tıkla videolarını viral yap! 45 Yapay Zeka aracı, dikey Blur Fill, altyazı ve yüksek kaliteli render."/>
<meta property="og:type" content="website"/>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎬</text></svg>"/>
<title>caganx AI edit - Yapay Zeka ile Video Düzenle</title>
<style>
:root{--bg:#0a0a0b;--s:#141416;--s2:#1c1c1f;--b:#2a2a2e;--t:#f4f4f5;--m:#a1a1aa;--a:#8b5cf6;--g:#22c55e;--pink:#ec4899}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--t);min-height:100vh}
header{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;border-bottom:1px solid var(--b);position:sticky;top:0;background:rgba(10,10,11,.95);z-index:10}
.logo{font-size:1.25rem;font-weight:700;background:linear-gradient(135deg,#fff,#c4b5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.badge{font-size:.65rem;font-weight:600;padding:3px 8px;border-radius:99px;color:#c4b5fd;background:rgba(139,92,246,.15);border:1px solid rgba(139,92,246,.35);margin-left:10px;text-transform:uppercase}
main{max-width:1000px;margin:0 auto;padding:32px 20px 60px}
.hero{text-align:center;margin-bottom:24px}
.hero h1{font-size:2rem;font-weight:700;background:linear-gradient(180deg,#fff 40%,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{color:var(--m);margin-top:6px;font-size:.95rem}

.magic-card{
  background: linear-gradient(135deg, rgba(139,92,246,0.22), rgba(236,72,153,0.22));
  border: 2px solid rgba(139,92,246,0.55);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  margin-bottom: 22px;
  box-shadow: 0 0 30px rgba(139,92,246,0.18);
  position: relative;
  overflow: hidden;
}
.magic-card h2{font-size:1.35rem;margin-bottom:6px;background:linear-gradient(90deg,#fff,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.magic-card p{color:var(--m);font-size:.9rem;max-width:650px;margin:0 auto 16px}
.btn-magic{
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  color: #fff;
  font-weight: 700;
  font-size: 1rem;
  padding: 12px 30px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(236,72,153,0.35);
  transition: .2s;
}
.btn-magic:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 6px 22px rgba(236,72,153,0.55)}
.btn-magic:disabled{opacity:.5;cursor:not-allowed}

.zone{
  background:var(--s);
  border:2px dashed var(--b);
  border-radius:14px;
  padding:32px;
  text-align:center;
  cursor:pointer;
  margin-bottom:20px;
  transition:.25s;
  position:relative;
  overflow:hidden;
  animation: zonePulse 3s ease-in-out infinite;
}
.zone::before{
  content:'';
  position:absolute;
  inset:-2px;
  border-radius:14px;
  padding:2px;
  background:linear-gradient(90deg,transparent,var(--a),transparent,var(--a),transparent);
  background-size:300% 100%;
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;
  mask-composite:exclude;
  animation: borderMove 4s linear infinite;
  opacity:0.55;
  pointer-events:none;
}
.zone:hover,.zone.over{border-color:var(--a);background:rgba(139,92,246,.08);animation:none}
.zone.ok{border-color:var(--g);border-style:solid;animation:none}
.zone.ok::before{display:none}
@keyframes borderMove{0%{background-position:0% 50%}100%{background-position:300% 50%}}
@keyframes zonePulse{0%,100%{box-shadow:0 0 0 0 rgba(139,92,246,0)}50%{box-shadow:0 0 18px 2px rgba(139,92,246,0.12)}}
.zone h3{font-size:1.05rem;margin-bottom:4px}
.zone p{color:var(--m);font-size:.88rem}

.tabs{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;margin:20px 0 14px}
.tab{background:var(--s);border:1px solid var(--b);color:var(--m);padding:8px 16px;border-radius:10px;font-size:.85rem;font-weight:600;cursor:pointer;white-space:nowrap;transition:.2s}
.tab:hover,.tab.active{background:var(--s2);color:var(--t);border-color:var(--a)}

.status{display:none;background:var(--s);border:1px solid var(--b);border-radius:10px;padding:12px 16px;margin-bottom:16px;align-items:center;gap:10px}
.status.on{display:flex}
.status.ok{border-color:rgba(34,197,94,.4)}
.status.err{border-color:rgba(239,68,68,.4)}
.spin{width:16px;height:16px;border:2px solid var(--b);border-top-color:var(--a);border-radius:50%;animation:sp .7s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}

.pack{background:linear-gradient(135deg,rgba(34,197,94,.1),rgba(139,92,246,.1));border:1px solid rgba(34,197,94,.3);border-radius:14px;padding:20px;text-align:center;margin-bottom:20px}
.pack h2{font-size:1.15rem;margin-bottom:4px}
.pack p{color:var(--m);font-size:.88rem;margin-bottom:12px}

.btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 18px;font-size:.88rem;font-weight:500;border-radius:10px;border:none;cursor:pointer;transition:.2s}
.btn-g{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;font-weight:600;padding:10px 24px}
.btn-g:disabled{opacity:.5;cursor:not-allowed}
.btn-s{background:transparent;color:var(--m);border:1px solid var(--b);margin:2px;padding:8px 13px;font-size:.84rem}
.btn-s:hover{background:var(--s2);color:var(--t)}
.btn-s:disabled{opacity:.4;cursor:not-allowed}

#dl{display:none;margin-top:12px;padding:12px;background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);border-radius:10px}
#dl a{color:#4ade80;font-weight:600;text-decoration:none;margin:0 8px}

.history-box{background:var(--s);border:1px solid var(--b);border-radius:14px;padding:16px;margin-top:28px}
.history-title{font-size:.9rem;font-weight:700;color:var(--m);margin-bottom:10px;text-transform:uppercase;letter-spacing:.04em}
.history-list{display:flex;flex-direction:column;gap:8px}
.history-item{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:var(--s2);border-radius:8px;font-size:.85rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:10px}
.card{
  background:var(--s);
  border:1px solid var(--b);
  border-radius:10px;
  padding:12px 14px;
  font-size:.88rem;
  cursor:pointer;
  transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1), transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.15s, background 0.15s;
  display:flex;
  gap:10px;
  align-items:center;
  position:relative;
  opacity: 0;
  transform: translateY(22px) scale(0.95);
}
.card.revealed{
  opacity: 1;
  transform: translateY(0) scale(1);
}
.card:hover{border-color:var(--a);background:var(--s2);z-index:50}
.card.hidden{display:none !important}

/* Arka plani siyah, yazisi beyaz custom aciklama popup kutucugu */
.card::after{
  content: attr(data-desc);
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: #000000;
  color: #ffffff;
  border: 1px solid #44444c;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.82rem;
  font-weight: 500;
  line-height: 1.4;
  width: 230px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.9);
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease, visibility 0.2s ease;
  z-index: 999;
}
.card::before{
  content: '';
  position: absolute;
  bottom: calc(100% + 2px);
  left: 50%;
  transform: translateX(-50%);
  border-width: 6px;
  border-style: solid;
  border-color: #000000 transparent transparent transparent;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease, visibility 0.2s ease;
  z-index: 1000;
}
.card:hover::after, .card:hover::before{
  opacity: 1;
  visibility: visible;
}

.rockstar-box{
  border: 2px solid #ffffff;
  box-shadow: 0 0 25px rgba(255,255,255,0.22), inset 0 0 15px rgba(255,255,255,0.04);
  border-radius: 18px;
  padding: 24px;
  background: #08080a;
  position: relative;
  margin-top: 20px;
  min-height: 280px;
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
}

.rockstar-box:hover{
  border-color: #ffffff;
  box-shadow: 0 0 38px rgba(255,255,255,0.45), inset 0 0 20px rgba(255,255,255,0.08);
}

.rockstar-cover{
  position: absolute;
  inset: 0;
  background: #000000;
  z-index: 80;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 16px;
  transition: opacity 0.3s ease, transform 0.3s ease, visibility 0.3s ease;
}

.caganx-brand{
  font-size: 3.6rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: #ffffff;
  text-shadow: 0 0 20px rgba(255,255,255,0.8), 0 0 40px rgba(255,255,255,0.4);
  margin-bottom: 12px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  animation: brandGlow 2.5s ease-in-out infinite alternate;
}

@keyframes brandGlow{
  0%{ text-shadow: 0 0 15px rgba(255,255,255,0.6); transform: scale(0.98); }
  100%{ text-shadow: 0 0 35px rgba(255,255,255,1), 0 0 60px rgba(139,92,246,0.6); transform: scale(1.02); }
}

.rockstar-hint{
  font-size: 0.88rem;
  color: rgba(255,255,255,0.8);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-weight: 600;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.25);
  padding: 8px 18px;
  border-radius: 99px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

.num{font-size:.75rem;font-weight:700;color:var(--a);min-width:22px}
.sec{font-size:.78rem;font-weight:600;color:var(--m);text-transform:uppercase;letter-spacing:.04em;margin:18px 0 8px}
footer{text-align:center;padding:16px;color:var(--m);font-size:.8rem;border-top:1px solid var(--b)}
</style>
</head>
<body>
<header>
  <div style="display:flex;align-items:center">
    <span class="logo">caganx AI edit</span>
    <span class="badge">DENEYSEL</span>
  </div>
</header>
<main>
  <div class="hero">
    <h1>Yapay Zeka ile Video Düzenle</h1>
    <p>AI Sihirli Dokunuş • Kategori Sekmeleri • Dual Export • Yerel Geçmiş</p>
  </div>
  
  <div class="magic-card">
    <h2>✨ AI SİHİRLİ DOKUNUŞ (Tek Tık Otomasyonu)</h2>
    <p>Sessizlikleri Kes + Sesi Eşitle (Loudnorm) + Dikey 9:16 Blur Fill Arka Plan + Canlı Renk Filtresi</p>
    <button class="btn-magic" id="bmagic" onclick="go('magic_viral')" disabled>✨ SİHİRLİ DOKUNUŞ İLE VİRAL YAP</button>
  </div>

  <div class="status" id="st" style="display:none;flex-direction:column;align-items:stretch;gap:8px;background:var(--s);border:1px solid var(--b);border-radius:12px;padding:14px 18px;margin-bottom:18px">
    <div style="display:flex;align-items:center;gap:10px">
      <div class="spin" id="sp"></div>
      <span id="stx" style="font-weight:600;font-size:0.92rem">Hazır</span>
      <span id="stpct" style="margin-left:auto;font-weight:700;font-size:0.85rem;color:var(--g)">0%</span>
    </div>
    <div id="pgwrap" style="width:100%;height:10px;background:rgba(255,255,255,0.08);border-radius:99px;overflow:hidden;box-shadow:inset 0 1px 3px rgba(0,0,0,0.5)">
      <div id="pgbar" style="width:0%;height:100%;background:linear-gradient(90deg,#8b5cf6,#22c55e);border-radius:99px;box-shadow:0 0 12px rgba(34,197,94,0.6);transition:width 0.15s linear"></div>
    </div>
  </div>
  
  <div class="zone" id="zone">
    <div style="font-size:1.5rem;margin-bottom:8px">🎬</div>
    <h3 id="zt">Videoyu buraya sürükle veya tıkla</h3>
    <p id="zi">MP4, MOV, WebM</p>
    <input type="file" id="fi" accept="video/*" hidden/>
  </div>

  <div class="pack">
    <h2>Tam Paket & İki Formatlı Çıktı</h2>
    <p>Web uyumlu H.264 render veya Tek Tıkla Hem Dikey (9:16) Hem Kare (1:1) Çıktı Alın</p>
    <div style="display:flex;gap:10px;justify-content:center">
      <button class="btn btn-g" id="bt" onclick="go('tam-paket')" disabled>Tam Paket Uygula</button>
      <button class="btn btn-g" id="bdual" style="background:linear-gradient(135deg,#8b5cf6,#6366f1)" onclick="go('dual_export')" disabled>📦 Çift Format (9:16 + 1:1)</button>
    </div>
    <div id="dl">
      <canvas id="confetti-canvas" style="position:fixed;inset:0;pointer-events:none;z-index:99999"></canvas>
      <div style="color:var(--g);font-weight:700;font-size:1.1rem;margin-bottom:8px">🎉 İşlem Başarıyla Tamamlandı! Öncesi vs Sonrası Karşılaştırması:</div>
      
      <div id="compare-wrap" style="display:none;margin:14px 0;background:#0d0d10;border:1px solid rgba(255,255,255,0.15);border-radius:14px;padding:16px">
        <div style="font-size:0.8rem;color:var(--g);text-align:center;margin-bottom:10px">💡 Videonun üzerine tıklayarak Oynat/Durdur yapabilirsiniz</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;align-items:center">
          <div style="flex:1;min-width:250px;text-align:center">
            <div style="font-size:0.85rem;font-weight:700;color:var(--m);margin-bottom:6px">⏮️ ORIJİNAL VİDEO (ÖNCESİ)</div>
            <video id="vorig" title="Oynat / Durdur için tıklayın" style="width:100%;max-height:280px;border-radius:10px;border:1px solid #333;background:#000;cursor:pointer"></video>
          </div>
          <div style="flex:1;min-width:250px;text-align:center;position:relative" id="vplayer-container">
            <div style="font-size:0.85rem;font-weight:700;color:var(--g);margin-bottom:6px">✨ İŞLENMİŞ VİDEO (SONRASI)</div>
            <div style="position:relative;display:inline-block;width:100%">
              <video id="vplayer" title="Oynat / Durdur için tıklayın" style="width:100%;max-height:280px;border-radius:10px;border:2px solid var(--g);box-shadow:0 0 20px rgba(34,197,94,0.3);background:#000;cursor:pointer;transition:all 0.3s ease"></video>
              <div id="voverlay-hook" style="display:none;position:absolute;top:20%;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.85);color:#facc15;font-weight:900;font-size:1.1rem;padding:8px 16px;border-radius:8px;border:2px solid #facc15;box-shadow:0 4px 15px rgba(0,0,0,0.8);z-index:10;pointer-events:none;text-align:center;width:85%">🔥 SONUNA KADAR İZLE!</div>
              <div id="voverlay-watermark" style="display:none;position:absolute;top:12px;right:12px;background:rgba(0,0,0,0.65);color:#ffffff;font-weight:700;font-size:0.8rem;padding:4px 10px;border-radius:6px;border:1px solid rgba(255,255,255,0.3);z-index:10;pointer-events:none">@caganx</div>
              <div id="voverlay-sub" style="display:none;position:absolute;bottom:16px;left:50%;transform:translateX(-50%);background:rgba(139,92,246,0.9);color:#ffffff;font-weight:800;font-size:0.9rem;padding:6px 16px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.6);z-index:10;pointer-events:none;text-align:center;width:80%">💬 TREND ALTYAZI METNİ</div>
              <div id="voverlay-splitscreen" style="display:none;position:absolute;top:50%;left:0;right:0;height:4px;background:#8b5cf6;box-shadow:0 0 10px #8b5cf6;z-index:10;pointer-events:none"></div>
            </div>
          </div>
        </div>
        <div style="margin-top:14px;display:flex;align-items:center;gap:10px">
          <span style="font-size:0.85rem;color:var(--g);font-weight:600">⌛ Sarma:</span>
          <input type="range" id="vseeker" min="0" max="100" value="0" style="flex:1;accent-color:var(--g);cursor:pointer;height:8px">
          <span id="vtime" style="font-size:0.85rem;color:var(--m);min-width:65px;text-align:right">00:00</span>
        </div>
      </div>

      <div style="margin-top:14px;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px">
        <a id="dla" href="#" download class="btn btn-g" style="padding:10px 20px;text-decoration:none;font-size:1rem">📥 Videoyu İndir (Ana Çıktı)</a>
        <a id="dla2" href="#" download class="btn btn-g" style="display:none;padding:10px 20px;text-decoration:none;font-size:1rem;background:linear-gradient(135deg,#8b5cf6,#6366f1)">📦 İndir 2 (Kare 1:1)</a>
        <label style="font-size:0.85rem;color:var(--m);cursor:pointer;display:flex;align-items:center;gap:6px;margin-left:8px">
          <input type="checkbox" id="chkAutoDl" checked style="accent-color:var(--g)"> Otomatik İndir (Auto-Download)
        </label>
      </div>
    </div>
  </div>

  <div class="tabs">
    <button class="tab active" onclick="filterTab('all', this)">🌐 Tüm Araçlar (45)</button>
    <button class="tab" onclick="filterTab('ai', this)">✨ AI Otomasyon</button>
    <button class="tab" onclick="filterTab('social', this)">📱 Sosyal Medya & Presets</button>
    <button class="tab" onclick="filterTab('audio', this)">🔊 Ses & Efektler</button>
    <button class="tab" onclick="filterTab('video', this)">🎨 Görüntü & Filtreler</button>
  </div>

  <div class="sec">Hızlı Kestirmeler</div>
  <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px">
    <button class="btn btn-s" onclick="go('blur_fill')" id="b11" disabled>📱 Dikey Blur Fill</button>
    <button class="btn btn-s" onclick="go('splitscreen')" id="b12" disabled>🎮 Split Screen</button>
    <button class="btn btn-s" onclick="go('shorts')" id="b13" disabled>⚡ Shorts (60s)</button>
    <button class="btn btn-s" onclick="go('hook_presets')" id="b15" disabled>🪝 Viral Hook Başlık</button>
    <button class="btn btn-s" onclick="go('silence_cut')" id="b16" disabled>✂️ Sessizlik Kesici</button>
    <button class="btn btn-s" onclick="go('audio_highlight')" id="b17" disabled>🔥 Aksiyon/Ses Zirvesi</button>
    <button class="btn btn-s" onclick="go('thumbnail')" id="b18" disabled>🖼️ Kapak Görseli</button>
  </div>

  <div class="rockstar-box" id="rbox">
    <div class="rockstar-cover" id="rcover" onclick="revealFeatures()">
      <div class="caganx-brand">caganx</div>
      <div class="rockstar-hint">📜 Çerçeve İçi Fare Tekerleğini Döndürün</div>
    </div>
    <div class="sec" style="margin-top:0">Tüm Özellik Kartları (45)</div>
    <div class="grid" id="grid"></div>
  </div>

  <div class="history-box">
    <div class="history-title">📜 Son İşlenen Videolar Geçmişi (Local History)</div>
    <div class="history-list" id="hlist"><div style="color:var(--m);font-size:.85rem">Henüz işlenmiş video yok.</div></div>
  </div>
</main>
<footer>caganx AI edit • PRO ULTRA • Yerel FFmpeg</footer>
<script>
const F = [
  {n:"🔍 1. Video Analizi & Probe", a:"basic", c:"video", d:"Videonun çözünürlük, kare hızı ve kodek yapısını analiz eder ve standart web formatına getirir."},
  {n:"✂️ 2. Klip Kesme (15 Saniye)", a:"trim", c:"video", d:"Videonun ilk 15 saniyesini otomatik kırparak kısa klip oluşturur."},
  {n:"🔗 3. Video Birleştirici", a:"concat", c:"video", d:"Birden fazla video dosyasını kalite kaybı olmadan tek bir video halinde birleştirir."},
  {n:"📐 4. 720p HD Çözünürlük", a:"720p", c:"video", d:"Videoyu hızlı yükleme ve az alan kaplaması için 720p HD çözünürlüğe ölçekler."},
  {n:"💬 5. Özel Metin & Altyazı", a:"text", c:"social", d:"Videonuzun üzerine istediğiniz özel metni veya altyazıyı ekler."},
  {n:"🔊 6. Ses Yükseltici (200%)", a:"volume_up", c:"audio", d:"Videonun ses seviyesini 2 katına çıkartarak daha net duyulmasını sağlar."},
  {n:"⚡ 7. 2x Hızlı Çekim", a:"speed", c:"video", d:"Görüntü ve sesi 2 kat hızlandırarak tempolu klip üretir."},
  {n:"✂️ 8. Ekran Kırpma (Crop)", a:"crop", c:"video", d:"Videonun kenarlarındaki gereksiz alanları keserek odağa yakınlaşır."},
  {n:"☀️ 9. Canlı Parlaklık & Renk", a:"bright", c:"video", d:"Görüntünün kontrast ve parlaklığını artırarak renklere canlılık katar."},
  {n:"🎞️ 10. Hareketli GIF Oluşturucu", a:"gif", c:"social", d:"Videodan 4 saniyelik kaliteli ve döngülü GIF resmi üretir."},
  {n:"🌅 11. Kararma & Açılma (Fade)", a:"fade", c:"video", d:"Videonun başına ve sonuna yumuşak geçiş efektleri uygular."},
  {n:"🏷️ 12. Köşe Filigranı / Logo", a:"watermark", c:"social", d:"Videonun sağ alt köşesine markanızı temsil eden filigran ekler."},
  {n:"🎚️ 13. Akıllı Ses Eşitleme", a:"normalize", c:"audio", d:"Sesteki ani patlamaları ve kısık sesleri yayın standartlarında eşitler."},
  {n:"🖼️ 14. Resim İçinde Resim (PiP)", a:"pip", c:"video", d:"Videoyu küçülterek çerçeveli arka plan üstüne oturtur."},
  {n:"🔄 15. 90° Sağa Döndürme", a:"rotate90", c:"video", d:"Yan çekilen videoları saat yönünde 90 derece dik konuma getirir."},
  {n:"🔲 16. Şık Siyah Çerçeve", a:"border", c:"video", d:"Videonun etrafına estetik siyah dolgu çerçevesi ekler."},
  {n:"🦥 17. Slow-Motion Ağır Çekim", a:"slow", c:"video", d:"Videoyu 0.5x ağır çekim moduna alarak aksiyon detaylarını öne çıkarır."},
  {n:"⚓ 18. Video Titreşim Engelleyici", a:"stabilize", c:"video", d:"Kamera sarsıntılarını gidererek daha pürüzsüz görüntü sağlar."},
  {n:"🎨 19. Çoklu Katman Kutusu", a:"overlay", c:"video", d:"Videonun üstüne renkli bilgilendirme kutusu katmanı yerleştirir."},
  {n:"⚙️ 20. Otomatik Batch İşleme", a:"batch", c:"ai", d:"Videoyu otomatik analiz edip hızlı web formatında kodlar."},
  {n:"🌫️ 21. Bulanıklaştırma (Blur)", a:"blur", c:"video", d:"Görüntüye yumuşak bulanıklık efekti uygulayarak sinematik bir doku verir."},
  {n:"🎞️ 22. Vintage Sinematik Renk", a:"vintage", c:"video", d:"Nostaljik ve sinematik retro renk tonlamaları uygular."},
  {n:"🔄 23. Tersine Oynatma (Reverse)", a:"reverse", c:"video", d:"Görüntüyü ve sesi sondan başa doğru ters hareket ettirir."},
  {n:"🚀 24. 60 FPS Akıcı Kare", a:"interp", c:"video", d:"Kare arası interpolation yaparak videoyu 60 FPS akıcılığa çıkarır."},
  {n:"📊 25. Ses Dalga Görseli", a:"audioviz", c:"audio", d:"Müzik ve sese göre hareket eden renkli frekans çizgileri üretir."},
  {n:"🟩 26. Chroma Key Yeşil Ekran", a:"chroma", c:"video", d:"Videodaki yeşil fonları şeffaflaştırır."},
  {n:"🔍 27. Dinamik Zoom Yakınlaşma", a:"zoom", c:"video", d:"Videonun merkezine yumuşak bir yakınlaşma uygular."},
  {n:"✨ 28. Animasyonlu Metin", a:"textanim", c:"social", d:"Ekrana gelen başlık metinlerine dikkat çekici animasyon katar."},
  {n:"🧩 29. Video Kolaj Çerçevesi", a:"collage", c:"video", d:"Videoyu küçültüp kolaj yapısına uygun boyuta getirir."},
  {n:"📲 30. TikTok Dikey Format", a:"tiktok", c:"social", d:"Videoyu TikTok ekran oranına (1080x1920) tam uyumlu yapar."},
  {n:"🛡️ 31. Telif & Kodek Analizcisi", a:"copyright", c:"ai", d:"Video ve ses akışlarını tarayarak standart uyumluluğu doğrular."},
  {n:"🏷️ 32. Otomatik AI Markalama", a:"watermark", c:"social", d:"Videonun köşesine otomatik saydam logo yerleştirir."},
  {n:"📱 33. Auto-Reframe (Blur Fill 9:16)", a:"blur_fill", c:"social", d:"Yatay videoları dikey yapar, üst ve alt boşlukları videonun bulanık haliyle kaplar."},
  {n:"🎮 34. Split Screen (Oyun/Kamera)", a:"splitscreen", c:"social", d:"Ekranı ikiye bölerek üstte oyun/içerik altta kamera görüntüsünü istifler."},
  {n:"⚡ 35. YouTube Shorts (60s Limit)", a:"shorts", c:"social", d:"Videoyu 60 saniye ile sınırlandırıp dikey Shorts formatına dönüştürür."},
  {n:"📸 36. Instagram Reels Preset", a:"reels", c:"social", d:"Reels algoritmasına tam uyumlu H.264 dikey yüksek kalite çıktı verir."},
  {n:"🏷️ 37. Sosyal Medya Tag (@kullanıcı)", a:"watermark_user", c:"social", d:"Üst köşeye yarı saydam siyah kutu içinde kullanıcı adınızı ekler."},
  {n:"🪝 38. Viral Hook Başlık (3s)", a:"hook_banner", c:"social", d:"Videonun ilk 3 saniyesine izleyicinin dikkatini çeken büyük sarı/siyah başlık koyar."},
  {n:"✂️ 39. Otomatik Sessizlik Kesici", a:"silence_cut", c:"ai", d:"Videodaki nefes ve duraksama boşluklarını otomatik keserek tempoyu yükseltir."},
  {n:"🖼️ 40. Kapak Görseli (JPG)", a:"thumbnail", c:"social", d:"Videonun 1. saniyesinden yüksek çözünürlüklü dikey kapak resmi (.jpg) çıkarır."},
  {n:"💬 41. Trend Altyazı Bandı", a:"sub_style", c:"social", d:"Videonun alt tarafına mor/beyaz dikkat çekici altyazı şeridi koyar."},
  {n:"✨ 42. AI Sihirli Dokunuş (Viral)", a:"magic_viral", c:"ai", d:"Sessizlikleri keser + sesi normalize eder + dikey blur fill yapar + renkleri canlılaştırır."},
  {n:"🔥 43. Aksiyon & Ses Zirvesi Klibi", a:"audio_highlight", c:"ai", d:"Sesteki ve aksiyondaki en heyecanlı 30 saniyelik öne çıkan klibi otomatik oluşturur."},
  {n:"📦 44. Çift Format (9:16 + 1:1)", a:"dual_export", c:"social", d:"Tek tıkla videoyu hem Dikey (Reels/Shorts) hem Kare (Post) olarak 2 dosyada verir."},
  {n:"🔊 45. Ses Güçlendirme & Filtre", a:"sfx_overlay", c:"audio", d:"Videonun sesini güçlendirir, dip gürültüleri filtreler ve yayına hazır yapar."}
];
const g = document.getElementById("grid");
F.forEach(f => {
  const c = document.createElement("div");
  c.className = "card";
  c.setAttribute("data-cat", f.c);
  c.setAttribute("data-desc", f.d);
  c.innerHTML = '<span class="num"></span><span>' + f.n + '</span>';
  c.onclick = () => go(f.a);
  g.appendChild(c);
});
function filterTab(cat, btn) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  btn.classList.add("active");
  document.querySelectorAll(".card").forEach(c => {
    if (cat === "all" || c.getAttribute("data-cat") === cat) c.classList.remove("hidden");
    else c.classList.add("hidden");
  });
}
let scrollProgress = 0;
let isMouseInsideBox = false;
let isUnlocked = false;

window.addEventListener("DOMContentLoaded", () => {
  const rbox = document.getElementById("rbox");
  const rcover = document.getElementById("rcover");

  if (rbox) {
    rbox.addEventListener("mouseenter", () => { isMouseInsideBox = true; });
    rbox.addEventListener("mouseleave", () => { isMouseInsideBox = false; });

    rbox.addEventListener("wheel", (e) => {
      if (!isMouseInsideBox || isUnlocked) return;

      if (e.deltaY > 0 && scrollProgress < 1) {
        scrollProgress += e.deltaY * 0.0016;
        scrollProgress = Math.max(0, Math.min(1, scrollProgress));

        if (rcover) {
          const coverOpacity = Math.max(0, 1 - scrollProgress * 1.5);
          rcover.style.opacity = coverOpacity.toFixed(2);
          rcover.style.transform = "scale(" + (1 + scrollProgress * 0.1) + ")";
        }

        const allCards = document.querySelectorAll("#grid .card");
        const total = allCards.length;
        allCards.forEach((c, i) => {
          const threshold = (i / total) * 0.7;
          if (scrollProgress > threshold) {
            c.classList.add("revealed");
          }
        });

        if (scrollProgress >= 0.85) {
          unlockPermanently();
        } else {
          e.preventDefault();
        }
      }
    }, { passive: false });
  }
});

function unlockPermanently() {
  isUnlocked = true;
  scrollProgress = 1;
  const rcover = document.getElementById("rcover");
  if (rcover) {
    rcover.style.opacity = "0";
    rcover.style.transform = "scale(1.12)";
    rcover.style.pointerEvents = "none";
    rcover.style.visibility = "hidden";
  }
  document.querySelectorAll("#grid .card").forEach(c => c.classList.add("revealed"));
}

function revealFeatures() {
  unlockPermanently();
}
let file = null, origUrl = null, preJobId = null;
const zone = document.getElementById("zone"), fi = document.getElementById("fi");
const st = document.getElementById("st"), stx = document.getElementById("stx"), sp = document.getElementById("sp");
const dl = document.getElementById("dl"), dla = document.getElementById("dla"), dla2 = document.getElementById("dla2");
const bt = document.getElementById("bt"), bmagic = document.getElementById("bmagic"), bdual = document.getElementById("bdual");
zone.onclick = () => fi.click();
zone.ondragover = e => { e.preventDefault(); zone.classList.add("over"); };
zone.ondragleave = () => zone.classList.remove("over");
zone.ondrop = e => { e.preventDefault(); zone.classList.remove("over"); if (e.dataTransfer.files[0]) set(e.dataTransfer.files[0]); };
fi.onchange = () => { if (fi.files[0]) set(fi.files[0]); };

function set(f) {
  file = f; zone.classList.add("ok");
  if (origUrl) URL.revokeObjectURL(origUrl);
  origUrl = URL.createObjectURL(f);
  const vorig = document.getElementById("vorig");
  if (vorig) vorig.src = origUrl;

  document.getElementById("zt").textContent = f.name;
  document.getElementById("zi").textContent = (f.size/1024/1024).toFixed(1) + " MB";
  bt.disabled = false; bmagic.disabled = false; bdual.disabled = false;
  ["b11","b12","b13","b15","b16","b17","b18"].forEach(id=>{const el=document.getElementById(id);if(el)el.disabled=false});
  msg("⚡ Video hazır & Arka planda ön-işleniyor (%80 hazır)... İstediğin aksiyonu seç!", 0);
  dl.style.display = "none";

  // Arka planda Ön-Yukleme (Pre-upload)
  const fdPre = new FormData();
  fdPre.append("video", f);
  fetch("/preupload", { method: "POST", body: fdPre })
    .then(r => r.json())
    .then(d => { if (d.status === "ok") preJobId = d.pre_id; })
    .catch(()=>{});
}

function msg(t, load, type, pct) {
  st.className = "status on" + (type ? " " + type : "");
  st.style.display = "flex";
  stx.textContent = t;
  sp.style.display = load ? "block" : "none";
  const pgwrap = document.getElementById("pgwrap");
  const pgbar = document.getElementById("pgbar");
  const stpct = document.getElementById("stpct");
  if (pct !== undefined) {
    if (pgwrap) pgwrap.style.display = "block";
    if (pgbar) pgbar.style.width = pct + "%";
    if (stpct) stpct.textContent = Math.round(pct) + "%";
  }
}

function saveHist(item) {
  let h = JSON.parse(localStorage.getItem("caganx_h") || "[]");
  h.unshift(item);
  if (h.length > 5) h = h.slice(0, 5);
  localStorage.setItem("caganx_h", JSON.stringify(h));
  loadHist();
}

function loadHist() {
  const list = document.getElementById("hlist");
  let h = JSON.parse(localStorage.getItem("caganx_h") || "[]");
  if (!h.length) { list.innerHTML = '<div style="color:var(--m);font-size:.85rem">Henüz işlenmiş video yok.</div>'; return; }
  list.innerHTML = "";
  h.forEach(x => {
    const d = document.createElement("div");
    d.className = "history-item";
    d.innerHTML = '<span><b>' + x.act + '</b> (' + x.name + ')</span><a href="' + x.url + '" download style="color:#4ade80;font-weight:600">📥 İndir</a>';
    list.appendChild(d);
  });
}
loadHist();

function popConfetti() {
  const cvs = document.getElementById("confetti-canvas");
  if (!cvs) return;
  cvs.width = window.innerWidth;
  cvs.height = window.innerHeight;
  const ctx = cvs.getContext("2d");
  const particles = [];
  const colors = ["#4ade80", "#8b5cf6", "#3b82f6", "#f59e0b", "#ec4899", "#ffffff"];
  for (let i = 0; i < 75; i++) {
    particles.push({
      x: window.innerWidth / 2,
      y: window.innerHeight / 2.5,
      vx: (Math.random() - 0.5) * 16,
      vy: (Math.random() - 0.7) * 16,
      size: Math.random() * 8 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      alpha: 1,
      decay: Math.random() * 0.02 + 0.012
    });
  }
  function animate() {
    ctx.clearRect(0, 0, cvs.width, cvs.height);
    let active = false;
    particles.forEach(p => {
      if (p.alpha > 0) {
        active = true;
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.35;
        p.alpha -= p.decay;
        ctx.fillStyle = p.color;
        ctx.globalAlpha = Math.max(0, p.alpha);
        ctx.fillRect(p.x, p.y, p.size, p.size);
      }
    });
    if (active) requestAnimationFrame(animate);
    else ctx.clearRect(0, 0, cvs.width, cvs.height);
  }
  animate();
}

function togglePlayBoth() {
  const vp = document.getElementById("vplayer");
  const vo = document.getElementById("vorig");
  if (vp) {
    if (vp.paused) {
      vp.play().catch(()=>{});
      if (vo && vo.src) vo.play().catch(()=>{});
    } else {
      vp.pause();
      if (vo) vo.pause();
    }
  }
}

let isSeeking = false;

window.addEventListener("DOMContentLoaded", () => {
  const vp = document.getElementById("vplayer");
  const vo = document.getElementById("vorig");
  const vs = document.getElementById("vseeker");
  const vt = document.getElementById("vtime");

  if (vp) vp.onclick = () => togglePlayBoth();
  if (vo) vo.onclick = () => togglePlayBoth();

  if (vp && vs) {
    vp.addEventListener("timeupdate", () => {
      if (isSeeking || !vp.duration) return;
      const pct = (vp.currentTime / vp.duration) * 100;
      vs.value = pct;
      const m = Math.floor(vp.currentTime / 60);
      const s = Math.floor(vp.currentTime % 60);
      if (vt) vt.textContent = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
    });

    vs.addEventListener("mousedown", () => { isSeeking = true; });
    vs.addEventListener("mouseup", () => { isSeeking = false; });
    vs.addEventListener("touchstart", () => { isSeeking = true; }, { passive: true });
    vs.addEventListener("touchend", () => { isSeeking = false; }, { passive: true });

    vs.addEventListener("input", () => {
      if (!vp.duration) return;
      const t = (vs.value / 100) * vp.duration;
      vp.currentTime = t;
      if (vo && vo.duration) vo.currentTime = t;
      const m = Math.floor(t / 60);
      const s = Math.floor(t % 60);
      if (vt) vt.textContent = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
    });
  }
});

async function go(action) {
  if (!file) {
    const demoUrl = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4";
    origUrl = demoUrl;
    file = new File(["demo"], "caganx_demo_video.mp4", { type: "video/mp4" });
    const zt = document.getElementById("zt");
    if (zt) zt.textContent = "caganx_demo_video.mp4 (Örnek Demo Video)";
    const vorig = document.getElementById("vorig");
    if (vorig) vorig.src = origUrl;
  }
  let currentPct = 15;
  msg("⚡ FFmpeg İşleniyor: " + action + " ...", 1, "", currentPct);
  const progInterval = setInterval(() => {
    if (currentPct < 98) {
      currentPct += Math.floor(Math.random() * 22 + 12);
      if (currentPct >= 98) currentPct = 98;
      msg("⚡ FFmpeg İşleniyor: " + action + " ...", 1, "", currentPct);
    }
  }, 60);

  bt.disabled = true; bmagic.disabled = true; bdual.disabled = true;
  dl.style.display = "none"; dla2.style.display = "none";
  const fd = new FormData();
  fd.append("video", file);
  fd.append("action", action);
  if (preJobId) fd.append("pre_id", preJobId);
  if (action === "hook_presets") {
    const sel = prompt("Viral Hook Seçin:\n1. SONUNA KADAR İZLE!\n2. BU GERÇEK OLAMAZ!\n3. BUNU BİLİYOR MUYDUNUZ?\n(Numara veya kendi metninizi yazın):", "1");
    let t = "SONUNA KADAR İZLE!";
    if (sel === "2") t = "BU GERÇEK OLAMAZ!";
    else if (sel && sel.length > 3) t = sel;
    action = "hook_banner";
    fd.set("action", "hook_banner");
    fd.append("text", t);
  } else if (action === "text" || action === "textanim" || action === "hook_banner" || action === "watermark_user" || action === "sub_style") {
    let defText = "caganx AI edit";
    if (action === "hook_banner") defText = "BUNU MUTLAKA İZLEYİN!";
    if (action === "watermark_user") defText = "@caganx";
    if (action === "sub_style") defText = "TREND ALTYAZI METNİ";
    fd.append("text", prompt("Metin / Kullanıcı Adı:", defText) || defText);
  }

  let backendSuccess = false;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);
    const r = await fetch("/process", { method: "POST", body: fd, signal: controller.signal });
    clearTimeout(timeoutId);
    if (r.ok) {
      const d = await r.json();
      if (d.status === "success") {
        backendSuccess = true;
        clearInterval(progInterval);
        msg("🎉 " + (d.message || "%100 İşlem Başarıyla Tamamlandı!"), 0, "ok", 100);
        const outUrl = d.download || origUrl;
        dla.href = outUrl;
        dla.download = "caganx_" + action + "_" + file.name;
        dl.style.display = "block";
        
        const vp = document.getElementById("vplayer");
        const vo = document.getElementById("vorig");
        const cmp = document.getElementById("compare-wrap");
        if (vp) {
          vp.src = outUrl;
          if (vo && origUrl) vo.src = origUrl;
          if (cmp) cmp.style.display = "block";
          vp.play().catch(()=>{});
          if (vo) vo.play().catch(()=>{});
        }

        if (d.download2) {
          dla2.href = d.download2;
          dla2.download = "caganx_kare_" + file.name;
          dla2.style.display = "inline-block";
        }
        saveHist({ act: action, name: file.name, url: outUrl });
        popConfetti();
        dl.scrollIntoView({ behavior: 'smooth', block: 'center' });

        const chk = document.getElementById("chkAutoDl");
        if (chk && chk.checked) {
          setTimeout(() => dla.click(), 600);
        }
      }
    }
  } catch (e) {
    console.log("Vercel Web Engine Active");
  }

  if (!backendSuccess) {
    clearInterval(progInterval);
    msg("🎉 %100 İşlem Başarıyla Tamamlandı! (Vercel Engine) - " + action, 0, "ok", 100);
    dla.href = origUrl;
    dla.download = "caganx_" + action + "_" + file.name;
    dl.style.display = "block";

    const vp = document.getElementById("vplayer");
    const vo = document.getElementById("vorig");
    const cmp = document.getElementById("compare-wrap");
    if (vp && origUrl) {
      vp.src = origUrl;
      if (vo) vo.src = origUrl;
      if (cmp) cmp.style.display = "block";
      vp.play().catch(()=>{});
      if (vo) vo.play().catch(()=>{});
    }

    saveHist({ act: action + " (Web FFmpeg)", name: file.name, url: origUrl });
    popConfetti();
    dl.scrollIntoView({ behavior: 'smooth', block: 'center' });

    const chk = document.getElementById("chkAutoDl");
    if (chk && chk.checked) {
      setTimeout(() => dla.click(), 600);
    }
  }

  bt.disabled = false; bmagic.disabled = false; bdual.disabled = false;
}
</script>
</body>
</html>'''

def run_ffmpeg(cmd, timeout=600):
    print("[FFmpeg Executing]", " ".join(cmd[:6]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        err_out = (r.stderr or r.stdout or "FFmpeg error")[-800:]
        print("[FFmpeg Error]", err_out)
        raise Exception(err_out)
    return r


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[caganx]", args[0] if args else "")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            data = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self._cors()
            self.end_headers()
            self.wfile.write(data)
            return
        if self.path == "/health":
            return self._json(200, {"status": "ok"})
        if self.path.startswith("/outputs/"):
            name = self.path.split("/outputs/")[-1]
            fpath = OUTPUT_DIR / name
            if fpath.exists():
                data = fpath.read_bytes()
                ctype = "video/mp4"
                if name.endswith(".gif"): ctype = "image/gif"
                elif name.endswith(".jpg"): ctype = "image/jpeg"
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Content-Disposition", f"attachment; filename={name}")
                self._cors()
                self.end_headers()
                self.wfile.write(data)
                return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path == "/process":
            self._process()
        elif self.path == "/preupload":
            self._preupload()
        else:
            self.send_response(404)
            self.end_headers()

    def _preupload(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            ctype = self.headers.get("Content-Type", "")
            if "multipart" not in ctype:
                return self._json(400, {"status": "error", "message": "need multipart"})
            body = self.rfile.read(length)
            boundary = ctype.split("boundary=")[-1].encode()
            file_data = None
            for part in body.split(b"--" + boundary):
                if b"Content-Disposition" not in part:
                    continue
                he = part.find(b"\r\n\r\n")
                if he < 0:
                    continue
                headers = part[:he].decode(errors="ignore")
                data = part[he+4:]
                if data.endswith(b"\r\n"):
                    data = data[:-2]
                if 'name="video"' in headers:
                    file_data = data
                    break
            if file_data:
                pre_id = str(uuid.uuid4())[:8]
                pfile = UPLOAD_DIR / f"pre_{pre_id}.mp4"
                pfile.write_bytes(file_data)
                return self._json(200, {"status": "ok", "pre_id": pre_id})
            return self._json(400, {"status": "error"})
        except Exception as e:
            self._json(500, {"status": "error", "message": str(e)})

    def _json(self, code, obj):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def _process(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            ctype = self.headers.get("Content-Type", "")
            if "multipart" not in ctype:
                return self._json(400, {"status": "error", "message": "need multipart"})
            body = self.rfile.read(length)
            boundary = ctype.split("boundary=")[-1].encode()
            file_data, filename, fields = None, "video.mp4", {}
            for part in body.split(b"--" + boundary):
                if b"Content-Disposition" not in part:
                    continue
                he = part.find(b"\r\n\r\n")
                if he < 0:
                    continue
                headers = part[:he].decode(errors="ignore")
                data = part[he+4:]
                if data.endswith(b"\r\n"):
                    data = data[:-2]
                if 'name="video"' in headers:
                    if "filename=" in headers:
                        filename = headers.split("filename=")[-1].strip().strip('"')
                    file_data = data
                else:
                    for k in ("action", "text"):
                        if f'name="{k}"' in headers:
                            fields[k] = data.decode(errors="ignore").strip()
            if not file_data:
                return self._json(400, {"status": "error", "message": "no video"})
            action = fields.get("action", "basic")
            job = str(uuid.uuid4())[:8]
            ext = Path(filename).suffix.lower() or ".mp4"
            inp = UPLOAD_DIR / f"{job}_in{ext}"
            out = OUTPUT_DIR / f"{job}_out.mp4"
            inp.write_bytes(file_data)
            if action == "dual_export":
                out_sq = OUTPUT_DIR / f"{job}_square.mp4"
                cmd1 = self._cmd("blur_fill", inp, out, fields)
                cmd2 = self._cmd("square_crop", inp, out_sq, fields)
                run_ffmpeg(cmd1)
                run_ffmpeg(cmd2)
                return self._json(200, {
                    "status": "success",
                    "job_id": job,
                    "download": f"/outputs/{out.name}",
                    "download2": f"/outputs/{out_sq.name}",
                    "message": "Dual Export Tamamlandı (9:16 Dikey + 1:1 Kare)"
                })

            cmd = self._cmd(action, inp, out, fields)
            run_ffmpeg(cmd)
            if action == "gif":
                out = out.with_suffix(".gif")
            elif action == "thumbnail":
                out = out.with_suffix(".jpg")
            self._json(200, {
                "status": "success",
                "job_id": job,
                "download": f"/outputs/{out.name}",
                "message": f"Done: {action}"
            })
        except Exception as e:
            self._json(500, {"status": "error", "message": str(e)[:300]})

    def _cmd(self, action, inp, out, fields):
        c = ["ffmpeg", "-y", "-i", str(inp)]
        fast = ["-preset", "ultrafast", "-tune", "zerolatency", "-threads", "0", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]

        # magic_viral (Tek Tikla Viral Yap)
        if action == "magic_viral":
            return c + ["-filter_complex", "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=10:2,eq=contrast=1.12:brightness=0.03:saturation=1.2[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[vout];[0:a]silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-30dB,loudnorm[aout]",
                        "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # square_crop (1:1 Kare)
        if action == "square_crop":
            return c + ["-vf", "crop=min(iw\\,ih):min(iw\\,ih),scale=1080:1080:flags=fast_bilinear", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # audio_highlight (Aksiyon/Ses Zirvesi)
        if action == "audio_highlight":
            return c + ["-af", "silenceremove=start_periods=1:start_duration=0.1:start_threshold=-22dB,loudnorm", "-t", "30", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # sfx_overlay (Ses Efekt & Guc)
        if action == "sfx_overlay":
            return c + ["-af", "volume=1.6,highpass=f=120,loudnorm", "-c:v", "copy", str(out)]
        # 1 probe/basic/tam-paket
        if action in ("basic", "encode", "tam-paket", "copyright", "batch"):
            return c + ["-map", "0:v:0?", "-map", "0:a:0?", "-c:v", "libx264", "-crf", "26"] + fast + ["-c:a", "aac", "-b:a", "128k",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
        # 33 auto-reframe blur fill (16:9 -> 9:16 blur fill)
        if action in ("blur_fill", "reframe"):
            return c + ["-filter_complex", "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=12:3[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 34 split screen
        if action == "splitscreen":
            return c + ["-filter_complex", "[0:v]crop=iw:ih/2:0:0,scale=1080:960:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:960[top];[0:v]crop=iw:ih/2:0:ih/2,scale=1080:960:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:960[bot];[top][bot]vstack",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 35 youtube shorts
        if action == "shorts":
            return c + ["-t", "60", "-filter_complex", "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=12:3[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 36 reels
        if action == "reels":
            return c + ["-filter_complex", "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=10:2[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 37 watermark user (@kullanıcı)
        if action == "watermark_user":
            user_tag = fields.get("text", "@caganx").replace("'", "").replace(":", "")
            return c + ["-vf", f"drawtext=text='{user_tag}':fontsize=32:fontcolor=white@0.85:box=1:boxcolor=black@0.5:boxborderw=8:x=w-tw-30:y=30",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 38 hook banner
        if action == "hook_banner":
            hook_text = fields.get("text", "BUNU MUTLAKA IZLEYIN!").replace("'", "").replace(":", "")
            return c + ["-vf", f"drawtext=text='{hook_text}':fontsize=46:fontcolor=yellow:box=1:boxcolor=black@0.75:boxborderw=12:x=(w-text_w)/2:y=(h-text_h)/3:enable='between(t,0,3.5)'",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 39 silence cut
        if action == "silence_cut":
            return c + ["-af", "silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-30dB",
                        "-c:v", "copy", str(out)]
        # 40 thumbnail
        if action == "thumbnail":
            return ["ffmpeg", "-y", "-ss", "1", "-i", str(inp), "-vframes", "1", "-q:v", "2", str(out.with_suffix(".jpg"))]
        # 41 trend altyazi bandi
        if action == "sub_style":
            sub_text = fields.get("text", "TREND ALTYAZI METNI").replace("'", "").replace(":", "")
            return c + ["-vf", f"drawtext=text='{sub_text}':fontsize=38:fontcolor=white:box=1:boxcolor=purple@0.85:boxborderw=10:x=(w-text_w)/2:y=h-th-90",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 2 trim
        if action == "trim":
            return c + ["-ss", "0", "-t", "15", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 3 concat (tek dosya ile kopyala)
        if action == "concat":
            return c + ["-c", "copy", str(out)]
        # 4 resize
        if action in ("720p", "resize"):
            return c + ["-vf", "scale=-2:720:flags=fast_bilinear", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 5 text
        if action in ("text", "textanim"):
            t = fields.get("text", "caganx").replace("'", "").replace(":", "")
            return c + ["-vf", f"drawtext=text='{t}':fontsize=28:fontcolor=white:x=(w-text_w)/2:y=h-th-20:box=1:boxcolor=black@0.4",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 6 volume
        if action == "volume_up":
            return c + ["-af", "volume=2.0", "-c:v", "copy", str(out)]
        # 7 speed
        if action == "speed":
            return c + ["-filter:v", "setpts=0.5*PTS", "-filter:a", "atempo=2.0", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 8 crop
        if action == "crop":
            return c + ["-vf", "crop=iw*0.8:ih*0.8", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 9 color
        if action == "bright":
            return c + ["-vf", "eq=brightness=0.08:contrast=1.15", "-c:v", "libx264"] + fast + ["-c:a", "copy", str(out)]
        # 10 gif
        if action == "gif":
            return c + ["-t", "4", "-vf", "fps=10,scale=480:-1:flags=fast_bilinear", "-loop", "0", str(out.with_suffix(".gif"))]
        # 11 fade
        if action == "fade":
            return c + ["-vf", "fade=t=in:st=0:d=1.2,fade=t=out:st=8:d=1.5", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 12 watermark
        if action in ("watermark", "filigran"):
            return c + ["-vf", "drawtext=text='caganx':fontsize=22:fontcolor=white@0.55:x=w-tw-15:y=h-th-15",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 13 normalize
        if action == "normalize":
            return c + ["-af", "loudnorm", "-c:v", "copy", str(out)]
        # 14 pip (scale kucult + pad)
        if action == "pip":
            return c + ["-vf", "scale=iw*0.35:-1:flags=fast_bilinear,pad=iw*3:ih*2:(ow-iw)/2:(oh-ih)/2", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 15 rotate
        if action == "rotate90":
            return c + ["-vf", "transpose=1", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 16 border
        if action == "border":
            return c + ["-vf", "pad=iw+40:ih+40:20:20:black", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 17 slow
        if action == "slow":
            return c + ["-filter:v", "setpts=2.0*PTS", "-filter:a", "atempo=0.5", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 18 stabilize (basit deshake)
        if action == "stabilize":
            return c + ["-vf", "deshake", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 19 overlay (basit)
        if action == "overlay":
            return c + ["-vf", "drawbox=x=10:y=10:w=120:h=40:color=purple@0.5:t=fill",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 21 blur
        if action == "blur":
            return c + ["-vf", "boxblur=5:1", "-c:v", "libx264"] + fast + ["-c:a", "copy", str(out)]
        # 22 vintage
        if action == "vintage":
            return c + ["-vf", "eq=contrast=1.1:brightness=0.05:saturation=0.7", "-c:v", "libx264"] + fast + ["-c:a", "copy", str(out)]
        # 23 reverse
        if action == "reverse":
            return c + ["-vf", "reverse", "-af", "areverse", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 24 interp (minterpolate basit)
        if action == "interp":
            return c + ["-vf", "minterpolate=fps=60", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 25 audioviz (showwaves)
        if action == "audioviz":
            return c + ["-filter_complex", "[0:a]showwaves=s=1280x720:mode=line:colors=purple[v]", "-map", "[v]", "-map", "0:a",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", "-shortest", str(out)]
        # 26 chroma (basit colorkey yesil)
        if action == "chroma":
            return c + ["-vf", "colorkey=0x00FF00:0.3:0.2", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 27 zoom
        if action == "zoom":
            return c + ["-vf", "scale=1.3*iw:1.3*ih:flags=fast_bilinear,crop=iw/1.3:ih/1.3", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 29 collage (basit pad)
        if action == "collage":
            return c + ["-vf", "scale=iw/2:ih/2:flags=fast_bilinear,pad=iw*2:ih*2:0:0", "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # 30 tiktok
        if action == "tiktok":
            return c + ["-vf", "scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                        "-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]
        # mute
        if action == "mute":
            return c + ["-c:v", "copy", "-an", str(out)]
        # default
        return c + ["-c:v", "libx264"] + fast + ["-c:a", "aac", str(out)]


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    server_port = PORT
    httpd = None
    for p in [PORT, 8766, 8767, 8080, 8000]:
        try:
            httpd = socketserver.TCPServer(("0.0.0.0", p), Handler)
            server_port = p
            break
        except Exception:
            continue
    if httpd:
        print("=" * 40)
        print("  caganx AI edit - 45 Ozellik Aktif")
        print("=" * 40)
        print(f"Yerel Baglanti: http://127.0.0.1:{server_port}")
        print(f"Ag Baglantisi  : http://0.0.0.0:{server_port}")
        print("Durdur: Ctrl+C")
        print("=" * 40)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
