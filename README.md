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
- Distance is currently calculated from the centre of objects.  
  A more 'realistic' approach would be to subtract the radii of each cell in the calculation to get surface-surface distance. This would not be difficult to implement. The current philosophy which justifies NOT implementing this is that all animas are logic-wise of equal size relative to the much larger world, ie. in a large savannah biome, the difference in size between an elephant and lizard does not account for much when vision generally extends well beyond either's size scope. Animas seem to travel very fast across the biome because each simulation tick can represent multiple minutes/hours. The difference in size in the GUI of animas is only to the benefit of the user, and logic-wise cells should still be treated as effectively equal 1D points. (This all also saves complexity on the spatial hash!)
- How long is the interval of time represented by a tick?  
  Currently all animas die after a blanket 500 ticks of no water, from a starting point of minimum thirst. The average lifespan, hunger rate, and sleepiness rate is dependent on their total energy consumption, but it is worth noting that the time it takes to die of starvation is roughly three times the length of the time it takes to exhaust into sleep (the two calculations are scalars of each other). So, we can from the water example, and using humans as a template, we can estimate 10 ticks = 1 hr and 1 tick = 6min. However, if we take the exhaustion timer to be the equivalent of 36hr (a somewhat arbitrary figure which corresponds to when humans begin to experience hallucination after a no-sleep period of that length), then, inputting also arbitrary figures into the energy parameters to give a 5.85 energy cost multiplier, we receive the result that 36hr = 136.75 ticks, 1hr = 3.8 ticks and 1min = 0.063 ticks. Then 1 tick becomes 15.795 minutes. If we take the exhaustion timer to symbolise a day, matching normal circadian rhythm, then that 1 tick is around 10.5 minutes. So with these various methods we have an estimate for how much time a tick represents- some value which we can somewhat arbitrarily understand as between 6 and 16 minutes. And an hour is somewhere between 4 and 10 ticks in length.

- Where is my notes.txt? Should locate through KEGS Cloud
