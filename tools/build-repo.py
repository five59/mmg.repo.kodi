#!/usr/bin/python

# *
# *  Copyright (C) 2012-2013 Garrett Brown
# *  Copyright (C) 2010      j48antialias
# *
# *     Modifed for MMG Repository (12/2014 onwards)
# *     Modified for FTV Guide (09/2014 onwards)
# *     by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  Based on code by j48antialias:
# *  https://anarchintosh-projects.googlecode.com/files/addons_xml_generator.py
# *
# *  Changelog:
# *  - [bluezed] Zip file creation changed to not include version number inside the zipped folder
# *  - [bluezed] File copying modified to only copy addon.xml and not addon.py as well
# *  - [bluezed] Changed to create changelog-x.x.x.txt
 
""" addons.xml generator """

import os
import sys
import re
import xml.etree.ElementTree as ET

try:
    import shutil, zipfile
except Exception as e:
    print('An error occurred importing module!\n%s\n'  %e)
 
# Compatibility with 3.0, 3.1 and 3.2 not supporting u"" literals
print(sys.version)
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

srcDir=os.path.join(os.path.dirname(sys.path[0]),"source","addons")
repoDir=os.path.join(os.path.dirname(sys.path[0]),"web","repo")

# webIndexSrc=os.path.join(os.path.dirname(sys.path[0]),"source","web","index.src.html")
# webIndexDst=os.path.join(os.path.dirname(sys.path[0]),"web","index.html")

