def update(self, logs):

    """
    Updates states of grid cells.
    Args:
        logs: Changes registered in the last iteration.
    Returns:
        gridChanges: Colour changes required for display purposes.
        intersectionPts: Intersection points for sources and destinations.
    """

    # Initialise required variables
    updates = {}
    intersectionPts = set()
    recursiveMode = False
    logs = list(filter(None, logs))
    gridChanges = []
    colorDict = {'free': 0, 'visited': 1, 'waitList': 2}

    if len(logs) == 0:
        return intersectionPts, gridChanges

    if logs[0][2] == 'inRecursion' or logs[0][2] == 'outOfRecursion':
        recursiveMode = True

    # Select just one update entry in case of clashes
    for log in logs:
        agent, cell, state = log
        if cell.type == 'wormholeEntry' or cell.type == 'wormholeExit':
            continue
        if cell not in updates:
            updates[cell] = log
        elif not recursiveMode and state == 'visited' and updates[cell][2] != 'visited':
            updates[cell] = log
        elif recursiveMode and state == 'inRecursion' and updates[cell][2] != 'inRecursion':
            updates[cell] = log

    # Update the cells based on entries selected
    for log in updates.values():
        agent, cell, state = log
        if cell.type != 'source' and cell.type != 'destination':
            cell.type = state
            if recursiveMode:
                if state == 'inRecursion':
                    cell.type = 'visited'
                else:
                    cell.type = 'free'
            gridChange = {'x': cell.location.x,
                            'y': cell.location.y, 'color': colorDict[cell.type]}
            gridChanges.append(gridChange)

        # Place the agents that reached first
        if agent.type == 'source' and cell.srcAgent == None:
            cell.srcAgent = agent

        if agent.type == 'destination' and cell.destAgent == None:
            cell.destAgent = agent

        # Check for intersection points
        if not recursiveMode and state == 'visited' and cell.srcAgent != None and cell.destAgent != None:
            intersectionPts.add(cell)

        if recursiveMode and cell.srcAgent != None and cell.destAgent != None:
            intersectionPts.add(cell)

    return intersectionPts, gridChanges




def idaupdate(self, logs, weight, prevPath):
    updates = {}
    success = set()
    recursiveMode = False
    logs = list(filter(None, logs))
    gridChanges = []
    colorDict = {'free': 0, 'visited': 1, 'waitList': 2}

    if len(logs) == 0:
        return success , gridChanges, []
    
    
    for log in logs:
        agent, cell, state = log
        if cell not in updates:
            updates[cell] = log
        elif not recursiveMode and state == 'visited' and updates[cell][2] != 'visited':
            updates[cell] = log
        elif recursiveMode and state == 'inRecursion' and updates[cell][2] != 'inRecursion':
            updates[cell] = log

    for log in updates.values():
        agent, cell, state = log

        if agent.type == 'source' and cell.srcAgent == None:
            cell.srcAgent = agent

        if agent.type == 'destination' and cell.destAgent == None:
            cell.destAgent = agent

        # if not recursiveMode and state == 'visited' and cell.srcAgent != None and cell.destAgent != None:
        #     success.add(cell)
        if cell.type == 'destination':
            success.add(cell)

        if recursiveMode and cell.srcAgent != None and cell.destAgent != None:
            success.add(cell)
    
    newPath = self.getIDAPath(logs[0][1])
    lenNew = len(newPath)
    lenPrv = len(prevPath)
    itr = 0
    for i in range(min(lenNew, lenPrv)):
        if prevPath[i] != newPath[i]:
            break
        itr += 1
    if prevPath != newPath:
        for i in range(itr, lenPrv):
            gridChange = {'x': prevPath[i]['x'],
                        'y': prevPath[i]['y'], 'color': 0}
            gridChanges.append(gridChange)
        for i in range(lenNew):
            gridChange = {'x': newPath[i]['x'],
                        'y': newPath[i]['y'], 'color': 2}
            gridChanges.append(gridChange)

    if logs[0][2] == 'inRecursion' or logs[0][2] == 'outOfRecursion':
        recursiveMode = True
    
    return success , gridChanges, newPath

def getActivatedCells(self):

    """
    Returns list of activated cells in the environment.
    """

    activatedCells = []
    for row in self.grid:
        for cell in row:
            if cell.type == 'visited' or cell.type == 'waitList':
                activatedCells.append(
                    {'x': cell.location.x, 'y': cell.location.y, 'color': 0})
    return activatedCells

def getActivatedCells_IDA(self, path):

    """
    Returns list of activated cells in the environment during IDA*.
    """
    
    activatedCells = []
    for c in path:
        activatedCells.append(
            {'x': c['x'], 'y': c['y'], 'color': 0})
    return activatedCells
