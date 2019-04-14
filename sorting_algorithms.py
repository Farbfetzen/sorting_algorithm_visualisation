class SortingAlgorithm:
    def __init__(self, values):
        self.values = values
        self.comparisons = []
        self.pivots = []
        self.is_sorted = False
        self.comparison_count = 0
        self.swaps_count = 0

    def compare(self, a, b):
        self.comparison_count += 1
        return self.values[a] > self.values[b]

    def swap(self, a, b):
        self.values[a], self.values[b] = self.values[b], self.values[a]
        self.swaps_count += 1

    def update(self):
        raise NotImplementedError("Missing update method.")


class BubbleSort(SortingAlgorithm):
    def __init__(self, values):
        super().__init__(values)
        self.i = 0
        self.i_max = len(self.values) - 1
        self.comparisons = [self.i, self.i + 1]

    def update(self):
        if self.is_sorted:
            return
        if self.compare(self.i, self.i + 1):
            self.swap(self.i, self.i + 1)
        self.i += 1
        if self.i == self.i_max:
            self.i = 0
            self.i_max -= 1
            if self.i_max == 1:
                self.is_sorted = True
        self.comparisons = [self.i, self.i + 1]
