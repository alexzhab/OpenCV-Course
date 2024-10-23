from chromakey import ChromaKey

if __name__ == "__main__":
    chromakey = ChromaKey((640, 480),
                          "/home/sasha/Downloads/door.mp4",
                          "/home/sasha/Downloads/beach.jpg")
    chromakey.process()
