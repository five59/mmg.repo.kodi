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
import time
import re
import xml.etree.ElementTree as ET

try:
    import shutil,zipfile
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
 
class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file.
    """

    def __init__( self ):
        # generate files
        print("\n\n--> Updating repo metadata.")
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user
 
    def _generate_addons_file( self ):
        print("     * Generating new addons.xml file for repo.")
        # Set up references
        src_dir = os.path.dirname(sys.path[0]) + os.sep + "source" + os.sep + "addons"
        repo_dir = os.path.dirname(sys.path[0]) + os.sep + "repo"
        # addon list
        addons = os.listdir(src_dir)        
        # final addons text
        addons_xml = u("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n")
        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                if re.search("plugin|script|service|skin|repository" , addon):
                    print("     * Found " + addon)
                    _path = os.path.join( src_dir, addon, "addon.xml" )
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
        addonfilename=repo_dir + os.sep + "addons.xml"
        self._save_file( addons_xml.encode( "UTF-8" ), file=addonfilename )
 
    def _generate_md5_file( self ):
        print("     * Generating new addons.xml MD5 hashfile for repo.")
        src_dir = os.path.dirname(sys.path[0]) + os.sep + "source" + os.sep + "addons"
        repo_dir = os.path.dirname(sys.path[0]) + os.sep + "repo"
        # create a new md5 hash
        try:
            import md5
            addonfilename = repo_dir + os.sep + "addons.xml"
            m = md5.new( open(addonfilename, "r" ).read() ).hexdigest()
        except ImportError:
            import hashlib
            m = hashlib.md5( open(addonfilename, "r", encoding="UTF-8" ).read().encode( "UTF-8" ) ).hexdigest()
        try:
            self._save_file( m.encode( "UTF-8" ), file=repo_dir + os.sep + "addons.xml.md5" )
        except Exception as e:
            print("* An error occurred creating addons.xml.md5 file!\n%s" % e)
 
    def _save_file( self, data, file ):
        src_dir = os.path.dirname(sys.path[0]) + os.sep + "source" + os.sep + "addons"
        repo_dir = os.path.dirname(sys.path[0]) + os.sep + "repo"
        try:
            open( file, "wb" ).write( data )
        except Exception as e:
            print("An error occurred saving %s file!\n%s" % ( file, e ))
 
def zipfolder(foldername, suffix, target_dir, zips_dir):
    src_dir = os.path.dirname(sys.path[0]) + os.sep + "source" + os.sep + "addons"
    repo_dir = os.path.dirname(sys.path[0]) + os.sep + "repo"
    zipobj = zipfile.ZipFile(zips_dir + foldername + suffix, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for f in files:
            fn = os.path.join(base, f)
            zipobj.write(fn, os.path.join(foldername,fn[rootlen:]))
    zipobj.close()

if ( __name__ == "__main__" ):
    Generator()
    try:
        src_dir = os.path.dirname(sys.path[0]) + os.sep + "source" + os.sep + "addons"
        repo_dir = os.path.dirname(sys.path[0]) + os.sep + "repo"
        filesinrootdir = os.listdir(src_dir)
        for x in filesinrootdir:
            if re.search("plugin|script|service|skin|repository" , x) and not re.search('.zip',x):
                print("\n--> Working on " + x + "...")
                zipfilename = x + '.zip'
                zipfilenamefirstpart = zipfilename[:-4]
                zipfilenamelastpart = zipfilename[len(zipfilename)-4:]
                zipsfolder = os.path.normpath(os.path.join(repo_dir,x)) + os.sep
                foldertozip = src_dir + os.sep + x
                filesinfoldertozip = os.listdir(foldertozip)        
                if not os.path.exists(zipsfolder):
                    os.makedirs(zipsfolder)
                    print('    * Directory doesn\'t exist, creating: ' + zipsfolder)                
                if "addon.xml" in filesinfoldertozip: 
                    print('    * Found plugin addon.xml file.')
                    tree = ET.parse(os.path.join(src_dir, x, "addon.xml"))
                    root = tree.getroot()
                    for elem in root.iter('addon'):
                        print('    * %s %s version: %s' %(x,elem.tag,elem.attrib['version']))
                        version = '-'+elem.attrib['version']                  
                for y in filesinfoldertozip: 
                    if re.search("addon.xml|changelog|icon|fanart", y):
                        shutil.copyfile(os.path.join(src_dir,x,y), os.path.join(zipsfolder,y))
                        if re.search("changelog", y):
                            verName = y[:-4]+version+'.txt'
                            shutil.copyfile(os.path.join(zipsfolder,y), os.path.join(zipsfolder,verName))
                        print('    * Copying %s to %s'  %(y, zipsfolder))                
                print('    * Zipping %s and moving to %s' %(x,zipsfolder))
                try:
                    zipfolder(zipfilenamefirstpart, version+zipfilenamelastpart, foldertozip, zipsfolder)
                    print('    * Zipped with zipfolder')
                except:
                    if os.path.exists(zipsfolder + x + version + '.zip' ):
                        os.remove(zipsfolder + x + version + '.zip' )
                        print('    * Trying shutil')
                    try:
                        shutil.move(shutil.make_archive(foldertozip + version, 'zip', foldertozip), zipsfolder)
                        print('    * Zipped with shutil')
                    except Exception as e:
                        print('Cannot create zip file\nshutil %s\n' %e)
    except Exception as e:
        print('    * Cannot create or move the needed files\n%s' %e)
    print('\n===== Done =====\n')
