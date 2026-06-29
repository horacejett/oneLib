# oneLib 品牌资源工具

把 oneLib / 一知纯图标（无文字）渲染成 oneLib 全套 App 图标与应用内 logo。
纯 Python 实现，零第三方依赖，配合 macOS 自带的 `sips` / `iconutil`。

## 文件
- `imglib.py` — 极简 RGBA PNG 工具（加载/保存/缩放/合成/圆角/重着色）
- `gen_assets.py` — 资源生成脚本
- `../onelib-mark-white.png` — 母版：oneLib 纯图标（白色 + alpha 形状）

## 品牌规范
- 主色：藏青 `#091842`；辅助色：绛红 `#94122C`
- App 图标：藏青圆角底（macOS 824×824，圆角 180）+ 居中白色图标
- 托盘：黑色图标 + alpha（macOS template，自动适配深浅菜单栏）

## 生成
```bash
cd brand-source/tools
python3 gen_assets.py all      # 生成 png/svg/托盘/应用内变体/模型图标

# icns（macOS）
cd ../../apps/electron/resources
mkdir -p icon.iconset
for s in "16:16x16" "32:16x16@2x" "32:32x32" "64:32x32@2x" "128:128x128" \
         "256:128x128@2x" "256:256x256" "512:256x256@2x" "512:512x512" "1024:512x512@2x"; do
  sips -z ${s%%:*} ${s%%:*} icon.png --out "icon.iconset/icon_${s##*:}.png" >/dev/null
done
iconutil -c icns icon.iconset -o icon.icns && rm -rf icon.iconset

# ico（在 tools 目录用 Python）
python3 -c "import gen_assets as g; g.build_ico('../../apps/electron/resources/icon.png','../../apps/electron/resources/icon.ico')"
```

> 项目自带的 `apps/electron/resources/generate-icons.sh` 走 SVG→栅格管线，
> 需要 `brew install librsvg imagemagick`。本 Python 管线是其零依赖替代方案。
