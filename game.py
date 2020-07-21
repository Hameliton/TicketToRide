####################################
# Author: Seth Bassetti
####################################

#Imports
import random
import networkx as nx
import matplotlib


class Player:
    """"Class that contains information about each player"""

    def __init__(self, color):
        self.color = color
        self.train_cards = {}
        self.trains = 45
        self.points = 0


class Card:
    """Generic card class"""

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.color


class RouteCard:
    """Class that represents route cards"""

    def __init__(self, value, origin, destination):
        self.value = value
        self.origin = origin
        self.destination = destination

    def __repr__(self):
        return f"{self.origin}-{self.destination}, {self.value}"


class RouteDeck:
    """Deck that holds the route cards"""

    def __init__(self, routes):
        # Creates a shuffled deck with all of the route cards
        self.route_file = routes
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        # Creates the route cards from an input text file
        with open(self.route_file, "r") as routes:
            for line in routes.readlines():
                route = line.split(",")
                value = route[1].strip()
                places = route[0].split("-")
                origin = places[0].strip()
                destination = places[1].strip()
                # Creates a route card and appends it to the deck
                self.cards.append(RouteCard(value, origin, destination))

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]


class Deck:
    """Deck that holds train cards"""

    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        """Builds a deck with the color cards"""
        for color in ["blue", "red", "green", "yellow", "black", "pink", "orange", "white"]:
            for i in range(0, 12):
                self.cards.append(Card(color))
        for i in range(0, 14):
            self.cards.append(Card("wild"))

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]


class Route:
    """Class that holds a route's destination, length, and color
    """
    def __init__(self, destination, length, color):
        self.destination = destination
        self.length = length
        self.color = color
        self.taken = False

    def __repr__(self):
        return f"{self.destination}, {self.length}, {self.color}"


class Routegraph:
    """Graph that contains each city and it's connections in an adjacency table"""
    def __init__(self, city_file):
        self.adj = {}
        self.build_graph(city_file)

    def build_graph(self, city_file):
        """Reads an input file and converts it into an adjacency table"""
        self.graph = nx.Graph()
        with open(city_file, "r") as infile:
            for line in infile:
                line = line.split(":")
                city = line[0].strip()
                self.adj[city] = []
                routes = line[1].split("|")
                for route in routes:
                    route = route.split(",")
                    destination = route[0].strip()
                    length = int(route[1].strip())
                    color = route[2].strip()
                    self.adj[city].append(Route(destination, length, color))
                    self.graph.add_edge(city, destination, weight=length)
        #nx.draw_networkx(self.graph)

class Game:
    """Main game class"""
    def __init__(self):
        self.players = []



def main():
    deck = Deck()
    print(deck.cards)
    routes = RouteDeck("routes.txt")
    print(routes.cards)
    route_map = Routegraph("route_map.txt")
    for key in route_map.adj:
        print(f"{key}: {route_map.adj[key]}")

    #matplotlib.pyplot.show()

if __name__ == "__main__":
    main()
