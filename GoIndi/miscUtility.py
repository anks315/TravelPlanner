
def limitResults(results,type):
    if len(results[type])>15:
        results[type] = results[type][0:15]

    return results