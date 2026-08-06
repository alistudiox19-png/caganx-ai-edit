from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import subprocess
import os
import uuid
import tempfile
from pathlib import Path

app = Flask(__name__)
CORS(app, origins="*")

UPLOAD_DIR = Path(tempfile.gettempdir()) / "caganx_uploads"
OUTPUT_DIR = Path(tempfile.gettempdir()) / "caganx_outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

MAX_SIZE = 50 * 1024 * 1024  # 50MB limit for free tier

import json
import urllib.request
import urllib.error

@app.route("/")
def index():
    return jsonify({"status": "ok", "service": "caganx AI edit - FFmpeg Cloud Backend", "features": 46})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json or {}
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"status": "error", "reply": "Lütfen bir mesaj yazın."}), 400

    system_instruction = """Sen 'caganx AI edit' platformunun akıllı, samimi, uzman video editör yapay zeka asistanısın. 
Kullanıcı seninle sohbet eder veya videosunu düzenlemen için komutlar verir.
Sen hem bir insan gibi samimi, coşkulu ve yardımsever cevap vereceksin hem de kullanıcının isteğine göre 45 video düzenleme özelliğimizden en uygun olan 'action' kodunu seçeceksin.

Kullanabileceğin 45 Action Kodu:
- magic_viral (Sihirli viral dokunuş, otomatik kombo edit)
- basic (Video analiz, standart kodlama)
- trim (15 saniyelik kısa klip kesme)
- concat (Video birleştirme)
- 720p (720p HD çözünürlük)
- text / textanim (Videoya animasyonlu yazı ekleme)
- volume_up (Sesi 2 katına 200% çıkarma)
- speed (2x hızlı çekim)
- crop (Ekran kenarlarını kırpma, odağa yakınlaşma)
- bright (Canlı parlaklık ve renk)
- gif (4 saniyelik döngülü GIF yapma)
- fade (Kararma açılma geçişi)
- watermark (Logo filigranı ekleme)
- normalize (Ses seviyesi eşitleme)
- pip (Resim içinde resim)
- rotate90 (90 derece dik döndürme)
- border (Siyah dolgu çerçevesi)
- slow (0.5x slow-motion ağır çekim)
- stabilize (Titreşim sarsıntı engelleme)
- overlay (Bilgilendirme kutusu katmanı)
- blur (Sinematik bulanıklık)
- vintage (Retro nostaljik renk)
- reverse (Tersine oynatma)
- interp (60 FPS akıcı kare)
- audioviz (Ses frekans dalgası)
- chroma (Yeşil ekran temizleme)
- zoom (Dinamik merkeze yakınlaşma)
- blur_fill / tiktok (1080x1920 dikey TikTok/Reels formatı)
- splitscreen (Oyun/kamera bölünmüş ekran)
- shorts (60 saniye YouTube Shorts)
- reels (Instagram Reels formatı)
- hook_banner / hook_presets (İlk 3sn viral sarı başlık)
- silence_cut (Sessizlik ve nefes boşluklarını kesme)
- thumbnail (Yüksek kalite kapak resmi .jpg çıkarma)
- sub_style (Trend altyazı bandı)
- audio_highlight (Sesteki en heyecanlı 30sn klip)
- dual_export (Hem 9:16 hem 1:1 çift format çıktı)
- sfx_overlay (Ses güçlendirme ve gürültü filtresi)

Yanıtını SADECE geçerli bir JSON objesi olarak ver. Başka hiçbir açıklama yazma:
{
  "reply": "Samimi, insan gibi arkadaş canlısı Türkçe cevabın",
  "action": "seçtiğin_action_kodu",
  "custom_text": "varsa_videoya_yazılacak_metin"
}"""

    return jsonify({
        "status": "fallback",
        "info": "Local AI Engine Active"
    })

