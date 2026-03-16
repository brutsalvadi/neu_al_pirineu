"""
Graciosillo mode - Funny descriptions for snow conditions and station status.

Inspired by Tuixent - La Vansa's hilarious snow reports:
"Polvazo", "Per flipar", "Una animalada"
"""

import random
from config import DEFAULT_GRACIOSILLO

# User graciosillo preferences storage
# In production, this should be replaced with a database
_user_graciosillo: dict[int, bool] = {}


def is_graciosillo_enabled(user_id: int) -> bool:
    """Check if graciosillo mode is enabled for a user."""
    return _user_graciosillo.get(user_id, DEFAULT_GRACIOSILLO)


def set_graciosillo(user_id: int, enabled: bool) -> None:
    """Enable or disable graciosillo mode for a user."""
    _user_graciosillo[user_id] = enabled


def toggle_graciosillo(user_id: int) -> bool:
    """Toggle graciosillo mode for a user. Returns new state."""
    current = is_graciosillo_enabled(user_id)
    _user_graciosillo[user_id] = not current
    return not current


# =============================================================================
# FUNNY SNOW DEPTH DESCRIPTIONS
# =============================================================================

SNOW_DESCRIPTIONS = {
    "es": {
        # Based on snow depth in cm
        "unknown": [
            "Ni idea de cuánta hay 🤷",
            "El medidor está roto 📏",
            "Dato clasificado ㊙️",
            "Sorpresa sorpresa 🎁",
        ],
        "none": [
            "Ni pa' trineo de perro 🐕",
            "Aquí la nieve es un mito 🏜️",
            "Mejor quédate en casa viendo Netflix",
            "La nieve está de vacaciones ✈️",
        ],
        "low": [  # < 30cm
            "Justito pa' no rayar los esquís 😅",
            "Hay nieve... técnicamente",
            "Más tierra que nieve, ¡aventurero!",
            "Pa' valientes con esquís de roca 🪨",
        ],
        "medium": [  # 30-80cm
            "Está apañao 👍",
            "Nieve decente, no te quejes",
            "Se puede esquiar sin rezar",
            "Nivel: 'me arriesgo'",
        ],
        "good": [  # 80-150cm
            "Polvazo 💨",
            "Esto ya es otra cosa 🎿",
            "Per flipar ❄️",
            "La nieve está guapa",
            "Día de gloria 🙌",
        ],
        "excellent": [  # > 150cm
            "Una animalada 🤯",
            "POW POW POW!!! 💥",
            "Nivel: 'llama a tu jefe, hoy no vas'",
            "Nieve hasta las orejas 👂",
            "¿Esquís o submarino? 🤿",
            "Avisa al San Bernardo, nos vamos a perder",
        ],
    },
    "ca": {
        "unknown": [
            "Ni idea de quanta n'hi ha 🤷",
            "El mesurador està trencat 📏",
            "Dada classificada ㊙️",
            "Sorpresa sorpresa 🎁",
        ],
        "none": [
            "Ni per trineu de gos 🐕",
            "Aquí la neu és un mite 🏜️",
            "Millor queda't a casa mirant Netflix",
            "La neu està de vacances ✈️",
        ],
        "low": [
            "Justeet per no ratllar els esquís 😅",
            "Hi ha neu... tècnicament",
            "Més terra que neu, aventurer!",
            "Per valents amb esquís de roca 🪨",
        ],
        "medium": [
            "Està apanyat 👍",
            "Neu decent, no et queixis",
            "Es pot esquiar sense resar",
            "Nivell: 'm'arrisco'",
        ],
        "good": [
            "Polvàs 💨",
            "Això ja és una altra cosa 🎿",
            "Per flipar ❄️",
            "La neu està ben bonica",
            "Dia de glòria 🙌",
        ],
        "excellent": [
            "Una animalada 🤯",
            "POW POW POW!!! 💥",
            "Nivell: 'truca al cap, avui no hi vas'",
            "Neu fins a les orelles 👂",
            "Esquís o submarí? 🤿",
            "Avisa al Sant Bernat, ens perdrem",
        ],
    },
    "en": {
        "unknown": [
            "No idea how much there is 🤷",
            "The measuring stick is broken 📏",
            "Classified data ㊙️",
            "Surprise surprise 🎁",
        ],
        "none": [
            "Not even for dog sledding 🐕",
            "Snow is a myth here 🏜️",
            "Better stay home watching Netflix",
            "The snow is on vacation ✈️",
        ],
        "low": [
            "Barely enough to not scratch your skis 😅",
            "There's snow... technically",
            "More dirt than snow, adventurer!",
            "For brave souls with rock skis 🪨",
        ],
        "medium": [
            "It's decent 👍",
            "Proper snow, don't complain",
            "You can ski without praying",
            "Level: 'I'll risk it'",
        ],
        "good": [
            "Powder alert! 💨",
            "Now we're talking 🎿",
            "Mind-blowing ❄️",
            "The snow is looking fine",
            "Glory day 🙌",
        ],
        "excellent": [
            "Absolutely bonkers 🤯",
            "POW POW POW!!! 💥",
            "Level: 'call your boss, you're not going today'",
            "Snow up to your ears 👂",
            "Skis or submarine? 🤿",
            "Alert the rescue dogs, we're getting lost",
        ],
    },
}


