from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class StpTopology(Topo):
  "Simple topology example."
  def __init__(self):
    "Create custom topo."
    # Initialize topology
    Topo.__init__(self)
    # Ad hosts and switches
    b1=self.addHost('b1', ip = '10.0.0.1/24')
    b2=self.addHost('b2', ip = '10.0.0.2/24')
    b3=self.addHost('b3', ip = '10.0.0.3/24')
    b4=self.addHost('b4', ip = '10.0.0.4/24')
    centralSwitch=self.addSwitch('s1')
    # Add links
    self.addLink(b1,centralSwitch)
    self.addLink(b2,centralSwitch)
    self.addLink(b3,centralSwitch)
    self.addLink(b4,centralSwitch)
    #print("added link")

#if __name__ == '__main__':
    # Start mininet
#    net = Mininet(StpTopology())
#    net.start()
#    print('started net')
#    # Get host references
#    b1 = net.get('b1')
#    b2 = net.get('b2')
#    b3 = net.get('b3')
#    b4 = net.get('b4')
#    print('got references')
#    # Invoke protocol.py calls on each host   
#    b1.cmd('python protocol.py')
#    b2.cmd('python protocol.py')
#    b3.cmd('python protocol.py')
#    b4.cmd('python protocol.py')
#    net.stop()

topos={'stpTopology': (lambda: StpTopology() ) }
