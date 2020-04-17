import re, argparse


logo = '''  __ _           _  ____    ___
 / _(_)         | |/ ___|  /   |
| |_ _ _ __   __| / /___  / /| |
|  _| | '_ \ / _` | ___ \/ /_| |
| | | | | | | (_| | \_/ |\___  |
|_| |_|_| |_|\__,_\_____/    |_/  https://github.com/KwnyPwny/find64'''


class B64Sequence():
	def __init__(self, start, end, real_start, real_end):
		self.start = start
		self.end = end
		self.length = end - start
		self.real_start = real_start
		self.real_end = real_end
		self.real_length = real_end - real_start
		self.stripped = not (self.length == self.real_length)


def detect_whitespaces(binary):
	whitespace_iter = re.finditer(b'\s+', binary)
	whitespaces = []
	for w in whitespace_iter:
		whitespaces.append(w)
	return whitespaces


def detect_b64_sequences(binary, min_length, special_characters):
	min_repititions = str(min_length - 4)
	all_characters = '[A-Za-z0-9' + re.escape(special_characters) + ']'
	regex_pattern = bytes(all_characters + '{' + min_repititions + ',}(?:' + all_characters + '{2}==|' + all_characters + '{3}=|' + all_characters + '{4})', 'utf-8')
	return re.finditer(regex_pattern, binary_stripped)


def calculate_real_span(span, whitespaces):
	real_start, real_end = span
	for w in whitespaces:
		w_start, w_end = w.span()
		w_length = w_end - w_start
		if w_end <= real_start:
			# Whitespaces before sequence
			real_start += w_length
			real_end += w_length
		else:
			if w_start >= real_end:
				# Whitespaces behind sequence
				break
			else:
				# Whitespaces inside sequence
				if w_start == real_start:
					real_start += w_length
				real_end += w_length
	return real_start, real_end


def print_results_CSV(results, binary, binary_stripped):
	for i, result in enumerate(results):
		print('{},{},{},{},{},{},{}'.format(i, result.real_start, result.real_end, result.real_length, result.stripped, result.real_length - result.length, binary_stripped[result.start:result.end].decode('utf-8')))


def print_results(results, binary, binary_stripped):
	for i, result in enumerate(results):
		print()
		print('Match #{}:'.format(i))
		print('  Start: {}  End: {}  Length: {}'.format(result.real_start, result.real_end, result.real_length))
		if result.stripped:
			print('  Stripped: True (by {} bytes)'.format(result.real_length - result.length))
		else:
			print('  Stripped: False')
		print('  Shell command: tail -c {} {} | head -c {}'.format(len(binary) - result.real_start, args.file, result.real_length))
		print('  Stripped Data: {}'.format(binary_stripped[result.start:result.end].decode('utf-8')))


def parse():
	parser = argparse.ArgumentParser(description='This tool parses files for base64 strings. Whitespaces, which are often used within base64 strings, are stripped during extraction.')
	parser.add_argument('file', help='The file to parse for base64.')
	parser.add_argument('-n', help='The minimum length for a base64 string to be returned. Default 16.', type=int, default=16)
	parser.add_argument('-s', help='The special characters the base64 string consists of. Default \'+/\'.', default='+/')
	parser.add_argument('-c', help='Output results as CSV.', action='store_true')
	args = parser.parse_args()
	if args.n < 4:
		parser.error('The minimum length for a base64 string is 4.')
	return args


if __name__ == '__main__':
	args = parse()
	if not args.c:
		print(logo)

	with open(args.file, 'rb') as f:
		binary = f.read()

	whitespaces = detect_whitespaces(binary)
	binary_stripped = re.sub(b'\s+', b'', binary)
	b64_sequences = detect_b64_sequences(binary, args.n, args.s)

	results = []

	for seq in b64_sequences:
		start, end = seq.span()
		real_start, real_end = calculate_real_span(seq.span(), whitespaces)
		results.append(B64Sequence(start, end, real_start, real_end))

	if args.c:
		print_results_CSV(results, binary, binary_stripped)
	else:
		print_results(results, binary, binary_stripped)