# =============================================================================
# FUNNY KM OPEN DESCRIPTIONS
# =============================================================================

KM_DESCRIPTIONS = {
    "es": {
        "unknown": [
            "Ni idea, bro 🤷",
            "Misterio sin resolver 🔮",
            "Pregunta a tu bola de cristal 🔮",
            "El dato está de vacaciones 📊",
            "Sin información... ¡aventúrate! 🎲",
        ],
        "closed": [
            "Cerrado a cal y canto 🔒",
            "Nada de nada 🚫",
            "La estación duerme 😴",
            "Los pisteros están en Canarias 🏝️",
        ],
        "few": [  # < 30%
            "Pa' dar una vueltita 🔄",
            "Solo para impacientes",
            "Más cerrado que abierto",
            "Algo es algo 🤷",
        ],
        "some": [  # 30-70%
            "Pa' echar el día 👌",
            "Se deja esquiar",
            "Suficiente pa' no repetir pista",
            "Nivel: 'me conformo'",
        ],
        "most": [  # 70-99%
            "Casi to' abierto 🎉",
            "Ya puedes presumir",
            "Solo falta el bar de cumbre",
            "Vas a acabar reventao",
        ],
        "full": [  # 100%
            "¡TODO ABIERTO! 🚀",
            "Ni los pisteros se lo creen",
            "Vende el coche, no vas a volver",
            "Nivel: 'avisa a la familia'",
        ],
    },
    "ca": {
        "unknown": [
            "Ni idea, bro 🤷",
            "Misteri sense resoldre 🔮",
            "Pregunta a la bola de cristall 🔮",
            "La dada està de vacances 📊",
            "Sense informació... aventura't! 🎲",
        ],
        "closed": [
            "Tancat a pany i clau 🔒",
            "Res de res 🚫",
            "L'estació dorm 😴",
            "Els pisters són a Canàries 🏝️",
        ],
        "few": [
            "Per fer una volteta 🔄",
            "Només per impacients",
            "Més tancat que obert",
            "Alguna cosa és alguna cosa 🤷",
        ],
        "some": [
            "Per passar el dia 👌",
            "Es deixa esquiar",
            "Suficient per no repetir pista",
            "Nivell: 'em conformo'",
        ],
        "most": [
            "Quasi tot obert 🎉",
            "Ja pots presumir",
            "Només falta el bar de cim",
            "Acabaràs rebentat",
        ],
        "full": [
            "TOT OBERT! 🚀",
            "Ni els pisters s'ho creuen",
            "Ven el cotxe, no tornaràs",
            "Nivell: 'avisa la família'",
        ],
    },
    "en": {
        "unknown": [
            "No clue, bro 🤷",
            "Mystery unsolved 🔮",
            "Ask your crystal ball 🔮",
            "Data is on vacation 📊",
            "No info... take a chance! 🎲",
        ],
        "closed": [
            "Locked up tight 🔒",
            "Nothing at all 🚫",
            "Station is sleeping 😴",
            "Staff went to the Bahamas 🏝️",
        ],
        "few": [
            "For a quick spin 🔄",
            "Only for the impatient",
            "More closed than open",
            "Something is something 🤷",
        ],
        "some": [
            "Enough for a day out 👌",
            "Skiable conditions",
            "Enough to not repeat runs",
            "Level: 'I'll settle'",
        ],
        "most": [
            "Almost everything open 🎉",
            "Time to show off",
            "Only the summit bar is missing",
            "You'll be exhausted",
        ],
        "full": [
            "FULLY OPEN! 🚀",
            "Even the staff can't believe it",
            "Sell your car, you're not coming back",
            "Level: 'notify your family'",
        ],
    },
}


