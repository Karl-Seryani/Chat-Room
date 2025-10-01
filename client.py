from chatroom import ClientTCP
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n', type=str, required=True, help='Client name')
parser.add_argument('--host', type=str, default='localhost', help='Server IP address (default: localhost)')
parser.add_argument('--port', '-p', type=int, default=12345, help='Server port (default: 12345)')
args = parser.parse_args()

client = ClientTCP(args.name, args.port, args.host)
client.run()