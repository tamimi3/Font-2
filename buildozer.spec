# buildozer.spec
[app]
title = FontMerger
package.name = fontmerger
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,otf
version = 1.0
requirements = python3,kivy,pillow,fonttools,arabic_reshaper,python-bidi,rich,colorama
orientation = portrait
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
log_level = 2

[buildozer]
log_level = 2
