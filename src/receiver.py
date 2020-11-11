
try:
    import pika
    import ast
except Exception as e:
    print("Some modules are missing. {}".format_map(e))


class MetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        """Singleton Design Pattern"""

        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitMQServerConfigure(metaclass=MetaClass):
    def __init__(self,
                 host='localhost',
                 queue='hello'):
        """
        Server initialization
        :param host: localhost by default
        :param queue: hello by default
        """
        self.host = host
        self.queue = queue


class RabbitMQServer:

    def __init__(self, server):
        """

        :param server: Object of RabbitMQServerConfigure
        :return: None
        """
        self.server = server
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.server.host)
        )
        self._channel = self._connection.channel()
        self._temp = self._channel.queue_declare(queue=self.server.queue)

    def callback(self, ch, method, properties, body):
        pay_load = ast.literal_eval(body.decode("utf-8"))
        with open("received.png", "wb") as f:
            f.write(pay_load)

        print("Data Received: {}".format(pay_load))
        # print("[x] Received %r" % body)

    def consume(self):
        """
        Consume
        :return: None
        """
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=self.callback,
            auto_ack=True
        )
        self._channel.start_consuming()


if __name__ == "__main__":
    server_configure = RabbitMQServerConfigure(host='localhost',
                                               queue='hello')
    server = RabbitMQServer(server_configure)

    print(" [*] Waiting for messages. To exit press Ctrl+C")

    server.consume()
