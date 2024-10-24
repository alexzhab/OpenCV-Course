from chromakey import ChromaKey

if __name__ == "__main__":
    chromakey = ChromaKey((640, 480),
                          "HW2/data/news.mp4",
                          "HW2/data/beach.jpg")
    chromakey.process()
