# Flask
from flask import Flask, request, render_template, redirect

# Other
import mebots
from threading import Thread
import requests
import os
import time
import argparse
from game import Game


app = Flask(__name__)
bot = mebots.Bot("tictactoebot", os.environ.get("BOT_TOKEN"))


MAX_MESSAGE_LENGTH = 1000
PREFIX = "#"


# Webhook receipt and response
@app.route("/", methods=["POST"])
def receive():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    group_id = message["group_id"]
    # Begin reply process in a new thread.
    # This way, the request won't time out if a response takes too long to generate.
    Thread(target=reply, args=(message, group_id)).start()
    return "ok", 200


def reply(message, group_id):
    send(process_message(message), group_id)


def process_message(message):
    responses = []
    if message.sender_type == "user":
        if message.text.startswith(PREFIX):
            query = message["text"][len(PREFIX):].strip().split(None, 1)
            arguments = query.split()
            command = arguments.pop(0).lower()
            group_id = message["group_id"]
            if command == "join":
                if self.players[0] == "":
                    self.players[0] = message.name
                    return f"{message.name} has joined, waiting on a second player"
                elif self.players[1] == "":
                    self.players[1] = message.name
                    return [f"{message.name} has joined, ready to play", self.string_board()]
                else:
                    return f"Game full. {self.players[0]} & {self.players[1]} are playing!"
            elif command == "end":
                self.clear()
            elif command == "help":
                desc = "Possible commands: help, join, end. Positions:\n"
                desc += "|".join(["a1", "a2", "a3"]) + "\n——————\n"
                desc += "|".join(["b1", "b2", "b3"]) + "\n——————\n"
                desc += "|".join(["c1", "c2", "c3"])
                return desc
            elif command in self.movements:
                loc = self.movements[command]
                if self.turn and message.name == self.players[0]:
                    self.turn = False
                    self.board[loc] = "x"
                elif not self.turn and message.name == self.players[1]:
                    self.turn = True
                    self.board[loc] = "o"
                if self.check() != "":
                    return self.check()
                return self.string_board()
            else:
                return "Unknown command."


    return responses


def send(message, group_id):
    """
    Reply in chat.
    :param message: text of message to send. May be a tuple with further data, or a list of messages.
    :param group_id: ID of group in which to send message.
    """
    if message is None:
        return
    # Recurse when sending multiple messages.
    if isinstance(message, list):
        for item in message:
            send(item, group_id)
        return
    data = {
        "bot_id": bot.instance(group_id).id,
    }
    if len(message) > MAX_MESSAGE_LENGTH:
        # If text is too long for one message, split it up over several
        for block in [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]:
            send(block, group_id)
            time.sleep(0.3)
        data["text"] = ""
    else:
        data["text"] = message
    # Prevent sending message if there's no content
    # It would be rejected anyway
    response = requests.post("https://api.groupme.com/v3/bots/post", data=data)


# Local testing
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?")
    args = parser.parse_args()
    message = {"sender_type": "user", "group_id": 49940116}))
    if args.command:
        message["text"] = args.command
        print(process_message(message))
    else:
        while True:
            message["text"] = input("> ")
            print(process_message(message))
