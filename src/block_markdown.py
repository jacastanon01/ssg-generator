def markdown_to_blocks(document):
    blocks_list = []
    split_blocks = document.split("\n")

    for line in split_blocks:
        line = line.strip()
        if line == "":
            continue
        blocks_list.append(line)
    return blocks_list
