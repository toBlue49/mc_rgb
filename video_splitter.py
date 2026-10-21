import cv2;
from PIL import Image;
import os;

class VideoSplitter:
    def __init__(self, out_path: str = "./temp"):
        self.out_path = out_path

    def split(self, path: str, size: tuple = (256, 144), FPS: int = 5):
        video_capture = cv2.VideoCapture(path)
        video_capture.set(cv2.CAP_PROP_FPS, 60)
        frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frameskip_counter = 0
        video_fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        frameskip = video_fps//FPS
        
        saved_frame = 0
        while saved_frame < frame_count//frameskip:
            frameskip_counter += 1
            frame_is_read, frame = video_capture.read()
            
            if frameskip != frameskip_counter:
                continue
            else:
                frameskip_counter = 0
            
            
            if frame_is_read:
                image: Image = self.convert_cv2_to_pil(frame)
                res_image = image.resize(size)
                res_image.save(os.path.join(self.out_path, f"f{str(saved_frame)}.webp"))
            else:
                print("Couldn't read frame.")
            
            saved_frame += 1

            print(f"{str(saved_frame)}/{str(frame_count//frameskip)} Frames")

    def convert_cv2_to_pil(self, cv2_img) -> Image:
        return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))