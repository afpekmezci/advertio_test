from paginator import paginate, Validator
import unittest


class PaginationTest(unittest.TestCase):

	def test_validate_current_page(self):
		with self.assertRaises(ValueError) as exp:
			# Test current_page non integer
			paginate(current_page='a', total_pages=1)
			self.assertEqual(
				str(exp.exception),
				Validator.integer_error.format(key='current_page')
			)

			# Test current_page zero
			paginate(current_page=0, total_pages=1)
			self.assertEqual(
				str(exp.exception),
				Validator.zero_error.format(key='current_page')
			)

			# Test current_page less then total_page
			paginate(current_page=3, total_pages=1)
			self.assertEqual(
				str(exp.exception),
				Validator.page_error
			)

	def test_validate_total_page(self):
		with self.assertRaises(ValueError) as exp:
			# Test total_pages non integer
			paginate(current_page=1, total_pages=None)
			self.assertEqual(
				str(exp.exception),
				Validator.integer_error.format(key='total_pages')
			)

			# Test current_page zero
			paginate(current_page=1, total_pages=0)
			self.assertEqual(
				str(exp.exception),
				Validator.zero_error.format(key='total_pages')
			)

	def test_validate_boundaries(self):
		with self.assertRaises(ValueError) as exp:
			# Test boundaries non integer
			paginate(current_page=1, total_pages=1, boundaries=[])
			self.assertEqual(
				str(exp.exception),
				Validator.integer_error.format(key='boundaries')
			)

			# Test boundaries zero
			paginate(current_page=1, total_pages=1, boundaries=0)
			self.assertEqual(
				str(exp.exception),
				Validator.zero_error.format(key='boundaries')
			)

	def test_validate_around(self):
		with self.assertRaises(ValueError) as exp:
			# Test around non integer
			paginate(current_page=1, total_pages=1, around=[])
			self.assertEqual(
				str(exp.exception),
				Validator.integer_error.format(key='around')
			)

	def test_single_page(self):
		self.assertEqual(paginate(current_page=1, total_pages=1), '1')

	def test_show_all_pages(self):
		self.assertEqual(paginate(current_page=3, total_pages=5, boundaries=2, around=0), '1 2 3 4 5')

	def test_with_combiner(self):
		self.assertEqual(paginate(current_page=2, total_pages=5, boundaries=1, around=0), '1 2 ... 5')

	def test_with_big_numbers(self):
		self.assertEqual(paginate(current_page=20, total_pages=100, boundaries=3, around=3),
		                 '1 2 3 ... 17 18 19 20 21 22 23 ... 98 99 100')

	def test_first_example(self):
		self.assertEqual(paginate(current_page=4, total_pages=5, boundaries=1, around=0), '1 ... 4 5')

	def test_first_example_backward(self):
		self.assertEqual(paginate(current_page=1, total_pages=5, boundaries=1, around=0), '1 ... 5')

	def test_first_example_backward_with_page_two(self):
		self.assertEqual(paginate(current_page=2, total_pages=5, boundaries=1, around=0), '1 2 ... 5')

	def test_second_example(self):
		self.assertEqual(paginate(current_page=4, total_pages=10, boundaries=2, around=2), '1 2 3 4 5 6 ... 9 10')

	def test_third_example(self):
		self.assertEqual(paginate(current_page=1, total_pages=10, boundaries=6, around=1), '1 2 3 4 5 6 7 8 9 10')

	def test_third_example_backward(self):
		self.assertEqual(paginate(current_page=10, total_pages=10, boundaries=6, around=1), '1 2 3 4 5 6 7 8 9 10')

	def test_third_example_backward_with_page_tree(self):
		self.assertEqual(paginate(current_page=3, total_pages=10, boundaries=6, around=1), '1 2 3 4 5 6 7 8 9 10')

	def test_third_example_backward_with_page_tree_smaller_boundaries(self):
		self.assertEqual(paginate(current_page=3, total_pages=10, boundaries=3, around=1), '1 2 3 4 ... 8 9 10')

	def test_third_example_with_center_page(self):
		self.assertEqual(paginate(current_page=5, total_pages=10, boundaries=3, around=1), '1 2 3 4 5 6 ... 8 9 10')

	def test_third_example_with_center_page_backward(self):
		self.assertEqual(paginate(current_page=6, total_pages=10, boundaries=3, around=1), '1 2 3 ... 5 6 7 8 9 10')

	def test_third_example_without_around(self):
		self.assertEqual(paginate(current_page=6, total_pages=10, boundaries=3, around=0), '1 2 3 ... 6 ... 8 9 10')

	def test_third_example_without_around_and_right_combiner(self):
		self.assertEqual(paginate(current_page=7, total_pages=10, boundaries=3, around=0), '1 2 3 ... 7 8 9 10')

	def test_forth_example(self):
		self.assertEqual(paginate(current_page=5, total_pages=10, boundaries=0, around=1), '... 4 5 6 ...')

	def test_first_page(self):
		self.assertEqual(paginate(current_page=1, total_pages=10, boundaries=1, around=0), '1 ... 10')

	def test_last_page(self):
		self.assertEqual(paginate(current_page=10, total_pages=10, boundaries=1, around=0), '1 ... 10')
