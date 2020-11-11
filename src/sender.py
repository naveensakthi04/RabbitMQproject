try:
    import pika
except Exception as e:
    print("Some modules are missing. {}".format_map(e))


class MetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        """Singleton Design Pattern"""

        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]




class RabbitMQConfigure(metaclass=MetaClass):     # Making this class as a Singleton class
    def __init__(self,
                 queue='hello',
                 host='localhost',
                 routing_key='hello',
                 exchange=''):

        """Configuring RabbitMQ Server"""

        self.queue = queue
        self.host = host
        self.routing_key = routing_key
        self.exchange = exchange


class Image(object):
    __slots__ = ["filename"]

    def __init__(self, filename):
        self.filename = filename

    @property
    def get(self):
        with open(self.filename, "rb") as f:
            data = f.read()
        return data


class RabbitMQ():

    # slots - for faster attribute access and efficient memory usage
    __slots__ = ["server", "_channel", "_connection"]

    def __init__(self, server):

        """

        :param server: Object of RabbitMQConfigure
        """

        self.server = server
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.server.host)
        )
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()
        print("Exit")

    def publish(self, payload):
        """

        :param payload:
        :return: None
        """
        self._channel.basic_publish(exchange=self.server.exchange,
                                    routing_key=self.server.routing_key,
                                    body=str(payload))
        print("Published message: {}".format(payload))


if __name__ == "__main__":
    server = RabbitMQConfigure(queue='hello',
                               host='localhost',
                               routing_key='hello',
                               exchange='')

    image = Image(filename=r"C:\Users\Naveen Sakthi\Pictures\Products\product2.png")
    data = image.get

    # Context Manager
    rabbit_mq = RabbitMQ(server)
    rabbit_mq.publish(payload=data)
