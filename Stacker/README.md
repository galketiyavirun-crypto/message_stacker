# Discord Stacker - Web Version

Turn your original Python desktop app into a beautiful web tool that anyone can use in their browser.  
No installation needed for users. Your Python code stays safe on the server.

## What Changed & Why
- **Original**: Tkinter desktop app with interactive popups ("Is this a MAIN message?"), per-frame duration dialogs, moviepy + ffmpeg for MP4 + audio.
- **Web version**: Simplified for the browser.
  - Upload multiple images → one progressive stack (builds up like your `create_stacked_frames`).
  - Single global duration (slider + number).
  - Outputs **animated GIF** (no ffmpeg / moviepy needed → much easier & cheaper to host).
  - Beautiful Discord-themed UI with ad spaces exactly as you wanted ("work in the middle, ads around it").
  - Full JavaScript UX: live thumbnails, drag & drop, processing spinner, instant preview of result GIF.

This keeps 95% of the magic of your original script while making it accessible to everyone.

## How to Run Locally (on your computer)

1. Make sure you have Python 3.8+
2. Open terminal / PowerShell in this folder
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python app.py
   ```
5. Open your browser → http://127.0.0.1:5000

Upload some test Discord screenshots and hit Generate. It should work exactly like your desktop version but without the annoying popups.

## File Structure
```
artifacts/
├── app.py              ← Flask backend (your logic lives here)
├── requirements.txt
├── templates/
│   └── index.html      ← The nice frontend with ads layout + Tailwind
└── README.md
```

## How to Deploy for Free (with ads later)

### Recommended: Render.com (easiest free tier in 2026)
1. Push this folder to a GitHub repo (public or private)
2. Go to render.com → New Web Service
3. Connect your GitHub repo
4. It auto-detects Python + Flask
5. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`   (or leave default)
6. Deploy → get your free .onrender.com URL

Free tier sleeps after 15 min inactivity (wakes in ~30s). Perfect for starting.

Other good free options: Railway.app, PythonAnywhere (great for pure Python).

**Note on moviepy / MP4 + audio**: Not included yet because it requires ffmpeg on the server (extra setup).  
The current GIF version is lighter, faster, and works everywhere. We can add MP4 + discord.mp3 audio later if you want (needs a paid plan or Docker on Render).

## Adding Real Ads (to get paid)

Your HTML already has perfect layout:
- Top banner
- Left + Right sidebars
- Bottom banner
- Tool perfectly centered

**To monetize**:
1. Sign up for Google AdSense (or Ezoic, Mediavine, etc.)
2. **Important**: Most ad networks require you to be **18+**. If you're under 18, your parent/guardian must create the AdSense account and add the site.
3. Replace the placeholder `<div class="ad-placeholder">` blocks with the real ad code snippets from AdSense.
4. Apply for approval (site must have some content + traffic).
5. Once approved, ads will show and you earn when people click / view.

The layout you wanted ("the work is done in the middle and all the ads are around it") is already built in!

## Future Upgrades You Can Add Easily
- Multiple conversation groups (with JS checkboxes or tabs)
- Per-frame duration editor
- MP4 export + background audio (discord.mp3)
- User accounts / history
- Darker / more Beluga-themed visuals

Everything is in `app.py` — your original stacking logic is preserved in `create_progressive_stacked_frames()`.

## Questions?
Just ask! I kept the code clean and commented so you can edit the backend Python anytime for upgrades.

Enjoy making Beluga videos 10x easier 🚀
