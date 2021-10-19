from collections import defaultdict
class BusRoute:
    def __init__(self) -> None:
        self.busNames = []
        self.nameMappings = {}
        self.idMappings = {}
        self.busCount = 0
        self.busRoutes = []
        self.adj = defaultdict(list)

    def addBus(self,name,route):
        self.busNames.append(name)
        self.busRoutes.append(set(route))
        self.nameMappings[self.busCount] = name
        self.idMappings[name] = self.busCount
        
        #establish an edge between two buses if they have a common stopping
        for i in range(self.busCount):
            if self.busRoutes[i] & self.busRoutes[-1]:
                self.adj[i].append(self.busCount)
                self.adj[self.busCount].append(i)
        self.busCount += 1

        
    def numBusesToDestination(self, source , target) -> int:
        #if is the source and destination are same you need not board any bus
        if source == target:
            return 0

        #enqueue queue with all the buses that have the source as one of the stopping
        queue = []
        visited = set()
        for i in range(self.busCount):
            if source in self.busRoutes[i]:
                if target in self.busRoutes[i]:
                    #if source and destination could be reached by a single bus
                    return 1 
                queue.append(i)
                visited.add(i)
        
        #if no bus passes through the source
        if len(queue) == 0:
            return -1
        
        #BFS
        busesBoarded = 1
        while queue:
            size = len(queue)
            for i in range(size):
                busId = queue.pop(0)
                if target in self.busRoutes[busId]:
                    return busesBoarded
                for bus in self.adj[busId]:
                    if bus not in visited:
                        queue.append(bus)
                        visited.add(bus)
            busesBoarded += 1
        return -1
    
    #dfs
    def takeBuses(self,source,destination):
        if source == destination:
            return []
        
        possibleBoardings = []
        visited = set()
        def dfs(busId,sofar):
            if destination in self.busRoutes[busId]:
                possibleBoardings.append(sofar+[self.nameMappings[busId]])
                return
            
            visited.add(busId)
            for bus in self.adj[busId]:
                if bus not in visited:
                    dfs(bus,sofar+[self.nameMappings[busId]])
            visited.remove(busId)
        
        for i in range(self.busCount):
            if source in self.busRoutes[i]:
                dfs(i,[])
        
        minShifts = len(possibleBoardings[0])
        buses = possibleBoardings[0]
        for i in possibleBoardings:
            temp = len(i)
            if temp<minShifts:
                minShifts = temp
                buses = i
        return buses

        
    def shiftsAt(self,buses):
        nBuses = len(buses)
        locations = []
        for i in range(nBuses-1):
            idx1,idx2 = self.idMappings[buses[i]],self.idMappings[buses[i+1]]
            locations.append(list(self.busRoutes[idx1] & self.busRoutes[idx2])[0])
        return locations




        
        
        