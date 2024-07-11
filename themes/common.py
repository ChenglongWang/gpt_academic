from functools import lru_cache
from toolbox import get_conf
CODE_HIGHLIGHT, ADD_WAIFU, LAYOUT = get_conf("CODE_HIGHLIGHT", "ADD_WAIFU", "LAYOUT")

def minimize_js(common_js_path):
    try:
        import rjsmin, hashlib, glob, os
        # clean up old minimized js files, matching `common_js_path + '.min.*'`
        for old_min_js in glob.glob(common_js_path + '.min.*.js'):
            os.remove(old_min_js)
        # use rjsmin to minimize `common_js_path`
        c_jsmin = rjsmin.jsmin
        with open(common_js_path, "r") as f:
            js_content = f.read()
        minimized_js_content = c_jsmin(js_content)
        # compute sha256 hash of minimized js content
        sha_hash = hashlib.sha256(minimized_js_content.encode()).hexdigest()[:8]
        minimized_js_path = common_js_path + '.min.' + sha_hash + '.js'
        # save to minimized js file
        with open(minimized_js_path, "w") as f:
            f.write(minimized_js_content)
        # return minimized js file path
        return minimized_js_path
    except:
        return common_js_path

@lru_cache
def get_common_html_javascript_code():
    js = "\n"
    common_js_path_list = [
        "themes/common.js",
        "themes/theme.js",
        "themes/init.js",
    ]

    if ADD_WAIFU: # 添加Live2D
        common_js_path_list += [
            "themes/waifu_plugin/jquery.min.js",
            "themes/waifu_plugin/jquery-ui.min.js",
        ]

    for common_js_path in common_js_path_list:
        if '.min.' not in common_js_path:
            minimized_js_path = minimize_js(common_js_path)
        else:
            minimized_js_path = common_js_path
        jsf = f"file={minimized_js_path}"
        js += f"""<script src="{jsf}"></script>\n"""

    if not ADD_WAIFU:
        js += """<script>window.loadLive2D = function(){};</script>\n"""

    return js
