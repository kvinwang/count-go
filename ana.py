#!/usr/bin/env python
import sys
from collections import defaultdict


def is_f_dec(line):
	line = line.strip()
	return line.startswith('static') and line.endswith(';') and '(' in line

def is_f_def(line):
	line = line.strip()
	return line.startswith('static') and not line.endswith(';') and '(' in line

def is_f_enddef(line):
	return line.startswith('}')

def count_line(f, cond_filter):
	state = 'out'	
	count = 0
	total = 0
	should_count = False
	for line in f:
		if state == 'out':
			if is_f_def(line):
				state = 'in'
				should_count = cond_filter(line)
		elif state == 'in':
			if is_f_enddef(line):
				state = 'out'
			else:
				total += 1
				if should_count:
					count += 1
	return count, total

def get_fname(line):
	arr = line.split()
	for t in arr:
		if '(' in t:
			return t.split('(')[0]
	assert False

def prefix_with(prefix):
	def f(line):
		return get_fname(line).startswith(prefix)
	return f

def get_key(line):
	arr = get_fname(line).split('_')
	arr = filter(bool, arr)
	n = 1
	if arr[0] == 'runtime':
		n = 2
	return '_'.join(arr[:n])

def count_all(f):
	state = 'out'	
	total = 0
	counters = defaultdict(lambda: [0])
	counter = []
	for line in f:
		if state == 'out':
			if is_f_def(line):
				state = 'in'
				counter = counters[get_key(line)]
		elif state == 'in':
			if is_f_enddef(line):
				state = 'out'
			else:
				total += 1
				counter[0] += 1
	return counters, total


if __name__ == '__main__':
	f = open(sys.argv[1])

	counters, total = count_all(f)

	fmt = "%-{}s: %.3f%%".format(max([len(k) for k in counters]) + 1)
	for k, v in sorted(counters.items(), key=lambda i: i[1]):
		percent = float(v[0])/total * 100
		print(fmt % (k, percent))

	f = open(sys.argv[1])
	def is_gc(line):
		fname = get_fname(line).lower()
		return 'gc' in fname or 'sweep' in fname or 'mark' in fname
 	count, total = count_line(f, is_gc)
	print("gc at least %.3f%%" % (float(count) / total * 100))

