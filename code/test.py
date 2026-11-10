from manimlib import *

## ./.venv/bin/manimgl -w -i -l --video_dir media --file_name test code/test.py SquareToCircle

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
        self.wait()