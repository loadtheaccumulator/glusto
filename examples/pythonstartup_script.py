from glusto.core import Glusto as g

print "Python startup starting"
config = g.load_config('examples/systems.yml')
rcode, uname_info, rerr = g.run(config['nodes'][0], 'uname -a')
print "Python startup complete"
