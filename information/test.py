def combinations(arr):
	temp = []
	i = 0
	j = 0
	arr_len = len(arr)
	while i < arr_len:
		while j < arr_len:
			print set(temp + [arr[j]])
			j += 1
		j = i + 1
		temp.append(arr[i])
		i += 1
