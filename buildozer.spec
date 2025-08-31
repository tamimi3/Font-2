[app]
title = تطبيق دمج الخطوط
package.name = font_merger
package.domain = org.example
source.dir = .
version = 0.1

# متطلبات الحزمة الأساسية، نضيف fonttools للدمج
requirements = python3,kivy,fonttools

# إعدادات منصة Android
android.api = 31
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a
android.permissions = INTERNET

# إمكانية دعم التخزين الخارجي إذا لزم
#android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# مسارات الملفات (اختياري إذا كانت الملفات في مسار آخر)
# source.include_exts = py,png,jpg,kv,atlas

# اتجاه التطبيق
orientation = portrait
fullscreen = 0
presplash.filename = %(source.dir)s/data/presplash.png

# نسخة لغة Python, يمكن ترك الافتراضي (3.9+)
#android.python_version = 3

[buildozer]
log_level = 2
warn_on_root = 1
