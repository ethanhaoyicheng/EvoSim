# EvoSim
An evolutionary simulator, built in Python (2025-present)

Current priorities:
- Fix bottleneck from animas' detection (for water and other animas), which currently runs on O(n^2) time and scales badly at the >1k range (In progress - 50%)
- Implement stats and records page with intuitive and user-friendly UI (In progress - 20%)  

Progress percentages are estimates

Future targets:
- Implement neural networks, memory systems, and further sensory/decision capabilities for animas
- Implement more realistic natural terrain (and possibly raycasting for realistic light response)
- Implement threading as an optimisation
- Add self-composed music
- Add dynamic art for animas, for aesthetic and (importantly) communication purposes, ie. a fast anima should be identifiable from a group of slow animas


Notes:
- Distance is currently calculated from the centre of objects. A more 'realistic' approach would be to subtract the radii of each cell in the calculation to get surface-surface distance. This would not be difficult to implement. The current philosophy which justifies NOT implementing this is that all animas are logic-wise of equal size relative to the much larger world, ie. in a large savannah biome, the difference in size between an elephant and lizard does not account for much when vision generally extends well beyond either's size scope. Animas seem to travel very fast across the biome because each simulation tick can represent multiple minutes/hours. The difference in size in the GUI of animas is only to the benefit of the user, and logic-wise cells should still be treated as effectively equal 1D points.
- How long is the interval of time represented by a tick?
