from mininet.topo import Topo  
from mininet.net import Mininet  
from mininet.node import Node, OVSController, OVSSwitch, OVSKernelSwitch
from mininet.link import TCLink, Link  
from mininet.cli import CLI  
from mininet.log import setLogLevel, info
from mininet.term import makeTerm

  
class LinuxRouter( Node ):  
    "A Node with IP forwarding enabled."  
  
    # pylint: disable=arguments-differ  
    def config( self, **params ):  
        super( LinuxRouter, self).config( **params )  
        # Enable forwarding on the router  
        self.cmd( 'sysctl -w net.ipv4.ip_forward=1' )  
  
    def terminate( self ):  
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )  
        super( LinuxRouter, self ).terminate()  
  
  
class MultiPathTopo(Topo):  
    def build(self):  
  
  
        defaultIP = '192.168.0.1/24'  # IP address for r0-eth1  
        router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )  
  
        s0, s1, s2, s3, s4, s5 = [ self.addSwitch( s ) for s in ( 's0' ,'s1', 's2', 's3', 's4', 's5') ]  
        
        self.addLink( s0, router, intfName2='r0-eth0',  
                      params2={ 'ip' : '192.168.0.1/24' } )  
        self.addLink( s1, router, intfName2='r0-eth1',  
                      params2={ 'ip' : '192.168.1.1/24' } )
        self.addLink( s2, router, intfName2='r0-eth2',  
                      params2={ 'ip' : '192.168.2.1/24' } )
        self.addLink( s3, router, intfName2='r0-eth3',  
                      params2={ 'ip' : '172.16.0.1/12' } )  
        self.addLink( s4, router, intfName2='r0-eth4',  
                      params2={ 'ip' : '10.0.0.1/8' } )
        self.addLink( s5, router, intfName2='r0-eth5',  
                      params2={ 'ip' : '10.0.1.1/8' } )  
  
        h1 = self.addHost( 'h1', ip='192.168.0.100/24',  
                           defaultRoute='via 192.168.0.1' )  
        h2 = self.addHost( 'h2', ip='172.16.0.100/12',  
                           defaultRoute='via 172.16.0.1' )  
        h3 = self.addHost( 'h3', ip='10.0.0.100/8',  
                           defaultRoute='via 10.0.0.1' )  
  
  
        self.addLink(h1, s0, intfName1="h1-eth0", bw=6, delay='4ms')  
        self.addLink(h2, s3, intfName1="h2-eth0", bw=10, delay='1ms')  
        self.addLink(h3, s4, intfName1="h3-eth0", bw=6, delay='1ms')  
  
        self.addLink(h1, s1, intfName1="h1-eth1", bw=6, delay='4ms', params1={ 'ip' : '192.168.1.100/24' })
        self.addLink(h1, s2, intfName1="h1-eth2", bw=6, delay='4ms', params1={ 'ip' : '192.168.2.100/24' })
        self.addLink(h3, s5, intfName1="h3-eth1", bw=6, delay='4ms', params1={ 'ip' : '10.0.1.100/8' })
  
def run():
    "Test linux router"
    topology = MultiPathTopo()  
    net = Mininet( topo=topology,
                   waitConnected=True, link=TCLink)  # controller is used by s1-s3
                  
    net.start()
        
    h1 = net['h1']
    h1.cmd("ip route del default")
    h1.cmd("ip route add default via 192.168.0.1 dev h1-eth0 metric 100")
    h1.cmd("ip route add default via 192.168.1.1 dev h1-eth1 metric 200")
    h1.cmd("ip route add default via 192.168.2.1 dev h1-eth2 metric 300")
    
    h3 = net['h3']
    h3.cmd("ip route del default")
    h3.cmd("ip route add default via 10.0.0.1 dev h3-eth0 metric 100")
    h3.cmd("ip route add default via 10.0.1.1 dev h3-eth1 metric 200")

    # Test connectivity  
    print("Testing connectivity:")  
    net.pingAll()  
    
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r0' ].cmd( 'route' ) )

    h2 = net['h2']
    
    #the appropriate part should be uncommented if needed for live tracking of the interface or the connection
    #h1.cmd('sudo wireshark -i any -k &')
    #h2.cmd('sudo wireshark -i any -k &')
    #h3.cmd('sudo wireshark -i any -k &')
    #h1.cmd('xterm -e bmon &')
    
    h2.cmd('xterm -e ./mnsetup/h2.sh &')
    h3.cmd('SSLKEYLOGFILE=keylog xterm -e ./mnsetup/h3.sh &')
    h1.cmd('SSLKEYLOGFILE=keylog xterm -e ./mnsetup/h1.sh &')

    cli = CLI(net)  # creates the cli for the mininet
    
    # After exiting from the mininet cli, close the xterm, wiresharks and bmons 
    for name in ['h1', 'h2','h3', 'r0']:
        net[name].cmd("killall xterm")
        net[name].cmd("killall wireshark")
        net[name].cmd("killall bmon")
    
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
