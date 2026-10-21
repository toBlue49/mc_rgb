import image_creator;
import blocks;
from PIL import Image;
import os;

rgb_blocks = blocks.generate_rgb_blocks(blocks.solid_blocks)
img_list = os.listdir("./temp")
img_cretor = image_creator.ImageCreator(rgb_blocks)
play_video_string = ""


counter = 0
for image_file in img_list:
    img = Image.open(os.path.join("./temp", image_file))

    string = img_cretor.convert_image(img, (128, 72))

    file = open("./out_mcfunction/f" + str(counter) + ".mcfunction", "w")
    file.write(string)
    file.close()

    print(counter)
    
    play_video_string += f"execute if score frame video matches {counter*2} run function rgb:video/f{counter}\n"
    
    counter += 1

final_file = open("./out_mcfunction/play_video.mcfunction", "w")
final_file.write(play_video_string)
final_file.close()