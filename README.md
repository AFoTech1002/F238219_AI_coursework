# COA207 Route Finding - BFS, UCS and A*

This project implements three classical search algorithms for route finding on a weighted graph of UK cities:

- BFS - finds the fewest-hop path
- UCS - finds the lowest-distance path
- A* - finds the lowest-distance path using a straight-line heuristic


## Main result

| Algorithm | Nodes Expanded | Cost | Path |
|---|---:|---:|---|
| BFS | 12 | 449 mi | London -> Cambridge -> Sheffield -> Leeds -> Newcastle -> Edinburgh |
| UCS | 12 | 440 mi | London -> Oxford -> Birmingham -> Sheffield -> Leeds -> Newcastle -> Edinburgh |
| A* | 9 | 440 mi | London -> Oxford -> Birmingham -> Sheffield -> Leeds -> Newcastle -> Edinburgh |

BFS finds the route with the fewest hops, but it is not distance optimal. UCS and A* both find the lowest-distance route. A* expands fewer nodes than UCS because the heuristic guides the search toward Edinburgh.

The Cambridge -> Sheffield edge is set to 160 miles. This was adjusted to create a meaningful comparison where BFS and cost-based search return different routes.
