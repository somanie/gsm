import simpy 
import random
env = simpy.Environment()

class Subscriber(object):
    def __init__(self, env, name:str, bss, call_duration, IMSI):
        self.env = env
        self.name = name
        self.bss = bss
        self.call_duration = call_duration
        # self.call_duration = random.randint(2,5)
        self.IMSI = IMSI
        self.received_cipher = env.event()
        self.service = "Voice Call"
        self.action = env.process(self.run())

    def run(self):
        # yield self.env.process(bss.allocate_radio_resource(self.name))
        with self.bss.radio_resource.request() as radio_resource:
            print(f"{self.name} sending a request for radio resource allocation to the BSS")
            yield radio_resource
            print(f"{self.name} received radio resource from BSS")

            # BSS Connects to MSC
            yield self.env.process(self.bss.connect_to_msc(self))

            # MS connects to the network
            print(f"{self.name} connected to the network")
            self.msc = self.bss.msc

            # AuC authenticates subscriber
            yield self.env.process(self.msc.authenticate_subscriber(self))
            # print(self.call_duration)

            # MSC initiates ciphering procedure and transmits to the BTS
            yield self.env.process(self.msc.initiate_cipher(self.bss.bts, self))
            print(f"{self.name} enabled {self.cipher} ciphering to BTS")

            # MSC verifies that the requested service is allowed for the subscriber
            yield self.env.process(self.msc.verify_requested_service_for_subscriber(self, self.service))
            print(f"{self.name} verified for {self.service}")

            # MSC starts the call setup
            yield self.env.process(self.msc.start_call_setup(self))

            # MSC initiates voice call channel 
            yield self.env.process(self.msc.create_voice_channel_to_bss(self.bss, self))

            # MS returns confirmation message
            # yield self.env

            yield self.env.timeout(self.call_duration)
            print(f"{self.name} disconnected from radio resource from BSS at {env.now}")

    def receive_cipher_from_bts(self, cipher):
        self.received_cipher.succeed(value=cipher)
        print(f"{self.name} received cipher from BTS")
        self.cipher = yield self.received_cipher

    def receive_channel_from_bss(self, channel):
        receival_of_channel_from_bss = self.env.event()
        receival_of_channel_from_bss.succeed(value=channel)

        self.channel_to_bss = yield receival_of_channel_from_bss
        print(f"{self.name} switched to {self.channel_to_bss} channel")

        
class BaseStationSubsystem(object):
    def __init__(self, env):
        self.env = env
        # self.radio_resource = env.event()
        self.msc = msc
        self.radio_resource = simpy.Resource(env, capacity=2)

        self.bts = BaseTranscieverStation(env=env, msc=msc, radio_resource=self.radio_resource)
        self.bsc = BaseStationController(env=env, msc=msc, radio_resource=self.radio_resource)

    def connect_to_msc(self, subscriber):
        print(f"BSS Connecting {subscriber.name} to MSC...")
        yield self.env.process(self.msc.connect_to_bss(subscriber))

    def receive_channel_from_msc(self, channel, subscriber:Subscriber):
        receival_of_channel_from_msc = self.env.event()
        receival_of_channel_from_msc.succeed(value=channel)

        channel = yield receival_of_channel_from_msc
        print(f"BSS received {channel} channel from MSC for {subscriber.name}")

        yield self.env.process(subscriber.receive_channel_from_bss(channel))

class BaseTranscieverStation:
    def __init__(self, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)

    def receive_cipher_from_msc(self, cipher, subscriber):
        received_cipher = self.env.event()
        received_cipher.succeed()

        print(f"BTS received cipher from MSC for {subscriber.name}")
        yield self.env.process(subscriber.receive_cipher_from_bts(cipher))

class BaseStationController:
    def __init__(self, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)
        

class MobileSwitchingCenter(object):
    def __init__(self, env):
        self.env = env
        self.auc = auc
        self.vlr = vlr

    def connect_to_bss(self, subscriber:Subscriber):
        connection_to_bss = env.event()
        print(f"MSC connected to BSS for {subscriber.name}")
        connection_to_bss.succeed()

        yield connection_to_bss

    def authenticate_subscriber(self, subscriber:Subscriber):
        print(f"MSC sending {subscriber.name}'s IMSI to AuC for authentication")
        yield self.env.process(self.auc.authenticate_IMSI(subscriber.name, subscriber.IMSI))

    def initiate_cipher(self, bts, subscriber:Subscriber):
        initiation_of_cipher = env.event()
        print(f"MSC initiated cipher procedure for {subscriber.name}")
        initiation_of_cipher.succeed(value="Ceaser Cipher")

        cipher = yield initiation_of_cipher

        yield self.env.process(bts.receive_cipher_from_msc(cipher, subscriber))

    def verify_requested_service_for_subscriber(self, subscriber:Subscriber, service:str):
        print(f"MSC verifying that {subscriber.name} has privilege to use {service}")
        yield self.env.process(self.vlr.verify_service_for_subscriber(subscriber, service))

    def start_call_setup(self, subscriber:Subscriber):
        call_setup = env.event()
        call_setup.succeed()
        print(f"MSC setup call for {subscriber.name}")

        yield call_setup

    def create_voice_channel_to_bss(self, bss:BaseStationSubsystem, subscriber:Subscriber):
        creation_of_voice_channel_to_bss = self.env.event()
        creation_of_voice_channel_to_bss.succeed("Voice")
        print(f"MSC created voice channel to BSS for {subscriber.name}")

        channel = yield creation_of_voice_channel_to_bss

        yield self.env.process(bss.receive_channel_from_msc(channel, subscriber))


class AuthenticationCenter(object):
    def __init__(self, env):
        self.env = env

    def authenticate_IMSI(self, subscriber_name:str, IMSI:str):
        user_authenticated = env.event()
        print(f"AuC authenticated {subscriber_name} with IMSI {IMSI}")
        user_authenticated.succeed()

        yield user_authenticated

class VirtualLocationRegister(object):
    def __init__(self, env) -> None:
        self.env = env

    def verify_service_for_subscriber(self, subscriber:Subscriber, service:str):
        subscriber_verified_for_service = env.event()
        print(f"VLR verifying that {subscriber.name} has privilege to use {service}")
        subscriber_verified_for_service.succeed()

        yield subscriber_verified_for_service

vlr = VirtualLocationRegister(env)
auc = AuthenticationCenter(env)
msc = MobileSwitchingCenter(env)
bss = BaseStationSubsystem(env)
# subscriber_a = Subscriber(env, "Subscriber A", bss, 10)
# subscriber_b = Subscriber(env, "Subscriber B", bss, 6)
# subscriber_c = Subscriber(env, "Subscriber C", bss, 4)
# subscriber_d = Subscriber(env, "Subscriber D", bss, 21)
# subscriber_e = Subscriber(env, "Subscriber E", bss, 17)
# env.run()
# env.event()