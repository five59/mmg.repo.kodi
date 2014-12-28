# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

import os, sys, json, xbmcgui, xbmcaddon, urlparse
import xbmc, xbmcplugin

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())

language = xbmcaddon.Addon().getLocalizedString

pathBase = xbmcaddon.Addon().getAddonInfo('path').decode(sys.getfilesystemencoding())
pathIcon = os.path.join(pathBase, "resources", "media", "icon")
pathFArt = os.path.join(pathBase, "resources", "media", "fanart")
backgroundImage = os.path.join(pathBase, "fanart.jpg")

ACTION_PREVIOUS_MENU = 10 # Esc
ACTION_NAV_BACK = 92 # Backspace
ALIGN_LEFT = 5
ALIGN_CENTER = 6

NAVMODE_CATEGORY = 10
NAVMODE_CHANNEL = 11


class MMGTTYAddon(xbmcgui.Window):
    
    def __init__(self):
        self.dialog = xbmcgui.Dialog()
        self.loadChannelList()
        self.setControls()
        self.setNavigation()
        self.setChannelList(30010)
        self.navMode = NAVMODE_CATEGORY
        xbmc.log("MMGTTYAddon Init",xbmc.LOGINFO)

    def setControls(self):
        # Set background
        self.addControl(xbmcgui.ControlImage(1,1, 1280, 720, backgroundImage))

        # Create Category Nav
        self.catBtn={}
        for grouping in range(30010, 30020):
            icon0=os.path.join(pathIcon, "category",str(64),"b",str(grouping)+".png")
            icon1=os.path.join(pathIcon, "category",str(64),"g",str(grouping)+".png")
            yPos=10 + (67 * (grouping - 30010))
            self.catBtn[str(grouping)]=xbmcgui.ControlButton(
                x=10,
                y=yPos,
                width=64,
                height=64,
                focusTexture=icon0,
                noFocusTexture=icon1,
                label=u''
                )
            # self.catBtn[str(grouping)].onFocus(self.set_channelList(grouping))
            self.addControl(self.catBtn[str(grouping)])

        # Create Title Bar
        self.catTitle=xbmcgui.ControlLabel(
            x=100,
            y=10,
            width=1150,
            height=100,
            label=u'Turkish TV',
            font='font48_title',
            textColor='0xFFFFFFFF'
        )
        self.addControl(self.catTitle)

        # Create Channel Menu
        self.chaMenu=xbmcgui.ControlList(
            x=100,
            y=150,
            width=1150,
            height=720-150,
            font='font14',
            textColor="0xFF999999",
            selectedColor="0xFFFFFFFF"
        )
        self.addControl(self.chaMenu)

        # Create Channel Detail
        self.setChannelList(30010)

    def loadChannelList(self):
        try:
            dataFile=os.path.join(pathBase, "resources", "data", "channels.json")
            json_data=open(dataFile,'r')
            self.channelData = json.load(json_data)
            json_data.close()
            xbmc.log("Channel Data Version: " + self.channelData['meta']['dtdVer'], xbmc.LOGINFO)
        except:
            xbmc.log("Channels did not load.",xbmc.LOGERROR)
            self.close()

    def setChannelList(self, categoryID):
        self.chaMenu.reset()
        self.setTitle(language(categoryID))
        category=self.channelData["channelGroups"][str(categoryID)]["channels"]
        for channel in category:
            chaItem=xbmcgui.ListItem(channel['label'])
            self.chaMenu.addItem(chaItem)

    def setTitle(self, newLabel):
        self.catTitle.setLabel(newLabel)

    def setNavigation(self):
        for grouping in range(30010, 30019):
            self.catBtn[str(grouping)].controlDown(self.catBtn[str(grouping+1)])
        for grouping in range(30011, 30020):
            self.catBtn[str(grouping)].controlUp(self.catBtn[str(grouping-1)])
        self.catBtn['30010'].controlUp(self.catBtn['30019'])
        self.catBtn['30019'].controlDown(self.catBtn['30010'])
        for grouping in range(30010, 30020):
            if (grouping<30019):
                self.catBtn[str(grouping)].controlDown(self.catBtn[str(grouping+1)])
            else:
                self.catBtn[str(grouping)].controlDown(self.catBtn[u'30010'])
            if (grouping>30010):
                self.catBtn[str(grouping)].controlUp(self.catBtn[str(grouping-1)])
            else:
                self.catBtn[str(grouping)].controlUp(self.catBtn[u'30019'])
        self.setFocus(self.catBtn['30010'])

    def onFocus(self, control):
        self.setTitle(str(control))

    def onClick(self, control):
        #print("onClick: " + str(control.getId()))
        pass

    def onAction(self, action):
        #print("onAction: " + str(control.getId()))
        if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
            self.close()

    def onControl(self, control):
        control.getId()


if __name__ == '__main__':
    addon = MMGTTYAddon()
    addon.doModal()
    del addon
