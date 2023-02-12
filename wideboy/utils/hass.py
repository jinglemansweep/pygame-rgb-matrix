import json
import logging
import paho.mqtt.client as mqtt


HASS_DISCOVERY_TOPIC_PREFIX = "homeassistant"
HASS_DISCOVERY_MANUFACTURER = "WideBoy"
OPTS_LIGHT_RGB = dict(color_mode=True, supported_color_modes=["rgb"], brightness=True)

logger = logging.getLogger("hass")

# MQTT


def _on_connect(client, userdata, flags, rc):
    logger.info(f"mqtt:connected rc={str(rc)}")


def _on_message(client, userdata, msg):
    pass
    # logger.debug(f"mqtt:message topic={msg.topic} message={str(msg.payload)}")


def setup_mqtt_client(host, port, user, password):
    logger.info(f"mqtt:connect host={host} port={port} user={user} password={password}")
    client = mqtt.Client()
    client.on_connect = _on_connect
    client.on_message = _on_message
    if user is not None:
        client.username_pw_set(user, password)
    client.connect(host, port, 60)
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
        logger.debug(f"hass:entity:configure name={self.name} config={config}")
        self.client.publish(self.topic_config, json.dumps(config), retain=True, qos=1)
        self.client.subscribe(self.topic_command, 1)
        del auto_config, config

    def update(self, new_state=None):
        if new_state is None:
            new_state = dict()
        self.state.update(new_state)
        logger.debug(f"hass:entity:update: name={self.name} state={self.state}")
        self.client.publish(
            self.topic_state, self._get_hass_state(), retain=True, qos=1
        )

    def _build_full_name(self):
        return f"{self.entity_prefix}_{self.host_id}_{self.name}"

    def _build_entity_topic_prefix(self):
        return f"{self.discovery_topic_prefix}/{self.device_class}/{self._build_full_name()}"

    def _get_hass_state(self):
        if self.device_class == "switch":
            return self.state["state"]
        elif self.device_class == "text":
            return json.dumps(self.state)
        else:
            return json.dumps(self.state)


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
            f"hass:entity:create name={name} device_class={device_class} options={options} initial_state={initial_state}"
        )
        return entity

    def process_message(self, topic, message):
        # logger.debug(f"hass:mqtt:message topic={topic} message={message}")
        for name, entity in self.store.items():
            if topic == entity.topic_command:
                # logger.debug(f"hass:mqtt:message:topic match={entity.name}")
                entity.update(_message_to_hass(message, entity))
                break

    def advertise_entities(self):
        # logger.info("hass:entities:advertise")
        for name, entity in self.store.items():
            entity.configure()


def _message_to_hass(message, entity):
    if entity.device_class == "switch":
        return dict(state="ON" if "ON" in message else "OFF")
    elif entity.device_class == "text":
        return dict(text=message)
    else:
        return json.loads(str(message))


def hass_to_color(rgb_dict, brightness=255):
    color = [
        rgb_dict.get("r") * (brightness / 255),
        rgb_dict.get("g") * (brightness / 255),
        rgb_dict.get("b") * (brightness / 255),
    ]
    return tuple(color)


def hass_to_visible(control, master):
    if not master:
        return 0
    return 1 if control else 0
