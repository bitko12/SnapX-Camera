[app]
title = SnapX Camera
package.name = snapx
package.domain = org.snapx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = CAMERA
android.api = 31
android.minapi = 21
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
