from flask import Flask
from flask import request
import pika
import json
import redis

r = redis.Redis(host='redis', port=6379, db=0)
app = Flask(__name__)

@app.route('/vote')
def vote():
    try:
        vote = request.args.get("score")
        id = request.args.get("postId")
    except Exception:
        print("Parameter error.")
    if vote == "1" or vote == "-1":
        data = {
            "score": vote,
            "postId": id
        }

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='vote_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='vote_queue',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
    connection.close()

    success = {
        "success": "true"
    }
    return json.dumps(success)

@app.route('/vote-counts')
def voteCount():
    id = request.args.get("postId")
    try:
        data = json.loads(r.get(id))
        return data
    except Exception:
        return "that ID does not exist"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')