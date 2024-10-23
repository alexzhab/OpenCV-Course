from chromakey import ChromaKey

if __name__ == "__main__":
    chromakey = ChromaKey((640, 480),
                          "data/door.mp4",
                          "data/beach.jpg")
    chromakey.process()
