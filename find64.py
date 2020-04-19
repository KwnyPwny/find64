import re, argparse, base64, csv, sys


logo = '''  __ _           _  ____    ___
 / _(_)         | |/ ___|  /   |
| |_ _ _ __   __| / /___  / /| |
|  _| | '_ \ / _` | ___ \/ /_| |
| | | | | | | (_| | \_/ |\___  |
|_| |_|_| |_|\__,_\_____/    |_/  https://github.com/KwnyPwny/find64'''


class B64Sequence():
	def __init__(self, start, end, data, stripped_start, stripped_end, stripped_data):
		self.start = start
		self.end = end
		self.length = end - start
		self.data = data

		self.stripped_start = stripped_start
		self.stripped_end = stripped_end
		self.stripped_length = stripped_end - stripped_start
		self.stripped_data = stripped_data

		self.stripped = not (self.stripped_length == self.length)

		self.decoded_stripped_data = []
		for o in range(4):
			o_end = self.stripped_length - (self.stripped_length - o) % 4
			self.decoded_stripped_data.append({'offset_end':o_end, 'data':base64.b64decode(stripped_data[o:o_end], bytes(args.s, 'utf-8'))})


def detect_whitespaces(binary):
	whitespace_iter = re.finditer(b'\s+', binary)
	whitespaces = []
	for w in whitespace_iter:
		whitespaces.append(w)
	return whitespaces


def detect_b64_sequences(stripped_binary, min_length, special_characters):
	min_reps = str(min_length - 4)
	charset = '[A-Za-z0-9' + re.escape(special_characters) + ']'
	regex_pattern = bytes(charset + '{' + min_reps + ',}(?:' + charset + '{2}==|' + charset + '{3}=|' + charset + '{4})', 'utf-8')
	return re.finditer(regex_pattern, stripped_binary)


def calculate_span(stripped_span, whitespaces):
	start, end = stripped_span
	for w in whitespaces:
		w_start, w_end = w.span()
		w_length = w_end - w_start
		if w_end <= start:
			# Whitespaces before sequence
			start += w_length
			end += w_length
		else:
			if w_start >= end:
				# Whitespaces behind sequence
				break
			else:
				# Whitespaces inside sequence
				if w_start == start:
					start += w_length
				end += w_length
	return start, end


def print_results_CSV(results):
	csvwriter = csv.writer(sys.stdout)
	if len(args.offsets) > 0:
		csvwriter.writerows([[i, result.start, result.end, result.length, result.stripped, result.length - result.stripped_length, result.stripped_data] + [result.decoded_stripped_data[o]['data'] for o in args.offsets] for i, result in enumerate(results)])
	else:
		csvwriter.writerows([[i, result.start, result.end, result.length, result.stripped, result.length - result.stripped_length, result.stripped_data] for i, result in enumerate(results)])


def print_results(results):
	for i, result in enumerate(results):
		print()
		print('Match #{}:'.format(i))
		print('  Start: {}  End: {}  Length: {}'.format(result.start, result.end, result.length))
		if result.stripped:
			print('  Stripped: True (by {} bytes)'.format(result.length - result.stripped_length))
		else:
			print('  Stripped: False')
		print('  Shell command: tail -c {} {} | head -c {}'.format(binary_len - result.start, args.file, result.length))
		print('  Stripped Data: {}'.format(result.stripped_data))
		if len(args.offsets) > 0:
			print('  Decoded Data:')
			for o in args.offsets:
				dsd = result.decoded_stripped_data[o]
				print('    [{}:{}]: {}'.format(o, dsd['offset_end'], dsd['data']))


def parse():
	parser = argparse.ArgumentParser(description='This tool parses files for base64 strings. Whitespaces, which are often used within base64 strings, are stripped during extraction.')
	parser.add_argument('file', help='The file to parse for base64.')
	parser.add_argument('-n', help='The minimum length for a base64 string to be returned. Default 16.', type=int, default=16)
	parser.add_argument('-s', help='The special characters the base64 string consists of. Default `+/`. Urlsafe `-_`. Order matters.', default='+/')
	parser.add_argument('-d', help='Decode the detected base64 string.', default='', const='0123', nargs='?')
	parser.add_argument('-c', help='Output results as CSV.', action='store_true')
	args = parser.parse_args()
	if args.n < 4:
		parser.error('The minimum length for a base64 string is 4.')
	if len(args.d) > 4:
		parser.error('d takes at most 1 parameter with a maximum length of 4.')
	args.offsets = []
	for v in args.d:
		if v not in '0123':
			parser.error('the parameter of d may only consist of the characters 0, 1, 2, and 3.')
		if int(v) in args.offsets:
			parser.error('the parameter of d may not contain identical characters.')
		args.offsets.append(int(v))
	return args


if __name__ == '__main__':
	args = parse()
	if not args.c:
		print(logo)

	with open(args.file, 'rb') as f:
		binary = f.read()

	binary_len = len(binary)

	whitespaces = detect_whitespaces(binary)
	stripped_binary = re.sub(b'\s+', b'', binary)
	b64_sequences = detect_b64_sequences(stripped_binary, args.n, args.s)

	results = []

	for seq in b64_sequences:
		stripped_start, stripped_end = seq.span()
		start, end = calculate_span(seq.span(), whitespaces)
		results.append(B64Sequence(start, end, binary[start:end].decode('utf-8'), stripped_start, stripped_end, stripped_binary[stripped_start:stripped_end].decode('utf-8')))

	if args.c:
		print_results_CSV(results)
	else:
		print_results(results)
