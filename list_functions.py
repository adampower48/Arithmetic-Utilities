def selection_sort(arr):
    i = 0
    while i < len(arr):
        min_ind = i
        j = i + 1
        while j < len(arr):
            if arr[j] < arr[min_ind]:
                min_ind = j
            j += 1

        arr[i], arr[min_ind] = arr[min_ind], arr[i]
        i += 1


def insertion_sort(arr):
    i = 1
    while i < len(arr):
        v = arr[i]
        j = i
        while j > 0 and arr[j - 1] > v:
            arr[j] = arr[j - 1]
            j -= 1

        arr[j] = v
        i += 1


def first_n_smallest(arr, n):
    first = []

    i = 0
    while i < len(arr):
        j = 0
        while j < n and j < len(first) and first[j] < arr[i]:  # Linear search for correct position
            j += 1

        if j < n:
            if len(first) < n:  # Expand list if less than first n
                first.append(None)

            k = len(first) - 1  # Insertion part of insterion sort
            while k > j:
                first[k] = first[k - 1]
                k -= 1

            first[k] = arr[i]  # End insertion

        i += 1

    return first
