import networkx as nx
import random
from os.path import exists

class Network:
    def __init__(self):
        self.graph = nx.Graph()

    def add_connection(self, node1, node2):
        if not self.graph.has_edge(node1, node2):
            self.graph.add_edge(node1, node2)
            print(f"Connection added: {node1} <--> {node2}")
        else:
            print(f"Connection {node1} <--> {node2} already exists.")

    def display(self):
        print("\nConnections in the network:")
        for edge in self.graph.edges():
            print(f"{edge[0]} <--> {edge[1]}")


def crc_encode(data, polynomial):
    """
    Oblicza CRC dla danego ciągu danych przy użyciu zadanego wielomianu.
    """
    data = list(data)
    poly = list(polynomial)
    data.extend(['0'] * (len(poly) - 1))

    for i in range(len(data) - len(poly) + 1):
        if data[i] == '1':
            for j in range(len(poly)):
                data[i + j] = str(int(data[i + j] != poly[j]))
    return ''.join(data[-(len(poly) - 1):])


def crc_validate(received_data, polynomial):
    """
    Waliduje wiadomość z kodem CRC przy użyciu wielomianu.
    """
    remainder = crc_encode(received_data, polynomial)
    return all(bit == '0' for bit in remainder)


def introduce_error(message, error_rate):
    """
    Wprowadza błędy do wiadomości z zadaną częstością (error_rate).
    """
    message = list(message)
    for i in range(len(message)):
        if random.random() < error_rate:
            message[i] = '1' if message[i] == '0' else '0'
    return ''.join(message)


def find_path(graph, src, dest):
    """
    Znajduje najkrótszą ścieżkę między węzłami w grafie za pomocą BFS.
    """
    try:
        return nx.shortest_path(graph, source=src, target=dest)
    except nx.NetworkXNoPath:
        return None


def simulate_message_transfer(path, message, polynomial, error_rate):
    """
    Symuluje przesyłanie wiadomości przez kolejne węzły na trasie.
    """
    print(f"Path from {path[0]} to {path[-1]}: {' -> '.join(map(str, path))}")
    current_message = message + crc_encode(message, polynomial)
    print(f"Initial encoded message: {current_message}")

    for i in range(len(path) - 1):
        print(f"Transmitting from Node {path[i]} to Node {path[i + 1]}...")
        current_message = introduce_error(current_message, error_rate)
        print(f"Message received at Node {path[i + 1]}: {current_message}")
        if not crc_validate(current_message, polynomial):
            print(f"Error detected at Node {path[i + 1]}! Transmission failed.")
            return False

    print(f"Message successfully transmitted to Node {path[-1]}.")
    return True

def save_edge_nodes_to_file(out_file, graph):
    with open(out_file, 'w') as f:
        for u, v in graph.edges():
            f.write(f"{u} {v}\n")
    print(f"Edges saved to {out_file}")

def load_edge_nodes_from_file(in_file, network):
    with open(in_file, 'r') as f:
        for line in f:
            node1 = line.strip()[0]
            node2 = line.strip()[2]
            network.add_connection(node1, node2)

def main():
    network = Network()
    while True:
        print("\n1. Add connection")
        print("2. Display network")
        print("3. Send message")
        print("4. Exit")
        print("5. Save edges to file")
        print("6. Load edges from file")
        choice = input("Choose an option: ")

        match choice:
            case "1":
                while True:
                    node1 = input("Node 1: ")
                    node2 = input("Node 2: ")
                    if node1.isnumeric() and node2.isnumeric() and node1 != node2:
                        break
                network.add_connection(int(node1), int(node2))
            case "2":
                network.display()
            case "3":
                src = int(input("Enter source node: "))
                dest = int(input("Enter destination node: "))
                if not nx.has_path(network.graph, src, dest):
                    print(f"No path exists between node {src} and node {dest}.")
                    continue

                message = input("Enter message (binary): ")
                polynomial = input("Enter CRC polynomial (binary): ")
                path = find_path(network.graph, src, dest)

                error_rate = float(input("Enter error rate (0-1): "))
                success = simulate_message_transfer(path, message, polynomial, error_rate)

                if success:
                    print("Message transmission was successful.")
                else:
                    print("Message transmission failed.")
            case "4":
                break
            case "5":
                while True:
                    out_file = str(input("Enter output file name (without extension): "))
                    if out_file.isalnum():
                        break
                out_file += ".txt"
                save_edge_nodes_to_file(out_file, network.graph)
            case "6":
                while True:
                    in_file = str(input("Enter name of input file (without extension): "))
                    in_file += ".txt"
                    if exists(in_file):
                        break
                load_edge_nodes_from_file(in_file, network)
            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
