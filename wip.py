"""def generate_pool(self, cx, cy, radius, type, shapetype):
        #using parametric polar curves to generate curved pools of varying shape

        angle_start = random.randint(0, POOL_ANGLE_GRADATION)
        r = radius
        pool_points = []
        maxr = 0
        velocity = 0
        acceleration = random.uniform(-0.5, 0.5)
        for u_theta in range (POOL_ANGLE_GRADATION):
            normalising_factor = 2 * PI / POOL_ANGLE_GRADATION
            n_theta = u_theta * normalising_factor
            t = (angle_start + u_theta) * normalising_factor

            #velocity += random.uniform(-1, 1) * sin(t)

            if random.random() < 0.1:
                acceleration = random.uniform(-0.5, 0.5)

            velocity += acceleration
            velocity *= 0.975
            if shapetype == "rounded":
                r = max(r + velocity, 1) 
            elif shapetype == "flattened":
                r = max(r * cos(t) + random.uniform(-2, 2) * sin(t), 1)  
            # -> collect points using rsintheta and rcostheta
            if r > maxr:
                maxr = r
            pool_points.append((cx + r*cos(n_theta), cy + r*sin(n_theta)))
            #print(theta)
        for point in pool_points:
            #print(point)
            if 0 <= point[0] < self.width and 0 <= point[1] < self.height:
                self.environment[int(point[1])][int(point[0])] = terrain_index[type]  #temporary code, need fill in            possible solution: keep choosing adjacent tile closest to next (polar?) function result until back to original tile, then closed object can be easily filled in using edge of pool as boundaries for fill in, for each row start filling in when reach one and stop when reach next, but need to cover edge cases of pools that go off map, cant then use polarity, so how?
                #print((int(point[0]), int(point[1])))
        # -> draw inside polygon of points, checking for edge of world
        centre = Cell(self, cx, cy)
        maxr = int(maxr+1)
        for row in range(cy-maxr, cy + maxr+1):
            for col in range(cx-maxr, cx + maxr+1):
                if 0 <= col < self.width and 0 <= row < self.height:
                    cell = Cell(self, col, row)
                    arg = centre.angle_to(cell)
                    u_theta = arg / normalising_factor
                    p1 = pool_points[floor(u_theta)]
                    p2 = pool_points[ceil(u_theta % (2*PI))]
                    d1 = centre.distance_to(p1)
                    d2 = centre.distance_to(p2)
                    lerpdist = d1 + (d2-d1) * (u_theta-floor(u_theta))
                    if cell.is_within(centre, lerpdist):
                        self.environment[row][col] = terrain_index[type]
                        #print((col,row))

        #fill in with terrain_index[type]
        
"""
