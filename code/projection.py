import numpy as np

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


class ThreeDSubspaceProjection(ThreeDScene):
    def setup(self):
        super().setup()
        # manimlib(3B1B 구버전)에서 카메라 각도를 안전하게 고정하는 방식
        self.camera.frame.set_euler_angles(
            theta=145 * DEGREES,  # 좌우 회전각
            phi=60 * DEGREES,    # 위아래 기울기
        )

    def construct(self):
        # 3차원 축 설정
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
        )

        # 1. 직교하는 두 기저 벡터 v1, v2 (xy 평면 상의 수직인 벡터들)
        v1_coords = [3, 0, 0]
        v2_coords = [0, 3, 0]
        
        # 2. 공중에 떠 있는 대상 벡터 u (z 성분이 있는 3차원 벡터)
        u_coords = [2, 2, 3]

        # --- v1에 대한 u의 정사영 계산 ---
        scale1 = (
            u_coords[0] * v1_coords[0] + u_coords[1] * v1_coords[1] + u_coords[2] * v1_coords[2]
        ) / (
            v1_coords[0] ** 2 + v1_coords[1] ** 2 + v1_coords[2] ** 2
        )
        proj1_coords = [scale1 * v1_coords[0], scale1 * v1_coords[1], scale1 * v1_coords[2]]

        # --- v2에 대한 u의 정사영 계산 ---
        scale2 = (
            u_coords[0] * v2_coords[0] + u_coords[1] * v2_coords[1] + u_coords[2] * v2_coords[2]
        ) / (
            v2_coords[0] ** 2 + v2_coords[1] ** 2 + v2_coords[2] ** 2
        )
        proj2_coords = [scale2 * v2_coords[0], scale2 * v2_coords[1], scale2 * v2_coords[2]]

        # --- 오브젝트 생성 ---
        u = Vector(u_coords, fill_color=GREEN)
        v1 = Vector(v1_coords, fill_color=BLUE)
        v2 = Vector(v2_coords, fill_color=BLUE)

        proj1 = Vector(proj1_coords, fill_color=YELLOW)
        proj2 = Vector(proj2_coords, fill_color=YELLOW)
        
        # 최종 평면 위에서의 정사영 벡터 (proj1 + proj2)
        final_proj_coords = [
            proj1_coords[0] + proj2_coords[0], 
            proj1_coords[1] + proj2_coords[1], 
            proj1_coords[2] + proj2_coords[2]
        ]
        final_projection = Vector(final_proj_coords, fill_color=RED)

        # 보조선들 (점선)
        projection_drop1 = DashedLine(u.get_end(), proj1.get_end(), color=GREY)
        projection_drop2 = DashedLine(u.get_end(), proj2.get_end(), color=GREY)
        drop_u = DashedLine(u.get_end(), final_projection.get_end(), color=GREY)

        def make_right_angle_marker(foot, along_projection, along_drop, size=0.3):
            projection_direction = np.array(along_projection, dtype=float)
            projection_direction /= np.linalg.norm(projection_direction)
            projection_direction *= -1
            drop_direction = np.array(along_drop, dtype=float)
            drop_direction /= np.linalg.norm(drop_direction)
            foot = np.array(foot)
            marker_a = foot + size * projection_direction
            marker_b = marker_a + size * drop_direction
            marker_c = foot + size * drop_direction
            return VGroup(
                Line(foot, marker_a, color=WHITE),
                Line(marker_a, marker_b, color=WHITE),
                Line(marker_b, marker_c, color=WHITE),
            )

        right_angle_marker1 = make_right_angle_marker(
            proj1.get_end(), v1_coords, np.array(u_coords) - np.array(proj1_coords)
        )
        right_angle_marker2 = make_right_angle_marker(
            proj2.get_end(), v2_coords, np.array(u_coords) - np.array(proj2_coords)
        )

        # Keep labels attached to vector endpoints while facing the camera
        camera_rotation = self.camera.frame.get_orientation().as_matrix()
        camera_right = camera_rotation @ RIGHT
        camera_up = camera_rotation @ UP

        def make_vector_label(tex, color, point, offset):
            label = Tex(tex, fill_color=color)
            label.apply_matrix(camera_rotation)
            label.move_to(point + offset)
            return label

        u_label = make_vector_label(
            r"\vec{u}", GREEN, u.get_end(), 0.25 * camera_up
        )
        v1_label = make_vector_label(
            r"\vec{v}_1", BLUE, v1.get_end(), 0.25 * camera_right
        )
        v2_label = make_vector_label(
            r"\vec{v}_2", BLUE, v2.get_end(), 0.25 * camera_right
        )
        formula1 = Tex(
            r"\operatorname{proj}_{\vec{v}_1}(\vec{u})"
            r"=\frac{\vec{u}\cdot\vec{v}_1}{\vec{v}_1\cdot\vec{v}_1}\vec{v}_1",
            fill_color=YELLOW,
        ).scale(0.45).to_corner(UL, buff=0.3).fix_in_frame()
        formula2 = Tex(
            r"\operatorname{proj}_{\vec{v}_2}(\vec{u})"
            r"=\frac{\vec{u}\cdot\vec{v}_2}{\vec{v}_2\cdot\vec{v}_2}\vec{v}_2",
            fill_color=YELLOW,
        ).scale(0.45).next_to(formula1, DOWN, aligned_edge=LEFT, buff=0.2).fix_in_frame()
        final_formula = Tex(
            r"\operatorname{proj}_{A}(\vec{u})"
            r"=\operatorname{proj}_{\vec{v}_1}(\vec{u})"
            r"+\operatorname{proj}_{\vec{v}_2}(\vec{u})",
            fill_color=RED,
        ).scale(0.45).next_to(formula2, DOWN, aligned_edge=LEFT, buff=0.2).fix_in_frame()

        # 애니메이션 실행
        self.add(axes)
        self.play(
            ShowCreation(v1), ShowCreation(v2),
            FadeIn(v1_label), FadeIn(v2_label)
        )
        self.play(ShowCreation(u), FadeIn(u_label))
        self.wait(1)

        # 1. Show each projected component in sequence
        self.add(proj1, set_depth_test=False)
        self.add(right_angle_marker1, set_depth_test=False)
        self.play(
            ShowCreation(projection_drop1),
            ShowCreation(proj1),
            ShowCreation(right_angle_marker1),
            FadeIn(formula1),
        )
        self.wait(1)

        self.add(proj2, set_depth_test=False)
        self.add(right_angle_marker2, set_depth_test=False)
        self.play(
            ShowCreation(projection_drop2),
            ShowCreation(proj2),
            ShowCreation(right_angle_marker2),
            FadeIn(formula2),
        )
        self.wait(1)

        # Add the components head-to-tail, then show their resultant.
        self.play(
            FadeOut(projection_drop1),
            FadeOut(projection_drop2),
            FadeOut(right_angle_marker1),
            FadeOut(right_angle_marker2),
            ApplyMethod(proj2.shift, proj1.get_end()),
        )
        self.wait(1)
        self.play(ShowCreation(final_projection))
        self.wait(1)

        # The resultant is the projection of u onto the plane.
        self.play(ShowCreation(drop_u))
        self.play(FadeIn(final_formula))
        self.wait(3)



