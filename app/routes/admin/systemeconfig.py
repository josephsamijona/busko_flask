# admin/system_config.py

class SystemConfig:
    def __init__(self):
        # Initialisez les paramètres du système ici
        self.system_parameters = {
            "notification_threshold": 10,
            "default_language": "fr",
            "log_level": "info",
            # ... autres paramètres ...
        }

    def get_system_parameter(self, parameter_name):
        # Obtenir la valeur d'un paramètre spécifique
        return self.system_parameters.get(parameter_name)

    def set_system_parameter(self, parameter_name, new_value):
        # Définir la valeur d'un paramètre spécifique
        if parameter_name in self.system_parameters:
            self.system_parameters[parameter_name] = new_value
            # Enregistrez les modifications dans la configuration persistante si nécessaire
            return True
        else:
            return False  # Le paramètre spécifié n'existe pas

if __name__ == "__main__":
    # Exemple d'utilisation du module
    config_manager = SystemConfig()

    # Obtenir la valeur d'un paramètre
    threshold_value = config_manager.get_system_parameter("notification_threshold")
    print(f"Notification Threshold: {threshold_value}")

    # Modifier la valeur d'un paramètre
    if config_manager.set_system_parameter("log_level", "debug"):
        print("Log level updated successfully.")
    else:
        print("Failed to update log level. Parameter not found.")
