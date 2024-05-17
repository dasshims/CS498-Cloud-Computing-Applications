import json
import boto3
import base64
from collections import defaultdict, deque

dynamodb = boto3.resource('dynamodb')
table_name = dynamodb.Table('locations')


def lambda_handler(event, context):
    print(f"event {event}")
    # graph = json.loads(event["body"])['graph']

    body = event["body"]
    print(f"body --- {body}")

    graph = json.loads(base64.b64decode(body).decode('ascii'))['graph']
    print(f"graph --- {graph}")

    distances_table = compute_distances(graph)
    print(f"distances_table --- {distances_table}")
    for source, destination, distance in distances_table:
        print(f"Key to write to dynamo {source}:{destination}:{distance}")
        table_name.put_item(
            Item={
                'sd_pair': f"{source}-{destination}",
                'source': source,
                'destination': destination,
                'distance': str(distance),
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Graph stored successfully!')
    }


def bfs(graph, start):
    distances = {}
    visited = set()
    queue = deque([(start, 0)])  # (node, distance)

    while queue:
        node, distance = queue.popleft()
        distances[node] = distance

        if node not in visited:
            visited.add(node)
            neighbors = graph[node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, distance + 1))

    return distances


def compute_distances(graph_str):
    graph = defaultdict(list)

    edges = graph_str.split(',')
    for edge in edges:
        source, destinations = edge.split('->')
        destinations = destinations.split(',')
        graph[source].extend(destinations)

    all_distances = []
    for node in list(graph):
        distances = bfs(graph, node)
        for destination, distance in distances.items():
            all_distances.append((node, destination, distance))

    return all_distances


def clear_table():
    table_name.scan().delete()