from __future__ import annotations

import uuid
from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from track3.demo.predictor import VehicleReIDPredictor


APP_ROOT = Path(__file__).parent

UPLOAD_FOLDER = APP_ROOT / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

CHECKPOINT = Path("track3/checkpoints/best_model.pth")

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
}

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)


predictor = None

if CHECKPOINT.exists():

    print(f"Loading checkpoint: {CHECKPOINT}")

    predictor = VehicleReIDPredictor(CHECKPOINT)

    print("Model loaded successfully.")

else:

    print("Checkpoint not found.")


def allowed_file(filename: str) -> bool:

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def index():

    return render_template("index.html")


@app.route(
    "/compare",
    methods=["POST"],
)
def compare():

    if predictor is None:

        return render_template(
            "index.html",
            error="Model checkpoint not found.",
        )

    query = request.files.get("query")
    gallery = request.files.get("gallery")

    if query is None or gallery is None:

        return render_template(
            "index.html",
            error="Please upload both images.",
        )

    if not allowed_file(query.filename):

        return render_template(
            "index.html",
            error="Invalid query image.",
        )

    if not allowed_file(gallery.filename):

        return render_template(
            "index.html",
            error="Invalid gallery image.",
        )

    query_name = (
        f"{uuid.uuid4()}_"
        + secure_filename(query.filename)
    )

    gallery_name = (
        f"{uuid.uuid4()}_"
        + secure_filename(gallery.filename)
    )

    query_path = UPLOAD_FOLDER / query_name
    gallery_path = UPLOAD_FOLDER / gallery_name

    query.save(query_path)
    gallery.save(gallery_path)

    result = predictor.compare(
        query_path,
        gallery_path,
    )

    return render_template(
        "index.html",
        result=result,
        query_image=query_name,
        gallery_image=gallery_name,
    )


if __name__ == "__main__":

    app.run(
        debug=True,
    )