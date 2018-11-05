import simpy

if __name__ == '__main__':
    env = simpy.Environment()

    h1 = Host(env, 'Host 1')
    h2 = Host(env, 'Host 2')

    link = Link(env, 10, 64, 10)
    flow = Tahoe(env, h1, h2, 20, 4, 10)

    env.process(link.run())
    env.process(flow.run())

    env.run()
