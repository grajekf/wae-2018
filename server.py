#!/usr/bin/env python3
import argparse
import asyncio
import base64
import json
from threading import Thread
from io import BytesIO

import websockets

from gen import args as ga_args
from gen import run


def img_to_base64(img):
    return base64.b64encode(img)


class Publisher:

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, id, notify):
        self.subscribers[id] = notify

    def unsubscribe(self, id):
        del self.subscribers[id]

    async def notify(self, message):
        to_remove = []
        for k in self.subscribers:
            try:
                await self.subscribers[k](message)
            except Exception as e:
                print(e)
                to_remove.append(k)
        for k in to_remove:
            del self.subscribers[k]


def create_handler(publisher):
    async def client_handler(websocket, path):
        publisher.subscribe(websocket, websocket.send)
        while True:
            await asyncio.sleep(60)

    return client_handler


def genetic_algorithm(args, hook):
    run(args, hook)


async def notifier(publisher, queue):
    objectiveFunctionData = {
        'best': [],
        'worst': [],
        'mean': [],
        'median': []
    }
    while 1:
        print("waiting for items on queue")
        item = await queue.get()
        objectiveFunctionData['best'].append(item['objectiveFunction']['best'])
        objectiveFunctionData['worst'].append(item['objectiveFunction']['worst'])
        objectiveFunctionData['mean'].append(item['objectiveFunction']['mean'])
        objectiveFunctionData['median'].append(item['objectiveFunction']['median'])

        buffered = BytesIO()
        image = item['bestSpecimen']['data']
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue())

        payload = json.dumps({
            'generation': item['generation'],
            'currentAction': 'None',
            'objectiveFunctionData': objectiveFunctionData,
            'bestSpecimenData': {
                'image': img_base64.decode('utf-8'),
                'predictions': item['bestSpecimen']['predictions']
            }
        })
        await publisher.notify(payload)


async def test():
    while 1:
        await asyncio.sleep(1)


async def main(args):
    publisher = Publisher()
    websocket_server = websockets.serve(create_handler(publisher), '0.0.0.0', args.port)
    queue = asyncio.Queue()

    thread = Thread(target=genetic_algorithm, args=(args, lambda x: queue.put_nowait(x)))
    thread.start()

    await asyncio.gather(
        websocket_server,
        notifier(publisher, queue),
        test()
    )


def parse_args():
    args = argparse.ArgumentParser()
    ga_args(args)
    args.add_argument('--port', default=3001, type=int, help="websocket server port", required=False)
    return args.parse_args()


if __name__ == '__main__':
    args = parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
    loop.close()
