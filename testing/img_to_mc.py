from PIL import Image;
import sys;
from blocks import solid_blocks;

rgb_blocks = []
green_list = []
red_list = []

the_string = ""

# Setup RGB Blocks
for B in range(9):
    green_list = []
    
    for G in range(9):
        red_list = []
        
        for R in range(9):
            this_block = solid_blocks.pop(0)
            red_list.append(this_block)

        green_list.append(red_list)

    rgb_blocks.append(green_list)

og_img = Image.open(sys.argv[1])
img = og_img.resize((256, 144))
img.show()
pixel_list = list(img.get_flattened_data())
for index in range(len(pixel_list)):
    pixel = pixel_list[index]
    rgb_8 = [(pixel[0]+1)//32, (pixel[1]+1)//32, (pixel[2]+1)//32]
    x = index % 256
    y = index // 256
    
    the_string += "setblock ~" + str(x) + " ~0 ~" + str(y) + " " + \
                rgb_blocks[rgb_8[0]][rgb_8[1]][rgb_8[2]] + " strict\n"

    print(x, y)
    
file = open("image.mcfunction", "w")
file.write(the_string)
file.close()