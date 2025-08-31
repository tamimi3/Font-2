# main.py
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import mainthread
from plyer import filechooser
from fontTools.ttLib import TTFont
from fontTools.merge import Merger
from fontTools.ttLib.scaleUpem import scale_upem
from fontTools import subset
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

class MainWidget(BoxLayout):
    arabic_font = StringProperty('')
    english_font = StringProperty('')

    def choose_arabic_font(self):
        filechooser.open_file(on_selection=self.arabic_selected)

    def arabic_selected(self, selection):
        if selection:
            self.arabic_font = selection[0]
            self.ids.arabic_label.text = os.path.basename(self.arabic_font)

    def choose_english_font(self):
        filechooser.open_file(on_selection=self.english_selected)

    def english_selected(self, selection):
        if selection:
            self.english_font = selection[0]
            self.ids.english_label.text = os.path.basename(self.english_font)

    @mainthread
    def merge_fonts(self):
        # تحقق من تحديد الملفين
        if not self.arabic_font or not self.english_font:
            self.ids.status_label.text = 'يرجى اختيار كلا الخطين أولاً'
            return

        log_lines = []
        try:
            log_lines.append(f"تم اختيار الخط العربي: {self.arabic_font}")
            log_lines.append(f"تم اختيار الخط الإنجليزي: {self.english_font}")

            # تحميل الخطوط باستخدام fontTools
            font_ar = TTFont(self.arabic_font)
            font_en = TTFont(self.english_font)
            log_lines.append(f"وحدات الحرف (UPM) قبل التوحيد: عربي={font_ar['head'].unitsPerEm}, إنجليزي={font_en['head'].unitsPerEm}")

            # توحيد الوحدات-per-Em إذا اختلفت
            upm_ar = font_ar['head'].unitsPerEm
            upm_en = font_en['head'].unitsPerEm
            if upm_ar != upm_en:
                new_upm = max(upm_ar, upm_en)
                scale_upem(font_ar, new_upm)
                scale_upem(font_en, new_upm)
                font_ar['head'].unitsPerEm = new_upm
                font_en['head'].unitsPerEm = new_upm
                log_lines.append(f"تم توحيد UPM إلى: {new_upm}")

            # إزالة الرموز غير العربية/اللاتينية بواسطة التجزئة (subset)
            # نحدد النطاقات المرغوبة للحروف العربية واللاتينية الأساسية
            arabic_ranges = [(0x0600,0x06FF), (0x0750,0x077F), (0x08A0,0x08FF), (0xFB50,0xFDFF), (0xFE70,0xFEFF)]
            latin_range = (0x0020, 0x007E)  # يشمل الحروف والأرقام وعلامات الترقيم الأساسية
            ranges = [f"U+{hex(latin_range[0])[2:]}-{hex(latin_range[1])[2:]}"]
            for r in arabic_ranges:
                ranges.append(f"U+{hex(r[0])[2:]}-{hex(r[1])[2:]}")
            ranges_str = ",".join(ranges)
            # ترميز الأحرف المطلوبة
            subset_args = [
                self.arabic_font,
                f"--output-file={self.arabic_font}.sub",
                f"--unicodes={ranges_str}"
            ]
            subset.main(subset_args)
            subset_args = [
                self.english_font,
                f"--output-file={self.english_font}.sub",
                f"--unicodes={ranges_str}"
            ]
            subset.main(subset_args)
            log_lines.append("تم إزالة الرموز غير المطلوبة من كلا الخطين")

            # دمج الخطوط باستخدام fontTools.merge
            merger = Merger()
            merged_font = merger.merge([f"{self.arabic_font}.sub", f"{self.english_font}.sub"])
            output_font = os.path.join(App.get_running_app().user_data_dir, "MergedFont.ttf")
            merged_font.save(output_font)
            log_lines.append(f"تم دمج الخطوط وحفظ الناتج في: {output_font}")

            # إنشاء معاينة بصيغة JPG باستخدام Pillow
            img = Image.new("RGB", (800, 400), color="white")
            draw = ImageDraw.Draw(img)
            # نص تجريبي بالإنجليزية والعربية
            text_en = "Hello Kivy"
            text_ar = "مرحبا"
            # تهيئة نص عربي للعرض الصحيح
            reshaped = arabic_reshaper.reshape(text_ar)
            bidi_text = get_display(reshaped)
            # تحميل الخط المدمج
            pil_font = ImageFont.truetype(output_font, 48)
            draw.text((10, 10), text_en, font=pil_font, fill="black")
            draw.text((10, 80), bidi_text, font=pil_font, fill="black")
            preview_path = os.path.join(App.get_running_app().user_data_dir, "preview.jpg")
            img.save(preview_path, "JPEG", quality=90)
            log_lines.append(f"تم إنشاء معاينة في: {preview_path}")

            # حفظ السجل
            log_path = os.path.join(App.get_running_app().user_data_dir, "merge_log.txt")
            with open(log_path, "w", encoding="utf-8") as f:
                for line in log_lines:
                    f.write(line + "\n")
            self.ids.log_text.text = "\n".join(log_lines)

            self.ids.status_label.text = "تمت عملية الدمج بنجاح"
        except Exception as e:
            self.ids.status_label.text = f"خطأ: {e}"

class FontMergerApp(App):
    def build(self):
        return MainWidget()
