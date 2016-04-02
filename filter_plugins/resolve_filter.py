# Install dependencies:
# apt-get install python-dnspython
import dns.resolver

class FilterModule (object):
  def filters(self):
    return {
      "resolve": self.resolve,
    }

  def resolve(self, hostname, rrtype):
    answers = dns.resolver.query(hostname, rrtype)
    for data in answers:
      return data.address

    raise errors.AnsibleFilterError('unable to get %s record for: %s' % (rrtype, hostname))
