from tqdm import tqdm
import numpy as np
import os
import matplotlib.pyplot as plt


def read_file(file):
    input_file = open(file, 'r')
    R, C, L, H = [int(num) for num in input_file.readline().split()]

    lines = input_file.readlines()

    pizza = np.array([list(map(lambda item: 1 if item == 'T' else 0, row.strip())) for row in lines])

    return R, C, L, H, pizza


def make_shapes(L, H):
    shapes = []
    for j in range(2 * L, H + 1):
        for i in range(1, H + 1):
            if j % i == 0:
                shapes.append((i, int(j / i)))
    return shapes


def validate_slice(x, y, shape, pizza, mask, L, R, C):
    tomtoes = 0
    mashrooms = 0
    for i in range(x, x + shape[0]):
        for j in range(y, y + shape[1]):
            if i >= R or j >= C or mask[i][j] == 1:
                return False

            if pizza[i][j] == 1:
                tomtoes += 1
            else:
                mashrooms += 1
    if tomtoes >= L and mashrooms >= L:
        return True
    return False


def mark_slice(x, y, shape, mask):
    for i in range(x, x + shape[0]):
        for j in range(y, y + shape[1]):
            mask[i][j] = 1


def main():
    input_folder = "input-folder"
    output_folder = "output-folder"

    if not os.path.exists(input_folder):
        print("Input folder does not exist! Input files must be placed in a folder named: '{}'".format(input_folder))
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    general_score = 0
    files = ['a_example.in', 'b_small.in', 'c_medium.in', 'd_big.in']
    for file in files:
        R, C, L, H, pizza = read_file(input_folder + '/' + file)
        shapes = make_shapes(L, H)
        mask = np.zeros_like(pizza)

        slices = []
        score = 0

        for row in tqdm(range(R)):
            for column in range(C):
                if mask[row][column] is 1:  # if start point is already cut from pizza
                    continue

                for shape in shapes:
                    if validate_slice(row, column, shape, pizza, mask, L, R, C):
                        score += shape[0] * shape[1]
                        slices.append((row, column, row + shape[0] - 1, column + shape[1] - 1))
                        # slices_location.append((row, column))
                        mark_slice(row, column, shape, mask)
                        break

        general_score += score
        out_file = output_folder + "/" + file.split('.')[0] + '.out'
        if os.path.exists(out_file):
            os.remove(out_file)
        with open(out_file, 'a+') as f:
            f.write(str(len(slices)) + "\n")
            for s in slices:
                f.write("{} {} {} {}\n".format(s[0], s[1], s[2], s[3]))

        print("number of slices for file {}: {}".format(file, len(slices)))
        print("number of cells for file {}: {}".format(file, score))

    print("general score is: {}".format(general_score))


if __name__ == "__main__":
    main()
