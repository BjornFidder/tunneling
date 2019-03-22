class WaveFunction(GraphScene):

    CONFIG = {
        "x_min": 0,
        "x_max": 12,
        "x_axis_label" : "$x$",
        "x_axis_label_direction" : DOWN + RIGHT,
        "y_min" : -6,
        "y_max" : 6,
        "y_axis_label" : "$\\psi(x)$",
        "graph_origin" : 4.5*LEFT,
        "num_graph_anchor_points": 1500,
    }

    def construct(self):
        self.setup_axes(animate=True)

        self.x_start_barrier = 4
        self.x_end_barrier = 5

        start_barrier = DashedLine(
            self.coords_to_point(self.x_start_barrier, self.y_min), 
            self.coords_to_point(self.x_start_barrier, self.y_max), 
            color=GRAY,
            )
        end_barrier = DashedLine(
            self.coords_to_point(self.x_end_barrier, self.y_min),
            self.coords_to_point(self.x_end_barrier, self.y_max),
            color=GRAY,
            )
            
        barrier = VGroup(start_barrier, end_barrier)
        

        nucleus_dummy = Nucleus()
        nucleus = Nucleus().scale(0.5)
        alpha_particle = Alpha_Particle().shift(0.35*RIGHT).scale(0.5)
        alpha_in_nucleus = VGroup(nucleus, alpha_particle)
        alpha_in_nucleus.shift(3*LEFT+3*UP)
        
        #Standing wave
        self.wait()
        self.update_graph=False
        self.tunnel_probability = 0.2
        standing_wave = WaveFunctionGraph(self, self.x_min, self.x_start_barrier, plot=False)
        standing_wave_simple = standing_wave.get_graph()
        self.play(FadeIn(standing_wave_simple))
        self.wait(3)
    
        probability_standing_wave = standing_wave.get_graph_squared()
        self.play(Transform(standing_wave_simple, probability_standing_wave))
        self.wait(3)
        self.play(Transform(standing_wave_simple, standing_wave.get_graph()))
        
        self.play(ShowCreation(barrier))
        self.wait()
        self.play(GrowFromCenter(alpha_in_nucleus))
        
        self.update_graph=False
        self.tunnel_probability = 0.2
        standing_wave = WaveFunctionGraph(self, self.x_min, self.x_start_barrier)
        self.add(standing_wave)
        self.play(FadeOut(standing_wave_simple))
        self.wait(5)
        
        #Standing
        self.update_graph = True
        self.wait(4)
        
        #Stop standing
        self.update_graph = False
        self.wait(3)
        standing_wave.remove()
    
        #Full graph
        graph = WaveFunctionGraph(self, self.x_min, self.x_max)
        self.add(graph)
        self.wait(2)
        
        #Move full graph
        self.update_graph = True
        self.wait(22)
        
        #Stop moving full graph
        self.update_graph = False
        self.wait(4)

        #Extend barrier
        self.x_end_barrier = 5.2
        self.tunnel_probability = 0.1
        graph2 = WaveFunctionGraph(self, self.x_min, self.x_max, plot=False)
        self.play(ApplyMethod(end_barrier.shift, 0.2*RIGHT))
        self.wait(2)
        self.play(ApplyMethod(end_barrier.shift, 0.2*LEFT))
        self.wait(3)

        self.play(Transform(graph.graph, graph2.graph), ApplyMethod(end_barrier.shift, 0.2*RIGHT))
        graph.remove()
        graph2 = WaveFunctionGraph(self, self.x_min, self.x_max, plot=True)
        self.add(graph2)
        self.wait(2)
        self.update_graph = True
        self.wait(18)
           
        
        

