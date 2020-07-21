from modes.nonCheckpointMode import nonCheckpointMode

def checkpointMode(config):

    """
    Simulates path-finding in checkpoint mode.
    Args:
        config: Dictionary with all the configuration settings.
    Returns:
        output: Final path taken and list of changes on the grid.
    """

    # Extract points to be visited in order.
    points = []
    for point in config['start']:
        points.append(point)
    for point in config['checkpoints']:
        points.append(point)
    for point in config['stop']:
        points.append(point)

    gridChanges = []
    path = []
    config['checkpoints'] = []

    # Iterate over all checkpoints
    for i in range(len(points)-1):

        # Treat each checkpoint as a destination in non-checkpoint mode
        config['start'] = [points[i]]
        config['stop'] = [points[i+1]]
        result = nonCheckpointMode(config)
        gridChanges.extend(result['gridChanges'])

        # Break if no path is found
        if len(result['path']) == 0:
            break
        else:
            path.extend(result['path'])

            # Clear the grid only if checkpoints present
            if(len(points) > 2):
                gridChanges.extend(result['activatedCells'])

            # To remove repeated points in path
            if i < len(points)-2:
                path.pop()

    output = {'gridChanges': gridChanges, 'path': path}
    return output
