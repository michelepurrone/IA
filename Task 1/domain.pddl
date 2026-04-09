(define (domain emergency_services)
  (:requirements :strips :typing)
  (:types 
    location agent box content carrier box_number person - object
  )
  (:predicates
    (at ?x - (either agent box content carrier person) ?l - location)
    (empty ?b - box)
    (filled ?b - box ?c - content)
    (carrier_loaded ?c - carrier ?b - box)
    (capacity ?c - carrier ?bn - box_number)
    (next ?c - carrier ?bn1 ?bn2 - box_number)
    (needs ?p - person ?c - content)
    (has ?p - person ?c - content)
  )
  
  (:action fill_box
    :parameters (?robot - agent ?box - box ?content - content ?at - location)
    :precondition (and (at ?robot ?at) (at ?box ?at) (empty ?box) (at ?content ?at))
    :effect (and (not (empty ?box)) (filled ?box ?content))
  )
  
  (:action load_box_on_carrier
    :parameters (?robot - agent ?box - box ?content - content ?carrier - carrier ?at - location ?bnbefore ?bnafter - box_number)
    :precondition (and (at ?robot ?at) (at ?box ?at) (filled ?box ?content) (at ?carrier ?at) (capacity ?carrier ?bnbefore) (next ?carrier ?bnbefore ?bnafter))
    :effect (and (not (at ?box ?at)) (carrier_loaded ?carrier ?box) (not (capacity ?carrier ?bnbefore)) (capacity ?carrier ?bnafter))
  )
  
  (:action unload_box_from_carrier
    :parameters (?robot - agent ?box - box ?carrier - carrier ?at - location ?bnbefore ?bnafter - box_number)
    :precondition (and (at ?robot ?at) (carrier_loaded ?carrier ?box) (empty ?box) (at ?carrier ?at) (capacity ?carrier ?bnbefore) (next ?carrier ?bnafter ?bnbefore)) 
    :effect (and (at ?box ?at) (not (carrier_loaded ?carrier ?box)) (not (capacity ?carrier ?bnbefore)) (capacity ?carrier ?bnafter))
  )
  
  ;(:action move
    ;:parameters (?robot - agent ?from - location ?to - location)
    ;:precondition (and (at ?robot ?from))
    ;:effect (and (not (at ?robot ?from)) (at ?robot ?to))
  ;)
  
  (:action move_with_carrier
    :parameters (?robot - agent ?carrier - carrier ?from - location ?to - location)
    :precondition (and (at ?robot ?from) (at ?carrier ?from))
    :effect (and
              (not (at ?robot ?from)) 
              (not (at ?carrier ?from)) 
              (at ?robot ?to) 
              (at ?carrier ?to))
  )
  
  (:action deliver_content
    :parameters (?robot - agent ?box - box ?content - content ?carrier - carrier ?person - person ?at - location)
    :precondition (and (at ?robot ?at) (filled ?box ?content) (at ?carrier ?at) (carrier_loaded ?carrier ?box) (needs ?person ?content) (at ?person ?at))
    :effect (and (empty ?box) (not (filled ?box ?content)) (has ?person ?content) (at ?person ?at) (at ?robot ?at) (at ?carrier ?at))
  )
  
)
