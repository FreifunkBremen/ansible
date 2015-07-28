import re

def ntuples(lst, n):
    return zip(*[lst[i::n] for i in range(n)])

class FilterModule(object):
    def filters(self):
        return {
            "derive_mac_addr": self.derive_mac_addr
        }

    def derive_mac_addr(self, original, offset):
        if not re.match('^(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}|([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4})$', original):
            raise Exception("Not a MAC address: %s" % original)

        splitbytes = [int("".join(x), 16) for x in ntuples(re.sub('[^0-9a-fA-F]', '', original), 2)]
        splitbytes[0] |= 2
        splitbytes[-1] += offset
        return ':'.join('%02x' % x for x in splitbytes)

if __name__ == '__main__':
    instance = FilterModule()
    for orig in ('00:00:00:00:00:00', '02:00:00:00:00:00', '0000.0000.0000'):
        derived = instance.derive_mac_addr(orig, 2)
        assert derived == '02:00:00:00:00:02', derived
