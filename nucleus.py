def random_direction(r_max):
    theta = random.uniform(0, TAU)
    r = random.uniform(0, r_max)
    return UP * r * np.sin(theta) + RIGHT * r * np.cos(theta)  

class Nucleus(VGroup):

    def __init__(self, size=238):
        VGroup.__init__(self)
        self.size = size

        for i in range(0,size):
            proton = random.choice([True, False])
            if proton:
                self.add(Proton(color = BLACK, fill_color=RED_E, fill_opacity=1).move_to(random_direction(size/300)))
            else:
                self.add(Neutron(color = BLACK, fill_color=BLUE_E, fill_opacity=1).move_to(random_direction(size/300))
