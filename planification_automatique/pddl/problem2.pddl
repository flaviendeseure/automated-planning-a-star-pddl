(define (problem rubik1)
    (:domain rubik)
    (:objects r w b g o y - color)
    (:init
        (= (cost) 0)
        (face1 o b y)
        (face2 r g w)
        (face3 y r b)
        (face4 b o w)
        (face5 y o g)
        (face6 r b w)
        (face7 w o g)
        (face8 r y g)
    )
    (:goal (and
        (face1 w r b)
        (face2 w o b)
        (face3 y r b)
        (face4 y o b)
        (face5 w r g)
        (face6 w o g)
        (face7 y r g)
        (face8 y o g)
        )
    )
)