#coding:utf-8
import os
import os.path
import xml.etree.ElementTree as ET
import plistlib

res_path = "/Users/heliang/rafotech/GuiYangCompanyClient/GuiYangArtResource/GuiYangChessUI/Resources/"
# src_path = "/Users/liqiang/projects/LuZhouChessClient/LuZhouArtResource/资源碎图/"

# res_path = "/Users/liqiang/projects/GuiYangCompanyClient/GuiYangArtResource/GuiYangChessUI/Resources"

#parse all the img
plist_map = {}
img_map = {}
ccbs = []
img_samename = {}
plist_samename = {}
for root, dirs, files in os.walk(res_path):
    if root.find('fonts/') >= 0:
       continue

    for name in files:
        newFromFilePath = os.path.join(root, name)
        fileName, fileSuffix = os.path.splitext(name)
        if fileSuffix == '.png' or fileSuffix == '.jpg':
            if name in img_map:
                if name not in img_samename:
                    img_samename[name] = [img_map[name]]
                img_samename[name].append("%s/%s" % (root[len(res_path):], name))

            path = "%s/%s" % (root[len(res_path):], name)
            if path == 'picture/teaHouse/btn_invite.png':
                continue

            img_map[name] = "%s/%s" % (root[len(res_path):], name)
        elif fileSuffix == '.plist':
            pl = plistlib.readPlist(newFromFilePath)
            frames = pl['frames']
            for k,v in frames.items():
                if k in plist_map:
                    if k not in plist_samename:
                        plist_samename[k] = [plist_map[k]]
                    plist_samename[k].append("%s/%s" % (root[len(res_path):], name))
                plist_map[k] = "%s/%s" % (root[len(res_path):], name)
        elif fileSuffix == '.ccb':
            ccbs.append("%s/%s" % (root[len(res_path):], name))

def scan_children(children):
    count = 0
    for p in children['properties']:
        if p.type == 'SpriteFrame':
            img_name = p['value'][1]
            if img_name.startswith('poker_animation'):
                continue
            if p['value'][0] == '': #sui tu
                img_name = os.path.basename(p['value'][1])
            elif p['value'][0][:7] == 'picture':
                continue

            if img_name in img_map:
                if p['value'][1] != img_map[img_name]:
                    n_path = img_map[img_name]
                    # if p['value'][1][:5] == 'image':
                    #     n_path = "picture" + p['value'][1][5:]
                    # else:
                    #     continue

                    if p['value'][1][:7] == 'picture':
                        continue

                    print "replace img %s to %s " % (p['value'][1], n_path)
                    p['value'][0] = ''
                    p['value'][1] = n_path
                    count += 1
            elif img_name in plist_map:
                if p['value'][0] != plist_map[img_name]:
                    n_path = plist_map[img_name]


                    # if p['value'][0][:5] == 'image':
                    #     n_path = "picture" + p['value'][0][5:]
                    # else:
                    #     continue
                    print "replace plist img %s %s to %s " % (p['value'][0], img_name, n_path)
                    p['value'][0] = n_path
                    p['value'][1] = img_name
                    count += 1
            else:
                print "can not find the img %s %s %s" % (img_name, p['value'][0], p['value'][1] )
                raise Exception("can not find the img %s %s %s" % (img_name, p['value'][0], p['value'][1] ))
        elif p.type == 'CCBFile':
            ccbname = p.value.split("/")[1]

            if p.value[:4] == 'data':
                print "===============%s %s"% (p.value, ccbname)
                p.value = "ui/%s"%ccbname
                count += 1
        elif p.type == 'Texture':
            # if p.value[:5] == 'image':
            #     n_path = "picture" + p.value[5:]
            #     print "replace Texture %s to %s " % (p.value, n_path)
            #     p.value = n_path
            #     count += 1
            img_name = os.path.basename(p['value'])
            if p['value'] != img_map[img_name]:
                n_path = img_map[img_name]
                print "replace Texture %s to %s " % (p.value, n_path)
                p.value = n_path
                count += 1
        elif p.type == 7:
            print(p.value[0])

    for cd in children['children']:
        count += scan_children(cd)
    if "animatedProperties" in children:
        for k,v in children['animatedProperties'].items():
            if 'displayFrame' not in v:
                continue
            for kf in v['displayFrame']['keyframes']:
                if kf.type == 7:
                    if kf.value[1] == 'Use regular file':
                        img_name = os.path.basename(kf.value[0])
                        if kf.value[0] != img_map[img_name]:
                            print "replace anim img %s to %s " % (kf.value[0], img_map[img_name])
                            kf['value'][0] = img_map[img_name]
                            count += 1
                    else:
                        img_name = os.path.basename(kf.value[0])
                        if kf.value[1] != plist_map[img_name]:
                            print "replace anim img plist %s to %s " % (kf.value[1], plist_map[img_name])
                            kf['value'][1] = plist_map[img_name]
                            count += 1

    return count

#pase ccb and replace it
def parseCCB():
    for cb in ccbs:
        # if cb.endswith('PPlayScene.ccb'):
        #     continue

        print "begin parse %s " % cb
        ccb = plistlib.readPlist("%s%s"%(res_path, cb))
        cs = ccb['nodeGraph']['children']

        count = 0
        for c in cs:
            count += scan_children(c)

        # if count > 0:
        #     print "end parse %s %s" % (cb, count)
        #
        # if count > 0:
        #     plistlib.writePlist(ccb, "%s%s"%(res_path, cb))
        #     print "end parse %s %s" % (cb, count)

parseCCB()

# for k,v in img_samename.items():
#     print("%s: %s"%(k, ";".join(v)))
#
# for k,v in plist_samename.items():
#     print("%s: %s"%(k, ";".join(v)))

# ccb = plistlib.readPlist("%s%s"%(res_path, "ccbi/MainScene.ccb"))
# print ccb








