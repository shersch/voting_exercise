import pika
import json
import redis

print("Connecting...")
connecting = True
while connecting:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
        connecting = False
        channel = connection.channel()
        channel.queue_declare(queue="vote_queue", durable=True)
        print("Connected!")
    except Exception:
        connecting = True

def submitVote(ch, method, properties, body):
    body = json.loads(body)
    score = int(body["score"])
    id = int(body["postId"])

    r = redis.Redis(host="redis", port=6379, db=0)

    try:
        data = json.loads(r.get(id))
    except Exception:
        data = {
            "upvote": 0,
            "downvote": 0
        }

    if score == 1:
        data["upvote"] += 1
    elif score == -1:
        data["downvote"] += 1

    try:
        r.set(id, json.dumps(data))
    except Exception:
        print("failed to submit vote")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='vote_queue', on_message_callback=submitVote)
channel.start_consuming()