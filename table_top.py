#! /usr/bin/env python
# coding: utf-8

from os import walk
from os.path import isfile, join
import math
# import gimp
from gimpfu import *

def table_top(img, layer, mypath, width, height, margin):
    for root, dirs, files in walk(mypath):
        files = filter(lambda x: not x.startswith('.'), files)
        pairs = [(files[i-1], files[i]) for i in range(1,len(files),2)]
        for pair in pairs:
            layers = []
            for i,p in enumerate(pair):
                fname = join(root, p)
                # img = gimp.image_list()[0]
                layers.append(pdb.gimp_file_load_layer(img, fname))
                img.add_layer(layers[-1])
                y_offset = abs(i*(img.height - width) - margin)
                # size to given size
                layers[-1].scale(width, height)
                # rotate clockwise
                pdb.gimp_item_transform_rotate(layers[-1], math.pi/2, True, 0, 0)
                # move margin left
                layers[-1].set_offsets(int(img.width/2 - width - margin), y_offset)
                # duplicate
                layers.append(layers[-1].copy())
                img.add_layer(layers[-1])
                # rotate duplicate counter clockwise
                pdb.gimp_item_transform_rotate(layers[-1], math.pi, True, 0, 0)
                # move margin right
                layers[-1].set_offsets(int(img.width/2 + margin), y_offset)
            new_image = pdb.gimp_image_duplicate(img)
            for layer in layers:
                img.remove_layer(layer)
            layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
            outname = join(root, 'out.'+p)
            pdb.gimp_file_save(new_image, layer, outname, '?')
            pdb.gimp_image_delete(new_image)

register("table-top",
    "Table Top",
    "Table Top",
    "Jordan Valansi", "Public domain", "2017",
    N_("Table Top"),
    "*",
    [(PF_IMAGE, "image",       "Input image", None),
     (PF_DRAWABLE, "layer", "Input drawable", None),
     (PF_DIRNAME, "mypath", "Source Directory", ""),
     (PF_INT, "width", "Width", 0),
     (PF_INT, "height", "Height", 0),
     (PF_INT, "margin", "Margin", 0),
     ], [],
    table_top,  menu="<Image>/Layer/",
    )

main()
