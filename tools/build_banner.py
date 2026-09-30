#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_banner.py -- regenerate readme_banner.html

The repo banner is drawn with the SAME 5x5 pixel font the MV itself renders
with (imported from world_execute_me_mv.py), coloured along the song's
emotion arc: green INIT -> pink LOVE -> blue LOSS -> red EXECUTION -> gray REST.

usage:  python tools/build_banner.py
then screenshot readme_banner.html at 1280x420 (any headless chromium),
or just open it in a browser.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from world_execute_me_mv import FONT5   # noqa: E402

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>world-execute-me-terminal-mv — banner</title>
<style>
  html,body{margin:0;padding:0;background:#050506;overflow:hidden}
  canvas{display:block}
</style>
</head>
<body>
<canvas id="c" width="1280" height="420"></canvas>
<script>
(function(){
  "use strict";
  var F = __FONT__;
  var W = 1280, H = 420;
  var cv = document.getElementById("c");
  var g = cv.getContext("2d");

  function mulberry(a){
    return function(){
      a|=0; a=(a+0x6D2B79F5)|0;
      var t=Math.imul(a^(a>>>15),1|a);
      t=(t+Math.imul(t^(t>>>7),61|t))^t;
      return ((t^(t>>>14))>>>0)/4294967296;
    };
  }

  function glyph(ch, x, y, px, py, col){
    var m = F[ch] || F[" "];
    g.fillStyle = col;
    for(var r=0;r<5;r++)
      for(var c=0;c<5;c++)
        if(m[r][c] === "#")
          g.fillRect(x+c*px, y+r*py, px, py);
  }
  function widthOf(s, px){ return s.length*6*px - px; }
  function text(s, x, y, px, py, colFn){
    s = s.toUpperCase();
    for(var i=0;i<s.length;i++)
      glyph(s[i], x+i*(6*px), y, px, py,
            typeof colFn === "function" ? colFn(i, s.length) : colFn);
    return x + widthOf(s, px);
  }

  /* emotion-arc gradient: the colours of the whole song across one word */
  var STOPS = [[0,"#55ff99"],[0.28,"#ff7ab8"],[0.52,"#6f9fff"],
               [0.78,"#ff2a2a"],[1,"#8899aa"]];
  function hx(h){ return [parseInt(h.slice(1,3),16),
                          parseInt(h.slice(3,5),16),
                          parseInt(h.slice(5,7),16)]; }
  function grad(f){
    for(var i=0;i<STOPS.length-1;i++){
      if(f >= STOPS[i][0] && f <= STOPS[i+1][0]){
        var t=(f-STOPS[i][0])/(STOPS[i+1][0]-STOPS[i][0]);
        var a=hx(STOPS[i][1]), b=hx(STOPS[i+1][1]);
        return "rgb(" + Math.round(a[0]+(b[0]-a[0])*t) + "," +
                        Math.round(a[1]+(b[1]-a[1])*t) + "," +
                        Math.round(a[2]+(b[2]-a[2])*t) + ")";
      }
    }
    return STOPS[STOPS.length-1][1];
  }

  g.fillStyle = "#050506"; g.fillRect(0,0,W,H);

  /* dying-screen texture (avoids the text bands) */
  var rnd = mulberry(1109);        // 1:52, when you left
  var CH = "/|-*+.";
  for(var i=0;i<170;i++){
    var x = rnd()*W, y = rnd()*H;
    if(x>24 && x<W-24 && y>80 && y<372) continue;
    var a = 0.07 + rnd()*0.13;
    glyph(CH[(rnd()*CH.length)|0], x, y, 2, 2,
          rnd()<0.7 ? "rgba(120,120,130,"+a.toFixed(2)+")"
                    : "rgba(110,140,190,"+a.toFixed(2)+")");
  }

  /* status line + prompt */
  text("HEART: 11 BPM", W-64-widthOf("HEART: 11 BPM",2), 34, 2, 2, "#7c1b1b");
  text("ME@WORLD:~$ PYTHON WORLD_EXECUTE_ME_MV.PY", 64, 34, 2, 2, "#4f7f63");

  /* the title, wearing the whole emotional arc */
  var T = "WORLD.EXECUTE(ME)";
  var tw = widthOf(T, 11);
  var tx = Math.floor((W-tw)/2);
  text(T, tx, 100, 11, 11, function(i, n){ return grad(i/(n-1)); });
  g.fillStyle = "#f2f2f2";                       // she is still waiting
  g.fillRect(tx+tw+18, 100, 12, 55);

  /* subtitles */
  var S1 = "TERMINAL ASCII MUSIC VIDEO";
  text(S1, Math.floor((W-widthOf(S1,4))/2), 196, 4, 4, "#3fa8c0");
  var S2 = "SINGLE FILE // ZERO DEPS // RUN = EXECUTE";
  text(S2, Math.floor((W-widthOf(S2,2))/2), 252, 2, 2, "#6a6a72");

  g.font = '900 30px "Microsoft YaHei","PingFang SC",sans-serif';
  g.textAlign = "center";
  g.fillStyle = "#c86ea5";
  g.fillText("运行即处决 —— 她还在等你的按键", W/2, 330);
  g.textAlign = "left";

  /* CRT scanlines + vignette */
  g.fillStyle = "rgba(0,0,0,0.16)";
  for(var sy=2; sy<H; sy+=3) g.fillRect(0, sy, W, 1);
  var rg = g.createRadialGradient(W/2,H*0.44,H*0.3, W/2,H*0.44,H*1.0);
  rg.addColorStop(0,"rgba(0,0,0,0)");
  rg.addColorStop(1,"rgba(0,0,0,0.5)");
  g.fillStyle = rg; g.fillRect(0,0,W,H);
})();
</script>
</body>
</html>
"""

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "readme_banner.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(HTML.replace("__FONT__", json.dumps(FONT5)))
    print("[banner] wrote %s (open it, or screenshot at 1280x420)" % out)

if __name__ == "__main__":
    main()
