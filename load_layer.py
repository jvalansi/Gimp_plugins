#! /usr/bin/env python
# coding: utf-8

from os import walk
from os.path import isfile, join
from gimpfu import *

def load_layer(img, layer, mypath):
    for root, dirs, files in walk(mypath):
        for f in files:
            if f.startswith('.'):
              continue
            fname = join(root, f)
            outname = join(root, 'out.'+f)
            # img = image_list()[0]
            layer = pdb.gimp_file_load_layer(img, fname)
            #gimp.pdb.gimp_image_insert_layer(img, layer, None, 0)
            img.add_layer(layer)
            factor = min (float(img.width) / layer.width, float(img.height) / layer.height);
            layer.scale(int(layer.width * factor), int(layer.height * factor));
            layer.set_offsets((img.width - layer.width) / 2, (img.height - layer.height) / 2)
            new_image = pdb.gimp_image_duplicate(img)
            layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
            pdb.gimp_file_save(new_image, layer, outname, '?')
            pdb.gimp_image_delete(new_image)

register("load-layer",
    "Load layer",
    "Load layer",
    "Jordan Valansi", "Public domain", "2017",
    N_("Load layer"),
    "*",
    [(PF_IMAGE, "image",       "Input image", None),
     (PF_DRAWABLE, "layer", "Input drawable", None),
     (PF_DIRNAME, "mypath", "Source Directory", ""),
     ], [],
    load_layer,  menu="<Image>/Layer/",
    )

main()
