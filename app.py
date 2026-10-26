"""Rekhalex Module 1: Flask app, written to run both locally and on Vercel.

Local:   python app.py      then open http://127.0.0.1:5000
Vercel:  Vercel finds the `app` object below automatically.

Nothing is written to disk. The enhanced image is sent back inside the same
response, because serverless functions have no permanent storage and two
requests may be handled by two different machines.
"""
import base64
import io
import time
from pathlib import Path

import cv2
from flask import Flask, jsonify, request
from PIL import Image, UnidentifiedImageError

from enhance import Options, enhance, load_image

ALLOWED = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
MAX_RESPONSE_BYTES = 3_200_000  # Vercel caps request and response bodies at 4.5 MB

app = Flask(__name__, static_folder="public", static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 4_400_000
Image.MAX_IMAGE_PIXELS = 120_000_000


@app.get("/")
def index():
    return app.send_static_file("index.html")


def encode(gray, binarized):
    """PNG for black and white (small). JPEG for greyscale, lowering the quality
    until the reply fits under the platform limit."""
    if binarized:
        ok, buf = cv2.imencode(".png", gray)
        return "png", buf.tobytes()
    for q in (92, 85, 75, 65):
        ok, buf = cv2.imencode(".jpg", gray, [cv2.IMWRITE_JPEG_QUALITY, q])
        if len(buf) * 4 / 3 < MAX_RESPONSE_BYTES:
            break
    return "jpg", buf.tobytes()


@app.post("/api/enhance")
def api_enhance():
    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify(error="Choose an image first."), 400
    if Path(f.filename).suffix.lower() not in ALLOWED:
        return jsonify(error="Unsupported file type. Use JPG, PNG, TIFF, BMP or WebP."), 400

    flag = lambda name, default: request.form.get(name, str(default)).lower() in ("1", "true", "on")
    try:
        opts = Options(
            deskew=flag("deskew", True),
            flatten=flag("flatten", True),
            denoise=flag("denoise", True),
            deblur=flag("deblur", True),
            contrast=flag("contrast", True),
            binarize=request.form.get("output") == "bw",
            deblur_strength=max(0.3, min(2.0, float(request.form.get("deblur_strength", 1.0)))),
        )
    except ValueError:
        return jsonify(error="Bad option value."), 400

    try:
        rgb = load_image(io.BytesIO(f.read()), opts.max_side)
    except (UnidentifiedImageError, OSError):
        return jsonify(error="That file could not be read as an image."), 400

    t0 = time.time()
    result = enhance(rgb, opts)
    elapsed = time.time() - t0

    ext, data = encode(result.image, opts.binarize)
    mime = "image/png" if ext == "png" else "image/jpeg"
    return jsonify(
        enhanced="data:%s;base64,%s" % (mime, base64.b64encode(data).decode()),
        ext=ext,
        before=result.before,
        after=result.after,
        steps=result.steps,
        seconds=round(elapsed, 1),
        size=[int(result.image.shape[1]), int(result.image.shape[0])],
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify(error="That file is too large for the server (4.4 MB limit)."), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
