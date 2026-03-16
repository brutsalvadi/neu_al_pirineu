"""
Internationalization (i18n) translations for the Nordic Ski Webcams Telegram Bot.
Supports: Spanish (es), Catalan (ca), English (en)
"""

from config import DEFAULT_LANG, BUYMEACOFFEE_URL

TRANSLATIONS = {
    "es": {
        # Welcome & Help
        "welcome_title": "🎿 *Bot de Webcams de Esquí Nórdico*",
        "welcome_desc": "Consulta las condiciones actuales y las webcams de las estaciones de esquí nórdico del Pirineo.",
        "available_stations": "*Estaciones disponibles:*",
        "example": "*Ejemplo:*",
        "use_help": "Usa /help para más información.",
        "help_title": "🎿 *Bot de Webcams - Ayuda*",

        # Commands
        "commands": "*Comandos:*",
        "cmd_start": "/start - Mensaje de bienvenida",
        "cmd_help": "/help - Esta ayuda",
        "cmd_list": "/list - Listar estaciones",
        "cmd_all": "/all - Resumen de todas",
        "cmd_lang": "/lang - Cambiar idioma",
        "cmd_support": "/support - ☕ Apoyar el bot",

        # Stations
        "station_shortcuts": "*Atajos de estaciones:*",
        "regions": "*Regiones:*",
        "region_catalan": "🏔️ Pirineo Catalán (7 estaciones)",
        "region_ariege": "🇫🇷 Ariège Pyrénées (2 estaciones)",
        "region_neiges": "❄️ Neiges Catalanes (3 estaciones)",
        "all_stations_title": "🎿 *Todas las Estaciones*",
        "overview_title": "🎿 *Resumen de Condiciones*",
        "km_open": "Km abiertos",
        "snow": "Nieve",
        "more_webcams": "Ver más webcams",

        # Errors
        "station_not_found": "❌ Estación '{}' no encontrada.\n\nUsa /list para ver las estaciones disponibles.",
        "image_error": "⚠️ _No se pudo cargar la imagen de la webcam_",

        # Language
        "lang_title": "🌐 *Selecciona tu idioma*",
        "lang_changed": "✅ Idioma cambiado a *Español*",
        "lang_current": "Idioma actual: *Español*",

        # Support
        "support_title": "☕ *¡Apoya este bot!*",
        "support_text": f"""Este bot funciona en un servidor privado, alimentado por café ☕ y la esperanza de que algún día la nieve llegue hasta mi casa.

🖥️ El servidor no tiene nombre, pero si lo tuviera se llamaría "Paciencia" porque a veces va lento.

💸 Si este bot te ha ayudado a decidir si ir a esquiar o quedarte en el sofá (opción válida), puedes invitarme a un café por solo *3€*:

👉 [¡Invítame a un café!]({BUYMEACOFFEE_URL})

⚠️ *Disclaimer:* Cada euro donado se invertirá en:
• 40% café para mantenerme despierto
• 30% pagar el servidor
• 20% forfaits de esquí (para "testear" las webcams)
• 10% terapia por ver webcams con niebla

¡Gracias por usar el bot! 🎿❄️""",

        # Graciosillo mode
        "graciosillo_enabled": "🤪 *¡Modo graciosillo activado!*\n\nAhora las condiciones vendrán con comentarios... _creativos_.",
        "graciosillo_disabled": "😐 *Modo graciosillo desactivado*\n\nVuelta al modo serio y aburrido.",
        "graciosillo_status_on": "🤪 Modo graciosillo: *ACTIVADO*",
        "graciosillo_status_off": "😐 Modo graciosillo: *desactivado*",
        "cmd_graciosillo": "/graciosillo - 🤪 Modo payaso",
    },

    "ca": {
        # Welcome & Help
        "welcome_title": "🎿 *Bot de Webcams d'Esquí Nòrdic*",
        "welcome_desc": "Consulta les condicions actuals i les webcams de les estacions d'esquí nòrdic del Pirineu.",
        "available_stations": "*Estacions disponibles:*",
        "example": "*Exemple:*",
        "use_help": "Usa /help per a més informació.",
        "help_title": "🎿 *Bot de Webcams - Ajuda*",

        # Commands
        "commands": "*Comandes:*",
        "cmd_start": "/start - Missatge de benvinguda",
        "cmd_help": "/help - Aquesta ajuda",
        "cmd_list": "/list - Llistar estacions",
        "cmd_all": "/all - Resum de totes",
        "cmd_lang": "/lang - Canviar idioma",
        "cmd_support": "/support - ☕ Donar suport al bot",

        # Stations
        "station_shortcuts": "*Dreceres d'estacions:*",
        "regions": "*Regions:*",
        "region_catalan": "🏔️ Pirineu Català (7 estacions)",
        "region_ariege": "🇫🇷 Ariège Pyrénées (2 estacions)",
        "region_neiges": "❄️ Neiges Catalanes (3 estacions)",
        "all_stations_title": "🎿 *Totes les Estacions*",
        "overview_title": "🎿 *Resum de Condicions*",
        "km_open": "Km oberts",
        "snow": "Neu",
        "more_webcams": "Veure més webcams",

        # Errors
        "station_not_found": "❌ Estació '{}' no trobada.\n\nUsa /list per veure les estacions disponibles.",
        "image_error": "⚠️ _No s'ha pogut carregar la imatge de la webcam_",

        # Language
        "lang_title": "🌐 *Selecciona el teu idioma*",
        "lang_changed": "✅ Idioma canviat a *Català*",
        "lang_current": "Idioma actual: *Català*",

        # Support
        "support_title": "☕ *Dona suport a aquest bot!*",
        "support_text": f"""Aquest bot funciona en un servidor privat, alimentat per cafè ☕ i l'esperança que algun dia la neu arribi fins a casa meva.

🖥️ El servidor no té nom, però si en tingués es diria "Paciència" perquè de vegades va lent.

💸 Si aquest bot t'ha ajudat a decidir si anar a esquiar o quedar-te al sofà (opció vàlida), pots convidar-me a un cafè per només *3€*:

👉 [Convida'm a un cafè!]({BUYMEACOFFEE_URL})

⚠️ *Disclaimer:* Cada euro donat s'invertirà en:
• 40% cafè per mantenir-me despert
• 30% pagar el servidor
• 20% forfets d'esquí (per "testejar" les webcams)
• 10% teràpia per veure webcams amb boira

Gràcies per fer servir el bot! 🎿❄️""",

        # Graciosillo mode
        "graciosillo_enabled": "🤪 *Mode graciós activat!*\n\nAra les condicions vindran amb comentaris... _creatius_.",
        "graciosillo_disabled": "😐 *Mode graciós desactivat*\n\nTornem al mode seriós i avorrit.",
        "graciosillo_status_on": "🤪 Mode graciós: *ACTIVAT*",
        "graciosillo_status_off": "😐 Mode graciós: *desactivat*",
        "cmd_graciosillo": "/graciosillo - 🤪 Mode pallasso",
    },

    "en": {
        # Welcome & Help
        "welcome_title": "🎿 *Nordic Ski Webcams Bot*",
        "welcome_desc": "Check current conditions and webcams from Nordic ski stations in the Pyrenees.",
        "available_stations": "*Available stations:*",
        "example": "*Example:*",
        "use_help": "Use /help for more info.",
        "help_title": "🎿 *Webcams Bot - Help*",

        # Commands
        "commands": "*Commands:*",
        "cmd_start": "/start - Welcome message",
        "cmd_help": "/help - This help",
        "cmd_list": "/list - List stations",
        "cmd_all": "/all - Overview of all",
        "cmd_lang": "/lang - Change language",
        "cmd_support": "/support - ☕ Support the bot",

        # Stations
        "station_shortcuts": "*Station shortcuts:*",
        "regions": "*Regions:*",
        "region_catalan": "🏔️ Catalan Pyrenees (7 stations)",
        "region_ariege": "🇫🇷 Ariège Pyrénées (2 stations)",
        "region_neiges": "❄️ Neiges Catalanes (3 stations)",
        "all_stations_title": "🎿 *All Stations*",
        "overview_title": "🎿 *Conditions Overview*",
        "km_open": "Km open",
        "snow": "Snow",
        "more_webcams": "View more webcams",

        # Errors
        "station_not_found": "❌ Station '{}' not found.\n\nUse /list to see available stations.",
        "image_error": "⚠️ _Could not load webcam image_",

        # Language
        "lang_title": "🌐 *Select your language*",
        "lang_changed": "✅ Language changed to *English*",
        "lang_current": "Current language: *English*",

        # Support
        "support_title": "☕ *Support this bot!*",
        "support_text": f"""This bot runs on a private server, powered by coffee ☕ and the hope that one day snow will reach my doorstep.

🖥️ The server doesn't have a name, but if it did, it would be called "Patience" because sometimes it's slow.

💸 If this bot helped you decide whether to go skiing or stay on the couch (valid option), you can buy me a coffee for just *3€*:

👉 [Buy me a coffee!]({BUYMEACOFFEE_URL})

⚠️ *Disclaimer:* Every euro donated will be invested in:
• 40% coffee to keep me awake
• 30% paying for the server
• 20% ski passes (to "test" the webcams)
• 10% therapy from watching foggy webcams

Thanks for using the bot! 🎿❄️""",

        # Graciosillo mode
        "graciosillo_enabled": "🤪 *Funny mode activated!*\n\nConditions will now come with... _creative_ comments.",
        "graciosillo_disabled": "😐 *Funny mode deactivated*\n\nBack to boring serious mode.",
        "graciosillo_status_on": "🤪 Funny mode: *ON*",
        "graciosillo_status_off": "😐 Funny mode: *off*",
        "cmd_graciosillo": "/graciosillo - 🤪 Clown mode",
    },
}


# User language preferences storage
# In production, this should be replaced with a database
_user_languages: dict[int, str] = {}


def get_user_lang(user_id: int) -> str:
    """Get user's language preference."""
    return _user_languages.get(user_id, DEFAULT_LANG)


def set_user_lang(user_id: int, lang: str) -> bool:
    """Set user's language preference. Returns True if successful."""
    if lang in TRANSLATIONS:
        _user_languages[user_id] = lang
        return True
    return False


def t(user_id: int, key: str) -> str:
    """Get translation for a key based on user's language preference."""
    lang = get_user_lang(user_id)
    return TRANSLATIONS[lang].get(key, TRANSLATIONS[DEFAULT_LANG].get(key, key))