class WaveFunctionGraph(ContinualAnimation):
    def __init__(self, scene, x_min, x_max, plot=True):
        self.graph = Point()
        self.scene = scene 
        self.x_min = x_min
        self.x_max = x_max
        self.plot = plot
        self.removed = False
        self.first = True
        self.max_amplitude = 2
        self.amplitude = self.max_amplitude
        self.amplitude_velocity = -2*self.max_amplitude
        self.displacement = self.scene.x_end_barrier%2
        self.displacement_velocity = -self.amplitude_velocity / (4 *self.max_amplitude)
        self.exponential_constants = self.get_exponential_constants() 
        ContinualAnimation.__init__(self, self.graph)
    
    def update_mobject(self,dt):
        if self.scene.update_graph and not self.removed:
            self.amplitude += self.amplitude_velocity * dt
            if self.amplitude > self.max_amplitude:
                self.amplitude_velocity = -self.amplitude_velocity
                error = self.amplitude - self.max_amplitude
                self.amplitude = self.max_amplitude - error
            if self.amplitude < -self.max_amplitude:
                self.amplitude_velocity = -self.amplitude_velocity
                error = -self.max_amplitude - self.amplitude
                self.amplitude = -self.max_amplitude + error
            self.displacement += self.displacement_velocity * dt
            if self.displacement >= 1:
                self.displacement -= 1
            self.exponential_constants = self.get_exponential_constants()
            self.scene.remove(self.graph) 
            self.graph = self.get_graph()
            self.scene.add(self.graph)

        if self.first:
            self.graph = self.get_graph()
            self.first = False

            if self.plot:
                self.scene.add(self.graph)
        
        else:
            pass

    def add(self):
        self.scene.add(self.graph)
    
    def remove(self):
        self.scene.remove(self.graph)
        self.removed = True
    
    def FadeIn(self, run_time=1):
        self.scene.play(FadeIn(self.graph, run_time=run_time))
        
    def FadeOut(self,run_time=1):
        self.scene.play(FadeOut(self.graph, run_time=run_time))
    
    

    def get_graph(self):
        return FunctionGraph(
                self.wave_function,
                x_min = self.scene.coords_to_point(self.x_min, 0)[0], 
                x_max = self.scene.coords_to_point(self.x_max, 0)[0],
                color = RED
                )
    
    def get_graph_squared(self):
        return FunctionGraph(
                self.wave_function_squared,
                x_min = self.scene.coords_to_point(self.x_min, 0)[0], 
                x_max = self.scene.coords_to_point(self.x_max, 0)[0],
                color = RED
                )
            
    def wave_function(self, x):
        x = self.scene.x_axis.point_to_number(x)
        if self.scene.x_min <= x <= self.scene.x_start_barrier:
            return self.standing_wave(x, self.amplitude)/2
        if self.scene.x_start_barrier < x < self.scene.x_end_barrier:
            return self.barrier_decay(x)
        if self.scene.x_end_barrier <= x <= self.scene.x_max:
            return self.travelling_wave(x, self.displacement)/2

        else:
            return 0

    def wave_function_squared(self, x):
        x = self.scene.x_axis.point_to_number(x)
        if self.scene.x_min <= x <= self.scene.x_start_barrier:
            return ((self.standing_wave(x, self.amplitude))**2)/2
        if self.scene.x_start_barrier < x < self.scene.x_end_barrier:
            return ((self.barrier_decay(x))**2)/2
        if self.scene.x_end_barrier <= x <= self.scene.x_max:
            return ((self.travelling_wave(x, self.displacement))**2)/2

        else:
            return 0     

    def standing_wave(self, x, amplitude):
        return amplitude *  np.cos(2.02*PI*x)

    def barrier_decay(self,x):
        a = self.exponential_constants[0]
        b = self.exponential_constants[1]
        return a * np.e ** (b * x) 

    def travelling_wave(self,x, displacement):
        return self.scene.tunnel_probability*np.cos(2*PI*(x-displacement))

    def get_exponential_constants(self):
        y1 = self.wave_function(self.scene.coords_to_point(self.scene.x_start_barrier, 0)[0]) 
        y2 = self.wave_function(self.scene.coords_to_point(self.scene.x_end_barrier, 0)[0]) 

        if y1 == 0:
            y1 = 0.001
        if y2 == 0:
            y2 = 0.001

        b = np.log(abs(y2/y1)) / (self.scene.x_end_barrier-self.scene.x_start_barrier)
        a = y1 / (np.e ** (self.scene.x_start_barrier * b))

        return [a,b]