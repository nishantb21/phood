def ratio(i_no = 1):
	fractal = round(100/i_no, 4)
	perc_list = list()
	for index in range(i_no):
		perc_list.append(fractal)

	for rrange in range(1, i_no):
		steal = round(((rrange/i_no)*fractal)/2, 4)
		perc_list[rrange] -= steal
		perc_list[0] += steal
	return perc_list