class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file.
    """

    srcDir=os.path.join(os.path.dirname(sys.path[0]),"source","addons")
    repoDir=os.path.join(os.path.dirname(sys.path[0]),"web","repo")

    def __init__( self ):
        # generate files
        print("\n\n--> Updating repo metadata.")
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user

    def _generate_addons_file( self ):
        print("     * Generating new addons.xml file for repo.")
        addons = os.listdir(self.srcDir)
        addons_xml = u("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n")
        for addon in addons:
            try:
                if re.search("plugin|script|service|skin|repository" , addon):
                    print("     * Found " + addon)
                    _path = os.path.join( self.srcDir, addon, "addon.xml" )
                    xml_lines = open( _path, "r" ).read().splitlines()
                    addon_xml = ""
                    for line in xml_lines:
                        if ( line.find( "<?xml" ) >= 0 ): continue
                        if sys.version < '3':
                            addon_xml += unicode( line.rstrip() + "\n", "UTF-8" )
                        else:
                            addon_xml += line.rstrip() + "\n"
                    addons_xml += addon_xml.rstrip() + "\n\n"
                else:
                    pass
            except Exception as e:
                # missing or poorly formatted addon.xml
                _path = os.path.join( addon, "addon.xml" )
                print("     * Excluding %s for %s" % ( _path, e ))
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u("\n</addons>\n")
        # save file
        addonFilename=os.path.join(self.repoDir,"addons.xml")
        self._save_file( addons_xml.encode( "UTF-8" ), file=addonFilename )

    def _generate_md5_file( self ):
        print("     * Generating new addons.xml MD5 hashfile for repo.")
        # create a new md5 hash
        try:
            import md5
            addonFilename=os.path.join(self.repoDir,"addons.xml")
            m = md5.new( open(addonFilename, "r" ).read() ).hexdigest()
        except ImportError:
            import hashlib
            m = hashlib.md5( open(addonFilename, "r", encoding="UTF-8" ).read().encode( "UTF-8" ) ).hexdigest()
        try:
            self._save_file( m.encode( "UTF-8" ), os.path.join(self.repoDir, "addons.xml.md5"))
        except Exception as e:
            print("* An error occurred creating addons.xml.md5 file!\n%s" % e)
 
    def _save_file( self, data, file ):
        try:
            open( file, "wb" ).write( data )
        except Exception as e:
            print("An error occurred saving %s file!\n%s" % ( file, e ))

def zipFolder(foldername, suffix, target_dir, zips_dir):
    zipObj = zipfile.ZipFile(zips_dir + foldername + suffix, 'w', zipfile.ZIP_DEFLATED)
    rootLen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for f in files:
            fn = os.path.join(base, f)
            zipObj.write(fn, os.path.join(foldername,fn[rootLen:]))
    zipObj.close()

if ( __name__ == "__main__" ):
    Generator()
    try:
        # webAddons={
        #     "Thumb":{
        #         "Filename":os.path.join(os.path.dirname(sys.path[0]),"source","server","web","addons.item.html"),
        #         "Template":"",
        #         "HTML":""
        #     },
        #     "Modal":{
        #         "Filename":os.path.join(os.path.dirname(sys.path[0]),"source","server","web","addons.modal.html"),
        #         "Template":"",
        #         "HTML":""
        #     },
        #     "Items":{}
        # }
        # print(str(webAddons["Thumb"]["File"]))
        # with open (str(webAddons["Thumb"]["File"]), "r") as fp:
        #     webAddons["Thumb"]["Template"]=fp.read()
        #     fp.close()
        # with open (webAddons["Modal"]["File"], "r") as fp:
        #     webAddons["Modal"]["Template"]=fp.read()
        #     fp.close()

        filesInRootDir=os.listdir(srcDir)
        for x in filesInRootDir:
            if re.search("plugin|script|service|skin|repository" , x) and not re.search('.zip',x):
                print("\n--> Working on " + x + "...")
                zipFilename = x + '.zip'
                zipFilenameFirstPart = zipFilename[:-4]
                zipFilenameLastPart = zipFilename[len(zipFilename)-4:]
                zipsFolder = os.path.normpath(os.path.join(repoDir,'zips',x)) + os.sep
                folderToZip = srcDir + os.sep + x
                filesInFolderToZip = os.listdir(folderToZip)        
                if not os.path.exists(zipsFolder):
                    os.makedirs(zipsFolder)
                    print('    * Directory doesn\'t exist, creating: ' + zipsFolder)                
                if "addon.xml" in filesInFolderToZip: 
                    print('    * Found plugin addon.xml file.')
                    tree = ET.parse(os.path.join(srcDir, x, "addon.xml"))
                    root = tree.getroot()
                    for elem in root.iter('addon'):
                        print('    * %s %s version: %s' %(x,elem.tag,elem.attrib['version']))
                        version = '-'+elem.attrib['version']
                        item = {
                            "id": elem.attrib['id'],
                            "Title": elem.attrib['name'],
                            "Version": elem.attrib['version']
                        }
                    # webAddons["Items"][id]={
                    #     "Title":item["Title"],
                    #     "Version":item["Version"]
                    # }
                    # for item in webAddons["Items"]:
                    #     webAddons["Thumb"]["HTML"] += str(webAddons["Thumb"]["Template"]).replace("{ID}",item['id']).replace("{TITLE}",item['Title']).replace("{VERSION}",item["Version"])
                    # TODO - Develop modal popup

                # print("    * Generate index.html.")
                # with open(webIndexSrc,"r") as fp:
                #     html=fp.read()
                #     fp.close()
                # html = html.replace("{ITEMS}",html)
                #
                # fp = open(webIndexDst,"wb").write(html)

                print('    * Copying repo files.')                
                for y in filesInFolderToZip: 
                    if re.search("addon.xml|changelog|icon|fanart", y):
                        shutil.copyfile(os.path.join(srcDir,x,y), os.path.join(zipsFolder,y))
                        if re.search("changelog", y):
                            verName = y[:-4]+version+'.txt'
                            shutil.copyfile(os.path.join(zipsFolder,y), os.path.join(zipsFolder,verName))
                print('    * Zipping %s and moving to %s' %(x,zipsFolder))
                try:
                    zipFolder(zipFilenameFirstPart, version+zipFilenameLastPart, folderToZip, zipsFolder)
                    print('    * Zipped with zipFolder')
                except:
                    if os.path.exists(zipsFolder + x + version + '.zip' ):
                        os.remove(zipsFolder + x + version + '.zip' )
                        print('    * Trying shutil')
                    try:
                        shutil.move(shutil.make_archive(folderToZip + version, 'zip', folderToZip), zipsFolder)
                        print('    * Zipped with shutil')
                    except Exception as e:
                        print('Cannot create zip file\nshutil %s\n' %e)
    except Exception as e:
        print('    * Cannot create or move the needed files\n%s' %e)
    print('\n===== Done =====\n')
