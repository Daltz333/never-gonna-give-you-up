import sphinx as Sphinx
from typing import Any, Dict, List
import os
from docutils import nodes
import json
import shutil


def get_files_to_cache(outDir: str):
    files_to_cache = []
    for (dirpath, dirname, filenames) in os.walk(outDir):
        dirpath = dirpath.split(outDir)[1]

        # skip adding sources to cache
        if os.sep + "_sources" + os.sep in dirpath:
            continue

        # add files to cache
        for name in filenames:
            dirpath = dirpath.replace("\\", "/")
            files_to_cache.append(dirpath + "/" + name)

    return files_to_cache


def build_finished(app: Sphinx, exception: Exception):
    outDir = app.outdir
    outDirStatic = outDir + os.sep + "_static" + os.sep
    files_to_cache = get_files_to_cache(outDir)

    # dumps a json file with our cache
    with open(outDirStatic + "cache.json", "w") as f:
        json.dump(files_to_cache, f)

    # copies over our service worker
    shutil.copyfile(os.path.dirname(__file__) + os.sep + "pwa_service_files" + os.sep + "sw.js", outDirStatic + "sw.js")


def html_page_context(
        app: Sphinx,
        pagename: str,
        templatename: str,
        context: Dict[str, Any],
        doctree: nodes.document,
) -> None:
    app.add_js_file(None, body="\"serviceWorker\"in navigator&&navigator.serviceWorker.register(\"/_static/sw.js\");",
                    loading_method="defer")
    if doctree:
        context["metatags"] += f'<link rel="manifest" href="/frcdocs.webmanifest"/>'


def setup(app: Sphinx) -> dict[str, any]:
    app.connect("html-page-context", html_page_context)
    app.connect("build-finished", build_finished)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
