from app.commands import handle_music_command
from .miles_command import miles_command
from .miles_speaker import miles_speaker
from .open_response import *
from colorama import Fore, Style
from database.greetings import *
from database.feelings import *
import traceback
from database.goodbyes import *
from .commands import *
import logging
from .commands import *

# =============================================================================================================


def miles_uget(porcupine):
    usersaid = miles_command()
    if not usersaid:
        pass

    elif re.search(
        r"\b(hi|hello|hey|greetings|salutations|yo|hiya|howdy|sup|hi there|hello there|what's up|yoohoo|hey there|hiya there|g'day|cheerio|hihi|aloha|bonjour|hallo|ciao|namaste|konichiwa|hola|szia|hei|hej|tjena|heya|hey ya|sup dude|sup bro|sup everyone|wassup|whaddup)\b",
        usersaid,
    ):
        response = generate_greeting_response(usersaid)
        miles_speaker(response)

    elif re.search(
        r"\bhow\s+(?:are\s+you|are\s+you\s+doing|do\s+you\s+feel|have\s+you\s+been)\s+(?:feeling|today|lately|these\s+days)\b",
        usersaid,
    ):
        response = generate_feelings_response(usersaid)
        miles_speaker(response)

    else:
        miles_speaker(f"Sorry, I cannot perform {usersaid} yet")


# play_regex = r"\b((?:can you|could you|would you|please) (?:play|sing|perform)|play (?:me )?(?:a )?(?:song|track)|sing (?:me )?(?:a )?(?:song|track)|perform (?:me )?(?:a )?(?:song|track)|\bsup\b|)\b"
# def miles_uget(porcupine):
#     try:
#         # Retrieve user's input
#         usersaid = miles_command()

#         # pass if user's input is empty
#         if not usersaid:
#             pass

#         # Check if user's input matches any of the greetings in the greetings list
#         elif any(re.search(greeting, usersaid) for greeting in greetings):
#             response = generate_greeting_response(usersaid)
#             miles_speaker(response)

#         # Check if the user's input contains the words "shutdown", "exit", or "quit"
#         elif re.search(r"(shutdown|exit|quit)", usersaid):  # Shut down the program
#             miles_speaker("Shutting down...")
#             os._exit(0)

#         elif any(word in usersaid for word in ["play", "music", "sing"]):
#             mathed = re.match(
#                 r"(?P<play>play)(ing)?(?P<artist>\s+[a-zA-Z]+)?(\s+by)?(\s+(the\s+)?(?P<song>[a-zA-Z]+))?|(?P<stop>stop|pause|resume)|(?P<volume>volume(\s+(?P<amount>[0-9]+(\.[0-9]+)?))?\s+(?P<direction>up|down))",
#                 usersaid,
#             )
#             if mathed:
#                 handle_music_command(usersaid)

#         # # Check if the user's input is related to music commands
#         # elif "play" in usersaid or "music" in usersaid or "sing" in usersaid:
#         #     mathed = re.match(
#         #         r"(?P<play>play)(ing)?(?P<artist>\s+[a-zA-Z]+)?(\s+by)?(\s+(the\s+)?(?P<song>[a-zA-Z]+))?|(?P<stop>stop|pause|resume)|(?P<volume>volume(\s+(?P<amount>[0-9]+(\.[0-9]+)?))?\s+(?P<direction>up|down))",
#         #         usersaid,
#         #     )
#         #     if mathed:
#         #         handle_music_command(usersaid)

#         # # Handle the wikipedia search command
#         # elif re.match(r"(?P<wikipedia>wikipedia|wiki) (?P<search_query>.+)", usersaid):
#         #     handle_wikipedia(usersaid)

#         # # check if user wants to know the current time
#         # elif re.match(r"(what time is it|what's the time|do you know the time)\b", usersaid):
#         #     response = get_time(usersaid)
#         #     miles_speaker(response)

#         # # check if user wants to hear a joke
#         # elif re.match(r"(tell me|say) a joke\b", usersaid):
#         #     response = get_joke(usersaid)
#         #     miles_speaker(response)

#         # # check if user wants to know the news
#         # elif re.match(r"(what's|what is|tell me) the news\b", usersaid):
#         #     get_news(usersaid)

#         # elif re.match(r"(what's|what is|tell me) the news\b", usersaid):
#         #     # match optional language argument
#         #     match = re.search(r"language (\w+)\b", usersaid)
#         #     language = match.group(1) if match else 'en'
#         #     # match optional page size argument
#         #     match = re.search(r"(\d+) (news|articles)\b", usersaid)
#         #     page_size = int(match.group(1)) if match else 5
#         #     # call get_news() function with parsed arguments
#         #     get_news(usersaid, language=language, page_size=page_size)

#         # # check if user wants to know date
#         # elif re.match(r"(what's|what is) today's date\b", usersaid):
#         #     get_date(usersaid)

#         #    # check if user wants to open a program
#         #     elif re.match(r"open (?P<program>.+)", usersaid):
#         #         program_name = re.match(
#         #             r"open (?P<program>.+)", usersaid).group("program")
#         #         open_program(program_name)

#         # # check if user wants to perform a search
#         # elif re.match(r"(search|look up|find) (?P<query>.+)", usersaid):
#         #     # If the user specified an engine
#         #     match = re.match(
#         #         r"(search|look up|find) (?P<query>.+?) (in|on) (?P<engine>\w+)", usersaid)
#         #     if match:
#         #         query = match.group("query")
#         #         engine = match.group("engine")
#         #         perform_search(query, engine)
#         #     else:
#         #         # If the user didn't specify an engine
#         #         match = re.match(
#         #             r"(search|look up|find) (?P<query>.+)", usersaid)
#         #         if match:
#         #             query = match.group("query")
#         #             perform_search(query)

#         # # check if user wants to perform a reminder
#         # elif re.match(r"remind me to (?P<reminder>.+) at (?P<time>.+)", usersaid):
#         #     schedule_reminder(usersaid)

#         # # check if user wants to send a message
#         # elif re.match(r"(send|write|compose) (?P<message_type>email|message) to (?P<recipient>.+) saying (?P<message>.+)", usersaid):
#         #     send_message(usersaid)

#         # # check if user wants to perform a file operation
#         # elif re.match(r"(copy|move) (?P<file>.+) (to|from) (?P<location>.+)", usersaid):
#         #     perform_file_operation(usersaid)

#         else:  # Generate a response for any other input
#             try:
#                 response = open_response(usersaid)
#                 miles_speaker(response)
#             except Exception as e:  # If an error occurs, print the error message in red color
#                 print(f"{Fore.RED}Error: {e}")
#                 miles_speaker(f"Sorry, I cannot perform {usersaid} yet")

#     except ValueError as e:
#         # Log a warning if an empty input is received
#         logging.warning(f"Empty input received from user: {e}")
#         # Use text-to-speech to ask the user to try again
#         miles_speaker("Sorry, I didn't catch that. Can you please try again?")

#     except Exception as e:
#         # Log an error if an exception occurs
#         logging.error(traceback.format_exc())
#         # Use text-to-speech to inform the user that an error has occurred
#         miles_speaker("Oops! Something went wrong. Please try again later.")

#     except:
#         # If an error occurs, speak the error message
#         miles_speaker(f"An error occurred: {str(e)}")