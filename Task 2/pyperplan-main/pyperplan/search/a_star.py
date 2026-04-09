#
# This file is part of pyperplan.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

"""
Implements the A* (a-star) and weighted A* search algorithm.
"""

import heapq
import logging

from . import searchspace


def ordered_node_astar(node, h, node_tiebreaker):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for A* search.

    @param node The node itself.
    @param heuristic A heuristic function to be applied.
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same.
    @returns A tuple to be inserted into priority queues.
    """
    f = node.g + h
    return (f, h, node_tiebreaker, node)


def ordered_node_weighted_astar(weight):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for weighted A* search (order: g+weight*h).

    @param weight The weight to be used for h
    @param node The node itself
    @param h The heuristic value
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same
    @returns A tuple to be inserted into priority queues
    """
    """
    Calling ordered_node_weighted_astar(42) actually returns a function (a
    lambda expression) which is the *actual* generator for ordered nodes.
    Thus, a call like
        ordered_node_weighted_astar(42)(node, heuristic, tiebreaker)
    creates an ordered node with weighted A* ordering and a weight of 42.
    """
    return lambda node, h, node_tiebreaker: (
        node.g + weight * h,
        h,
        node_tiebreaker,
        node,
    )


def ordered_node_greedy_best_first(node, h, node_tiebreaker):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for greedy best first search (the value with lowest
    heuristic value is used).

    @param node The node itself.
    @param h The heuristic value.
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same.
    @returns A tuple to be inserted into priority queues.
    """
    f = h
    return (f, h, node_tiebreaker, node)


def greedy_best_first_search(task, heuristic, use_relaxed_plan=False):
    """
    Searches for a plan in the given task using greedy best first search.

    @param task The task to be solved.
    @param heuristic A heuristic callable which computes the estimated steps
                     from a search node to reach the goal.
    """
    return astar_search(
        task, heuristic, ordered_node_greedy_best_first, use_relaxed_plan
    )


def weighted_astar_search(task, heuristic, weight=5, use_relaxed_plan=False):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved.
    @param heuristic  A heuristic callable which computes the estimated steps.
                      from a search node to reach the goal.
    @param weight A weight to be applied to the heuristics value for each node.
    """
    return astar_search(
        task, heuristic, ordered_node_weighted_astar(weight), use_relaxed_plan
    )


