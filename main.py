# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty
import os

class FontMergerApp(App):
    font1_path = StringProperty('')
    font2_path = StringProperty('')

    def build(self):
        return Builder.load_file('main.kv')

    def open_font1(self):
        chooser = FileChooserListView(filters=['*.ttf'])
        popup = Popup(title='اختر الخط 1', content=chooser, size_hint=(0.9, 0.9))
        def select(instance, selection, touch):
            if selection:
                self.font1_path = selection[0]
                popup.dismiss()
        chooser.bind(on_submit=select)
        popup.open()

    def open_font2(self):
        chooser = FileChooserListView(filters=['*.ttf'])
        popup = Popup(title='اختر الخط 2', content=chooser, size_hint=(0.9, 0.9))
        def select(instance, selection, touch):
            if selection:
                self.font2_path = selection[0]
                popup.dismiss()
        chooser.bind(on_submit=select)
        popup.open()

    def merge_fonts(self):
        status_label = self.root.ids.status_label
        if not self.font1_path or not self.font2_path:
            status_label.text = 'الرجاء اختيار كلا الخطين'
            return
        try:
            from fontTools.merge import Merger
            merger = Merger()
            merged_font = merger.merge([self.font1_path, self.font2_path])
            try:
                from kivy.utils import platform as kivy_platform
                if kivy_platform == 'android':
                    from android.storage import primary_external_storage_path
                    save_dir = primary_external_storage_path()
                else:
                    save_dir = os.getcwd()
            except ImportError:
                save_dir = os.getcwd()
            output_path = os.path.join(save_dir, 'merged_font.ttf')
            merged_font.save(output_path)
            status_label.text = f'تم حفظ الملف: {output_path}'
        except Exception as e:
            status_label.text = 'خطأ في الدمج: ' + str(e)

if __name__ == '__main__':
    FontMergerApp().run()
