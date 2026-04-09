(define (problem emergency_aid)
  (:domain emergency_services)
  (:objects
    depot loc2 loc3 - location
    robot - agent
    box1 box2 box3 box4 box5 - box
    food medicine - content
    carrier - carrier
    zero one two three four - box_number
    p1 p2 p3 - person
  )
  (:init
    (at robot depot)
    (at box1 depot)
    (at box2 depot)
    (at box3 depot)
    (at box4 depot)
    (at box5 depot)
    (empty box1)
    (empty box2)
    (empty box3)
    (empty box4)
    (empty box5)
    (at food depot)
    (at medicine depot)
    (at carrier depot)
    (capacity carrier zero)
    (next carrier zero one)
    (next carrier one two)
    (next carrier two three)
    (next carrier three four)
    (at p1 loc2)
    (at p2 loc2)
    (at p3 loc3)
    (needs p1 food)
    (needs p1 medicine)
    (needs p2 medicine)
    (needs p3 food)
    
  )
  (:goal
    (and
       (has p1 food)
       (has p1 medicine)
       (has p2 medicine)
       (has p3 food)
    )
  )
)