def astar_search(
    task, heuristic, make_open_entry=ordered_node_astar, use_relaxed_plan=False
):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved
    @param heuristic  A heuristic callable which computes the estimated steps
                      from a search node to reach the goal.
    @param make_open_entry An optional parameter to change the bahavior of the
                           astar search. The callable should return a search
                           node, possible values are ordered_node_astar,
                           ordered_node_weighted_astar and
                           ordered_node_greedy_best_first with obvious
                           meanings.
    """
    open = []
    state_cost = {task.initial_state: 0}
    node_tiebreaker = 0

    root = searchspace.make_root_node(task.initial_state)
    init_h = heuristic(root)
    heapq.heappush(open, make_open_entry(root, init_h, node_tiebreaker))
    logging.info("Initial h value: %f" % init_h)

    besth = float("inf")
    counter = 0
    expansions = 0

    while open:
        (f, h, _tie, pop_node) = heapq.heappop(open)
        if h < besth:
            besth = h
            logging.debug("Found new best h: %d after %d expansions" % (besth, counter))

        pop_state = pop_node.state
        # Only expand the node if its associated cost (g value) is the lowest
        # cost known for this state. Otherwise we already found a cheaper
        # path after creating this node and hence can disregard it.
        if state_cost[pop_state] == pop_node.g:
            expansions += 1

            if task.goal_reached(pop_state):
                logging.info("Goal reached. Start extraction of solution.")
                logging.info("%d Nodes expanded" % expansions)
                return pop_node.extract_solution()
            rplan = None
            if use_relaxed_plan:
                (rh, rplan) = heuristic.calc_h_with_plan(
                    searchspace.make_root_node(pop_state)
                )
                logging.debug("relaxed plan %s " % rplan)

            for op, succ_state in task.get_successor_states(pop_state):
                if use_relaxed_plan:
                    if rplan and not op.name in rplan:
                        # ignore this operator if we use the relaxed plan
                        # criterion
                        logging.debug(
                            "removing operator %s << not a "
                            "preferred operator" % op.name
                        )
                        continue
                    else:
                        logging.debug("keeping operator %s" % op.name)

                succ_node = searchspace.make_child_node(pop_node, op, succ_state)
                h = heuristic(succ_node)
                if h == float("inf"):
                    # don't bother with states that can't reach the goal anyway
                    continue
                old_succ_g = state_cost.get(succ_state, float("inf"))
                if succ_node.g < old_succ_g:
                    # We either never saw succ_state before, or we found a
                    # cheaper path to succ_state than previously.
                    node_tiebreaker += 1
                    heapq.heappush(open, make_open_entry(succ_node, h, node_tiebreaker))
                    state_cost[succ_state] = succ_node.g

        counter += 1
    logging.info("No operators left. Task unsolvable.")
    logging.info("%d Nodes expanded" % expansions)
    return None
    
def mb_astar_search(task, heuristic, make_open_entry=ordered_node_astar, use_relaxed_plan=False):
    max_memory = 1000 #limite di memoria
    open = []        #coda di priorità
    state_cost = {task.initial_state: 0}  #state_cost tiene traccia del costo g accumulato per raggiungere uno stato specifico durante la ricerca.
    node_tiebreaker = 0  

    #seleziona il nodo radice e calcola il suo valore euristico
    root = searchspace.make_root_node(task.initial_state)  
    init_h = heuristic(root)

    #il nodo radice viene inserito nell'heap open (l'heap garantisce che il nodo più piccolo sia sempre posizionato nella posizione radice).
    #Il nodo lo seleziona mediante il metodo ordered_node_astar.
    #messo a disposizione dalla classe, il quale preleva il nodo con il valore di h più piccolo 
    heapq.heappush(open, make_open_entry(root, init_h, node_tiebreaker))
    logging.info("Initial h value: %f" % init_h)

    besth = float("inf")  #viene inizializzato a + infinito un parametro che indica il valore della migliore euristica
    counter = 0         #conta il numero di nodi in open
    expansions = 0      #conta il numero di nodi espansi

    while open:         #finchè ci sono elementi in open
        (f, h, _tie, pop_node) = heapq.heappop(open) #PRELEVA DA open il nodo radice,
                                                    #chiamato pop_node e i suoi valori vengono assegnati a f, h, _tie e pop_node.
        if h < besth: #se il valore di h è minore di besth 
            besth = h #viene assegnato un nuovo valore per l'euristica
            logging.debug("Found new best h: %d after %d expansions" % (besth, counter))

        pop_state = pop_node.state	#pop_state = stato del nodo prelevato (pop_node)
		#se il costo per raggiungere quello stato è uguale al costo g di pop_node
        #espandiamo questo nodo se il suo costo associato (g) è il costo più basso per raggiungere questo stato (cioè state_cost[pop_state])
        if state_cost[pop_state] == pop_node.g:
            expansions += 1
            if task.goal_reached(pop_state):
                logging.info("Goal reached. Start extraction of solution.")
                logging.info("%d Nodes expanded" % expansions)
                return pop_node.extract_solution()
            
        rplan = None
        #non usiamo un piano rilassato
        if use_relaxed_plan:
            (rh, rplan) = heuristic.calc_h_with_plan(searchspace.make_root_node(pop_state))
            logging.debug("relaxed plan %s " % rplan)

        #get_success_states restituisce una lista di coppie (op, new_state) dove "op" è l'operatore applicabile
       #e new_state è lo stato risultante quando op viene applicato a state
        for op, succ_state in task.get_successor_states(pop_state):
                if use_relaxed_plan:
                    if rplan and not op.name in rplan:
                        # Ignore this operator if it's not in the relaxed plan
                        logging.debug(
                            "removing operator %s << not a preferred operator" % op.name
                        )
                        continue
                    else:
                        logging.debug("keeping operator %s" % op.name)
			
                #costruisce un nuovo nodo successore del nodo corrente
                succ_node = searchspace.make_child_node(pop_node, op, succ_state)
                h = heuristic(succ_node)  #calcola il valore euristico del nodo successivo
                if h == float("inf"): #si ignorano gli stati che non  possono raggiungere il goal
                    continue
                #cerca il valore associato a succ_state in state_cost. se succ_state è presente, old_succ_g viene impostato con il suo valore.
                #altrimenti viene impostato con un valore infinito.
                old_succ_g = state_cost.get(succ_state, float("inf"))
                if succ_node.g < old_succ_g: #se viene trovato un percorso più economico per raggiungere succ_state
                    #incrementa una variabile node_tiebreaker per garantire un ordine stabile dei nodi nella coda prioritaria in caso di parità di priorità.
                    node_tiebreaker += 1
                     # inserisce il nodo successore succ_node nella coda prioritaria open. L'ordine di inserimento viene determinato da una combinazione di fattori:
                    #la valutazione euristica h del nodo,il costo del percorso succ_node.g e il valore di node_tiebreaker per risolvere eventuali parità.
                    heapq.heappush(open, make_open_entry(succ_node, h, node_tiebreaker))
                    state_cost[succ_state] = succ_node.g # aggiorna il costo associato a succ_state nel dizionario state_cost con il nuovo costo succ_node.g.
 

        counter += 1

    #CONTROLLO MEMORIA
    if counter % 1000 == 0: #ogni mille nodi 
            if len(open) > max_memory: #se la lunghezza di open supera la soglia massima
                logging.info("Memory limit reached. Pruning open nodes.")
                # utilizza la funzione nsmallest() del modulo heapq per ottenere i primi max_memory elementi più piccoli da
                # open e assegna il risultato a open.
                
                open = heapq.nsmallest(max_memory, open) 

    logging.info("No operators left. Task unsolvable.")
    logging.info("%d Nodes expanded" % expansions)
    return None
