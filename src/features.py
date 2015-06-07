#!/usr/bin/python
import numpy as np
import model as md
import dao
from model import Mechanics

class Composition:
	def __init__(self, cards):
		self.keys = sorted(list([card.id for card in cards]))
		self.nb = len(self.keys)
		
	def exfe(self, deck):
		res = [0] * self.nb
		cards = deck.cardsMap
		for card in cards.keys():
			try:
				res[self.keys.index(card.id)] = cards[card] / 2
			except ValueError:
				print "ERROR: card " + str(card.id) + " not found in the list (" + ', '.join(map(str,self.keys)) + ")"
				
		return res
	
def normalize(values,vmin,vmax):
	return [max(0,min(1,float(value-vmin)/float(vmax-vmin))) for value in values]
	
#TODO add more mechanics
MECHANICS = [Mechanics.TAUNT, Mechanics.ONETURNEFFECT, Mechanics.MORPH, Mechanics.COMBO, Mechanics.SUMMON, Mechanics.SECRET, Mechanics.CHARGE]
def exfe_mechanics(deck):
	
	result = [0] * len(MECHANICS)
	occurrences = deck.cardsMap	
	for card in occurrences.keys():
		for mech in card.mechanics:
			if mech in MECHANICS:
				result[MECHANICS.index(mech)] += occurrences[card]
		
	return normalize(result,0,15)
	
def exfe_type(deck,type):
	val = 0
	occurrences = deck.cardsMap
	for card in occurrences.keys():
		if type == card.type:
			val += occurrences[card]
			
	return val
	
def exfe_types(deck):
	result = []
	
	result.append(exfe_type(deck,md.Types.MINION))
	result.append(exfe_type(deck,md.Types.SPELL))
	result.append(exfe_type(deck,md.Types.WEAPON))
	
	return normalize(result,0,30)
	
def exfe_count_range(deck,attribut,split_tab):
	result = [0] * (len(split_tab) + 1)
	
	for card,occ in deck.cardsMap.iteritems():
		cost = attribut(card)
		for idx,v in enumerate(split_tab):
			if cost <= v:
				result[idx] += occ
				break
			elif idx+1 == len(split_tab):
				result[idx+1] += occ

	return normalize(result,0,deck.nbCards)
	
def exfe_distri_range(deck):
	return	exfe_count_range(deck,lambda card: card.manacost,[3,6])
	
def exfe_distri_general(deck,check,attribut,MINIMANA=0,MAXMANA=7):
	result = [0] * ((MAXMANA-MINIMANA) + 1)

	occurrences = deck.cardsMap
	for card in occurrences.keys():
		if(check(card)):
			continue
		cost = attribut(card)
		if cost>MAXMANA:
			cost = MAXMANA
		elif cost<MINIMANA:
			cost = MINIMANA
		result[cost] += occurrences[card]
		
	return normalize(result,0,15)

def exfe_distri(deck):
	result = []
	
	result.extend(exfe_distri_general(deck,lambda card: False,lambda card: card.manacost,0,7))
	result.extend(exfe_distri_general(deck,lambda card: card.type == md.Types.SPELL,lambda card: card.attack,0,7))
	result.extend(exfe_distri_general(deck,lambda card: card.type != md.Types.MINION,lambda card: card.health,0,7))
	
	return result
	 
def exfe_winrates(deck):
	result = []
	result.append(deck.constructedWinRate)
	#result.append(deck.arenaWinRate)
	return result
	
def exfe_deck(deck,comp):
	result = []
	
	result.extend(comp.exfe(deck))
	result.extend(exfe_mechanics(deck))
	result.extend(exfe_types(deck))
	result.extend(exfe_distri(deck))
	result.extend(exfe_distri_range(deck))
	#result.extend(exfe_winrates(deck))
	
	return result

def exfe_decks(decks,cards):
	results = []
	
	comp = Composition(cards)
	for deck in decks:
		results.append(exfe_deck(deck,comp))
	
	return np.array(results)
	
def load_dataset():
	with dao.Dao() as da:
		cards = da.cards
		decks = da.decks

	return np.array(exfe_decks(filter(lambda deck: deck.isValidConstructed, decks), cards))
	
#DEBUG
if __name__ == "__main__":
	print load_dataset()[400]