# =============================================================================
# RANDOM COMMENTS
# =============================================================================

RANDOM_COMMENTS = {
    "es": {
        "normal": [
            "🎿 _Recuerda: caer con estilo también cuenta_",
            "⚠️ _El forfait no incluye dignidad_",
            "🍷 _Après-ski es francés para 'me lo he ganado'_",
            "🥶 _Si no sientes los dedos, es que lo estás haciendo bien_",
            "📱 _Foto o no ha pasado_",
            "🏔️ _La montaña llama... y no acepta excusas_",
            "☕ _Parada técnica = chocolate caliente_",
            "🎯 _Objetivo del día: no acabar en YouTube_",
            "🦵 _Mañana caminarás como un pingüino_",
            "💪 _Lo que pasa en la pista, queda en la pista_",
            "🎒 _¿Llevas el bocata? Es lo más importante_",
            "🧤 _Perder un guante: tradición desde 1936_",
            "⛷️ _Estilo libre = no sé lo que hago pero mola_",
        ],
        "unknown": [
            "🔮 _Sin datos... ¡pero el corazón sabe!_",
            "🎲 _La incertidumbre es parte de la aventura_",
            "🤷 _Cuando no hay datos, hay fe_",
            "📡 _El informador está tomando un café_",
            "🧭 _Confía en tu instinto esquiador_",
            "🎰 _Sin info pero con ganas, ¡suficiente!_",
            "🦉 _El búho de la estación no ha reportado_",
            "📵 _Datos en modo avión_",
        ],
    },
    "ca": {
        "normal": [
            "🎿 _Recorda: caure amb estil també compta_",
            "⚠️ _El forfet no inclou dignitat_",
            "🍷 _Après-ski és francès per 'me l'he guanyat'_",
            "🥶 _Si no sents els dits, ho estàs fent bé_",
            "📱 _Foto o no ha passat_",
            "🏔️ _La muntanya crida... i no accepta excuses_",
            "☕ _Parada tècnica = xocolata calenta_",
            "🎯 _Objectiu del dia: no acabar a YouTube_",
            "🦵 _Demà caminaràs com un pingüí_",
            "💪 _El que passa a la pista, queda a la pista_",
            "🎒 _Portes l'entrepà? És el més important_",
            "🧤 _Perdre un guant: tradició des del 1936_",
            "⛷️ _Estil lliure = no sé què faig però mola_",
        ],
        "unknown": [
            "🔮 _Sense dades... però el cor ho sap!_",
            "🎲 _La incertesa és part de l'aventura_",
            "🤷 _Quan no hi ha dades, hi ha fe_",
            "📡 _L'informador està prenent un cafè_",
            "🧭 _Confia en el teu instint esquiador_",
            "🎰 _Sense info però amb ganes, n'hi ha prou!_",
            "🦉 _El mussol de l'estació no ha reportat_",
            "📵 _Dades en mode avió_",
        ],
    },
    "en": {
        "normal": [
            "🎿 _Remember: falling with style also counts_",
            "⚠️ _Ski pass doesn't include dignity_",
            "🍷 _Après-ski is French for 'I've earned it'_",
            "🥶 _If you can't feel your toes, you're doing it right_",
            "📱 _Pics or it didn't happen_",
            "🏔️ _The mountain calls... and doesn't accept excuses_",
            "☕ _Technical stop = hot chocolate_",
            "🎯 _Today's goal: don't end up on YouTube_",
            "🦵 _Tomorrow you'll walk like a penguin_",
            "💪 _What happens on the slopes, stays on the slopes_",
            "🎒 _Got your sandwich? That's the priority_",
            "🧤 _Losing a glove: tradition since 1936_",
            "⛷️ _Freestyle = I don't know what I'm doing but it's cool_",
        ],
        "unknown": [
            "🔮 _No data... but the heart knows!_",
            "🎲 _Uncertainty is part of the adventure_",
            "🤷 _When there's no data, there's faith_",
            "📡 _The reporter is having a coffee break_",
            "🧭 _Trust your skiing instincts_",
            "🎰 _No info but plenty of enthusiasm!_",
            "🦉 _The station owl hasn't reported yet_",
            "📵 _Data in airplane mode_",
        ],
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _parse_snow_depth(snow_str: str) -> tuple[int | None, bool]:
    """
    Extract numeric snow depth from string like '150 cm' or '- cm'.

    Returns:
        Tuple of (depth, is_unknown)
        - (None, True) = data not available ("- cm")
        - (0, False) = known to be 0 ("0 cm")
        - (150, False) = known depth ("150 cm")
    """
    try:
        parts = snow_str.replace("cm", "").strip().split()
        if parts:
            if parts[0] == "-":
                return None, True  # Unknown
            return int(parts[0]), False  # Known value
    except (ValueError, IndexError):
        pass
    return None, True


def _parse_km_percentage(km_str: str) -> tuple[float | None, bool]:
    """
    Extract percentage of km open from string like '30/32' or '-/33'.

    Returns:
        Tuple of (percentage, is_unknown)
        - (None, True) = data not available ("-/33")
        - (0.0, False) = known to be 0 ("0/33")
        - (50.0, False) = known percentage ("16.5/33")
    """
    try:
        parts = km_str.split("/")
        if len(parts) == 2:
            open_km = parts[0].strip()
            total_km = float(parts[1].strip())
            if open_km == "-":
                return None, True  # Unknown, not zero!
            open_val = float(open_km)
            if total_km > 0:
                return (open_val / total_km * 100), False
            return 0.0, False
    except (ValueError, IndexError):
        pass
    return None, True


def get_snow_category(snow_str: str) -> str:
    """Get snow category based on depth."""
    depth, is_unknown = _parse_snow_depth(snow_str)
    if is_unknown:
        return "unknown"  # "- cm" = we don't know
    if depth == 0:
        return "none"  # "0 cm" = we know there's no snow
    elif depth < 30:
        return "low"
    elif depth < 80:
        return "medium"
    elif depth < 150:
        return "good"
    else:
        return "excellent"


def get_km_category(km_str: str) -> str:
    """Get km category based on percentage open."""
    percentage, is_unknown = _parse_km_percentage(km_str)
    if is_unknown:
        return "unknown"  # "-/33" = we don't know
    if percentage == 0:
        return "closed"  # "0/33" = we know it's closed
    elif percentage < 30:
        return "few"
    elif percentage < 70:
        return "some"
    elif percentage < 100:
        return "most"
    else:
        return "full"


def get_funny_snow_description(snow_str: str, lang: str) -> str:
    """Get a random funny description for snow depth."""
    category = get_snow_category(snow_str)
    descriptions = SNOW_DESCRIPTIONS.get(lang, SNOW_DESCRIPTIONS["es"])
    options = descriptions.get(category, descriptions["medium"])
    return random.choice(options)


def get_funny_km_description(km_str: str, lang: str) -> str:
    """Get a random funny description for km open."""
    category = get_km_category(km_str)
    descriptions = KM_DESCRIPTIONS.get(lang, KM_DESCRIPTIONS["es"])
    options = descriptions.get(category, descriptions["some"])
    return random.choice(options)


def get_random_comment(lang: str, has_unknown_data: bool = False) -> str:
    """Get a random funny comment.

    Args:
        lang: Language code (es, ca, en)
        has_unknown_data: If True, picks from "unknown" category comments
    """
    comments_dict = RANDOM_COMMENTS.get(lang, RANDOM_COMMENTS["es"])
    category = "unknown" if has_unknown_data else "normal"
    comments = comments_dict.get(category, comments_dict["normal"])
    return random.choice(comments)
