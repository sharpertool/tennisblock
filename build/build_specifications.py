
import os
from os.path import join

class BuildSpec(object):

    def __init__(self,static_root):
        self.static_root = static_root

    def getSpec(self):

        jsroot = join(self.static_root,'js')
        lessroot = join(self.static_root,'less')
        cssroot = join(self.static_root,'css')

        spec = {
            'main': {
                'less': [
                ],
                'cssmin': [
                    {
                        'src' : [
                                    #join(cssroot,"jPicker-1.1.6.min.css"),
                                    #join(cssroot,"schematics_en.css"),
                                ],
                        'dest' : join(cssroot,'tennisblock_min.css')
                    },
                ],
                'static_dir': self.static_root,
            }
        }

        lessfiles = [
            'about',
            'accounts',
            'availability',
            'banner',
            'base'
            'contacts',
            'footer',
            'home',
            'layout',
            'members',
            'playsheet',
            'schedule',
            'tbdefs'
        ]

        l = spec['main']['less']

        for file in lessfiles:
            l.append({
                'src' : join(lessroot,'%s.less' % file),
                'dest': join(cssroot,'%s.css' % file)
            })


        return spec
