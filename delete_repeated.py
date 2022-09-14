def delete_repeated_lines():
    with open('user-ct-test-collection-09.txt', 'r') as f:
        lines = f.readlines()
        lines_set = set(lines)
        with open('user-ct-test-collection-09.txt', 'w') as f:
            for line in lines_set:
                f.write(line)

if __name__ == '__main__':
    delete_repeated_lines()