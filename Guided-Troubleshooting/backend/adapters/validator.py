class MockAction:
    def __init__(self, actionName, description, steps, deeplink, category="Connectivity"):
        self.actionName = actionName
        self.description = description
        self.steps = steps
        self.deeplink = deeplink
        self.category = category
        self.id = "act-1"
        self.score = 0.95

    def dict(self, *args, **kwargs):
        return {
            "actionName": self.actionName,
            "description": self.description,
            "steps": self.steps,
            "deeplink": self.deeplink,
            "category": self.category
        }

    def __getattr__(self, name):
        return ""

class ResponseValidator:
    def __init__(self, *args, **kwargs): pass
    def validate(self, *args, **kwargs): return True
    def validate_and_order_actions(self, actions=None, *args, **kwargs):
        if not actions:
            actions = [
                MockAction(
                    actionName="Restart Network Settings",
                    description="Reset Wi-Fi and Bluetooth settings to default.",
                    steps=["Open Settings", "Select General", "Tap Transfer or Reset", "Reset Network Settings"],
                    deeplink="prefs:root=General&path=Reset",
                    category="Network"
                ),
                MockAction(
                    actionName="Toggle Airplane Mode",
                    description="Toggle Airplane Mode on for 10 seconds and turn off.",
                    steps=["Control Center", "Tap Airplane Icon", "Wait 10s", "Tap again"],
                    deeplink="prefs:root=AIRPLANE_MODE",
                    category="Connectivity"
                )
            ]
        return actions, {"status": "success"}

class Person3DeeplinkValidator:
    def __init__(self, *args, **kwargs): pass
    def validate(self, *args, **kwargs): return True

class Validator:
    def __init__(self, *args, **kwargs): pass
    def validate(self, *args, **kwargs): return True
