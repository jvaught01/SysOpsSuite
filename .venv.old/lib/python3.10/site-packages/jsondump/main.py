import json
import inspect

FuncFlag = '_$$ND_FUNC$$_'
CircularFlag = '_$$ND_CC$$_'
KeyPathSeparator = '_$$.$$_'

def getKeyPath(obj, path):
    path = path.split(KeyPathSeparator)
    currentObj = obj
    for i, val in enumerate(path):
        if i > 0:
            currentObj = currentObj[val]
    return currentObj


def dumps(obj, ignoreNativeFunc=False, outputObj=None, cache=None, path=''):
    path = path or '$'
    cache = cache or {}
    cache[path] = obj
    outputObj = outputObj or {}

    for key in obj:
        if obj.get(key) != None:
            if type(obj[key]) is dict and obj[key] != None:
                outputObj[key] = {}
                found = False
                for subKey in cache:
                    if cache.get(subKey) != None:
                        if cache[subKey] == obj[key]:
                            outputObj[key] = CircularFlag + subKey
                            found = True
                if found == False:
                    outputObj[key] = dumps(obj[key], ignoreNativeFunc, outputObj[key], cache, path + KeyPathSeparator + key)
            elif callable(obj[key]):
                funcName = obj[key].__name__
                funcStr = inspect.getsource(obj[key])
                outputObj[key] = FuncFlag + funcName + FuncFlag + funcStr;
            else:
                outputObj[key] = obj[key]

    if path == '$':
        ret = json.dumps(outputObj, separators=(',', ':'))
        return ret
    else:
        return outputObj

def loads(obj, originObj=None):
    isIndex = False
    if type(obj) is str:
        obj = json.loads(obj)
        isIndex = True

    originObj = originObj or obj
    circularTasks = []
    for key in obj:
        if obj.get(key) != None:
            if type(obj[key]) is dict:
                obj[key] = loads(obj[key], originObj)
            elif type(obj[key]) is str:
                if obj[key].find(FuncFlag) == 0:
                    funcStr = obj[key][len(FuncFlag):]
                    nameIndex = funcStr.find(FuncFlag)
                    if nameIndex > 0:
                        funcName = funcStr[:nameIndex]
                        funcStr = funcStr[nameIndex + len(FuncFlag):]
                        exec(funcStr, globals())
                        obj[key] = globals()[funcName]
                    else:
                        obj[key] = None
                elif obj[key].find(CircularFlag) == 0:
                    obj[key] = obj[key][len(CircularFlag):]
                    circularTasks.append({obj: obj, key: key})
    if isIndex == True:
        for task in circularTasks:
            task.obj[task.key] = getKeyPath(originObj, task.obj[task.key])

    return obj