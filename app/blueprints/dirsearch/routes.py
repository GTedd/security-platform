from flask import Blueprint, request, render_template, Response
from app.decorators import login_required
from .dirsearch import dirsearch

bp = Blueprint("dirsearch", __name__, url_prefix="/dirsearch")


@bp.route("/", methods=["GET"])
@login_required
def index():
    target_url = request.args.get('target_url')
    if target_url:
        def generate():
            for result in dirsearch(target_url):
                yield f"data: {result}\n\n"
                
        return Response(generate(), mimetype='text/event-stream')
    return render_template("dirsearch.html")