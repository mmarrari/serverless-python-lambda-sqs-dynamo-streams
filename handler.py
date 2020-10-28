import json
import uuid
import os
import boto3

def hacerPedido(event, context):
    print('Mando la cola PRINCIPIO')
    clienteSQS = boto3.client('sqs')
    queue_url = os.environ.get('PENDING_ORDER_QUEUE')
    v_uuid = str(uuid.uuid4())
    body = {
        "message": "Funcion que hace el pedido {}!".format(v_uuid),
        "input": event,
        "queue": queue_url
    }
    order = {'orderId': v_uuid,
            'otroCampo' : 'pepe'}


    clienteSQS.send_message( QueueUrl=queue_url,
                             MessageBody=json.dumps(order),
                             DelaySeconds=1 )
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
    print('Mando la cola FIN')

def prepararPedido(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('COMPLETED_ORDER_TABLE'))
    for record in event['Records']:
        payload=record["body"]
        table.put_item(Item=json.loads(payload))
        print(str(payload))

    body = {
        "message": "Función que prepara el pedido!",
        "input": event
    }
    print(str(event))
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def enviarPedido(event, context):
    body = {
        "message": "Función que envia el pedido!",
        "input": event
    }
    print(str(event))
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response