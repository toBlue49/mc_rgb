from PIL import Image;
from colorama import Fore, Style;

class ImageCreator:
    def __init__(self, rgb_blocks: list):
        self.rgb_blocks = rgb_blocks

    ## Converts the given image to commands in one string
    def convert_image(self, img: Image, size: tuple) -> str:
        res_img = img.resize(size)
        pixel_list = list(res_img.get_flattened_data())
        the_string = ""
        
        for index in range(len(pixel_list)):
            pixel = pixel_list[index]
            rgb_8 = [(pixel[0]+1)//32, (pixel[1]+1)//32, (pixel[2]+1)//32]
            
            x = index % size[0]
            y = index // size[0]
            
            the_string += "setblock ~" + str(x) + " ~0 ~" + str(y) + " " + \
                        self.rgb_blocks[rgb_8[0]][rgb_8[1]][rgb_8[2]] + " strict\n"

        return the_string

    ## VIDEO ONLY
    # Uses the last frame, to skip pixels which did not change.
    def convert_image_skip_pixels(self, img: Image, size: tuple, last_frame_img: Image) -> str:
            #lf = last frame
            res_img = img.resize(size)
            res_lf_img = last_frame_img.resize(size)
            pixel_list = list(res_img.get_flattened_data())
            lf_pixel_list = list(res_lf_img.get_flattened_data())
            skipped_pixels = 0
            the_string = ""
            
            for index in range(len(pixel_list)):
                pixel = pixel_list[index]
                lf_pixel = lf_pixel_list[index]
                
                x = index % size[0]
                y = index // size[0]
                
                if (pixel == lf_pixel):
                    skipped_pixels += 1
                    continue;
                
                rgb_8 = [(pixel[0]+1)//32, (pixel[1]+1)//32, (pixel[2]+1)//32]
                

                the_string += "setblock ~" + str(x) + " ~0 ~" + str(y) + " " + \
                    self.rgb_blocks[rgb_8[0]][rgb_8[1]][rgb_8[2]] + " strict\n"
            
            print(Fore.YELLOW + "Skipped Pixels: " + str(skipped_pixels) + Fore.RESET)
            return the_string
    
    ## Uses /fill commands instead of only /setblock commands.
    def convert_image_smart(self, img: Image, size: tuple) -> str:
        res_img = img.resize(size)
        pixel_list = list(res_img.get_flattened_data())
        same_color_counter = 0
        the_string = ""
        
        for index in range(len(pixel_list)):
            pixel = pixel_list[index]
            col_change = False
            
            x = index % size[0]
            y = index // size[0]
            
            if index != 0 and y == (index-1) // size[0]:
                if pixel != pixel_list[index-1]:
                    col_change = True
                else:
                    same_color_counter += 1
            else:
                same_color_counter = 0
            
            
            rgb_8 = [(pixel[0]+1)//32, (pixel[1]+1)//32, (pixel[2]+1)//32]
            

            if col_change:
                if same_color_counter == 0: #Color changed instantly
                    the_string += "setblock ~" + str(x) + " ~0 ~" + str(y) + " " + \
                        self.rgb_blocks[rgb_8[0]][rgb_8[1]][rgb_8[2]] + " strict\n"
                else: #Else:
                    prev_pixel = pixel_list[index-1]
                    prev_rgb_8 = [(prev_pixel[0]+1)//32, (prev_pixel[1]+1)//32, (prev_pixel[2]+1)//32]
                    
                    
                    the_string += "fill ~" + str(x-same_color_counter) + " ~0 ~" + str(y) + " ~" + str(x) + " ~0 ~" + str(y) + \
                        " " + self.rgb_blocks[prev_rgb_8[0]][prev_rgb_8[1]][prev_rgb_8[2]] + " strict\n"
                same_color_counter = 0
        
        return the_string