class ErrorVectorScene(ThreeDScene):
    def setup(self):
        super().setup()
        self.camera.frame.set_euler_angles(
            theta=145 * DEGREES,
            phi=60 * DEGREES,
        )

    def construct(self):
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-1, 4, 1],
        )

        # Subspace W = xy-plane
        plane = ParametricSurface(
            lambda x, y: np.array([x, y, 0]),
            u_range=[-3.5, 3.5],
            v_range=[-3.5, 3.5],
            resolution=(12, 12),
            color=BLUE_E,
            opacity=0.12,
        ).set_z_index(-2)

        # Original vector, projection, and error
        u_coords = np.array([2.0, 1.5, 3.0])
        p_coords = np.array([2.0, 1.5, 0.0])
        e_coords = u_coords - p_coords

        u = Vector(u_coords, fill_color=GREEN)
        p = Vector(p_coords, fill_color=RED)
        p.set_z_index(2)

        # Error vector starts at the endpoint of p
        error = Arrow(
            p_coords,
            u_coords,
            buff=0,
            fill_color=YELLOW,
        )

        # Dashed line emphasizes the projection drop
        drop = DashedLine(
            u_coords,
            p_coords,
            color=YELLOW,
        )

        # Right-angle marker between p and the vertical error vector
        size = 0.3
        along_p = -p_coords / np.linalg.norm(p_coords)
        along_error = e_coords / np.linalg.norm(e_coords)
        corner = p_coords + size * along_p
        opposite_corner = corner + size * along_error
        marker = VGroup(
            Line(p_coords, corner, color=WHITE),
            Line(corner, opposite_corner, color=WHITE),
            Line(opposite_corner, p_coords + size * along_error, color=WHITE),
        )

        # Labels facing the camera
        rotation = self.camera.frame.get_orientation().as_matrix()
        camera_right = rotation @ RIGHT
        camera_up = rotation @ UP

        def make_label(tex, color, point, offset):
            label = Tex(tex, fill_color=color)
            label.apply_matrix(rotation)
            label.move_to(point + offset)
            return label

        u_label = make_label(
            r"\vec{u}", GREEN, u_coords,
            0.3 * camera_up
        )
        p_equation = VGroup(
            Tex(r"\vec{p}=A\vec{c}", fill_color=RED),
            Tex(r"=c_1\vec{v}_1", fill_color=RED),
            Tex(r"+c_2\vec{v}_2", fill_color=RED),
            Tex(r"+\cdots+c_n\vec{v}_n", fill_color=RED),
        ).arrange(RIGHT, buff=0.12)
        p_equation.scale(0.6)
        p_equation.apply_matrix(rotation)
        p_equation.move_to(p_coords - 0.65 * camera_up)
        p_equation.set_z_index(2)
        e_label = make_label(
            r"\vec{e}=\vec{u}-A\vec{c}",
            YELLOW,
            (u_coords + p_coords) / 2,
            1.0 * camera_right + 0.2 * camera_up,
        ).scale(0.8)

        # Animation
        self.add(axes)

        self.play(FadeIn(plane))
        self.wait(0.5)

        self.play(
            ShowCreation(u),
            FadeIn(u_label),
        )
        self.wait(1)

        self.add(p, set_depth_test=False)
        self.play(ShowCreation(p))
        for equation_part in p_equation:
            self.add(equation_part, set_depth_test=False)
            self.wait(0.4)
        self.wait(1)

        self.add(drop, marker, set_depth_test=False)
        self.play(
            ShowCreation(drop),
        )
        self.wait(0.5)

        self.add(error, e_label, set_depth_test=False)
        self.play(
            FadeOut(drop),
            ShowCreation(error),
            FadeIn(e_label),
        )
        self.wait(1)

        self.play(ShowCreation(marker))
        self.wait(3)