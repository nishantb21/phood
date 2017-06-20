from sys import argv

ingredient_number = range(int(argv[-2]), int(argv[-1]) + 1)

for i_no in ingredient_number:
    fractal = round(100/i_no, 4)
    print(i_no, fractal, sep=" : ")
    perc_list = list()
    for index in range(i_no):
        perc_list.append(fractal)

    #print(perc_list)
    for rrange in range(1, i_no):
        steal = round(((rrange/i_no)*fractal)/2, 4)
        #print("Stole " + str(steal) + " from " + str(rrange))
        perc_list[rrange] -= steal
        perc_list[0] += steal
    print(perc_list)
