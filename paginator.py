class Validator:
	required_error = "{key} is required."
	integer_error = "{key} shoud be an integer."
	zero_error = "{key} should be bigger than 0."
	page_error = "current_page should be smaller than total_pages"

	def validate_num(self, key, value):
		if value is None:
			raise ValueError(self.required_error.format(key=key))
		if not isinstance(value, int):
			raise ValueError(self.integer_error.format(key=key))

	def validate_zero(self, key, value):
		if value < 1:
			raise ValueError(self.zero_error.format(key=key))

	def validate_page(self, page, total_page):
		self.validate_num('page', page)
		self.validate_zero('page', page)
		if page > total_page:
			raise ValueError(self.page_error)


def validate(current_page: int, total_pages: int, boundaries: int, around: int):
	validator = Validator()
	validator.validate_num('total_page', total_pages)
	validator.validate_zero('total_page', total_pages)

	validator.validate_num('boundaries', boundaries)
	validator.validate_zero('boundaries', boundaries)

	validator.validate_num('around', around)
	validator.validate_page(current_page, total_pages)


def paginate(current_page: int, total_pages: int, *args, **kwargs):
	boundaries: int = kwargs.get('boundaries', 1)
	around: int = kwargs.get('around', 1)
	validate(current_page, total_pages, boundaries, around)

	combiner = '...'

	displayed_pages = set()
	displayed_pages.add(current_page)

	i = 0
	while i < boundaries:
		displayed_pages.add(i + 1)
		displayed_pages.add(total_pages - i)
		i += 1

	k = 0
	while k < around:
		displayed_pages.add(current_page - k - 1)
		displayed_pages.add(current_page + k + 1)
		k += 1

	displayed_pages = list(displayed_pages)
	displayed_pages = sorted(displayed_pages)
	displayed_pages = list(filter(lambda x: 0 < x <= total_pages, displayed_pages))

	if current_page - around > boundaries + 1:
		displayed_pages.insert(boundaries, combiner)
	if total_pages - boundaries > current_page + around:
		displayed_pages.insert(len(displayed_pages) - boundaries, combiner)
	displayed_text = ' '.join(list(map(str, displayed_pages)))
	print(displayed_text)
	return displayed_text
