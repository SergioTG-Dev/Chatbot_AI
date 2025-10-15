# actions/actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionGetAllPokemon(Action):
    """Acción para obtener la lista de los primeros 20 Pokémon."""

    def name(self) -> Text:
        return "action_get_all_pokemon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Hacer la petición a la PokeAPI
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=20")
        
        if response.status_code == 200:
            data = response.json()
            # Crear una lista de nombres
            pokemon_list = [pokemon['name'] for pokemon in data['results']]
            # Formatear la respuesta
            message = "¡Aquí tienes una lista de Pokémon:\n" + "\n".join(f"- {name.title()}" for name in pokemon_list)
        else:
            message = "Lo siento, no pude obtener la información en este momento."
        
        dispatcher.utter_message(text=message)
        return []

class ActionGetPokemonDetail(Action):
    """Acción para obtener detalles de un Pokémon específico."""

    def name(self) -> Text:
        return "action_get_pokemon_detail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extraer la entidad 'pokemon_name' del mensaje del usuario
        pokemon_name = next(tracker.get_latest_entity_values("pokemon_name"), None)
        
        if not pokemon_name:
            dispatcher.utter_message(text="Por favor, dime de qué Pokémon quieres saber.")
            return []
        
        # Hacer la petición a la PokeAPI para el Pokémon específico
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        
        if response.status_code == 200:
            data = response.json()
            # Extraer información específica
            name = data['name'].title()
            abilities = [ability['ability']['name'] for ability in data['abilities']]
            types = [type_data['type']['name'] for type_data in data['types']]
            
            message = f"**{name}**\n"
            message += f"**Tipo(s):** {', '.join(types)}\n"
            message += f"**Habilidades:** {', '.join(abilities[:3])}" # Muestra las 3 primeras
        else:
            message = f"No pude encontrar información para {pokemon_name}. ¿Estás seguro de que ese es un Pokémon?"
        
        dispatcher.utter_message(text=message)
        return []