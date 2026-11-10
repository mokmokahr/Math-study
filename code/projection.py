from manimlib import *


class ProjectionScene(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
        )

        u_coords = [3, 1.5]
        v_coords = [1.5, 3]

        scale = (
            v_coords[0] * u_coords[0] + v_coords[1] * u_coords[1]
        ) / (
            u_coords[0] ** 2 + u_coords[1] ** 2
        )
        proj_coords = [scale * u_coords[0], scale * u_coords[1]]

        u = Vector(u_coords, fill_color=GREEN)
        v = Vector(v_coords, fill_color=BLUE)
        projection = Vector(proj_coords, fill_color=RED)
        projection_drop = DashedLine(
            v.get_end(),
            projection.get_end(),
            color=YELLOW,
        )
        u_label = Tex(r"\vec{u}", fill_color=GREEN).next_to(u.get_end(), RIGHT)
        v_label = Tex(r"\vec{v}", fill_color=BLUE).next_to(v.get_end(), UP)
        projection_equation = VGroup(
            Tex(r"\operatorname{proj}_{\vec{u}}(\vec{v})", fill_color=RED),
            Tex(r"=\frac{\vec{v}\cdot\vec{u}}{\vec{u}\cdot\vec{u}}\vec{u}"),
        )
        projection_equation.scale(0.55).arrange(RIGHT, buff=0.12)
        projection_equation.next_to(projection.get_end(), DOWN, buff=0.5)

        self.add(plane)
        self.play(
            ShowCreation(u),
            ShowCreation(v),
            FadeIn(u_label),
            FadeIn(v_label),
        )
        self.play(ShowCreation(projection_drop))
        self.play(ShowCreation(projection))
        self.play(FadeIn(projection_equation))
        self.wait(3)