@app.route("/process", methods=["POST"])
def process():
    try:
        if "video" not in request.files:
            return jsonify({"status": "error", "message": "Video dosyasi bulunamadi"}), 400

        video = request.files["video"]
        action = request.form.get("action", "basic")
        text = request.form.get("text", "caganx")
        job_id = str(uuid.uuid4())[:8]

        inp = UPLOAD_DIR / f"{job_id}_{video.filename}"
        video.save(str(inp))

        if inp.stat().st_size > MAX_SIZE:
            inp.unlink()
            return jsonify({"status": "error", "message": "Dosya 50MB limitini asiyor"}), 400

        out = OUTPUT_DIR / f"{job_id}_out.mp4"
        cmd = build_cmd(action, str(inp), str(out), text)

        if action == "thumbnail":
            out = out.with_suffix(".jpg")
        if action == "gif":
            out = out.with_suffix(".gif")

        result = subprocess.run(cmd, capture_output=True, timeout=120)

        if result.returncode != 0 or not out.exists():
            inp.unlink(missing_ok=True)
            err = result.stderr.decode("utf-8", errors="ignore")[:200]
            return jsonify({"status": "error", "message": f"FFmpeg hatasi: {err}"}), 500

        inp.unlink(missing_ok=True)

        return jsonify({
            "status": "success",
            "job_id": job_id,
            "download": f"/outputs/{out.name}",
            "message": f"Basarili: {action}"
        })
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Islem zaman asimina ugradi (120s)"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)[:300]}), 500

@app.route("/outputs/<filename>")
def serve_output(filename):
    fpath = OUTPUT_DIR / filename
    if fpath.exists():
        res = make_response(send_file(str(fpath), as_attachment=True))
        res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Access-Control-Allow-Headers"] = "*"
        return res
    return jsonify({"status": "error", "message": "Dosya bulunamadi"}), 404

@app.route("/preupload", methods=["POST"])
def preupload():
    return jsonify({"status": "ok", "pre_id": str(uuid.uuid4())[:8]})


