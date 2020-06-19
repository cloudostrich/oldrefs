from osbrain import run_nameserver
from osbrain import run_agent


if __name__ == '__main__':

    # System deployment
    ns1 = run_nameserver()
    run_agent('Agent0')
    run_agent('Agent1')
    run_agent('Agent2')

    ns2 = run_nameserver()
    run_agent('Agent4')
    run_agent('Agent5')
    run_agent('Agent6')
    # Show agents registered in the name server
    for alias in ns1.agents():
        print('for ns1 {}.'.format(alias))

    for alias in ns2.agents():
        print('for ns2 {}.'.format(alias))

    ns1.shutdown()
    ns2.shutdown()
