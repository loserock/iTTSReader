#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import pyttsx
import ttk
import argparse

def log(*args, **kwargs):
    pass    

class ITTSWindow(ttk.Tkinter.Tk):
    __CUSTOM_SETTINGS = [
        "title_suffix"
    ]
    def __init__(self, *args, **kwargs):
        _s_kwargs = {k: v for k, v in kwargs.iteritems() if k not in self.__CUSTOM_SETTINGS}
        ttk.Tkinter.Tk.__init__(self, *args, **_s_kwargs)
        # ttk.Tkinter.Tk.iconbitmap(self,default='clienticon.ico')
        _title_text = u"iTTS Reader - tiny text reader app, using your native TTS"
        if kwargs.has_key("title_suffix"):
            _title_text += u" - {}".format(kwargs["title_suffix"])
        ttk.Tkinter.Tk.wm_title(
            self, _title_text)

        self.__ttsService = None

        layout = ttk.Tkinter.Frame(self)
        layout.pack(side="top", fill="both", expand=True)
        layout.grid_rowconfigure(0, weight=1)
        layout.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frames[TextFrame] = TextFrame(layout, self)
        self.frames[TextFrame].grid(row=1, column=0, sticky="n s e w")
        self.frames[TextFrame].grid_propagate(True)

        self.frames[ControlFrame] = ControlFrame(layout, self)
        self.frames[ControlFrame].grid(row=2, column=0, sticky="E W")

        self.show_frame(TextFrame)

    def show_frame(self, frameObj):
        self.frames[frameObj].tkraise()
        self.frames[frameObj].focus_set()

    @property
    def ttsService(self):
        if self.__ttsService is None:
            raise TypeError("TTS Service is still None, set it before use!")
        return self.__ttsService

    @ttsService.setter
    def ttsService(self, value):
        if not isinstance(value, TTSService):
            raise TypeError("The given TTS Service Engine {!r} is not an instance of {!r}.".format(type(value), TTSService))
        self.__ttsService = value
        self.frames[ControlFrame].fill_voice_combo()
        log(u"ttsService was set to {!r}.".format(type(value)))

class TextFrame(ttk.Tkinter.Frame):
    def __init__(self, parent, controller):
        ttk.Tkinter.Frame.__init__(self, parent)
        self.app = controller
        self.NormalFont=("Verdana", 10)
        label=ttk.Label(self, text=u"TTS Text:", font=self.NormalFont)
        label.grid(row=0, column=0, sticky="W E")
        # TODO use a bigger text box instead of an Entry
        self.textBox=ttk.Tkinter.Text(self, undo=True, wrap="word")
        self.textBox.grid(row=1, column=0, sticky="W E N S")
        self.textBox.bind("<Control-Return>", self.speak)
        self.scrollbar = ttk.Scrollbar(self, command=self.textBox.yview)
        self.scrollbar.grid(row=1, column=1, sticky='nsew')
        self.textBox['yscrollcommand'] = self.scrollbar
        # label.bind("<Key>", self.driveKey)

        log(u"Text frame initiated.")

    def speak(self, event):
        txt = self.textBox.get(1.0, ttk.Tkinter.END)
        self.app.ttsService.speakNow(txt)
        self.textBox.delete(1.0, ttk.Tkinter.END)

class ControlFrame(ttk.Tkinter.Frame):
    def __init__(self, parent, controller):
        ttk.Tkinter.Frame.__init__(self, parent)
        self.app = controller
        self.NormalFont=("Verdana", 10)
        self.voiceCombo = ttk.Combobox(self, values=[], state="readonly", text=u"Select voice")
        self.voiceCombo.grid(row=0, column=1)
        self.voiceCombo.bind("<<ComboboxSelected>>", self.set_voice)
        self.voiceCombo.bind("<Button-1>", self.fill_voice_combo)
        self.speakButton = ttk.Button(self, text=u"Speak")
        self.speakButton.grid(row=0, column=2)
        self.speakButton.config(command=self.speak)

        log(u"Control frame initiated.")

    def speak(self):
        log(u"Speak button pressed")
        _event=ttk.Tkinter.Event()
        _event.keycode = "<Control-Return>"
        self.app.frames[TextFrame].speak(_event)

    def fill_voice_combo(self, event=None):
        log(u"Filling voice combo box with new values.")
        voices = self.app.ttsService.getVoices(human_format=True)
        last_combo_pos = self.voiceCombo.current()
        self.voiceCombo.config(values=voices)
        if 0 <= last_combo_pos < len(voices):
            self.voiceCombo.current(last_combo_pos)
        else:
            self.voiceCombo.current(0)
        log(u"Voice combo box filled with {} value(s).".format(len(voices)))

    def set_voice(self, event=None):
        log(u"Voice combo box selected.")
        idx = event.widget.current()
        log(u"Selected voice item index: {}".format(idx))
        if idx >= 0:
            self.app.ttsService.setVoice(idx)





class TTSService(object):
    def __init__(self):
        self.__engine=pyttsx.init()

    def getVoices(self, human_format=False):
        _voices=self.__engine.getProperty("voices")
        voice_list=[]
        for v in _voices:
            voice={u"{}".format(attr): getattr(v, attr)
                                for attr in dir(v) if not attr.startswith("_")}
            if len(voice):
                voice_list.append(voice)
        if human_format:
            voice_list = [v["id"].split("\\")[-1] for v in voice_list]
        return voice_list

    def setVoice(self, voice):
        if type(voice) is int:
            _voice=self.__engine.getProperty("voices")[voice]
            voice=_voice.id
        elif type(voice) is pyttsx.voice.Voice:
            voice=voice.id
        elif type(voice) not in (str, unicode):
            raise NotImplementedError(
                "Not implemented to handle input type of: {!r}".format(type(voice)))
        self.__engine.setProperty("voice", voice)
        log(u"Voice was set to {}.".format(voice))

    def addSpeak(self, text):
        self.__engine.say(text)

    def startSpeaking(self):
        self.__engine.runAndWait()

    def speakNow(self, text):
        self.addSpeak(text)
        self.startSpeaking()

def test():
    global log
    def _test_log(*args, **kwargs):
        print(*args, **kwargs)
    log = _test_log
    window = ITTSWindow(title_suffix=u"TEST MODE")
    window.ttsService = TTSService()
    window.mainloop()
    exit(0)

def main():
    window = ITTSWindow()
    window.ttsService = TTSService()
    window.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run application in test mode.")
    params = parser.parse_args()
    if params.test:
        test()
    main()
