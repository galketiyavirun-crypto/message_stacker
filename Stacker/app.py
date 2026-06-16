from flask import Flask, request, send_file, jsonify, render_template
import io
from PIL import Image

app = Flask(__name__)
app.secret_key = "discord-stacker-dev-key"  # change in production

def create_progressive_stacked_frames(images):
    """Create progressive stack frames like the original desktop app (one big group)."""
    if not images:
        return []
    frames = []
    stacked = images[0].copy()
    frames.append(stacked.copy())
    for img in images[1:]:
        total_width = max(stacked.width, img.width)
        total_height = stacked.height + img.height
        new_stack = Image.new("RGB", (total_width, total_height), color=(54, 57, 63))
        new_stack.paste(stacked, (0, 0))
        new_stack.paste(img, (0, stacked.height))
        stacked = new_stack
        frames.append(stacked.copy())
    return frames

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        files = request.files.getlist("images")
        if not files or all(f.filename == "" for f in files):
            return jsonify({"error": "No images uploaded. Please select at least one screenshot."}), 400

        # Get duration (seconds per frame)
        try:
            duration = float(request.form.get("duration", 1.75))
        except:
            duration = 1.75
        if duration < 0.1:
            duration = 0.1
        if duration > 10:
            duration = 10

        # Load all images in the exact order uploaded (respect user selection order)
        images = []
        for file in files:
            if file.filename == "":
                continue
            try:
                img = Image.open(file.stream).convert("RGB")
                images.append(img)
            except Exception as img_err:
                return jsonify({"error": f"Could not read image '{file.filename}': {str(img_err)}"}), 400

        if len(images) < 1:
            return jsonify({"error": "No valid images could be processed."}), 400

        # Build progressive stacked frames (adapted from your original create_stacked_frames)
        frames = create_progressive_stacked_frames(images)

        # Create animated GIF entirely in memory (no disk, no ffmpeg/moviepy needed!)
        gif_buffer = io.BytesIO()
        if len(frames) == 1:
            frames[0].save(gif_buffer, format="GIF")
        else:
            frames[0].save(
                gif_buffer,
                format="GIF",
                save_all=True,
                append_images=frames[1:],
                duration=int(duration * 1000),  # milliseconds
                loop=0,
                optimize=False  # set True if you want smaller files (slower to generate)
            )
        gif_buffer.seek(0)

        return send_file(
            gif_buffer,
            mimetype="image/gif",
            as_attachment=True,
            download_name="discord_stacked_beluga_style.gif"
        )

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

if __name__ == "__main__":
    print("🚀 Discord Stacker Web running at http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
