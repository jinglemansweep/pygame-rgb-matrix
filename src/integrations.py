import json
import logging
import paho.mqtt.client as mqtt

from config import (
    MQTT_HOST,
    MQTT_PORT,
    MQTT_USER,
    MQTT_PASSWORD,
)

HASS_DISCOVERY_TOPIC_PREFIX = "homeassistant"
HASS_DISCOVERY_MANUFACTURER = "jinglemansweep"
OPTS_LIGHT_RGB = dict(color_mode=True, supported_color_modes=["rgb"], brightness=False)

logger = logging.getLogger("integration")

# MQTT


def _on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/rgbmatrix")


def _on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def setup_mqtt_client():
    print(MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
    client = mqtt.Client()
    client.on_connect = _on_connect
    client.on_message = _on_message
    if MQTT_USER is not None:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    return client


# HOME ASSISTANT


class HASSEntity:
    def __init__(
        self,
        client,
        store,
        host_id,
        entity_prefix,
        name,
        description,
        device_class,
        discovery_topic_prefix,
        options=None,
    ):
        if options is None:
            options = dict()
        self.client = client
        self.store = store
        self.host_id = host_id
        self.entity_prefix = entity_prefix
        self.name = name
        self.description = description
        self.device_class = device_class
        self.options = options
        self.discovery_topic_prefix = discovery_topic_prefix
        topic_prefix = self._build_entity_topic_prefix()
        self.topic_config = f"{topic_prefix}/config"
        self.topic_command = f"{topic_prefix}/set"
        self.topic_state = f"{topic_prefix}/state"
        self.state = dict()

    def configure(self):
        auto_config = dict(
            name=self.description,
            object_id=self._build_full_name(),
            unique_id=self._build_full_name(),
            device_class=self.device_class,
            device=dict(
                identifiers=[self.host_id],
                name=self.host_id,
                model=self.entity_prefix,
                manufacturer=HASS_DISCOVERY_MANUFACTURER,
                sw_version="1.X",
            ),
            schema="json",
            command_topic=self.topic_command,
            state_topic=self.topic_state,
        )
        config = auto_config.copy()
        config.update(self.options)
        logger.info(f"hass entity configure: name={self.name} config={config}")
        self.client.publish(self.topic_config, json.dumps(config), retain=True, qos=1)
        self.client.subscribe(self.topic_command, 1)
        del auto_config, config

    def update(self, new_state=None):
        if new_state is None:
            new_state = dict()
        self.state.update(new_state)
        logger.info(f"hass entity update: name={self.name} state={self.state}")
        self.client.publish(
            self.topic_state, self._get_hass_state(), retain=True, qos=1
        )

    def _build_full_name(self):
        return f"{self.entity_prefix}_{self.host_id}_{self.name}"

    def _build_entity_topic_prefix(self):
        return f"{self.discovery_topic_prefix}/{self.device_class}/{self._build_full_name()}"

    def _get_hass_state(self):
        return (
            self.state["state"]
            if self.device_class == "switch"
            else json.dumps(self.state)
        )


class HASSManager:
    def __init__(
        self,
        client,
        host_id,
        entity_prefix,
        discovery_topic_prefix=HASS_DISCOVERY_TOPIC_PREFIX,
    ):
        self.client = client
        self.host_id = host_id
        self.entity_prefix = entity_prefix
        self.discovery_topic_prefix = discovery_topic_prefix
        self.store = dict()
        logger.info(
            f"hass manager: host_id={host_id} discovery_topic_prefix={discovery_topic_prefix}"
        )
        pass

    def add_entity(
        self, name, description, device_class, options=None, initial_state=None
    ):
        entity = HASSEntity(
            self.client,
            self.store,
            self.host_id,
            self.entity_prefix,
            name,
            description,
            device_class,
            self.discovery_topic_prefix,
            options,
        )
        entity.configure()
        entity.update(initial_state)
        self.store[name] = entity
        logger.info(
            f"hass entity created: name={name} device_class={device_class} options={options} initial_state={initial_state}"
        )
        return entity

    def process_message(self, topic, message):
        logger.info(f"hass process message: topic={topic} message={message}")
        for name, entity in self.store.items():
            if topic == entity.topic_command:
                logger.debug(f"hass topic match entity={entity.name}")
                entity.update(_message_to_hass(message, entity))
                break

    def advertise_entities(self):
        logger.info("advertising entities")
        for name, entity in self.store.items():
            entity.configure()


def _message_to_hass(message, entity):
    return (
        dict(state="ON" if "ON" in message else "OFF")
        if entity.device_class == "switch"
        else json.loads(message)
    )
