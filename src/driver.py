from agent import Agent
from environment.env import Environment
from environment.utils import Location

# Create environment
env = Environment(10, 10)
sources = [Agent(Location(1, 3), 'source')]
destinations = [Agent(Location(4, 0), 'destination', False)]
for agent in sources + destinations:
    env.placeAgent(agent)

# walls = env.recursiveMaze()
# env.randomizedPrim()

# env.printInitial()
# env.grid[2][2].type = 'wall'
# env.grid[2][3].type = 'wall'
# env.grid[2][1].type = 'wall'
# env.grid[2][0].weight = 100

while True:
    logs = []
    for src in sources:
        # src.dijkstra(env)
        # src.bestFirstSearch(env, destinations)
        src.aStar(env, destinations)
        logs.extend(src.logs)
    for dest in destinations:
        if dest.isMovingAgent:
            # dest.dijkstra(env)
            # dest.bestFirstSearch(env, sources)
            src.aStar(env, sources)
            logs.extend(dest.logs)
    success = env.update(logs)
    env.print()
    if len(success) > 0:
        paths = env.getPaths(success)
        print('Paths:', paths)
        break
    if len(src.logs) == 0 and len(dest.logs) == 0:
        break
