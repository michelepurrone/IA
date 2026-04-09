(define (problem emergency_aid)
  (:domain emergency_services)
  (:objects
    loc1 loc2 loc3 - location
    robot - agent
    box1 box2 box3 box4 box5 - box
    food drug tool - content
    transporter - carrier
    p1 p2 p3 - person
  )
  (:init
  
    (at robot loc1)
    (at box1 loc1)
    (at box2 loc1)
    (at box3 loc1)
    (at box4 loc1)
    (at box5 loc1)
    (empty box1)
    (empty box2)
    (empty box3)
    (empty box4)
    (empty box5)
    (at food loc1)
    (= (content_weight food) 2)
    (at drug loc1)
    (= (content_weight drug) 1)
    (at tool loc1)
    (= (content_weight tool) 3)
    (= (total_weight) 0)
    (at transporter loc1)
    (= (capacity transporter) 0)
    (= (max_capacity) 4)
    (at p1 loc2)
    (at p2 loc2)
    (at p3 loc3)
    (needs p1 food)
    (needs p1 drug)
    (needs p2 drug)
    (needs p3 food)
    (handsfree robot)
  )
  (:goal
    (and
       (has p1 food)
       (has p1 drug)
       (has p2 drug)
       (has p3 food)
    )
  )
)

