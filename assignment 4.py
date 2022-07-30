def most_frequent(string):
  d = dict()
  for key in string:
    if key not in d:
      d[key] = 1
    else
      d[key] += 1
  return d

print most_frequent('Mississippi')

output
m = 01
p = 02
i = 04
s = 04
