(define (domain emergency_services)

  ;per eseguire planutils run tfd domain_da.pddl problem_da.pddl
  
  (:requirements :strips :typing :universal-preconditions :durative-actions :fluents)
  
  (:types 
    location agent box content carrier person - object
  )

  (:predicates
    (at ?x - (either agent box content carrier person) ?l - location)
    (empty ?b - box)
    (filled ?b - box ?c - content)
    (carrier_loaded ?c - carrier ?b - box)
    (needs ?p - person ?c - content)
    (has ?p - person ?c - content)
    (handsfree ?r - agent)
  )
  
  (:functions 
        (capacity ?c - carrier) ;capacità corrente
        (max_capacity) ;capacità massima
        (content_weight ?c - content)
        (total_weight)
   ) 


 :durative-action fill_box
    :parameters (?robot - agent ?box - box ?content - content ?at - location ?p - person)
    :duration (= ?duration 0.001)
    :condition (and (at start (at ?robot ?at)) (at start (at ?box ?at)) (at start (empty ?box)) (at start (at ?content ?at)) (at start(needs ?p ?content))
    		 (at start (handsfree ?robot)))
    :effect (and (at end (not (empty ?box))) (at end (filled ?box ?content)) (at end(not(needs ?p ?content))) (at end(not (handsfree ?robot))) 
     )
  )


  (:durative-action load_box_on_carrier
    :parameters (?robot - agent ?box - box ?content - content ?carrier - carrier ?at - location)
    :duration (= ?duration 0.002)
    :condition (and (at start (at ?robot ?at)) (at start (at ?box ?at)) (at start (filled ?box ?content)) (at start (at ?carrier ?at)) 
                    (at start (<= (capacity ?carrier) (max_capacity))) (at start(not(handsfree ?robot)))               
               )
    :effect (and (at end (not (at ?box ?at))) (at end (increase (total_weight) 1)) (at end (carrier_loaded ?carrier ?box))
    		 (at end (increase (capacity ?carrier) 1)) (at end (handsfree ?robot))
            )     
  )

  (:durative-action unload_box_from_carrier
    :parameters (?robot - agent ?box - box ?carrier - carrier ?at - location)
    :duration (= ?duration 0.002)
    :condition (and (at start (at ?robot ?at)) (at start (carrier_loaded ?carrier ?box)) (at start (empty ?box)) (at start (at ?carrier ?at))(at start (> (capacity ?carrier) 0))              
               ) 
    :effect (and (at end (at ?box ?at)) (at start (not (carrier_loaded ?carrier ?box))) (at end (decrease (capacity ?carrier) 1))
            
            )
  )

  
  (:durative-action move_with_carrier
    :parameters (?robot - agent ?box - box ?carrier - carrier ?from - location ?to - location)
    :duration (= ?duration (*(total_weight)1))
    :condition (and (at start (at ?robot ?from)) (at start (at ?carrier ?from))
                    
               )
    :effect (and
              (at start (not (at ?robot ?from))) 
              (at start (not (at ?carrier ?from))) 
              (at end (at ?robot ?to)) 
              (at end (at ?carrier ?to))
            )
   )
 

  (:durative-action deliver_content
    :parameters (?robot - agent ?box - box ?content - content ?carrier - carrier ?person - person ?at - location)
    :duration (= ?duration 0.003)
    :condition (and (at start (at ?robot ?at)) (at start (filled ?box ?content)) (at start (at ?carrier ?at)) (at start (carrier_loaded ?carrier ?box))(at start (at ?person ?at)))
    :effect (and (at end (empty ?box)) (at end (not (filled ?box ?content))) (at end (decrease (total_weight) (content_weight ?content))) (at end (has ?person ?content)) 
    
            )
  )

)


