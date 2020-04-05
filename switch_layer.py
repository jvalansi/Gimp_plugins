
from os import listdir
from os.path import isfile, join

mypath = '/Users/jordanvalansi/projects/qrs/'
outpath = '/Users/jordanvalansi/projects/qrcodes/'

for f in listdir(mypath):
    if f.startswith('.'):
      continue
    print(f)
    fname = join(mypath, f)
    img = gimp.image_list()[0]
    layer = gimp.pdb.gimp_file_load_layer(img, fname)
    #gimp.pdb.gimp_image_insert_layer(img, layer, None, 0)
    img.add_layer(layer)
    factor = min (float(img.width) / layer.width, float(img.height) / layer.height);
    layer.scale(int(layer.width * factor), int(layer.height * factor));
    layer.set_offsets((img.width - layer.width) / 2, (img.height - layer.height) / 2)
    new_image = pdb.gimp_image_duplicate(img)
    layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
    pdb.gimp_file_save(new_image, layer, join(outpath,f), '?')
    pdb.gimp_image_delete(new_image)
