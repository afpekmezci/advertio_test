class Validator:
	required_error = "{key} is required."
	integer_error = "{key} shoud be a positive integer."
	zero_error = "{key} should be bigger than 0."
	page_error = "current_page should be smaller than total_pages."

	def validate_num(self, key, value):
		if value is None:
			raise ValueError(self.required_error.format(key=key))
		if not isinstance(value, int):
			raise ValueError(self.integer_error.format(key=key))
		if value < 0:
			raise ValueError(self.zero_error.format(key=key))

	def validate_positive_int(self, key, value):
		if value < 1:
			raise ValueError(self.zero_error.format(key=key))

	def validate_page(self, page, total_page):
		self.validate_num('page', page)
		self.validate_positive_int('page', page)
		if page > total_page:
			raise ValueError(self.page_error)


def validate(current_page: int, total_pages: int, boundaries: int, around: int):
	validator = Validator()
	validator.validate_num('total_page', total_pages)
	validator.validate_positive_int('total_page', total_pages)

	validator.validate_num('boundaries', boundaries)

	validator.validate_num('around', around)

	validator.validate_page(current_page, total_pages)


def paginate(current_page: int, total_pages: int, boundaries: int = 1, around: int = 0):
	validate(current_page, total_pages, boundaries, around)

	combiner = '...'

	boundaries_set = set([x for i in range(0, boundaries) for x in (i + 1, total_pages - i)])
	around_set = set([x for k in range(0, around) for x in (current_page - k - 1, current_page + k + 1)])

	displayed_pages = boundaries_set | around_set | {current_page}

	displayed_pages = list(displayed_pages)
	displayed_pages = sorted(displayed_pages)
	displayed_pages = list(filter(lambda x: 0 < x <= total_pages, displayed_pages))

	boundaries_right_min = total_pages - boundaries + 1
	boundaries_left_max = boundaries

	around_min = current_page - around
	around_max = current_page + around

	if boundaries_left_max + 1 < around_min and boundaries_left_max + 1 < boundaries_right_min:
		displayed_pages.insert(boundaries, combiner)

	if boundaries_right_min - 1 > around_max and boundaries_right_min > boundaries + 1:
		displayed_pages.insert(len(displayed_pages) - boundaries, combiner)

	displayed_text = ' '.join(list(map(str, displayed_pages)))
	print(displayed_text)
	return displayed_text

