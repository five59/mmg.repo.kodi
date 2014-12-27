# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

import os, sys
import xbmcgui, xbmcaddon, urlparse

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())

language = xbmcaddon.Addon().getLocalizedString
path_base = xbmcaddon.Addon().getAddonInfo('path').decode(sys.getfilesystemencoding())
path_icon = path_base + "/resources/media/icon"
path_fanart = path_base + "/resources/media/fanart"

ACTION_PREVIOUS_MENU = 10 # Esc
ACTION_NAV_BACK = 92 # Backspace
ALIGN_CENTER = 6

#background_img = os.path.join(_addon_path, 'images', 'SKINDEFAULT.jpg')
#button_nf_img = os.path.join(_addon_path, 'images', 'KeyboardKeyNF.png')
#button_fo_img = os.path.join(_addon_path, 'images', 'KeyboardKey.png')
#banana_img = os.path.join(_addon_path, 'images', 'banana.gif')

class MMGTTYAddon(xbmcgui.Window):
    
    def __init__(self):
        self.dialog = xbmcgui.Dialog()
#        background = xbmcgui.ControlImage(1, 1, 1280, 720, background_img)
#        self.addControl(background)
#        banana_picture = xbmcgui.ControlImage(500, 200, 256, 256, banana_img)
#        self.addControl(banana_picture)
        self.set_controls()
        self.set_navigation()

    def set_controls(self):
        for grouping in range(30010, 30020):
            # url = build_url({'mode': 'folder', 'foldername': language(grouping)})
            buttonImageURL=path_icon + os.sep + "category" + os.sep + str(grouping) + ".png"
            cb=xbmcgui.ControlButton(0 + ((grouping-30010)*130), 0, 128, 128, language(grouping), 
                                    focusTexture=buttonImageURL, noFocusTexture=buttonImageURL)
            self.addControl(cb)
        
        self.privet_btn = xbmcgui.ControlButton(500, 500, 110, 40, u'Button1')
        self.addControl(self.privet_btn)
        self.exit_btn = xbmcgui.ControlButton(650, 500, 110, 40, u'Button2')
        self.addControl(self.exit_btn)

    def set_navigation(self):
        self.privet_btn.controlRight(self.exit_btn)
        self.privet_btn.controlLeft(self.exit_btn)
        self.exit_btn.controlRight(self.privet_btn)
        self.exit_btn.controlLeft(self.privet_btn)
        self.setFocus(self.privet_btn)

    def onAction(self, action):
        if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
            self.close()

    def onControl(self, control):
        if control == self.privet_btn:
            self.dialog.ok(u'Button3', u'Button4')
        elif control == self.exit_btn:
            self.close()

if __name__ == '__main__':
    addon = MMGTTYAddon()
    addon.doModal()
    del addon
