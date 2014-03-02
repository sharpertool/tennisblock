
import os
from os.path import join

class BuildSpec(object):

    def __init__(self,static_root,mxgraph_root):
        self.static_root = static_root
        self.mxroot = mxgraph_root

    def getSpec(self):

        jsroot = join(self.static_root,'js')
        lessroot = join(self.static_root,'less')
        cssroot = join(self.static_root,'css')

        return {
            'embed': {
                'static_dir': self.static_root,
                'less': [
                    {
                        'src' : join(lessroot,'schematics_embed_en.less'),
                        'dest' : join(cssroot,'schematics_embed_en.css')
                    },
                    {
                        'src' : join(lessroot,'schematics_embed_zh.less'),
                        'dest' : join(cssroot,'schematics_embed_zh.css')
                    },
                ],
                'cssmin': [
                    {
                        'src' : [
                                    join(cssroot,'schematics_embed_en.css')
                                ],
                        'dest' : join(cssroot,'schematics_embed_en_min.css')
                    },
                    {
                        'src' : [
                            join(cssroot,'schematics_embed_zh.css')
                        ],
                        'dest' : join(cssroot,'schematics_embed_zh_min.css')
                    }
                ],
                'client': {
                    'src' : join(jsroot,'schClientEmbed.js'),
                    'pre' : [join(jsroot,'eeweb','core-schematic','schBackend.js')],
                    'post' : [],
                    'dest' : join(jsroot,'library/eeLibraryEmbedMin.js'),
                },
            },
            'main': {
                'less': [
                    {
                        'src' : join(lessroot,'schematics_en.less'),
                        'dest' : join(cssroot,'schematics_en.css')
                    },
                    {
                        'src' : join(lessroot,'schematics_zh.less'),
                        'dest' : join(cssroot,'schematics_zh.css')
                    }
                ],
                'cssmin': [
                    {
                        'src' : [
                                    join(cssroot,"jPicker-1.1.6.min.css"),
                                    join(cssroot,"schematics_en.css"),
                                ],
                        'dest' : join(cssroot,'schematics_en_min.css')
                    },
                    {
                        'src' : [
                            join(cssroot,"jPicker-1.1.6.min.css"),
                            join(cssroot,"schematics_zh.css"),
                            ],
                        'dest' : join(cssroot,'schematics_zh_min.css')
                    },
                ],
                'static_dir': self.static_root,
                'client': {
                    'src' : join(jsroot,'schClient.js'),
                    'pre' : [join(jsroot,'eeweb/core-schematic/schBackend.js')],
                    'post' : [],
                    'dest' : join(jsroot,'library/eeLibraryMin.js'),
                },
                'mxgraph': {
                    'src' : join(self.mxroot,'javascript/src/js/mxClient.js'),
                    'pre' : [],
                    'post' : [],
                    'dest' : join(jsroot,'library/mxClient.gen.min.js'),
                }
            }
        }

