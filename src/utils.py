import random
from .sensor.rfssensor import RfsSensor
from .sensor.basecomnios import hostname, get_nios_status


bridge = None
bridges = get_nios_status(hostname)
sensor = None

if (bridges[0] is not None):
    bridge = bridges[1]
    sensor = RfsSensor(name="RfsSensor", real=True, offset=0x40100)


def get_friendly_description(category, value):
    """Generate friendly descriptions based on sensor values"""
    if category == "temperature":
        if value < 18:
            return f"it's quite cool at {value:.1f}°C"
        elif value < 22:
            return f"it's comfortable at {value:.1f}°C"
        elif value < 26:
            return f"it's warm at {value:.1f}°C"
        else:
            return f"it's quite warm at {value:.1f}°C"

    elif category == "humidity":
        if value < 30:
            return f"the air is quite dry with {value:.1f}% relative humidity"
        elif value < 60:
            return f"humidity is at a comfortable {value:.1f}%"
        else:
            return f"it's quite humid at {value:.1f}%"

    else:
        if value < 10:
            return f"it's very dark at {value:.1f} lux"
        elif value < 50:
            return f"it's dim at {value:.1f} lux"
        elif value < 150:
            return f"lighting is moderate at {value:.1f} lux"
        elif value < 500:
            return f"it's well lit at {value:.1f} lux"
        elif value < 1000:
            return f"it's bright at {value:.1f} lux"
        else:
            return f"it's very bright at {value:.1f} lux"


def get_response(intent):
    categories = intent["categories"]
    if categories[0] == "unknown":
        responses = [
            "I'm not quite sure what you're asking about. Could you rephrase that?",
            "I didn't catch that. Could you ask in a different way?",
            "Could you be more specific about what you'd like to know?",
            "I'm not sure which measurement you're interested in. Could you clarify?"
        ]
        return random.choice(responses)
    
    stats = sensor.get_telemetries(bridge)
    print(stats)
    
    # Handle single category response
    if len(categories) == 1:
        category = categories[0]
        return get_friendly_description(category, stats[category])
    
    # Handle multiple category response
    responses = []
    for category in categories:
        value = stats[category]
        responses.append(get_friendly_description(category, value))
    
    # Join multiple responses with natural language
    if len(responses) == 2:
        return f"Right now, {responses[0]}, and {responses[1]}"
    else:
        *first_parts, last_part = responses
        return f"Right now, {', '.join(first_parts)}, and {last_part}"