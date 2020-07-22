from agent import Agent
from environment.env import Environment
from environment.utils import Location


def nonCheckpointMode(config):

    """
    Simulates path-finding in multistart and multidestination mode.
    Args:
        config: Dictionary with all the configuration settings.
    Returns:
        output: Final path taken and list of changes on the grid.
    """

    # Extract all the sources and destinations from congig
    sources = []
    destinations = []

    for source in config['start']:
        sources.append(Agent(Location(source['x'], source['y']), 'source'))
    for destination in config['stop']:
        destinations.append(Agent(Location(destination['x'], destination['y']), 'destination', int(config['biDirectional'])))

    for checkpoint in config['checkpoints']:
        if int(config['multistart'])==1:
            sources.append(Agent(Location(checkpoint['x'], checkpoint['y']), 'source', True))
        else:
            destinations.append(Agent(Location(checkpoint['x'], checkpoint['y']), 'destination', int(config['biDirectional'])))

    # Initialise the environment
    env = Environment(config, sources + destinations)

    gridChanges = []
    path = []
    algo = int(config['algo'])
    
    # For all algorithms other than IDA*
    if algo != 6 and algo != 7:

        # Run till a path is found
        while True:
            logs = []

            # Run the correct algorithm for all the movable agents and log the changes
            for agent in sources + destinations:
                targets = destinations if agent in sources else sources
                if agent.isMovingAgent: 
                    if algo == 0:
                        agent.aStar(env, targets)
                    if algo == 1:
                        agent.staticAStar(env, targets, float(config['relaxation']))
                    if algo == 2:
                        agent.dynamicAStar(env, targets, float(config['relaxation']), 1000)
                    if algo == 3:
                        agent.beamSearch(env, targets, int(config['beamWidth']))
                    if algo == 4:
                        agent.bestFirstSearch(env, targets)
                    if algo == 5:
                        agent.breadthFirstSearch(env)
                    if algo == 8:
                        agent.depthFirstSearch(env)
                    if algo == 9:
                        agent.dijkstra(env)
                    if algo == 10:
                        agent.jumpPointSearch(env, targets)
                    if algo == 11:
                        agent.uniformCostSearch(env)
                    logs.extend(agent.logs)

            # Update grid and check for intersection points
            intersectionPts, gridChange = env.update(logs)
            gridChanges.extend(gridChange)

            # If intersection point found, get final path and break
            if len(intersectionPts) > 0:
                intersectionPt = intersectionPts.pop()
                if algo == 10:
                    path = env.getJpsPath(intersectionPt)
                else:
                    path = env.getPath(intersectionPt)
                break

            # If no changes being registered, break
            if len(logs) == 0:
                break
        
        # Get currently activated cells for grid cleanup, and return output
        activatedCells = env.getActivatedCells()
        output = {'gridChanges': gridChanges,
                  'path': path, 'activatedCells': activatedCells}
        return output

    # Driver for IDA*
    else:
        threshold = env.bestHeuristic(sources[0], destinations)
        newThreshold = 50000         # Large Value
        itrCount = 0                 # IterationCount is necessary for tle
        prevPath = []
        while True and itrCount < 1000:
            logs = []
            for src in sources:
                if algo == 6:
                    X, Y = src.ida(env, threshold, destinations)
                if algo == 7:
                    X, Y = src.idaStar(env, threshold, destinations)
                logs.extend(src.logs)
                if X > threshold :
                    newThreshold = min(X, newThreshold)
                else:
                    intersectionPts, gridChange, prevPath = env.idaUpdate(logs, Y, prevPath)        
            gridChanges.extend(gridChange)
            if len(intersectionPts) > 0:
                intersectionPt = intersectionPts.pop()
                path = env.getIDAPath(intersectionPt)
                break
            if len(src.logs) == 0 and len(sources[0].waitList) == 0:
                if newThreshold == 50000:     # No Path exists
                    break
                threshold = newThreshold
                itrCount += 1
                newThreshold = 50000
                for agent in sources + destinations:
                    agent.visited.clear()
                    agent.waitList = None
                    agent.path = {}
                    agent.logs = []
                    agent.distances = {}

        activatedCells = env.getActivatedCells_IDA(path)
        # print(path)
        output = {'gridChanges': gridChanges,
                  'path': path, 'activatedCells': activatedCells}
        # print(gridChanges)
        return output