def build_cmd(action, inp, out, text="caganx"):
    c = ["ffmpeg", "-y", "-i", inp]
    fast = ["-preset", "ultrafast", "-tune", "zerolatency", "-threads", "0",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    text = text.replace("'", "").replace(":", "").replace('"', '')

    if action == "magic_viral":
        return c + ["-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=10:2,eq=contrast=1.12:brightness=0.03:saturation=1.2[bg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[vout];"
            "[0:a]silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-30dB,loudnorm[aout]",
            "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action in ("basic", "encode", "tam-paket", "copyright", "batch"):
        return c + ["-map", "0:v:0?", "-map", "0:a:0?", "-c:v", "libx264", "-crf", "26"] + fast + ["-c:a", "aac", "-b:a", "128k", out]

    if action in ("blur_fill", "reframe"):
        return c + ["-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=12:3[bg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2",
            "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "splitscreen":
        return c + ["-filter_complex",
            "[0:v]crop=iw:ih/2:0:0,scale=1080:960:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:960[top];"
            "[0:v]crop=iw:ih/2:0:ih/2,scale=1080:960:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:960[bot];"
            "[top][bot]vstack",
            "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "shorts":
        return c + ["-t", "60", "-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=12:3[bg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2",
            "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "reels":
        return c + ["-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=10:2[bg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2",
            "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "tiktok":
        return c + ["-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=10:2[bg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2",
            "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "square_crop":
        return c + ["-vf", "crop=min(iw\\,ih):min(iw\\,ih),scale=1080:1080:flags=fast_bilinear",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "trim":
        return c + ["-ss", "0", "-t", "15", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "concat":
        return c + ["-c", "copy", out]

    if action in ("720p", "resize"):
        return c + ["-vf", "scale=-2:720:flags=fast_bilinear", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action in ("text", "textanim"):
        return c + ["-vf", f"drawtext=text='{text}':fontsize=28:fontcolor=white:x=(w-text_w)/2:y=h-th-20:box=1:boxcolor=black@0.4",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "volume_up":
        return c + ["-af", "volume=2.0", "-c:v", "copy", out]

    if action == "speed":
        return c + ["-filter:v", "setpts=0.5*PTS", "-filter:a", "atempo=2.0", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "crop":
        return c + ["-vf", "crop=iw*0.8:ih*0.8", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "bright":
        return c + ["-vf", "eq=brightness=0.08:contrast=1.15", "-c:v", "libx264"] + fast + ["-c:a", "copy", out]

    if action == "gif":
        out_gif = out.replace(".mp4", ".gif") if out.endswith(".mp4") else out
        return c + ["-t", "4", "-vf", "fps=10,scale=480:-1:flags=fast_bilinear", "-loop", "0", out_gif]

    if action == "fade":
        return c + ["-vf", "fade=t=in:st=0:d=1.2,fade=t=out:st=8:d=1.5", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action in ("remove_watermark", "clean_watermark", "logo_clean"):
        # AI üretimi videolardaki (Runway, Sora, Pika, Kling) köşe filigranlarını delogo ile siler
        return c + ["-filter_complex",
                    "[0:v]delogo=x=main_w-240:y=main_h-100:w=230:h=90:show=0[v1];"
                    "[v1]delogo=x=10:y=main_h-100:w=220:h=90:show=0[v2];"
                    "[v2]delogo=x=main_w-240:y=10:w=230:h=90:show=0[vout]",
                    "-map", "[vout]", "-map", "0:a?", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action in ("watermark", "filigran"):
        return c + ["-vf", "drawtext=text='caganx':fontsize=22:fontcolor=white@0.55:x=w-tw-15:y=h-th-15",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "normalize":
        return c + ["-af", "loudnorm", "-c:v", "copy", out]

    if action == "pip":
        return c + ["-vf", "scale=iw/3:ih/3,pad=iw*3:ih*3:(ow-iw)/1.1:(oh-ih)/1.1:black",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "rotate90":
        return c + ["-vf", "transpose=1", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "border":
        return c + ["-vf", "pad=iw+40:ih+40:20:20:black", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "slow":
        return c + ["-filter:v", "setpts=2.0*PTS", "-filter:a", "atempo=0.5", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "stabilize":
        return c + ["-vf", "deshake", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "overlay":
        return c + ["-vf", "drawbox=x=10:y=10:w=200:h=40:color=purple@0.7:t=fill,drawtext=text='caganx AI':fontsize=20:fontcolor=white:x=20:y=18",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "blur":
        return c + ["-vf", "boxblur=8:2", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "vintage":
        return c + ["-vf", "colorbalance=rs=0.15:gs=-0.05:bs=-0.15,eq=contrast=1.15:saturation=0.8",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "reverse":
        return c + ["-vf", "reverse", "-af", "areverse", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "interp":
        return c + ["-vf", "minterpolate=fps=60:mi_mode=mci", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "audioviz":
        return c + ["-filter_complex", "[0:a]showwaves=s=1280x720:mode=line:colors=0x8b5cf6|0x22c55e:rate=25[v]",
                    "-map", "[v]", "-map", "0:a", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "chroma":
        return c + ["-vf", "chromakey=0x00ff00:0.3:0.1", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "zoom":
        return c + ["-vf", "zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=30",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "collage":
        return c + ["-vf", "scale=540:540,pad=1080:1080:270:270:black", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "watermark_user":
        return c + ["-vf", f"drawtext=text='{text}':fontsize=32:fontcolor=white@0.85:box=1:boxcolor=black@0.5:boxborderw=8:x=w-tw-30:y=30",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "hook_banner":
        return c + ["-vf", f"drawtext=text='{text}':fontsize=46:fontcolor=yellow:box=1:boxcolor=black@0.75:boxborderw=12:x=(w-text_w)/2:y=(h-text_h)/3:enable='between(t,0,3.5)'",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "silence_cut":
        return c + ["-af", "silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-30dB",
                    "-c:v", "copy", out]

    if action == "thumbnail":
        out_jpg = out.replace(".mp4", ".jpg") if out.endswith(".mp4") else out
        return ["ffmpeg", "-y", "-ss", "1", "-i", inp, "-vframes", "1", "-q:v", "2", out_jpg]

    if action == "sub_style":
        return c + ["-vf", f"drawtext=text='{text}':fontsize=38:fontcolor=white:box=1:boxcolor=purple@0.85:boxborderw=10:x=(w-text_w)/2:y=h-th-90",
                    "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "audio_highlight":
        return c + ["-af", "silenceremove=start_periods=1:start_duration=0.1:start_threshold=-22dB,loudnorm",
                    "-t", "30", "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    if action == "sfx_overlay":
        return c + ["-af", "volume=1.6,highpass=f=120,loudnorm", "-c:v", "copy", out]

    if action == "dual_export":
        return c + ["-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,crop=1080:1920,boxblur=10:2[bg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease:flags=fast_bilinear[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2",
            "-c:v", "libx264"] + fast + ["-c:a", "aac", out]

    # fallback
    return c + ["-c:v", "libx264"] + fast + ["-c:a", "aac", out]


# ═══════════════════════════════════════════════
# GERÇEK ZAMANLI ANALİTİK & ADMIN PANELİ API
# ═══════════════════════════════════════════════
import sqlite3 as _sql
import time as _time

ANALYTICS_DB = Path(tempfile.gettempdir()) / "caganx_analytics.db"

def _init_analytics():
    conn = _sql.connect(str(ANALYTICS_DB))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        sid TEXT PRIMARY KEY, ip TEXT, ua TEXT, page TEXT,
        first_seen REAL, last_seen REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, sid TEXT, username TEXT,
        ip TEXT, action TEXT, details TEXT, ts REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS errors (
        id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, page TEXT,
        msg TEXT, stack TEXT, ts REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bans (
        ip TEXT PRIMARY KEY, reason TEXT, ts REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY, val TEXT)''')
    c.execute("INSERT OR IGNORE INTO settings VALUES ('maintenance','0')")
    c.execute("INSERT OR IGNORE INTO settings VALUES ('announcement','')")
    conn.commit(); conn.close()

_init_analytics()

def _adb():
    conn = _sql.connect(str(ANALYTICS_DB))
    conn.row_factory = _sql.Row
    return conn

# --- Heartbeat Ping (siteden her 5 saniyede gelir) ---
@app.route("/api/ping", methods=["POST"])
def api_ping():
    d = request.json or {}
    sid = d.get("session_id", request.remote_addr)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    ua = request.headers.get("User-Agent", "?")[:200]
    page = d.get("page", "/")
    now = _time.time()
    conn = _adb(); c = conn.cursor()
    # Ban kontrol
    c.execute("SELECT ip FROM bans WHERE ip=?", (ip,))
    if c.fetchone():
        conn.close()
        return jsonify({"status":"banned","message":"Erişiminiz engellenmiştir."}), 403
    c.execute("SELECT sid FROM sessions WHERE sid=?", (sid,))
    if c.fetchone():
        c.execute("UPDATE sessions SET last_seen=?,page=?,ip=? WHERE sid=?", (now,page,ip,sid))
    else:
        c.execute("INSERT INTO sessions VALUES(?,?,?,?,?,?)", (sid,ip,ua,page,now,now))
        c.execute("INSERT INTO logs(sid,username,ip,action,details,ts) VALUES(?,?,?,?,?,?)",
                  (sid,"Misafir",ip,"Siteye Giriş",page,now))
    c.execute("SELECT key,val FROM settings")
    sets = {r["key"]:r["val"] for r in c.fetchall()}
    conn.commit(); conn.close()
    return jsonify({"status":"ok",
                    "maintenance": sets.get("maintenance","0")=="1",
                    "announcement": sets.get("announcement","")})

# --- Aksiyon Logu ---
@app.route("/api/log_activity", methods=["POST"])
def api_log_activity():
    d = request.json or {}
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    conn = _adb()
    conn.execute("INSERT INTO logs(sid,username,ip,action,details,ts) VALUES(?,?,?,?,?,?)",
                 (d.get("session_id",""), d.get("username","Misafir"), ip,
                  d.get("action",""), d.get("details",""), _time.time()))
    conn.commit(); conn.close()
    return jsonify({"status":"ok"})

# --- Hata Logu ---
@app.route("/api/log_error", methods=["POST"])
def api_log_error():
    d = request.json or {}
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    conn = _adb()
    conn.execute("INSERT INTO errors(ip,page,msg,stack,ts) VALUES(?,?,?,?,?)",
                 (ip, d.get("page",""), d.get("error",""), d.get("stack",""), _time.time()))
    conn.commit(); conn.close()
    return jsonify({"status":"ok"})

# --- Admin İstatistik API (admin panel bunu çeker) ---
@app.route("/api/admin/stats", methods=["GET"])
def api_admin_stats():
    conn = _adb(); c = conn.cursor()
    now = _time.time()
    # Eski oturumları temizle (60s inaktif)
    c.execute("DELETE FROM sessions WHERE last_seen < ?", (now-60,))
    conn.commit()
    c.execute("SELECT COUNT(*) FROM sessions"); active = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM logs WHERE ts>=?", (now-86400,)); today = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT ip) FROM logs"); total = c.fetchone()[0]
    c.execute("SELECT sid,ip,ua,page,last_seen FROM sessions ORDER BY last_seen DESC LIMIT 20")
    active_list = [dict(r) for r in c.fetchall()]
    c.execute("SELECT sid,username,ip,action,details,ts FROM logs ORDER BY id DESC LIMIT 30")
    recent = [dict(r) for r in c.fetchall()]
    c.execute("SELECT ip,page,msg,ts FROM errors ORDER BY id DESC LIMIT 20")
    errs = [dict(r) for r in c.fetchall()]
    c.execute("SELECT ip,reason,ts FROM bans"); bans = [dict(r) for r in c.fetchall()]
    c.execute("SELECT key,val FROM settings"); sets = {r["key"]:r["val"] for r in c.fetchall()}
    conn.close()
    return jsonify({"active":active,"today":today,"total":total,
                    "active_list":active_list,"logs":recent,"errors":errs,
                    "bans":bans,"settings":sets})

# --- Admin: Bakım Modu ---
@app.route("/api/admin/toggle_maintenance", methods=["POST"])
def api_toggle_maint():
    d = request.json or {}
    val = "1" if d.get("maintenance") else "0"
    conn = _adb()
    conn.execute("INSERT OR REPLACE INTO settings VALUES('maintenance',?)", (val,))
    conn.commit(); conn.close()
    return jsonify({"status":"ok","maintenance": val=="1"})

# --- Admin: Duyuru ---
@app.route("/api/admin/set_announcement", methods=["POST"])
def api_set_ann():
    d = request.json or {}
    conn = _adb()
    conn.execute("INSERT OR REPLACE INTO settings VALUES('announcement',?)", (d.get("text",""),))
    conn.commit(); conn.close()
    return jsonify({"status":"ok"})

# --- Admin: Ban ---
@app.route("/api/admin/ban_ip", methods=["POST"])
def api_ban():
    d = request.json or {}
    ip = d.get("ip","").strip()
    if not ip: return jsonify({"status":"error"}), 400
    conn = _adb()
    conn.execute("INSERT OR REPLACE INTO bans VALUES(?,?,?)", (ip, d.get("reason","Kural ihlali"), _time.time()))
    conn.commit(); conn.close()
    return jsonify({"status":"ok"})

@app.route("/api/admin/unban_ip", methods=["POST"])
def api_unban():
    d = request.json or {}
    conn = _adb()
    conn.execute("DELETE FROM bans WHERE ip=?", (d.get("ip",""),))
    conn.commit(); conn.close()
    return jsonify({"status":"ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

