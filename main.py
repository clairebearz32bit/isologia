from src.word import Word

if __name__ == '__main__':
    word = Word("etymology")
    # r = word.get_etymology()

    for node in word.parse_etymology():
        print(node)

