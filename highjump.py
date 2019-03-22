class HighJump(Scene):
    phase=-1
    landscape = None
    cat = None
    vCatx = 0.0
    vCaty = 0.0
    def construct(self):

        self.always_continually_update = True

        thirdPlacePodium = Rectangle(height=0.375, width=0.5).shift(0.5*RIGHT)
        secondPlacePodium = Rectangle(height=0.5, width=0.5).shift(0.5*LEFT+0.0625*UP)
        firstPlacePodium = Rectangle(height=0.625, width=0.5).shift(0.125*UP)
        floor = Line(np.array([-0.5*FRAME_WIDTH, -3, 0]), np.array([0.5*FRAME_WIDTH, -3, 0]), color=WHITE)
        first = TextMobject("1", color=GOLD).scale(0.5).move_to(firstPlacePodium.get_center())
        second = TextMobject("2", color=LIGHT_GREY).scale(0.5).move_to(secondPlacePodium.get_center())
        third = TextMobject("3", color=DARK_BROWN).scale(0.5).move_to(thirdPlacePodium.get_center())
        horde = Line(np.array([23.5, -4, 0]), np.array([23.5, 2, 0]))
        teacher = Cat("teacher").move_to(np.array([-2, -1, 0]))
        student = Cat().move_to(np.array([0, -1, 0]))
        self.cat = Cat().move_to(np.array([-6, -2, 0]))
        bubble = ThoughtBubble().scale(0.8).move_to(student.get_center() + np.array([3.5, 3, 0]))
        self.add(horde)

        podium = VGroup(thirdPlacePodium, secondPlacePodium, firstPlacePodium, first, second, third).shift(3.5 * LEFT + 1.5 * UP)
        scenesmall = VGroup(podium, floor, self.cat).scale(0.25).move_to(bubble.get_center() + 0.5 * UP)
        scenelarge = copy.deepcopy(scenesmall).scale(4).center()



        self.add(student, teacher)
        self.wait(1)
        self.add(bubble, scenesmall)
        self.wait(2)
        self.play(Transform(scenesmall, scenelarge), FadeOut(student), FadeOut(teacher), FadeOut(bubble))
        self.landscape = VGroup(podium, floor, horde)
        floor.scale(100)
        self.phase=0
        self.wait(4)
        self.phase = 1
        self.vCaty = 6
        self.wait(1)
        self.phase = 2
        self.vCatx = - self.vCat
        self.wait(1)
        self.phase = 3
        self.wait(1)
        self.phase = 4
        self.wait(1)
        self.phase = -1
        self.wait(12)
        self.play(ShrinkToCenter(floor), ShrinkToCenter(horde), FadeOut(self.cat))



    def continual_update(self, *args, **kwargs):
        numcalc=10
        dt = self.frame_duration/numcalc
        for i in range(numcalc):
            if self.phase == 0:
                self.landscape.shift(-dt * np.array([self.vCatx, 0.0, 0.0]))
                self.cat.shift(0.2*dt*np.array([self.vCatx, 0.0, 0.0]))
                self.vCatx += 2 * dt
            if self.phase == 1:
                self.vCaty -= 6 * dt
                self.landscape.shift(-dt * np.array([self.vCatx, 0.0, 0.0]))
                self.cat.shift(dt * np.array([0.2*self.vCatx, self.vCaty, 0]))
            if self.phase == 2:
                self.cat.rotate(-2 * PI * dt, Z_AXIS)
                if self.cat.get_center()[1] >-1:
                    self.vCaty -= 6 * dt
                    self.cat.shift(dt * np.array([0.2 * self.vCatx, self.vCaty, 0]))
                if self.cat.get_center().tolist()[1] < -1:
                    self.cat.move_to(np.array([self.cat.get_center()[0], -1.4, self.cat.get_center()[2]]))
                self.landscape.shift(-0.5 * dt * np.array([self.vCatx, 0.0, 0.0]))
            if self.phase == 3:
                self.cat.rotate(-2 * PI * dt, Z_AXIS)
                self.landscape.shift(-0.5 * dt * np.array([self.vCatx, 0.0, 0.0]))
                self.cat.shift(dt * np.array([-0.2 * self.vCatx, -0.1 * dt, 0]))










