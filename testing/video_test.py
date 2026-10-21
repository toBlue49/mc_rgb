import video_splitter;
vspl = video_splitter.VideoSplitter("./temp")

vspl.split("testing/testing.mp4", (256, 144), 10)

