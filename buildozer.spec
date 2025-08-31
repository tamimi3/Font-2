[app]
title = MyApp
package.name = myapp
package.domain = org.myapp
# تضمين امتدادات الملفات الضرورية
source.include_exts = py,kv,ttf,json

# الحزم المطلوبة (تأكد من وجود fonttools)
requirements = python3,kivy,fonttools

# ضبط واجهة التطبيق واتجاهه
orientation = portrait

# إعدادات Android API
android.api = 31
android.minapi = 21

# أذونات Android
android.permissions = android.permission.INTERNET
