import collections

# Below is good for debugging since it has unparsed (raw string) cells C & E
# Minirow = collections.namedtuple('Minirow', 'C, D, E, CP, EP')
Minirow = collections.namedtuple("Minirow", "CP, DP, EP")
MinirowExt = collections.namedtuple("MinirowExt", "CP, DP, EP, next_CP")
