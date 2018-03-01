
from pprint import pprint

s  = """When registering to neighboring
slicesbasedonthecomputeddeformationfromtwo
adjacent chest regions, the outline and the landmarks
were simultaneously deformed and used to extract the
breast region of the neighboring slice. Based on the
high similarity between the two adjacent slices, the
procedure above could be propagated to each two
adjacent slices from midd
le transverse slice to the"""
s = s.replace("-\n", "")
s = s.replace("[\n", "[")
s = s.replace("\n]", "]")
s = s.replace("\n", " ")
pprint(s)
# L = []
# for x in s.split():
#     L.append(x)
#
# print(" ".join(L))

